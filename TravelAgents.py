from crewai import Agent
from dotenv import load_dotenv
from TravelTools import fetch_prayer_times
from crewai import LLM
import sqlite3
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("API key not loaded! Check your .env file.")
fast_llm = LLM(
    model="llama-3.3-70b-versatile",
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
    temperature=0.5,
)

#  Agents

# Spiritual Guide Agent
spiritual_guide_agent = Agent(
    role="Al-Mursheed AI - Spiritual Guide",
    goal="Guide pilgrims through Hajj & Umrah rituals with step-by-step instructions, Duas, and prayers timings 2026.",
    backstory="""You are a master of 'Fiqh-al-Ibadah'. Your expertise is ensuring 
    that pilgrims perform their Tawaf and Sa'i at times that do not conflict with 
    obligatory prayers, while utilizing the quietest windows (like between Isha and Fajr)."""   ,
    tools=[fetch_prayer_times],
    verbose=True,
    max_iter=2,
    llm=fast_llm,
    allow_delegation=False,
)

# Logistics Agent
logistics_agent = Agent(
    role="Pilgrim Logistics Expert",
    goal="Assist pilgrims with flights, hotels, visas, and transport between Makkah & Madinah.",
    backstory="""You are an expert in pilgrim logistics.
- Suggest hotels near Haram & Masjid Nabawi.
- Include Nusuk app and visa requirements.
- Recommend transport routes and timings.
- Optimize for minimal walking and convenience.""",
    tools=[fetch_prayer_times],
    verbose=True,
    max_iter=2,
    llm=fast_llm,
    allow_delegation=False,
)

# Health & Safety Agent
health_safety_agent = Agent(
    role="Pilgrim Health & Safety Advisor",
    goal="Provide health tips, hydration advice, crowd safety, and emergency precautions for pilgrims.",
    backstory="""You are a travel health expert for pilgrims.
- Suggest heat precautions, hydration, and first-aid.
- Warn about peak crowd times.
- Provide step-by-step safety instructions during rituals.""",
    tools=[fetch_prayer_times],
    verbose=True,
    max_iter=2,
    llm=fast_llm,
    allow_delegation=False,
)

# Packing Agent
packing_agent = Agent(
    role="Pilgrim Packing Assistant",
    goal="Suggest a packing list including spiritual and physical essentials.",
    backstory="""You are a packing expert for pilgrims.
- Include spiritual essentials: Musalla, Dua books, Ihram clothing.
- Include physical essentials: comfortable shoes, toiletries, sunscreen, medications.
- Suggest packing order for easy access during rituals.""",
    tools=[fetch_prayer_times],
    verbose=True,
    max_iter=2,
    llm=fast_llm,
    allow_delegation=False,
)

# Transport Agent
transport_agent = Agent(
    role="Transport Expert for Pilgrims",
    goal="Provide transportation options within Saudi Arabia, between Makkah, Madinah, and key points.",
    backstory="""You are a transportation expert for pilgrims.
- Recommend buses, taxis, trains, and walking routes.
- Optimize for time and safety.
- Include estimated travel times between holy sites.""",
    tools=[fetch_prayer_times],
    verbose=True,
    max_iter=2,
    llm=fast_llm,
    allow_delegation=False,
)

# Budget Agent
budget_agent = Agent(
    role="Pilgrim Budget Planner",
    goal="Optimize pilgrim travel within user budget including flights, hotels, food, and transport.",
    backstory="""You are an expert in pilgrim budgeting.
- Suggest budget-friendly hotels and meals.
- Estimate transport costs.
- Provide daily budget summary for the trip.""",
    tools=[fetch_prayer_times],
    verbose=True,
    max_iter=2,
    llm=fast_llm,
    allow_delegation=False,
)

# Weather Agent
weather_agent = Agent(
    role="Weather & Climate Advisor for Pilgrims",
    goal="Provide accurate weather forecasts for Makkah & Madinah during travel dates.",
    backstory="""You are a weather expert for pilgrims.
- Give daily temperature, rain probability, and heat index.
- Suggest clothing and hydration adjustments for each day.""",
    tools=[fetch_prayer_times],
    verbose=True,
    max_iter=2,
    llm=fast_llm,
    allow_delegation=False,
)

# Food & Restaurant Agent
food_agent = Agent(
    role="Pilgrim Food & Restaurant Expert",
    goal="Recommend Halal-friendly foods and best restaurants near holy sites.",
    backstory="""You are a food travel expert for pilgrims.
- Suggest local cuisine, Halal-certified options.
- Recommend affordable and nearby restaurants.
- Include opening hours and peak times for each location.""",
    tools=[fetch_prayer_times],
    verbose=True,
    max_iter=2,
    llm=fast_llm,
    allow_delegation=False,
)

# 4. Planner Agent
planner_agent = Agent(
    role="Pilgrim Trip Planner",
    goal="Aggregate all expert agents' information and create a day-by-day personalized Hajj/Umrah itinerary.",
    backstory="""You are the master travel planner for pilgrims.
- Integrate outputs from spiritual guide, logistics, health, packing, transport, budget, weather, and food agents.
- Generate a complete chronological itinerary.
- Include rituals, meals, transport, prayer times, safety tips, and packing reminders.
- Use bullet points and step-by-step instructions for clarity.""",
    tools=[fetch_prayer_times],
    verbose=True,
    max_iter=3,
    llm=fast_llm,
    allow_delegation=True,
)
