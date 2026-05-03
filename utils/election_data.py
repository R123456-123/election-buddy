"""
election_data.py — Static Election Reference Data
===================================================
Contains curated election facts, key dates, and quick-reference data.
This module is designed to be cached by Streamlit's @st.cache_data
to avoid unnecessary API calls for information that never changes.
"""


def get_election_key_dates() -> list[dict]:
    """Return a list of key election dates and milestones.

    Each entry is a dict with 'event', 'date', and 'description' keys.
    This data is static and should be cached at the app level.

    Returns:
        list[dict]: A list of election milestone dictionaries.
    """
    return [
        {
            "event": "🇺🇸 US Presidential Election",
            "date": "November 3, 2026",
            "description": "United States presidential and congressional elections.",
        },
        {
            "event": "🇮🇳 Indian General Election",
            "date": "April–May 2029 (projected)",
            "description": "World's largest democratic exercise with 900M+ eligible voters.",
        },
        {
            "event": "🇬🇧 UK General Election",
            "date": "2029 (projected)",
            "description": "Election of Members of Parliament to the House of Commons.",
        },
        {
            "event": "🇧🇷 Brazilian General Election",
            "date": "October 2026",
            "description": "Presidential and congressional elections in Brazil.",
        },
        {
            "event": "🇩🇪 German Federal Election",
            "date": "2029 (projected)",
            "description": "Election of members to the Bundestag.",
        },
    ]


def get_voting_systems_info() -> list[dict]:
    """Return descriptions of common voting systems worldwide.

    Returns:
        list[dict]: Each dict has 'system', 'description', and 'used_in' keys.
    """
    return [
        {
            "system": "First-Past-The-Post (FPTP)",
            "description": (
                "The candidate with the most votes in a constituency wins. "
                "Simple but can lead to disproportionate representation."
            ),
            "used_in": "USA, UK, India, Canada",
        },
        {
            "system": "Proportional Representation (PR)",
            "description": (
                "Seats are allocated in proportion to the total votes each party receives. "
                "Encourages multi-party systems."
            ),
            "used_in": "Germany, Netherlands, South Africa",
        },
        {
            "system": "Mixed-Member Proportional (MMP)",
            "description": (
                "Combines FPTP for local seats with PR for additional seats "
                "to correct disproportionality."
            ),
            "used_in": "Germany, New Zealand",
        },
        {
            "system": "Ranked-Choice Voting (RCV)",
            "description": (
                "Voters rank candidates by preference. If no candidate has a majority, "
                "the lowest-ranked candidate is eliminated and votes redistributed."
            ),
            "used_in": "Australia, Ireland, select US cities",
        },
        {
            "system": "Two-Round System",
            "description": (
                "If no candidate wins a majority in the first round, "
                "a runoff is held between the top two candidates."
            ),
            "used_in": "France, Brazil",
        },
    ]


def get_quick_facts() -> list[str]:
    """Return a list of interesting election facts for the sidebar.

    Returns:
        list[str]: Short, engaging election trivia strings.
    """
    return [
        "🗳️ The word 'democracy' comes from Greek: *demos* (people) + *kratos* (power).",
        "🌍 Over 2 billion people voted in elections worldwide in 2024.",
        "📊 India's 2024 general election was the largest in history with ~970 million eligible voters.",
        "🇦🇺 Australia has had compulsory voting since 1924 — turnout regularly exceeds 90%.",
        "📱 Estonia was the first country to allow legally binding internet voting in 2005.",
        "🗓️ The US always holds presidential elections on the Tuesday after the first Monday in November.",
        "🏛️ Switzerland holds up to 4 national referendums per year, making it the most direct democracy.",
    ]


def format_dates_for_display(dates: list[dict]) -> str:
    """Format election dates into a readable Markdown table.

    Args:
        dates: A list of date dictionaries from get_election_key_dates().

    Returns:
        str: A Markdown-formatted table string.
    """
    if not dates:
        return "_No election dates available._"

    header = "| Event | Date | Description |\n|---|---|---|"
    rows = [
        f"| {d['event']} | {d['date']} | {d['description']} |"
        for d in dates
    ]
    return f"{header}\n" + "\n".join(rows)
