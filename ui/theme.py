"""YatraAI design system.

A single inject_theme() call wires up the global look-and-feel: web fonts, a
violet -> blue -> sky brand gradient, a glassmorphism surface treatment, styled
controls, and a set of reusable CSS classes (.glass-card, .pill, .badge, ...)
that the rest of the UI renders into.

Keep all visual constants here so the product has one consistent design language.
"""

import streamlit as st

# ----------------------------------------------------------------------------
# Brand palette (single source of truth for colors used across the UI)
# ----------------------------------------------------------------------------
COLORS = {
    "violet": "#7C3AED",
    "blue": "#2563EB",
    "sky": "#0EA5E9",
    "coral": "#F97316",
    "mint": "#10B981",
    "ink": "#0F172A",
    "slate": "#475569",
    "mist": "#94A3B8",
    "line": "rgba(148, 163, 184, 0.18)",
    "surface": "rgba(255, 255, 255, 0.72)",
}

BRAND_GRADIENT = "linear-gradient(120deg, #7C3AED 0%, #2563EB 48%, #0EA5E9 100%)"
CORAL_GRADIENT = "linear-gradient(120deg, #F97316 0%, #FB7185 100%)"


def inject_theme() -> None:
    """Inject the global stylesheet. Call once, right after st.set_page_config."""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

        :root {{
            --violet: {COLORS['violet']};
            --blue: {COLORS['blue']};
            --sky: {COLORS['sky']};
            --coral: {COLORS['coral']};
            --mint: {COLORS['mint']};
            --ink: {COLORS['ink']};
            --slate: {COLORS['slate']};
            --line: {COLORS['line']};
            --brand-gradient: {BRAND_GRADIENT};
        }}

        /* ---- Base canvas: soft mesh gradient background ---- */
        .stApp {{
            background:
                radial-gradient(1100px 600px at 8% -8%, rgba(124,58,237,0.14), transparent 60%),
                radial-gradient(1000px 620px at 102% 0%, rgba(14,165,233,0.14), transparent 55%),
                radial-gradient(900px 700px at 50% 120%, rgba(249,115,22,0.08), transparent 60%),
                #F6F8FC;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--ink);
        }}

        /* widen the work area a touch */
        .block-container {{
            padding-top: 1.4rem;
            padding-bottom: 3rem;
            max-width: 1280px;
        }}

        /* ---- Hide default Streamlit chrome for a product feel ---- */
        #MainMenu, header[data-testid="stHeader"], footer {{ visibility: hidden; }}
        header[data-testid="stHeader"] {{ height: 0; }}

        /* ---- Typography ---- */
        h1, h2, h3, h4 {{
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            color: var(--ink);
            letter-spacing: -0.02em;
        }}
        h1 {{ font-weight: 800 !important; }}
        h2, h3 {{ font-weight: 700 !important; }}

        /* ---- Sidebar: frosted glass ---- */
        [data-testid="stSidebar"] > div:first-child {{
            background: rgba(255,255,255,0.66);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border-right: 1px solid var(--line);
        }}
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {{ font-size: 1.02rem !important; }}

        /* ---- Buttons: gradient pill, primary CTA ---- */
        .stButton > button {{
            border-radius: 12px;
            border: 1px solid var(--line);
            background: rgba(255,255,255,0.85);
            color: var(--ink);
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 600;
            padding: 0.5rem 1.1rem;
            transition: transform .12s ease, box-shadow .12s ease, background .12s ease;
        }}
        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 10px 24px rgba(37,99,235,0.16);
            border-color: rgba(37,99,235,0.35);
        }}
        /* primary buttons (type="primary") get the brand gradient */
        .stButton > button[kind="primary"] {{
            background: var(--brand-gradient);
            color: #fff;
            border: none;
            box-shadow: 0 10px 26px rgba(124,58,237,0.30);
        }}
        .stButton > button[kind="primary"]:hover {{
            box-shadow: 0 14px 32px rgba(124,58,237,0.42);
        }}

        /* ---- Chat input: floating glass bar ---- */
        [data-testid="stChatInput"] {{
            border-radius: 16px;
            border: 1px solid var(--line);
            background: rgba(255,255,255,0.9);
            box-shadow: 0 12px 30px rgba(15,23,42,0.08);
        }}
        [data-testid="stChatInput"] textarea {{ font-size: 0.98rem; }}

        /* ---- Chat bubbles ---- */
        [data-testid="stChatMessage"] {{
            background: rgba(255,255,255,0.7);
            border: 1px solid var(--line);
            border-radius: 16px;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }}

        /* ---- Tabs ---- */
        [data-testid="stTabs"] [data-baseweb="tab-list"] {{
            gap: 6px;
            background: rgba(255,255,255,0.55);
            padding: 6px;
            border-radius: 14px;
            border: 1px solid var(--line);
        }}
        [data-testid="stTabs"] [data-baseweb="tab"] {{
            border-radius: 10px;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 600;
            color: var(--slate);
            padding: 6px 14px;
        }}
        [data-testid="stTabs"] [aria-selected="true"] {{
            background: var(--brand-gradient);
            color: #fff !important;
        }}

        /* ---- Metric cards ---- */
        [data-testid="stMetric"] {{
            background: rgba(255,255,255,0.78);
            border: 1px solid var(--line);
            border-radius: 16px;
            padding: 14px 16px;
            box-shadow: 0 6px 18px rgba(15,23,42,0.05);
        }}
        [data-testid="stMetricLabel"] {{ color: var(--slate); }}

        /* ===================================================================
           Reusable component classes (rendered via st.markdown(unsafe_allow_html))
           =================================================================== */

        /* Glassmorphism surface */
        .glass-card {{
            background: rgba(255,255,255,0.72);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255,255,255,0.55);
            border-radius: 20px;
            padding: 22px 24px;
            box-shadow: 0 14px 40px rgba(15,23,42,0.08);
        }}

        /* Hero */
        .yatra-hero {{
            position: relative;
            border-radius: 28px;
            padding: 46px 44px;
            color: #fff;
            overflow: hidden;
            background: {BRAND_GRADIENT};
            box-shadow: 0 30px 70px rgba(37,99,235,0.32);
        }}
        .yatra-hero::after {{
            content: "";
            position: absolute; inset: 0;
            background:
                radial-gradient(420px 220px at 88% 12%, rgba(255,255,255,0.28), transparent 70%),
                radial-gradient(360px 240px at 6% 100%, rgba(249,115,22,0.30), transparent 70%);
            pointer-events: none;
        }}
        .yatra-hero h1 {{
            color: #fff !important;
            font-size: 2.7rem;
            line-height: 1.08;
            margin: 10px 0 8px 0;
        }}
        .yatra-hero p.sub {{
            color: rgba(255,255,255,0.92);
            font-size: 1.08rem;
            max-width: 640px;
            margin: 0;
        }}
        .hero-stats {{ display: flex; gap: 26px; margin-top: 26px; flex-wrap: wrap; }}
        .hero-stat .n {{ font-family:'Plus Jakarta Sans'; font-weight:800; font-size:1.5rem; }}
        .hero-stat .l {{ color: rgba(255,255,255,0.82); font-size:.82rem; letter-spacing:.04em; text-transform:uppercase; }}

        /* Badge / pill */
        .badge {{
            display: inline-flex; align-items: center; gap: 7px;
            background: rgba(255,255,255,0.18);
            border: 1px solid rgba(255,255,255,0.35);
            color: #fff;
            padding: 6px 14px; border-radius: 999px;
            font-size: .8rem; font-weight: 600; letter-spacing: .03em;
            backdrop-filter: blur(6px);
        }}
        .pill {{
            display:inline-flex; align-items:center; gap:6px;
            background: rgba(124,58,237,0.10);
            color: var(--violet);
            border: 1px solid rgba(124,58,237,0.22);
            padding: 5px 12px; border-radius: 999px;
            font-size: .8rem; font-weight: 600; margin: 0 6px 6px 0;
        }}
        .pill.coral {{ background: rgba(249,115,22,0.12); color: var(--coral); border-color: rgba(249,115,22,0.25); }}
        .pill.mint  {{ background: rgba(16,185,129,0.12); color: var(--mint);  border-color: rgba(16,185,129,0.25); }}

        /* Section heading */
        .section-head {{ display:flex; align-items:center; gap:10px; margin: 6px 0 14px 0; }}
        .section-head .t {{ font-family:'Plus Jakarta Sans'; font-weight:700; font-size:1.25rem; color:var(--ink); }}
        .section-head .d {{ color: var(--slate); font-size:.92rem; }}

        /* subtle entrance animation */
        @keyframes yatraFadeUp {{ from {{opacity:0; transform: translateY(10px);}} to {{opacity:1; transform:none;}} }}
        .glass-card, .yatra-hero {{ animation: yatraFadeUp .45s ease both; }}

        a {{ color: var(--blue); text-decoration: none; }}

        /* ---- Bordered containers become glass cards (used for day cards) ---- */
        [data-testid="stVerticalBlockBorderWrapper"] {{
            background: rgba(255,255,255,0.72);
            border: 1px solid var(--line) !important;
            border-radius: 18px;
            box-shadow: 0 10px 30px rgba(15,23,42,0.06);
        }}

        /* ---- Day-card header ---- */
        .day-head {{ display:flex; align-items:center; justify-content:space-between; gap:12px; flex-wrap:wrap; }}
        .day-badge {{
            display:inline-flex; align-items:center; gap:8px;
            background: var(--brand-gradient); color:#fff;
            font-family:'Plus Jakarta Sans'; font-weight:700;
            padding:6px 14px; border-radius:999px; font-size:.9rem;
        }}
        .day-title {{ font-family:'Plus Jakarta Sans'; font-weight:700; font-size:1.18rem; color:var(--ink); }}
        .day-meta {{ color:var(--slate); font-size:.86rem; display:flex; gap:14px; flex-wrap:wrap; }}
        .day-meta b {{ color:var(--ink); }}

        /* ---- Activity timeline ---- */
        .tl {{ margin-top: 14px; }}
        .tl-item {{ display:flex; gap:14px; align-items:flex-start; }}
        .tl-time {{ width:70px; flex:0 0 70px; text-align:right; padding-top:1px; }}
        .tl-time .t {{ font-family:'Plus Jakarta Sans'; font-weight:700; color:var(--ink); font-size:.95rem; }}
        .tl-time .l {{ color:var(--mist); font-size:.7rem; text-transform:uppercase; letter-spacing:.04em; }}
        .tl-rail {{ flex:0 0 16px; display:flex; flex-direction:column; align-items:center; align-self:stretch; }}
        .tl-dot {{ width:12px; height:12px; border-radius:50%; background:var(--brand-gradient); margin-top:4px;
                   box-shadow:0 0 0 4px rgba(124,58,237,0.14); }}
        .tl-line {{ flex:1; width:2px; background:linear-gradient(var(--violet), var(--sky)); opacity:.35; margin:4px 0; }}
        .tl-body {{ flex:1; padding-bottom:16px; }}
        .tl-act {{ font-weight:600; color:var(--ink); }}
        .tl-cost {{ color:var(--coral); font-size:.8rem; font-weight:600; }}
        .tl-travel {{ color:var(--slate); font-size:.78rem; margin:2px 0 10px 0; }}
        .tl-travel .chip {{ background:rgba(37,99,235,0.08); border:1px solid rgba(37,99,235,0.18);
                            color:var(--blue); border-radius:999px; padding:2px 10px; font-weight:600; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, desc: str = "", icon: str = "✦") -> None:
    """Render a consistent section heading with optional description."""
    st.markdown(
        f"""
        <div class="section-head">
            <span class="pill">{icon}</span>
            <span class="t">{title}</span>
            {f'<span class="d">— {desc}</span>' if desc else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )
