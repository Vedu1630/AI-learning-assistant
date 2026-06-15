import os
import streamlit as st

from graph.learning_graph import learning_graph
from rag.pdf_loader import load_pdf
from rag.youtube_loader import load_youtube
from rag.vector_store import create_vector_store

# =====================================
# Page Config & Advanced Styling
# =====================================
st.set_page_config(
    page_title="AI Learning Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom SVG flat-shaded 3D graphics
HERO_SVG = """
<svg viewBox="0 0 400 280" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <!-- Grid background lines -->
  <path d="M 50 180 L 200 105 L 350 180 L 200 255 Z" fill="none" stroke="#F4F4F5" stroke-width="1.5" />
  <path d="M 80 165 L 200 105 L 320 165" fill="none" stroke="#F4F4F5" stroke-width="1.5" />
  <path d="M 110 150 L 200 105 L 290 150" fill="none" stroke="#F4F4F5" stroke-width="1.5" />
  <path d="M 140 135 L 200 105 L 260 135" fill="none" stroke="#F4F4F5" stroke-width="1.5" />
  <path d="M 170 120 L 200 105 L 230 120" fill="none" stroke="#F4F4F5" stroke-width="1.5" />
  
  <path d="M 50 180 L 200 255" fill="none" stroke="#E4E4E7" stroke-dasharray="2 2" stroke-width="1" />
  <path d="M 350 180 L 200 255" fill="none" stroke="#E4E4E7" stroke-dasharray="2 2" stroke-width="1" />

  <!-- Base Platform -->
  <polygon points="200,160 300,210 200,260 100,210" fill="#FAFAFA" stroke="#E4E4E7" stroke-width="1" />
  <polygon points="100,210 200,260 200,268 100,218" fill="#F4F4F5" stroke="#E4E4E7" stroke-width="1" />
  <polygon points="200,260 300,210 300,218 200,268" fill="#E4E4E7" stroke="#E4E4E7" stroke-width="1" />

  <!-- 3D Stack of Documents -->
  <!-- Document 3 (Bottom) -->
  <polygon points="140,175 190,200 160,215 110,190" fill="#E2E8F0" stroke="#CBD5E1" stroke-width="1" />
  <polygon points="110,190 160,215 160,218 110,193" fill="#CBD5E1" stroke="#CBD5E1" stroke-width="1" />
  <polygon points="160,215 190,200 190,203 160,218" fill="#94A3B8" stroke="#CBD5E1" stroke-width="1" />
  <!-- Document 2 (Middle) -->
  <polygon points="135,168 185,193 155,208 105,183" fill="#C7D2FE" stroke="#A5B4FC" stroke-width="1" />
  <polygon points="105,183 155,208 155,211 105,186" fill="#A5B4FC" stroke="#A5B4FC" stroke-width="1" />
  <polygon points="155,208 185,193 185,196 155,211" fill="#818CF8" stroke="#A5B4FC" stroke-width="1" />
  <!-- Document 1 (Top) -->
  <polygon points="130,160 180,185 150,200 100,175" fill="#FFFFFF" stroke="#E4E4E7" stroke-width="1" />
  <polygon points="100,175 150,200 150,203 100,178" fill="#E4E4E7" stroke="#E4E4E7" stroke-width="1" />
  <polygon points="150,200 180,185 180,188 150,203" fill="#D4D4D8" stroke="#E4E4E7" stroke-width="1" />
  <line x1="120" y1="172" x2="140" y2="182" stroke="#A1A1AA" stroke-width="1.5" />
  <line x1="125" y1="180" x2="155" y2="195" stroke="#A1A1AA" stroke-width="1.5" />
  <line x1="130" y1="188" x2="150" y2="198" stroke="#A1A1AA" stroke-width="1.5" />

  <!-- Dotted lines indicating learning/reading -->
  <path d="M 140 170 Q 200 130 200 90" fill="none" stroke="#4F46E5" stroke-width="1.5" stroke-dasharray="3 3" />
  <path d="M 270 170 Q 200 130 200 90" fill="none" stroke="#4F46E5" stroke-width="1.5" stroke-dasharray="3 3" />

  <!-- Floating 3D Octahedron AI Core -->
  <polygon points="200,40 170,80 200,95" fill="#C7D2FE" stroke="#818CF8" stroke-width="0.5" />
  <polygon points="200,40 200,95 230,80" fill="#818CF8" stroke="#4F46E5" stroke-width="0.5" />
  <polygon points="200,40 170,80 200,65" fill="#E0E7FF" opacity="0.6" />
  <polygon points="200,40 230,80 200,65" fill="#C7D2FE" opacity="0.6" />
  <polygon points="200,115 170,80 200,95" fill="#818CF8" stroke="#4F46E5" stroke-width="0.5" />
  <polygon points="200,115 200,95 230,80" fill="#4F46E5" stroke="#4F46E5" stroke-width="0.5" />

  <!-- Floating Rings / Halo around Core -->
  <ellipse cx="200" cy="80" rx="45" ry="22" fill="none" stroke="#18181B" stroke-width="1" stroke-dasharray="6 4" transform="rotate(-5, 200, 80)" />
  <ellipse cx="200" cy="80" rx="55" ry="27" fill="none" stroke="#4F46E5" stroke-width="0.8" stroke-dasharray="20 15" />

  <!-- Database Cylinder -->
  <ellipse cx="260" cy="170" rx="20" ry="10" fill="#F4F4F5" stroke="#D4D4D8" stroke-width="1" />
  <path d="M 240 170 L 240 195 A 20 10 0 0 0 280 195 L 280 170 Z" fill="#E4E4E7" stroke="#D4D4D8" stroke-width="1" />
  <path d="M 240 182 A 20 10 0 0 0 280 182" fill="none" stroke="#D4D4D8" stroke-width="1" />
  <path d="M 260 170 L 260 205" fill="none" stroke="#D4D4D8" stroke-width="1" opacity="0.4" />
  <ellipse cx="260" cy="195" rx="20" ry="10" fill="none" stroke="#D4D4D8" stroke-width="1" />
</svg>
"""

FEAT1_SVG = """
<svg viewBox="0 0 160 120" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <!-- Isometric Grid Base -->
  <polygon points="80,25 130,50 80,75 30,50" fill="#FAFAFA" stroke="#E4E4E7" stroke-width="1" />
  <line x1="55" y1="37.5" x2="105" y2="62.5" stroke="#F4F4F5" stroke-width="1" />
  <line x1="67.5" y1="43.75" x2="117.5" y2="68.75" stroke="#F4F4F5" stroke-width="1" />
  <line x1="105" y1="37.5" x2="55" y2="62.5" stroke="#F4F4F5" stroke-width="1" />
  <line x1="92.5" y1="43.75" x2="42.5" y2="68.75" stroke="#F4F4F5" stroke-width="1" />
  <polygon points="80,50 92.5,56.25 80,62.5 67.5,56.25" fill="#E0E7FF" stroke="#818CF8" stroke-width="1" />

  <!-- 3D Magnifying Glass -->
  <polygon points="45,85 50,82 65,95 60,98" fill="#818CF8" stroke="#4F46E5" stroke-width="1" />
  <polygon points="45,85 60,98 60,101 45,88" fill="#4F46E5" stroke="#4F46E5" stroke-width="1" />
  <ellipse cx="75" cy="70" rx="16" ry="10" fill="none" stroke="#4F46E5" stroke-width="2.5" />
  <ellipse cx="75" cy="70" rx="16" ry="10" fill="#C7D2FE" opacity="0.3" />
  <line x1="75" y1="70" x2="80" y2="56.25" stroke="#4F46E5" stroke-width="1" stroke-dasharray="2 2" />
</svg>
"""

FEAT2_SVG = """
<svg viewBox="0 0 160 120" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <!-- Notebook Cover -->
  <polygon points="75,25 125,50 85,78 35,53" fill="#E4E4E7" stroke="#D4D4D8" stroke-width="1" />
  <polygon points="35,53 85,78 85,82 35,57" fill="#D4D4D8" stroke="#D4D4D8" stroke-width="1" />
  <polygon points="85,78 125,50 125,54 85,82" fill="#A1A1AA" stroke="#D4D4D8" stroke-width="1" />

  <!-- Notebook Pages -->
  <polygon points="75,22 122,46 82,74 35,50" fill="#FFFFFF" stroke="#E4E4E7" stroke-width="1" />
  <polygon points="35,50 82,74 82,77 35,53" fill="#E4E4E7" stroke="#E4E4E7" stroke-width="1" />
  <polygon points="73,19 115,40 78,66 36,45" fill="#FAFAFA" stroke="#4F46E5" stroke-width="1" />
  
  <!-- Spiral bindings -->
  <path d="M 40,43 Q 38,39 42,37 Q 46,35 44,39" fill="none" stroke="#18181B" stroke-width="1.5" />
  <path d="M 50,49 Q 48,45 52,43 Q 56,41 54,45" fill="none" stroke="#18181B" stroke-width="1.5" />
  <path d="M 60,55 Q 58,51 62,49 Q 66,47 64,51" fill="none" stroke="#18181B" stroke-width="1.5" />
  <path d="M 70,61 Q 68,57 72,55 Q 76,53 74,57" fill="none" stroke="#18181B" stroke-width="1.5" />

  <!-- Page Lines -->
  <line x1="55" y1="48" x2="85" y2="63" stroke="#A5B4FC" stroke-width="1" />
  <line x1="60" y1="53" x2="90" y2="68" stroke="#A5B4FC" stroke-width="1" />
  <line x1="65" y1="58" x2="95" y2="73" stroke="#A5B4FC" stroke-width="1" />
</svg>
"""

FEAT3_SVG = """
<svg viewBox="0 0 160 120" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <!-- Clipboard Backing -->
  <polygon points="80,20 125,42 85,78 40,56" fill="#F4F4F5" stroke="#E4E4E7" stroke-width="1" />
  <polygon points="40,56 85,78 85,83 40,61" fill="#E4E4E7" stroke="#E4E4E7" stroke-width="1" />
  <polygon points="85,78 125,42 125,47 85,83" fill="#D4D4D8" stroke="#E4E4E7" stroke-width="1" />

  <!-- Sheet of Paper -->
  <polygon points="78,24 118,44 80,74 44,54" fill="#FFFFFF" stroke="#E4E4E7" stroke-width="1" />

  <!-- 3D Clip at Top -->
  <polygon points="72,23 83,28 78,32 67,27" fill="#94A3B8" stroke="#64748B" stroke-width="1" />
  <polygon points="67,27 78,32 78,34 67,29" fill="#64748B" stroke="#64748B" stroke-width="1" />

  <!-- Quiz Questions -->
  <line x1="60" y1="42" x2="95" y2="59.5" stroke="#71717A" stroke-width="1.2" />
  <polygon points="50,42 55,44.5 52,47 47,44.5" fill="#FFFFFF" stroke="#4F46E5" stroke-width="1" />
  <polyline points="49,44 50,45 53,42" fill="none" stroke="#4F46E5" stroke-width="1" />

  <line x1="66" y1="51" x2="101" y2="68.5" stroke="#71717A" stroke-width="1.2" />
  <polygon points="56,51 61,53.5 58,56 53,53.5" fill="#FFFFFF" stroke="#E4E4E7" stroke-width="1" />

  <line x1="72" y1="60" x2="97" y2="72.5" stroke="#71717A" stroke-width="1.2" />
  <polygon points="62,60 67,62.5 64,65 59,62.5" fill="#FFFFFF" stroke="#4F46E5" stroke-width="1" />
  <polyline points="61,62 62,63 65,60" fill="none" stroke="#4F46E5" stroke-width="1" />
</svg>
"""

# Helper function to render framed SVGs
def render_framed_svg(svg_markup, caption=None):
    caption_html = f'<div style="text-align: center; color: #71717A; font-size: 0.75rem; margin-top: 8px; font-weight: 500;">{caption}</div>' if caption else ''
    st.html(
        f"""
        <div class="framed-graphic-container">
            <div class="framed-graphic-content">
                {svg_markup}
            </div>
            {caption_html}
        </div>
        """
    )

# Inject Light Minimal UI CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Set font globally on main containers to inherit naturally, avoiding breaking icon fonts */
    html, body, .stApp, [data-testid="stSidebar"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Hide standard Streamlit header and footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Enforce light theme backgrounds */
    .stApp {
        background-color: #ffffff !important;
        color: #18181B !important;
    }
    
    /* Enforce light theme in dark mode environments */
    [data-theme="dark"] {
        --background-color: #ffffff !important;
        --text-color: #18181B !important;
    }

    /* ── SIDEBAR: permanently-open white left panel ── */
    /* Force sidebar open at all times by overriding Streamlit's collapse CSS */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E4E4E7 !important;
        min-width: 300px !important;
        max-width: 300px !important;
        width: 300px !important;
        transform: none !important;
        visibility: visible !important;
        display: flex !important;
        flex-direction: column !important;
        pointer-events: auto !important;
        transition: none !important;
    }
    /* Ensure sidebar inner content is always visible */
    [data-testid="stSidebar"] > div {
        display: flex !important;
        flex-direction: column !important;
        visibility: visible !important;
        opacity: 1 !important;
        width: 300px !important;
    }
    /* Hide BOTH collapse and expand arrow buttons so sidebar state can't be toggled */
    button[data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
    }
    /* Sidebar headings & text */
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #18181B !important;
        font-size: 0.9rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
        margin-bottom: 4px !important;
    }
    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] caption,
    [data-testid="stSidebar"] small {
        color: #71717A !important;
        font-size: 0.8rem !important;
    }
    [data-testid="stSidebar"] label {
        color: #3F3F46 !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
    }
    /* Sidebar divider */
    [data-testid="stSidebar"] hr {
        border-color: #E4E4E7 !important;
        margin: 16px 0 !important;
    }
    /* Ensure main content area accounts for fixed-width sidebar */
    section.main {
        margin-left: 300px !important;
    }
    
    /* Global button styling (secondary/default button) */
    .stButton>button, .stDownloadButton>button {
        background-color: #FFFFFF !important;
        color: #18181B !important;
        border: 1px solid #E4E4E7 !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        box-shadow: 0px 1px 2px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.15s ease-in-out !important;
        width: 100%;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background-color: #F4F4F5 !important;
        border-color: #D4D4D8 !important;
        color: #18181B !important;
        box-shadow: 0px 1px 2px rgba(0, 0, 0, 0.05) !important;
    }
    .stButton>button:active, .stDownloadButton>button:active {
        background-color: #E4E4E7 !important;
    }

    /* Primary button override (accent charcoal) */
    button[data-testid="baseButton-primary"] {
        background-color: #18181B !important;
        color: #FFFFFF !important;
        border: 1px solid #18181B !important;
        box-shadow: 0px 1px 2px rgba(24, 24, 27, 0.15) !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
    }
    button[data-testid="baseButton-primary"]:hover {
        background-color: #27272A !important;
        border-color: #27272A !important;
        color: #FFFFFF !important;
    }
    button[data-testid="baseButton-primary"]:active {
        background-color: #3F3F46 !important;
        border-color: #3F3F46 !important;
    }

    /* Form input capsule styled like ChatGPT */
    div[data-testid="stForm"] {
        border: 1px solid #E4E4E7 !important;
        border-radius: 24px !important;
        background-color: #FFFFFF !important;
        padding: 6px 16px !important;
        box-shadow: 0px 1px 2px rgba(0, 0, 0, 0.05) !important;
        transition: border-color 0.15s ease-in-out !important;
        margin-bottom: 24px !important;
        display: flex !important;
        align-items: center !important;
    }
    div[data-testid="stForm"]:focus-within {
        border-color: #A1A1AA !important;
    }
    div[data-testid="stForm"] > div {
        border: none !important;
        width: 100% !important;
    }
    div[data-testid="stForm"] [data-testid="stHorizontalBlock"] {
        align-items: center !important;
        gap: 12px !important;
    }
    div[data-testid="stForm"] input {
        border: none !important;
        box-shadow: none !important;
        padding: 8px 0px !important;
        background-color: transparent !important;
        font-size: 0.95rem !important;
        color: #18181B !important;
    }
    div[data-testid="stForm"] input:focus,
    div[data-testid="stForm"] input:active,
    div[data-testid="stForm"] input:focus-visible {
        box-shadow: none !important;
        outline: none !important;
        border: none !important;
        border-color: transparent !important;
    }
    /* Remove red border Streamlit adds to focused inputs */
    div[data-testid="stForm"] [data-baseweb="input"]:focus-within,
    div[data-testid="stForm"] [data-baseweb="input"] input:focus,
    div[data-testid="stForm"] div[class*="stTextInput"] input,
    div[data-testid="stForm"] div[class*="stTextInput"] input:focus {
        border: none !important;
        border-color: transparent !important;
        box-shadow: none !important;
        outline: none !important;
    }
    /* BaseWeb Input container focus ring override */
    div[data-testid="stForm"] [data-baseweb="input"] {
        border: none !important;
        background-color: transparent !important;
        box-shadow: none !important;
    }
    div[data-testid="stForm"] button {
        background-color: #18181B !important;
        color: #FFFFFF !important;
        border: 1px solid #18181B !important;
        border-radius: 20px !important;
        padding: 6px 16px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        box-shadow: none !important;
        width: auto !important;
    }
    div[data-testid="stForm"] button:hover {
        background-color: #27272A !important;
        border-color: #27272A !important;
    }

    /* Hide the 'Press Enter to submit form' hint text inside the input */
    div[data-testid="stForm"] [data-testid="InputInstructions"],
    div[data-testid="stForm"] .st-emotion-cache-wnm74r,
    div[data-testid="stForm"] small,
    div[data-testid="stForm"] [class*="InputInstructions"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* Tabs styling (flat centered pill style) */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #F4F4F5 !important;
        border: 1px solid #E4E4E7 !important;
        border-radius: 20px !important;
        padding: 3px !important;
        gap: 2px !important;
        display: flex !important;
        justify-content: center !important;
        width: fit-content !important;
        margin: 0 auto 2rem auto !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 500 !important;
        color: #71717A !important;
        padding: 6px 18px !important;
        border: none !important;
        border-radius: 16px !important;
        transition: all 0.1s ease !important;
        background-color: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #18181B !important;
        box-shadow: 0px 1px 2px rgba(0, 0, 0, 0.05) !important;
        border: none !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }
    
    /* File Uploader — clean white theme */
    [data-testid="stFileUploader"] {
        border: 1px dashed #D4D4D8 !important;
        border-radius: 8px !important;
        background-color: #FAFAFA !important;
        padding: 8px !important;
    }
    [data-testid="stFileUploader"] section {
        background-color: #FAFAFA !important;
    }
    [data-testid="stFileUploader"] button {
        background-color: #FFFFFF !important;
        color: #18181B !important;
        border: 1px solid #E4E4E7 !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        padding: 6px 14px !important;
        font-size: 0.85rem !important;
    }
    [data-testid="stFileUploader"] button:hover {
        background-color: #F4F4F5 !important;
        border-color: #D4D4D8 !important;
    }
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] small {
        color: #71717A !important;
    }

    /* Chat Messages styling (Claude/ChatGPT alignment) */
    div[data-testid="stChatMessage"] {
        padding: 16px 0px !important;
        margin-bottom: 8px !important;
        box-shadow: none !important;
    }
    div[data-testid="stChatMessage"]:has([class*="user"]),
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatar"] [class*="user"]) {
        background-color: #F4F4F5 !important;
        border: 1px solid #E4E4E7 !important;
        border-radius: 18px !important;
        padding: 12px 18px !important;
        max-width: 75% !important;
        margin-left: auto !important;
        margin-right: 0px !important;
        box-shadow: 0px 1px 2px rgba(0, 0, 0, 0.02) !important;
    }
    div[data-testid="stChatMessage"]:has([class*="assistant"]),
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatar"] [class*="assistant"]) {
        background-color: transparent !important;
        border: none !important;
        border-radius: 0px !important;
        padding: 16px 0px !important;
        max-width: 100% !important;
        margin-left: 0px !important;
    }
    [data-testid="stChatMessageContent"] p {
        margin: 0 !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        color: #18181B !important;
    }

    /* Containers for notes/quiz/summary */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #E4E4E7 !important;
        border-radius: 8px !important;
        background-color: #FAFAFA !important;
        padding: 24px !important;
        box-shadow: none !important;
    }

    /* Custom empty state components formatting */
    .empty-state-container {
        text-align: center !important;
        margin-top: 40px !important;
        margin-bottom: 24px !important;
    }
    .empty-state-container .framed-graphic-container {
        max-width: 340px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        margin-bottom: 24px !important;
        background-color: #FAFAFA !important;
        border: 1px solid #E4E4E7 !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }
    .empty-state-title {
        font-size: 2.25rem !important;
        font-weight: 700 !important;
        color: #18181B !important;
        margin-bottom: 12px !important;
        letter-spacing: -0.03em !important;
    }
    .empty-state-subtitle {
        font-size: 1.05rem !important;
        color: #71717A !important;
        margin-bottom: 32px !important;
    }

    .framed-graphic-content {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }
    .framed-graphic-content svg {
        max-width: 100%;
        height: auto;
    }
    
    /* Main content area — shifted right since sidebar is fixed */
    .block-container {
        max-width: 820px !important;
        padding-top: 2.5rem !important;
        padding-bottom: 3rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Clear any cached sidebar collapsed state from browser localStorage on every page load.
st.markdown("""
<script>
(function() {
    // Wipe Streamlit localStorage sidebar state so it always loads expanded
    try {
        for (var key in localStorage) {
            if (/sidebar|collapsed/i.test(key)) {
                localStorage.removeItem(key);
            }
        }
    } catch(e) {}
})();
</script>
""", unsafe_allow_html=True)

# =====================================
# Session State Initialization
# =====================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "notes" not in st.session_state:
    st.session_state.notes = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "quiz" not in st.session_state:
    st.session_state.quiz = ""
if "content_processed" not in st.session_state:
    st.session_state.content_processed = False

# =====================================
# Sidebar: Knowledge Context Panel
# =====================================
with st.sidebar:
    st.markdown("### 📚 Knowledge Context")
    st.caption("Feed documents or videos to your AI assistant.")
    st.divider()

    uploaded_file = st.file_uploader("Upload PDF Document", type=["pdf"])
    youtube_url = st.text_input("YouTube URL", placeholder="https://youtu.be/...")

    st.markdown("")
    process_btn = st.button("Initialize Knowledge Base", type="primary", use_container_width=True)

    if st.session_state.content_processed:
        st.success("✅ Context ready")

# =====================================
# Processing Logic
# =====================================
if process_btn:
    try:
        combined_text = ""
        os.makedirs("data", exist_ok=True)

        if uploaded_file:
            pdf_path = os.path.join("data", uploaded_file.name)
            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            combined_text += load_pdf(pdf_path)

        if youtube_url:
            combined_text += "\n\n" + load_youtube(youtube_url)

        if not combined_text.strip():
            st.sidebar.error("⚠️ Please upload a PDF or add a YouTube URL.")
        else:
            with st.sidebar.status("🔄 Analyzing Context...", expanded=True) as status:
                st.write("Generating vector embeddings...")
                create_vector_store(combined_text)
                with open("data/document.txt", "w", encoding="utf-8") as f:
                    f.write(combined_text)
                status.update(label="✅ System Ready!", state="complete", expanded=False)
                st.session_state.content_processed = True
            st.rerun()

    except Exception as e:
        st.sidebar.error(f"Error: {str(e)}")

# =====================================
# Main Interface Layout
# =====================================

# --- Welcome Screen (only when chat is empty) ---
if not st.session_state.chat_history:
    st.html("""
    <div class="empty-state-container">
    """)
    render_framed_svg(HERO_SVG, None)
    st.html("""
        <div class="empty-state-title">What are you learning today?</div>
        <div class="empty-state-subtitle">Upload a PDF or paste a YouTube link in the left panel to start learning.</div>
    </div>
    """)

# --- Input Bar (always visible at top) ---
with st.container():
    with st.form("chat_input_form", clear_on_submit=True, border=False):
        col1, col2 = st.columns([6, 1])
        with col1:
            question = st.text_input(
                "Ask a question...",
                label_visibility="collapsed",
                placeholder="Message your AI Learning Assistant..."
            )
        with col2:
            submitted = st.form_submit_button("Send ✨", use_container_width=True)

# Process submitted question
if submitted and question:
    if not st.session_state.content_processed and not os.path.exists("data/document.txt"):
        st.error("Please initialize the knowledge base from the left panel first.")
    else:
        with st.spinner("Synthesizing response..."):
            try:
                state = {"query": question, "task": "", "result": ""}
                result = learning_graph.invoke(state)
                answer = result["result"]
                st.session_state.chat_history.insert(0, {
                    "question": question,
                    "answer": answer
                })
                st.rerun()
            except Exception as e:
                st.error(f"Processing error: {str(e)}")

# --- Tabs below the input bar ---
chat_tab, notes_tab, summary_tab, quiz_tab = st.tabs([
    "✨ Chat",
    "📝 Smart Notes",
    "📖 Executive Summary",
    "❓ Knowledge Check"
])

# -------------------------------------
# CHAT TAB
# -------------------------------------
with chat_tab:
    for item in st.session_state.chat_history:
        with st.chat_message("user", avatar="👤"):
            st.markdown(item["question"])
        with st.chat_message("assistant", avatar="✨"):
            st.markdown(item["answer"])

# -------------------------------------
# NOTES TAB
# -------------------------------------
with notes_tab:
    if st.button("Generate Structured Notes", use_container_width=True, type="primary"):
        with st.spinner("Extracting key insights..."):
            state = {"query": "create notes", "task": "", "result": ""}
            st.session_state.notes = learning_graph.invoke(state)["result"]

    if st.session_state.notes:
        with st.container(border=True):
            st.markdown(st.session_state.notes)
        st.download_button("Download Notes (.txt)", st.session_state.notes, "notes.txt")

# -------------------------------------
# SUMMARY TAB
# -------------------------------------
with summary_tab:
    if st.button("Generate Executive Summary", use_container_width=True, type="primary"):
        with st.spinner("Condensing information..."):
            state = {"query": "create summary", "task": "", "result": ""}
            st.session_state.summary = learning_graph.invoke(state)["result"]

    if st.session_state.summary:
        with st.container(border=True):
            st.markdown(st.session_state.summary)
        st.download_button("Download Summary (.txt)", st.session_state.summary, "summary.txt")

# -------------------------------------
# QUIZ TAB
# -------------------------------------
with quiz_tab:
    if st.button("Generate Knowledge Check", use_container_width=True, type="primary"):
        with st.spinner("Formulating questions..."):
            state = {"query": "generate quiz", "task": "", "result": ""}
            st.session_state.quiz = learning_graph.invoke(state)["result"]

    if st.session_state.quiz:
        with st.container(border=True):
            st.markdown(st.session_state.quiz)
        st.download_button("Download Quiz (.txt)", st.session_state.quiz, "quiz.txt")