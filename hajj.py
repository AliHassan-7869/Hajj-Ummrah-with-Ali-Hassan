import streamlit as st
from datetime import date
from crewai import Crew
from TravelAgents import (spiritual_guide_agent, logistics_agent, health_safety_agent, packing_agent, food_agent, transport_agent, budget_agent, planner_agent)
from TravelTasks import (spiritual_guide_task, logistics_task, health_safety_task, packing_task, food_task, transport_task, budget_task, planner_task)

# ================= STREAMLIT CONFIG =================
st.set_page_config(
    page_title="🕋 Al-Mursheed Hajj & Umrah Planner",
    layout="wide"
)

st.title("🕋 Ali Hassan Hajj & Umrah Planner")
st.markdown("""
Welcome to **Ali Hassan AI**, your personal Hajj & Umrah assistant.  
Plan your spiritual journey with step-by-step guidance, travel logistics, safety, and budget recommendations.
""")

# ================= SIDEBAR =================
with st.sidebar:
    st.header("🕌 Pilgrim Details")
    pilgrim_name = st.text_input("Your Name", placeholder="e.g., Ahmed Khan")
    from_city = st.text_input("Departure City", placeholder="e.g., Karachi, Lahore")
    
    spiritual_focus = st.selectbox(
        "🕌 Spiritual Focus",
        ["General", "Hajj rituals", "Umrah rituals", "Duas & Prayers"]
    )
    
    travel_type = st.selectbox("Travel Type", ["Solo", "Family", "Couple", "Group"])
    travel_dates = st.date_input("Travel Dates", min_value=date.today())
    group_size = st.number_input("Number of Pilgrims", min_value=1, max_value=10, value=1, step=1)
    budget_level = st.selectbox("Budget Level", ["Budget", "Mid-range", "Luxury"])
    
    st.markdown("---")
    if st.button("🔄 Reset Form"):
        st.session_state.clear()
        st.rerun()

# ================= GENERATE PLAN =================
if st.button("🕋 Generate Hajj/Umrah Plan"):

    if not pilgrim_name or not from_city or not travel_dates:
        st.error("⚠️ Please fill all required fields before generating your plan.")
    else:
        st.info("🚀 Generating your personalized Hajj/Umrah itinerary... please wait ⏳")
        try:
            # ================= CREATE TASKS =================
            spiritual_task = spiritual_guide_task(
                agent=spiritual_guide_agent,
                pilgrim_name=pilgrim_name,
                travel_dates=travel_dates,
                spiritual_focus=spiritual_focus
            )
            logistics_tsk = logistics_task(
                agent=logistics_agent,
                pilgrim_name=pilgrim_name,
                travel_dates=travel_dates
            )

            health_task = health_safety_task(
                agent=health_safety_agent,
                pilgrim_name=pilgrim_name,
                travel_dates=travel_dates
            )

            pack_task = packing_task(
                agent=packing_agent,
                pilgrim_name=pilgrim_name,
                travel_dates=travel_dates
            )

            food_tsk = food_task(
                agent=food_agent,
                pilgrim_name=pilgrim_name,
                travel_dates=travel_dates,
                budget_level=budget_level
            )

            transport_tsk = transport_task(
                agent=transport_agent,
                from_city=from_city,
                pilgrim_name=pilgrim_name,
                travel_dates=travel_dates
            )

            budget_tsk = budget_task(
                agent=budget_agent,
                pilgrim_name=pilgrim_name,
                travel_dates=travel_dates,
                group_size=group_size,
                budget_level=budget_level
            )

            # ================= FINAL PLANNER TASK =================
            final_planner_tsk = planner_task(
                agent=planner_agent,
                pilgrim_name=pilgrim_name,
                travel_dates=travel_dates,
                group_size=group_size,
                budget_level=budget_level,
                context=[
                    spiritual_task,
                    logistics_tsk,
                    health_task,
                    pack_task,
                    food_tsk,
                    transport_tsk,
                    budget_tsk
                ]
            )

            # ================= INITIALIZE CREW =================
            crew = Crew(
                agents=[
                    spiritual_guide_agent,
                    logistics_agent,
                    health_safety_agent,
                    packing_agent,
                    food_agent,
                    transport_agent,
                    budget_agent,
                    planner_agent
                ],
                tasks=[
                    spiritual_task,
                    logistics_tsk,
                    health_task,
                    pack_task,
                    food_tsk,
                    transport_tsk,
                    budget_tsk,
                    final_planner_tsk
                ],
                full_output=True,
                verbose=True
            )

            # ================= RUN CREW =================
            result = crew.kickoff()

            # ================= DISPLAY RESULT =================
            st.success("✅ Your Hajj/Umrah itinerary is ready!")
            st.subheader(f"🕋 {pilgrim_name}'s Hajj/Umrah Plan")
            st.markdown(result if isinstance(result, str) else str(result))

            # ================= DOWNLOAD BUTTON =================
            file_name = f"Hajj_Umrah_Plan_{pilgrim_name.replace(' ', '_')}.md"
            st.download_button(
                label="📥 Download Itinerary (Markdown)",
                data=str(result),
                file_name=file_name,
                mime="text/markdown"
            )

        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")