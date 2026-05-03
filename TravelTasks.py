from crewai import Task

def spiritual_guide_task(agent, pilgrim_name, travel_dates, spiritual_focus="general"):
    return Task(
        agent=agent,
        description=f"""
        ### ROLE
        You are the Lead Ritual Analyst for {pilgrim_name}.
        
        ### OBJECTIVE
        Construct a 'Zero-Error' ritual roadmap for {travel_dates} focusing on {spiritual_focus}.
        
        ### EXECUTION STEPS
        1. Calendar Sync: Use 'fetch_prayer_times' to map the 5 daily prayers for every day of the trip.
        2. Ritual Overlay: Identify 'Low-Crowd Windows' for performing Tawaf and Sa'i.
        3. Categorization: For every step, create a 'Fiqh Status' column: [FARD | WAJIB | SUNNAH].
        4. Dua Mapping: Attach a short transliterated Dua for each station (Meeqat, Safa, Marwa).
        
        ### QUALITY GATES
        - Avoid peak heat (12pm-4pm) unless required by Arafah/Mina schedule.
        - Include a 'Scholarly Disclaimer' for Qurbani instructions.
        """,
        expected_output="Detailed spiritual guidance"
    )


def logistics_task(agent, pilgrim_name, travel_dates):
    return Task(
        agent=agent,
        description=f"""
        You are a Pilgrim Logistics Expert for {pilgrim_name} traveling from {travel_dates}.
        Plan and suggest:
        - Flights to Jeddah/Madina
        - Local transport (taxis, buses, shuttles)
        - Hotels near Haram & Masjid Nabawi
        - Visa & Nusuk app guidance
        - Best timings for holy site visits
        - Crowd management tips
        """,
        expected_output="Markdown logistics plan including flights, hotels, and transport.",
        output_file='logistics_plan.md',
        async_execution=True
    )


def health_safety_task(agent, pilgrim_name, travel_dates):
    return Task(
        agent=agent,
        description=f"""
        You are the Chief Medical Officer for {pilgrim_name}.
        Your goal is zero medical incidents during {travel_dates}.

        ### PROTOCOLS
        1. Heat Stress: Identify danger zones (10AM-4PM) and create safe ritual timing.
        2. Crowd Intelligence: Identify peak congestion points and provide 'Escape & Regroup' plan.
        3. Biometric Maintenance: Water intake & electrolyte schedule based on walking intensity.
        4. Infection Control: Vaccination checklist & 'Hajj-Cough' prevention guide.
        
        ### OUTPUT
        - Daily Health Dashboard: Heat Risk vs Planned Activity
        - Emergency Directory: 2026 Saudi ambulance & hospital contacts
        """,
        expected_output="High-Performance Health & Risk Mitigation Dossier in Markdown.",
        output_file='health_safety_plan.md'
    )


def packing_task(agent, pilgrim_name, travel_dates):
    return Task(
        agent=agent,
        description=f"""
        You are a Packing Specialist for {pilgrim_name} traveling on Hajj/Umrah from {travel_dates}.
        Prepare a checklist including:
        - Spiritual essentials: Musalla, Dua books, Ihram clothing, prayer beads
        - Clothing & footwear for hot weather
        - Toiletries, sunscreen, hat, comfortable shoes
        - Electronics & travel adapters
        - Travel documents: passport, visa, health insurance
        - Optional: portable fan, snacks, water bottles, umbrella
        """,
        expected_output="Complete Hajj/Umrah packing checklist in markdown format.",
        output_file='packing_list.md',
        async_execution=True
    )


def food_task(agent, pilgrim_name, travel_dates, budget_level):
    return Task(
        agent=agent,
        description=f"""
        You are a Nutrition Planner for {pilgrim_name}.
        Create a food plan based on budget: {budget_level}.
        
        - Recommend only SFDA licensed restaurants
        - Suggest high-energy, Sunnah-inspired meals
        - Map restaurants near King Fahd Gate (Makkah) & Rawdah (Madinah)
        - Provide queue management tips for popular local foods
        """,
        expected_output="Curated Culinary & Nutrition Guide optimized for rituals.",
        output_file='pilgrim_food_guide.md'
    )


def transport_task(agent, from_city, pilgrim_name, travel_dates):
    return Task(
        agent=agent,
        description=f"""
        You are a Transportation Expert for {pilgrim_name} from {from_city}.
        Provide:
        - Flights, durations, and costs to Jeddah/Medina
        - Airport transfers
        - Transport between Makkah & Madinah
        - Local taxis, buses, ride-hailing apps
        - Walking routes for rituals
        - Booking tips during peak season
        """,
        expected_output="Markdown-based transport guide for pilgrims.",
        output_file='transport_guide.md',
        async_execution=True
    )


def budget_task(agent, pilgrim_name, travel_dates, group_size, budget_level):
    return Task(
        agent=agent,
        description=f"""
        You are a Budget Planner for {pilgrim_name}, group size {group_size}, trip dates {travel_dates}.
        Create a detailed budget including:
        - Flights
        - Hotels (Budget, Mid-range, Luxury)
        - Meals
        - Transport
        - Miscellaneous & Emergency funds
        """,
        expected_output="Markdown-based Hajj/Umrah budget plan.",
        output_file='budget_plan.md',
        async_execution=True
    )


def planner_task(agent, pilgrim_name, travel_dates, group_size, budget_level, context):
    return Task(
        agent=agent,
        context=context,
        description=f"""
        You are the Chief Coordinator. Merge outputs from all agents for {pilgrim_name}.

        ### USER DETAILS
        - Trip Dates: {travel_dates}
        - Group Size: {group_size}
        - Budget Level: {budget_level}

        ### RULES
        1. Conflict Check: Prioritize rituals over transport if overlapping.
        2. Safety Filter: If walking route >1km during peak heat, suggest Taxi/Shuttle.
        3. Budget Audit: Sum Food, Transport, Hotels. If over budget, flag downgrades.

        ### OUTPUT
        - Trip-at-a-glance summary table
        - Daily deep-dive section in Markdown
        """,
        expected_output="Reconciled, conflict-free Master Itinerary in Markdown.",
        output_file='final_hajj_plan.md'
    )