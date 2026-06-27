import streamlit as st
import time
from pipeline import run_research_pipeline

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* ── Base ── */
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

  html, body, [class*="css"] {
      font-family: 'Space Grotesk', sans-serif;
  }

  /* Dark background */
  .stApp {
      background-color: #0d0f14;
      color: #e2e8f0;
  }

  /* ── Hero header ── */
  .hero {
      text-align: center;
      padding: 3rem 1rem 2rem;
  }
  .hero-eyebrow {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      letter-spacing: 0.22em;
      color: #6ee7b7;
      text-transform: uppercase;
      margin-bottom: 0.75rem;
  }
  .hero-title {
      font-size: clamp(2rem, 5vw, 3.4rem);
      font-weight: 700;
      line-height: 1.1;
      color: #f8fafc;
      margin-bottom: 0.5rem;
  }
  .hero-title span {
      color: #6ee7b7;
  }
  .hero-sub {
      color: #94a3b8;
      font-size: 1.05rem;
      max-width: 560px;
      margin: 0 auto;
  }

  /* ── Pipeline steps row ── */
  .steps-row {
      display: flex;
      justify-content: center;
      gap: 0;
      margin: 2rem auto 2.5rem;
      max-width: 780px;
  }
  .step-pill {
      display: flex;
      align-items: center;
      gap: 0.45rem;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      color: #64748b;
      padding: 0.3rem 0.8rem;
  }
  .step-pill .dot {
      width: 6px; height: 6px;
      border-radius: 50%;
      background: #334155;
      flex-shrink: 0;
  }
  .step-pill.active .dot  { background: #6ee7b7; }
  .step-pill.active       { color: #6ee7b7; }
  .step-arrow {
      color: #1e293b;
      font-size: 0.9rem;
      align-self: center;
  }

  /* ── Input area ── */
  .input-card {
      background: #131720;
      border: 1px solid #1e293b;
      border-radius: 12px;
      padding: 1.5rem 2rem;
      max-width: 680px;
      margin: 0 auto 2rem;
  }

  div[data-testid="stTextInput"] input {
      background: #0d0f14 !important;
      border: 1px solid #1e293b !important;
      border-radius: 8px !important;
      color: #f8fafc !important;
      font-family: 'Space Grotesk', sans-serif !important;
      font-size: 1rem !important;
      padding: 0.65rem 1rem !important;
  }
  div[data-testid="stTextInput"] input:focus {
      border-color: #6ee7b7 !important;
      box-shadow: 0 0 0 3px rgba(110,231,183,0.12) !important;
  }

  div[data-testid="stTextInput"] label {
      color: #94a3b8 !important;
      font-size: 0.82rem !important;
      font-family: 'JetBrains Mono', monospace !important;
      letter-spacing: 0.1em !important;
  }

  /* ── Run button ── */
  div[data-testid="stButton"] > button {
      background: #6ee7b7 !important;
      color: #0d0f14 !important;
      border: none !important;
      border-radius: 8px !important;
      font-family: 'Space Grotesk', sans-serif !important;
      font-weight: 600 !important;
      font-size: 0.95rem !important;
      padding: 0.6rem 2rem !important;
      cursor: pointer !important;
      transition: opacity 0.15s !important;
      width: 100% !important;
  }
  div[data-testid="stButton"] > button:hover {
      opacity: 0.88 !important;
  }

  /* ── Status bar ── */
  .status-bar {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      background: #131720;
      border: 1px solid #1e293b;
      border-left: 3px solid #6ee7b7;
      border-radius: 8px;
      padding: 0.75rem 1.25rem;
      margin-bottom: 1.5rem;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      color: #6ee7b7;
  }
  .status-spinner {
      width: 10px; height: 10px;
      border-radius: 50%;
      background: #6ee7b7;
      animation: pulse 1.2s ease-in-out infinite;
      flex-shrink: 0;
  }
  @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50%       { opacity: 0.4; transform: scale(0.7); }
  }

  /* ── Result panels ── */
  .panel {
      background: #131720;
      border: 1px solid #1e293b;
      border-radius: 12px;
      padding: 1.5rem;
      margin-bottom: 1.25rem;
  }
  .panel-header {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      margin-bottom: 1rem;
  }
  .panel-num {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.68rem;
      color: #6ee7b7;
      background: rgba(110,231,183,0.1);
      border: 1px solid rgba(110,231,183,0.25);
      border-radius: 4px;
      padding: 0.15rem 0.45rem;
      letter-spacing: 0.08em;
  }
  .panel-title {
      font-weight: 600;
      font-size: 0.95rem;
      color: #e2e8f0;
  }
  .panel-body {
      color: #94a3b8;
      font-size: 0.9rem;
      line-height: 1.7;
      white-space: pre-wrap;
      word-break: break-word;
  }

  /* Report panel gets a slightly lighter body color */
  .panel.report .panel-body {
      color: #cbd5e1;
  }

  /* Feedback panel accent */
  .panel.feedback {
      border-left: 3px solid #f59e0b;
  }
  .panel.feedback .panel-num {
      color: #f59e0b;
      background: rgba(245,158,11,0.08);
      border-color: rgba(245,158,11,0.25);
  }

  /* ── Divider ── */
  .divider {
      border: none;
      border-top: 1px solid #1e293b;
      margin: 2rem 0;
  }

  /* ── Hide Streamlit chrome ── */
  #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">// multi-agent ai system</div>
  <div class="hero-title">Research, <span>automated.</span></div>
  <div class="hero-sub">Four specialized agents work in sequence — searching, scraping, writing, and critiquing — to produce a polished research report on any topic.</div>
</div>

<div class="steps-row">
  <div class="step-pill"><span class="dot"></span>Search Agent</div>
  <div class="step-arrow">→</div>
  <div class="step-pill"><span class="dot"></span>Reader Agent</div>
  <div class="step-arrow">→</div>
  <div class="step-pill"><span class="dot"></span>Writer Chain</div>
  <div class="step-arrow">→</div>
  <div class="step-pill"><span class="dot"></span>Critic Chain</div>
</div>
""", unsafe_allow_html=True)


# ── Input card ────────────────────────────────────────────────────────────────
st.markdown('<div class="input-card">', unsafe_allow_html=True)

topic = st.text_input(
    "RESEARCH TOPIC",
    placeholder="e.g. Quantum computing breakthroughs in 2025",
    label_visibility="visible",
)

run = st.button("Run Research Pipeline →")

st.markdown('</div>', unsafe_allow_html=True)


# ── Pipeline execution ────────────────────────────────────────────────────────
if run:
    if not topic.strip():
        st.warning("Please enter a research topic before running.")
    else:
        # Step-by-step status display
        status_placeholder = st.empty()
        results_placeholder = st.empty()

        steps = [
            ("01", "Search Agent", "Querying the web for recent, reliable information…"),
            ("02", "Reader Agent", "Scraping the most relevant source for deeper content…"),
            ("03", "Writer Chain", "Drafting a structured research report…"),
            ("04", "Critic Chain", "Reviewing the report for accuracy and completeness…"),
        ]

        def show_status(num, label, message):
            status_placeholder.markdown(f"""
            <div class="status-bar">
              <div class="status-spinner"></div>
              <span style="color:#475569">STEP {num} /</span>
              <strong>{label}</strong>
              <span style="color:#475569">—</span>
              {message}
            </div>
            """, unsafe_allow_html=True)

        show_status(*steps[0])

        try:
            # We monkey-patch print so we can surface real-time step changes.
            # The actual pipeline is called once; status updates simulate progress.
            import builtins
            original_print = builtins.print
            step_index = [0]

            def custom_print(*args, **kwargs):
                text = " ".join(str(a) for a in args)
                for i, (num, label, msg) in enumerate(steps):
                    if label.split()[0].lower() in text.lower():
                        step_index[0] = i
                        show_status(num, label, msg)
                        break
                original_print(*args, **kwargs)

            builtins.print = custom_print

            state = run_research_pipeline(topic)

        except Exception as e:
            builtins.print = original_print
            status_placeholder.empty()
            st.error(f"Pipeline error: {e}")
            st.stop()
        finally:
            builtins.print = original_print

        status_placeholder.empty()

        # ── Results ──────────────────────────────────────────────────────────
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown(
            '<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.72rem;'
            'letter-spacing:0.18em;color:#6ee7b7;text-transform:uppercase;'
            'margin-bottom:1.25rem">// pipeline output</div>',
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2, gap="medium")

        with col1:
            st.markdown(f"""
            <div class="panel">
              <div class="panel-header">
                <span class="panel-num">STEP 01</span>
                <span class="panel-title">Search Results</span>
              </div>
              <div class="panel-body">{state.get("search_results", "—")}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="panel feedback">
              <div class="panel-header">
                <span class="panel-num">STEP 04</span>
                <span class="panel-title">Critic Feedback</span>
              </div>
              <div class="panel-body">{state.get("feedback", "—")}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="panel">
              <div class="panel-header">
                <span class="panel-num">STEP 02</span>
                <span class="panel-title">Scraped Content</span>
              </div>
              <div class="panel-body">{state.get("scraped_content", "—")}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="panel report">
              <div class="panel-header">
                <span class="panel-num">STEP 03</span>
                <span class="panel-title">Final Report</span>
              </div>
              <div class="panel-body">{state.get("report", "—")}</div>
            </div>
            """, unsafe_allow_html=True)

        # ── Download report ───────────────────────────────────────────────────
        report_text = state.get("report", "")
        if report_text:
            st.download_button(
                label="⬇  Download Report as .txt",
                data=report_text,
                file_name=f"research_{topic[:40].replace(' ','_')}.txt",
                mime="text/plain",
            )