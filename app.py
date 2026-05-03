"""
app.py — Election Buddy: Interactive Election Process Education Assistant
=========================================================================
Main Streamlit application. Handles the UI, session state, and user
interactions. All AI logic is delegated to utils/gemini_helper.py and
all static data lives in utils/election_data.py.

Run locally:
    streamlit run app.py
"""

import streamlit as st
from utils.gemini_helper import get_model, get_chat_session, send_message
from utils.election_data import (
    get_election_key_dates,
    get_voting_systems_info,
    get_quick_facts,
    format_dates_for_display,
)

# ──────────────────────────────────────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Election Buddy — Election Education Assistant",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# Custom CSS — Premium dark theme polish
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Global ────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Header gradient ──────────────────────────────── */
    .main-header {
        background: linear-gradient(135deg, #FF6B35 0%, #F7C948 50%, #4ECDC4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.6rem;
        font-weight: 700;
        margin-bottom: 0;
        line-height: 1.2;
    }
    .sub-header {
        color: #9CA3AF;
        font-size: 1.1rem;
        margin-top: 0;
        margin-bottom: 1.5rem;
    }

    /* ── Chat bubbles ─────────────────────────────────── */
    .chat-user {
        background: linear-gradient(135deg, #1E3A5F, #1A1F2E);
        border-left: 4px solid #FF6B35;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
    }
    .chat-assistant {
        background: linear-gradient(135deg, #1A2332, #0E1117);
        border-left: 4px solid #4ECDC4;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
    }

    /* ── Sidebar card ─────────────────────────────────── */
    .fact-card {
        background: linear-gradient(135deg, #1A2332, #1E293B);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-size: 0.92rem;
        line-height: 1.5;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .fact-card:hover {
        transform: translateY(-2px);
        border-color: #FF6B35;
    }

    /* ── Metric cards ─────────────────────────────────── */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1A2332, #1E293B);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1rem;
    }

    /* ── Expander polish ──────────────────────────────── */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 1rem;
    }

    /* ── Input field ──────────────────────────────────── */
    .stChatInput > div {
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# Cached data loaders — avoids repeated computation / API calls
# ──────────────────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def load_election_dates() -> list[dict]:
    """Load and cache static election dates (never changes mid-session)."""
    return get_election_key_dates()


@st.cache_data(show_spinner=False)
def load_voting_systems() -> list[dict]:
    """Load and cache voting system descriptions."""
    return get_voting_systems_info()


@st.cache_data(show_spinner=False)
def load_quick_facts() -> list[str]:
    """Load and cache sidebar quick facts."""
    return get_quick_facts()


# ──────────────────────────────────────────────────────────────────────────────
# Session state initialisation
# ──────────────────────────────────────────────────────────────────────────────

def init_session_state() -> None:
    """Initialise all session-state keys if they don't exist yet."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = None
    if "model" not in st.session_state:
        st.session_state.model = None
    if "api_configured" not in st.session_state:
        st.session_state.api_configured = False


# ──────────────────────────────────────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────────────────────────────────────

def render_sidebar() -> None:
    """Render the sidebar with quick facts and navigation."""
    with st.sidebar:
        st.markdown("## 🗳️ Election Buddy")
        st.markdown("Your non-partisan guide to understanding elections worldwide.")
        st.divider()

        # ── Quick Facts ──
        st.markdown("### 💡 Did You Know?")
        facts = load_quick_facts()
        for fact in facts:
            st.markdown(f'<div class="fact-card">{fact}</div>', unsafe_allow_html=True)

        st.divider()

        # ── Navigation hints ──
        st.markdown("### 📚 Explore Topics")
        st.markdown(
            "Try asking me about:\n"
            "- How does voting work in my country?\n"
            "- What is ranked-choice voting?\n"
            "- How are votes counted?\n"
            "- What is gerrymandering?\n"
            "- How do electoral colleges work?",
            help="Suggested conversation starters to explore election topics.",
        )

        st.divider()
        st.caption("Built with ❤️ using Streamlit & Google Gemini")


# ──────────────────────────────────────────────────────────────────────────────
# Main content sections
# ──────────────────────────────────────────────────────────────────────────────

def render_header() -> None:
    """Render the main page header and introduction."""
    st.markdown('<p class="main-header">🗳️ Election Buddy</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">'
        "Your AI-powered, non-partisan guide to understanding elections and democracy."
        "</p>",
        unsafe_allow_html=True,
    )


def render_key_dates_section() -> None:
    """Render the upcoming elections reference section."""
    with st.expander("📅 Upcoming Key Election Dates", expanded=False):
        st.markdown(
            "A quick reference of upcoming major elections around the world. "
            "Dates are approximate and subject to official confirmation.",
            help="This section displays static reference data about upcoming elections.",
        )
        dates = load_election_dates()
        table_md = format_dates_for_display(dates)
        st.markdown(table_md)


def render_voting_systems_section() -> None:
    """Render the voting systems explainer section."""
    with st.expander("🏛️ Voting Systems Explained", expanded=False):
        st.markdown(
            "Understanding how different countries count votes is key to "
            "understanding democracy. Here are the most common systems:",
            help="This section explains different voting systems used globally.",
        )
        systems = load_voting_systems()
        for sys_info in systems:
            st.markdown(f"**{sys_info['system']}**")
            st.markdown(f"{sys_info['description']}")
            st.caption(f"Used in: {sys_info['used_in']}")
            st.markdown("---")


def render_metrics() -> None:
    """Display headline election statistics as metric cards."""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="Democracies Worldwide",
            value="167",
            help="Number of countries classified as democracies by the EIU Democracy Index.",
        )
    with col2:
        st.metric(
            label="Voters in 2024",
            value="2B+",
            help="Estimated number of people who voted in national elections in 2024.",
        )
    with col3:
        st.metric(
            label="Voting Systems",
            value="5+",
            help="Major categories of voting systems used around the world.",
        )
    with col4:
        st.metric(
            label="Countries Covered",
            value="195",
            help="The assistant can answer questions about elections in all 195 UN-recognized countries.",
        )


# ──────────────────────────────────────────────────────────────────────────────
# Chat interface
# ──────────────────────────────────────────────────────────────────────────────

def setup_gemini() -> bool:
    """Attempt to configure the Gemini model. Returns True on success.

    Returns:
        bool: Whether the API was successfully configured.
    """
    try:
        st.session_state.model = get_model()
        st.session_state.chat_session = get_chat_session(st.session_state.model)
        st.session_state.api_configured = True
        return True
    except ValueError as exc:
        st.error(
            f"⚠️ {exc}\n\n"
            "**Setup instructions:**\n"
            "1. Copy `.env.example` to `.env`\n"
            "2. Add your free Gemini API key from [AI Studio](https://aistudio.google.com/apikey)\n"
            "3. Restart the app",
            icon="🔑",
        )
        return False


def render_chat_history() -> None:
    """Display all previous messages in the chat session."""
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        css_class = "chat-user" if role == "user" else "chat-assistant"
        icon = "👤" if role == "user" else "🗳️"

        with st.chat_message(role, avatar=icon):
            st.markdown(
                f'<div class="{css_class}">{content}</div>',
                unsafe_allow_html=True,
            )


def handle_user_input() -> None:
    """Process new user input from the chat box."""
    if prompt := st.chat_input(
        "Ask me anything about elections and voting...",
        key="chat_input",
    ):
        # Display user message immediately
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(
                f'<div class="chat-user">{prompt}</div>',
                unsafe_allow_html=True,
            )

        # Generate and display assistant response
        with st.chat_message("assistant", avatar="🗳️"):
            with st.spinner("Thinking..."):
                try:
                    response = send_message(st.session_state.chat_session, prompt)
                    st.markdown(
                        f'<div class="chat-assistant">{response}</div>',
                        unsafe_allow_html=True,
                    )
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )
                except RuntimeError as exc:
                    st.error(f"❌ {exc}", icon="🚫")


# ──────────────────────────────────────────────────────────────────────────────
# Main App Orchestration
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    """Main entry point — composes all UI sections."""
    init_session_state()
    render_sidebar()
    render_header()
    render_metrics()

    # Reference sections
    col_left, col_right = st.columns(2)
    with col_left:
        render_key_dates_section()
    with col_right:
        render_voting_systems_section()

    st.divider()

    # Chat section
    st.markdown("### 💬 Ask Election Buddy")
    st.markdown(
        "Chat with an AI assistant specialized in election education. "
        "Ask about voting processes, election systems, voter registration, and more.",
        help="This is a conversational AI powered by Google Gemini. "
             "It is restricted to election and democracy topics only.",
    )

    # Attempt Gemini setup (only on first run)
    if not st.session_state.api_configured:
        if not setup_gemini():
            st.stop()

    render_chat_history()
    handle_user_input()


if __name__ == "__main__":
    main()
