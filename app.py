import html
import markdown as md_lib
import streamlit as st
import streamlit.components.v1 as components
from agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 16px;
}
.stApp { background-color: #0d0f14 !important; color: #e2e8f0 !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 2rem 3rem !important;
    max-width: 900px !important;
    margin: 0 auto !important;
}

/* ── Hero ── */
.hero { text-align: center; padding: 2.5rem 1rem 1.25rem; }
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    color: #6ee7b7;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 700;
    line-height: 1.15;
    color: #f8fafc;
    margin-bottom: 0.45rem;
}
.hero-title span { color: #6ee7b7; }
.hero-sub {
    color: #64748b;
    font-size: 0.92rem;
    max-width: 500px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Steps row ── */
.steps-row {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    margin: 1.25rem auto 1.75rem;
}
.step-pill {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #334155;
    padding: 0.2rem 0.6rem;
    white-space: nowrap;
}
.step-pill .dot { width: 5px; height: 5px; border-radius: 50%; background: #1e293b; flex-shrink: 0; }
.step-arrow { color: #1e293b; font-size: 0.8rem; }

/* ── Input card ── */
.input-wrap {
    max-width: 600px;
    margin: 0 auto 1.75rem;
    background: #131720;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
}
div[data-testid="stTextInput"] label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.66rem !important;
    letter-spacing: 0.14em !important;
    color: #475569 !important;
    text-transform: uppercase !important;
    margin-bottom: 0.35rem !important;
    display: block !important;
}
div[data-testid="stTextInput"] input {
    background: #0d0f14 !important;
    border: 1px solid #1e293b !important;
    border-radius: 8px !important;
    color: #f1f5f9 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.92rem !important;
    padding: 0.5rem 0.85rem !important;
    height: auto !important;
    width: 100% !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #6ee7b7 !important;
    box-shadow: 0 0 0 3px rgba(110,231,183,0.08) !important;
    outline: none !important;
}
div[data-testid="stTextInput"] input::placeholder { color: #2d3f55 !important; }

/* ── Submit button ── */
div[data-testid="stFormSubmitButton"] > button {
    background: #6ee7b7 !important;
    color: #0d0f14 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 0.5rem 1.5rem !important;
    width: 100% !important;
    margin-top: 0.65rem !important;
    cursor: pointer !important;
    transition: opacity 0.15s !important;
}
div[data-testid="stFormSubmitButton"] > button:hover { opacity: 0.85 !important; }

/* ── Status rows ── */
.status-active {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    background: #131720;
    border: 1px solid #1e293b;
    border-left: 3px solid #6ee7b7;
    border-radius: 0 8px 8px 0;
    padding: 0.6rem 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #6ee7b7;
    margin-bottom: 0.4rem;
}
.status-done {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    background: #0f1419;
    border: 1px solid #1a2332;
    border-left: 3px solid #1e4d3a;
    border-radius: 0 8px 8px 0;
    padding: 0.45rem 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #2d6b52;
    margin-bottom: 0.4rem;
}
.status-done .ck { color: #6ee7b7; }
.status-waiting {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    background: #0d0f14;
    border: 1px solid #141920;
    border-left: 3px solid #141920;
    border-radius: 0 8px 8px 0;
    padding: 0.45rem 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #1e293b;
    margin-bottom: 0.4rem;
}
.pulse {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #6ee7b7;
    flex-shrink: 0;
    animation: blink 1.2s ease-in-out infinite;
}
@keyframes blink {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.3; transform: scale(0.6); }
}

/* ── Divider ── */
.divider { border: none; border-top: 1px solid #1e293b; margin: 1.5rem 0 1rem; }

/* ── Section label ── */
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    color: #6ee7b7;
    text-transform: uppercase;
    margin-bottom: 0.9rem;
}

/* ── Download button ── */
div[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    color: #6ee7b7 !important;
    border: 1px solid #1e293b !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 0.42rem 1.1rem !important;
    margin-top: 0.4rem !important;
    width: auto !important;
    transition: border-color 0.15s !important;
}
div[data-testid="stDownloadButton"] > button:hover { border-color: #6ee7b7 !important; }

/* ── Alert ── */
div[data-testid="stAlert"] {
    background: rgba(245,158,11,0.06) !important;
    border: 1px solid rgba(245,158,11,0.18) !important;
    border-radius: 8px !important;
    color: #f59e0b !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.83rem !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers for step rendering ────────────────────────────────────────────────
STEPS = [
    ("01", "Search Agent",  "Querying the web for recent, reliable information…"),
    ("02", "Reader Agent",  "Scraping the most relevant source for deeper content…"),
    ("03", "Writer Chain",  "Drafting a structured research report…"),
    ("04", "Critic Chain",  "Reviewing the report for accuracy and completeness…"),
]

def render_done(slot, idx):
    num, label, _ = STEPS[idx]
    slot.markdown(
        f'<div class="status-done">'
        f'<span class="ck">✓</span> STEP {num} / {label}'
        f'</div>',
        unsafe_allow_html=True,
    )

def render_active(slot, idx):
    num, label, msg = STEPS[idx]
    slot.markdown(
        f'<div class="status-active">'
        f'<div class="pulse"></div>'
        f'<span style="color:#475569">STEP {num} /</span>'
        f'&nbsp;<strong style="color:#6ee7b7">{label}</strong>'
        f'&nbsp;<span style="color:#475569">—</span>&nbsp;'
        f'<span style="color:#94a3b8">{msg}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

def render_waiting(slot, idx):
    num, label, _ = STEPS[idx]
    slot.markdown(
        f'<div class="status-waiting">STEP {num} / {label}</div>',
        unsafe_allow_html=True,
    )

def to_str(value) -> str:
    """Safely convert any pipeline output to a clean plain string."""
    if isinstance(value, str):
        return value
    if hasattr(value, "content"):
        value = value.content
    if isinstance(value, list):
        parts = []
        for item in value:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                if item.get("type") == "text":
                    parts.append(item.get("text", ""))
                # skip reference/citation blocks
            elif hasattr(item, "content"):
                parts.append(to_str(item.content))
            else:
                parts.append(str(item))
        return "\n".join(p for p in parts if p.strip())
    return str(value)


def extract_agent_output(result: dict) -> str:
    """Extract final clean text from a LangGraph agent result."""
    messages = result.get("messages", [])
    for msg in reversed(messages):
        role = getattr(msg, "type", None) or getattr(msg, "role", None)
        if role in ("ai", "assistant"):
            text = to_str(msg.content)
            if text.strip():
                return text
    if messages:
        return to_str(messages[-1].content)
    return "—"


def render_panel(title, num, content, amber=False, full_width=False):
    """Return an HTML string for a result panel with rendered markdown."""
    border   = "border-left:3px solid #f59e0b;border-radius:0 10px 10px 0;" if amber else ""
    max_h    = "380px" if full_width else "210px"
    body_col = "#94a3b8" if full_width else "#64748b"
    # Convert markdown → HTML so ** and ## render properly
    rendered = md_lib.markdown(to_str(content), extensions=["nl2br"])
    accent   = "#f59e0b" if amber else "#6ee7b7"
    bg_acc   = "rgba(245,158,11,0.07)" if amber else "rgba(110,231,183,0.07)"
    bd_acc   = "rgba(245,158,11,0.18)" if amber else "rgba(110,231,183,0.18)"
    return f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
      .body {{ margin:0; padding:0; background:transparent; }}
      .panel-body h1,.panel-body h2,.panel-body h3 {{
        font-family:'Space Grotesk',sans-serif;
        color:#e2e8f0; font-weight:600; margin:0.6rem 0 0.3rem;
        font-size:0.88rem; line-height:1.4;
      }}
      .panel-body p {{ margin:0 0 0.5rem; }}
      .panel-body strong {{ color:#cbd5e1; font-weight:600; }}
      .panel-body ul,.panel-body ol {{ padding-left:1.1rem; margin:0.3rem 0 0.5rem; }}
      .panel-body li {{ margin-bottom:0.25rem; }}
      .panel-body a {{ color:#6ee7b7; text-decoration:none; word-break:break-all; }}
      .panel-body a:hover {{ text-decoration:underline; }}
      .panel-body hr {{ border:none; border-top:1px solid #1e293b; margin:0.5rem 0; }}
    </style>
    <div style="background:#131720;border:1px solid #1e293b;border-radius:10px;
                {border}padding:0.9rem 1rem;display:flex;flex-direction:column;
                height:100%;font-family:'Space Grotesk',sans-serif">
      <div style="display:flex;align-items:center;gap:0.45rem;margin-bottom:0.65rem;flex-shrink:0">
        <span style="font-family:'JetBrains Mono',monospace;font-size:0.62rem;
                     color:{accent};background:{bg_acc};border:1px solid {bd_acc};
                     border-radius:4px;padding:0.1rem 0.38rem;letter-spacing:0.06em">
          STEP {num}
        </span>
        <span style="font-weight:600;font-size:0.85rem;color:#e2e8f0">{title}</span>
      </div>
      <div class="panel-body"
           style="color:{body_col};font-size:0.81rem;line-height:1.65;
                  word-break:break-word;overflow-y:auto;max-height:{max_h};flex:1;
                  scrollbar-width:thin;scrollbar-color:#1e293b transparent">
        {rendered}
      </div>
    </div>"""


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">// multi-agent ai system</div>
  <div class="hero-title">Research, <span>automated.</span></div>
  <div class="hero-sub">Four specialized agents work in sequence — searching, scraping,
  writing, and critiquing — to produce a polished research report on any topic.</div>
</div>
<div class="steps-row">
  <div class="step-pill"><span class="dot"></span>Search Agent</div>
  <span class="step-arrow">→</span>
  <div class="step-pill"><span class="dot"></span>Reader Agent</div>
  <span class="step-arrow">→</span>
  <div class="step-pill"><span class="dot"></span>Writer Chain</div>
  <span class="step-arrow">→</span>
  <div class="step-pill"><span class="dot"></span>Critic Chain</div>
</div>
""", unsafe_allow_html=True)


# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="input-wrap">', unsafe_allow_html=True)
with st.form(key="research_form", clear_on_submit=False):
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        label_visibility="visible",
    )
    run = st.form_submit_button("Run Research Pipeline →")
st.markdown('</div>', unsafe_allow_html=True)


# ── Pipeline (each step runs separately so UI can update between them) ────────
if run:
    if not topic.strip():
        st.warning("Please enter a research topic before running.")
    else:
        # Create one st.empty() slot per step — these update in real time
        slots = [st.empty() for _ in range(4)]

        # Initial state: step 0 active, rest waiting
        render_active(slots[0], 0)
        render_waiting(slots[1], 1)
        render_waiting(slots[2], 2)
        render_waiting(slots[3], 3)

        state = {
            "search_results": "",
            "scraped_content": "",
            "report": "",
            "feedback": "",
        }

        try:
            # ── STEP 1: Search Agent ──────────────────────────────────────────
            search_agent  = build_search_agent()
            search_result = search_agent.invoke({
                "messages": [("user",
                    f"Find recent, reliable and detailed information about {topic}")]
            })
            state["search_results"] = extract_agent_output(search_result)

            render_done(slots[0], 0)
            render_active(slots[1], 1)

            # ── STEP 2: Reader Agent ──────────────────────────────────────────
            reader_agent  = build_reader_agent()
            reader_result = reader_agent.invoke({
                "messages": [("user", f"""
Based on the following search results about "{topic}",
Pick the most relevant URL and scrape it for detailed content.
Search Results:
{state["search_results"][:1000]}
""")]
            })
            state["scraped_content"] = extract_agent_output(reader_result)

            render_done(slots[1], 1)
            render_active(slots[2], 2)

            # ── STEP 3: Writer Chain ──────────────────────────────────────────
            research = (
                f"SEARCH RESULTS\n{state['search_results']}\n\n"
                f"SCRAPED CONTENT\n{state['scraped_content']}"
            )
            state["report"] = writer_chain.invoke({
                "topic": topic,
                "research": research,
            })

            render_done(slots[2], 2)
            render_active(slots[3], 3)

            # ── STEP 4: Critic Chain ──────────────────────────────────────────
            state["feedback"] = critic_chain.invoke({
                "report": state["report"],
            })

            render_done(slots[3], 3)

        except Exception as e:
            st.error(f"Pipeline error: {e}")
            st.stop()

        # ── Results ──────────────────────────────────────────────────────────
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">// pipeline output</div>', unsafe_allow_html=True)

        FONT_LINK = '<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'

        # Row 1: Search Results | Scraped Content
        col1, col2 = st.columns(2, gap="small")
        with col1:
            components.html(
                FONT_LINK + render_panel("Search Results", "01", state["search_results"]),
                height=290, scrolling=False,
            )
        with col2:
            components.html(
                FONT_LINK + render_panel("Scraped Content", "02", state["scraped_content"]),
                height=290, scrolling=False,
            )

        # Row 2: Full report (full width)
        st.markdown('<div class="section-label" style="margin-top:0.75rem">// full report</div>', unsafe_allow_html=True)
        components.html(
            FONT_LINK + render_panel("Final Report", "03", state["report"], full_width=True),
            height=460, scrolling=False,
        )

        # Row 3: Critic Feedback (full width)
        st.markdown('<div class="section-label" style="margin-top:0.75rem">// critic feedback</div>', unsafe_allow_html=True)
        components.html(
            FONT_LINK + render_panel("Critic Feedback", "04", state["feedback"], amber=True, full_width=True),
            height=320, scrolling=False,
        )

        # Download
        if state.get("report"):
            st.download_button(
                label="⬇  Download Report as .txt",
                data=state["report"],
                file_name=f"research_{topic[:40].replace(' ', '_')}.txt",
                mime="text/plain",
            )