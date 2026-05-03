import os
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from pydantic import BaseModel
from typing import Optional
from crewai import Crew, Process

# Import Agents
from TravelAgents import (
    spiritual_guide_agent,
    logistics_agent,
    health_safety_agent,
    packing_agent,
    transport_agent,
    budget_agent,
    weather_agent,
    food_agent,
    planner_agent,
)

# Import Tasks
from TravelTasks import (
    spiritual_guide_task,
    logistics_task,
    health_safety_task,
    packing_task,
    food_task,
    transport_task,
    budget_task,
    planner_task,
)

app = FastAPI(title="AI - Hajj & Umrah Planner API")

# -------------------- CORS --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- CONFIG --------------------
API_KEY = os.getenv("API_KEY") or "AI - Hajj & Umrah-secret"


# -------------------- REQUEST MODEL --------------------
class HajjUmrahRequest(BaseModel):
    pilgrim_name: str
    travel_dates: str               # e.g. "2026-05-01 to 2026-05-15"
    from_city: str                  # e.g. "Lahore"
    group_size: int = 1
    budget_level: str = "mid-range" # "budget" | "mid-range" | "luxury"
    spiritual_focus: Optional[str] = "general"  # e.g. "Umrah" | "Hajj" | "general"


# -------------------- ROOT --------------------
@app.get("/")
def home():
    return {"message": " AI - Hajj & Umrah Planner API 🕋 Running!"}


# -------------------- HEALTH --------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# -------------------- POST /plan --------------------
@app.post("/plan")
def generate_hajj_plan(request: HajjUmrahRequest, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        # ---------- Build Tasks ----------
        t_spiritual = spiritual_guide_task(
            agent=spiritual_guide_agent,
            pilgrim_name=request.pilgrim_name,
            travel_dates=request.travel_dates,
            spiritual_focus=request.spiritual_focus,
        )

        t_logistics = logistics_task(
            agent=logistics_agent,
            pilgrim_name=request.pilgrim_name,
            travel_dates=request.travel_dates,
        )

        t_health = health_safety_task(
            agent=health_safety_agent,
            pilgrim_name=request.pilgrim_name,
            travel_dates=request.travel_dates,
        )

        t_packing = packing_task(
            agent=packing_agent,
            pilgrim_name=request.pilgrim_name,
            travel_dates=request.travel_dates,
        )

        t_food = food_task(
            agent=food_agent,
            pilgrim_name=request.pilgrim_name,
            travel_dates=request.travel_dates,
            budget_level=request.budget_level,
        )

        t_transport = transport_task(
            agent=transport_agent,
            from_city=request.from_city,
            pilgrim_name=request.pilgrim_name,
            travel_dates=request.travel_dates,
        )

        t_budget = budget_task(
            agent=budget_agent,
            pilgrim_name=request.pilgrim_name,
            travel_dates=request.travel_dates,
            group_size=request.group_size,
            budget_level=request.budget_level,
        )

        # Async tasks run in parallel; planner waits for all context
        async_tasks = [t_logistics, t_packing, t_transport, t_budget]
        sync_tasks  = [t_spiritual, t_health, t_food]

        t_planner = planner_task(
            agent=planner_agent,
            pilgrim_name=request.pilgrim_name,
            travel_dates=request.travel_dates,
            group_size=request.group_size,
            budget_level=request.budget_level,
            context=[t_spiritual, t_logistics, t_health, t_packing,
                     t_food, t_transport, t_budget],
        )

        # ---------- Assemble Crew ----------
        crew = Crew(
            agents=[
                spiritual_guide_agent,
                logistics_agent,
                health_safety_agent,
                packing_agent,
                food_agent,
                transport_agent,
                budget_agent,
                planner_agent,
            ],
            tasks=[
                *sync_tasks,
                *async_tasks,
                t_planner,          # planner always runs last
            ],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()

        return {
            "status": "success",
            "data": {
                "pilgrim_name": request.pilgrim_name,
                "travel_dates": request.travel_dates,
                "from_city": request.from_city,
                "group_size": request.group_size,
                "budget_level": request.budget_level,
                "spiritual_focus": request.spiritual_focus,
                "plan": str(result),
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crew execution error: {str(e)}")


# -------------------- GET /plan (browser hint) --------------------
@app.get("/plan")
def generate_plan_get(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return {
        "status": "info",
        "message": (
            "Send a POST request to /plan with a JSON body. Example:\n"
            "{\n"
            '  "pilgrim_name": "Ahmed",\n'
            '  "travel_dates": "2026-05-01 to 2026-05-15",\n'
            '  "from_city": "Lahore",\n'
            '  "group_size": 2,\n'
            '  "budget_level": "mid-range",\n'
            '  "spiritual_focus": "Umrah"\n'
            "}"
        )
    }


# -------------------- GLOBAL EXCEPTION HANDLER --------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"status": "error", "detail": str(exc)},
    )