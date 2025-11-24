import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime
import random
import time

# --- CONFIGURATION & PALETTE (Defected-Inspired "Premium Underground") ---
# Palette: Deep Black background, Stark White text, Acid Red Accents
COLOR_BG = "#080808"
COLOR_TEXT = "#F0F0F0" 
COLOR_ACCENT = "#FF0033" # Acid Red for that premium label feel
COLOR_SECONDARY = "#1A1A1A" # Dark Grey for cards

# --- BRANDING: CLEAN TYPOGRAPHIC LOGO ---
TNF_LOGO_SVG = f"""
<svg width="120" height="40" viewBox="0 0 120 40" fill="none" xmlns="http://www.w3.org/2000/svg">
<text x="0" y="30" font-family="Helvetica, Arial, sans-serif" font-weight="900" font-size="32" fill="{COLOR_TEXT}" letter-spacing="-2">TNF</text>
<circle cx="80" cy="20" r="8" fill="{COLOR_ACCENT}"/>
<rect x="95" y="12" width="25" height="16" fill="{COLOR_TEXT}"/>
</svg>
"""

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="TUESDAYNIGHTFREAK | OFFICIAL",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# 2. CUSTOM CSS (Professional, Clean, Editorial)
# -----------------------------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&display=swap');

    /* GLOBAL RESET */
    .stApp {{
        background-color: {COLOR_BG};
        color: {COLOR_TEXT};
        font-family: 'Inter', sans-serif;
    }}

    /* REMOVE DEFAULT UI */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .block-container {{ padding-top: 2rem !important; max-width: 1400px; }}

    /* --- TYPOGRAPHY --- */
    
    /* "Defected" Style Headlines: Bold, Uppercase, Tight Spacing */
    h1, h2, h3 {{
        font-family: 'Inter', sans-serif;
        text-transform: uppercase;
        font-weight: 900;
        color: {COLOR_TEXT};
        letter-spacing: -1px;
        margin-bottom: 0.5rem;
    }}
    
    h4, h5 {{
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: {COLOR_ACCENT} !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.9rem;
    }}

    /* --- UI ELEMENTS --- */
    
    /* Premium Buttons */
    .stButton>button {{
        background-color: {COLOR_TEXT};
        color: {COLOR_BG};
        border: none;
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        text-transform: uppercase;
        padding: 12px 28px;
        border-radius: 0px; /* Square edges for that brutalist/label feel */
        transition: all 0.3s;
    }}
    .stButton>button:hover {{
        background-color: {COLOR_ACCENT};
        color: {COLOR_TEXT};
        transform: scale(1.02);
    }}

    /* Cards / Containers */
    .news-card {{
        background-color: {COLOR_SECONDARY};
        padding: 20px;
        border-left: 4px solid {COLOR_ACCENT};
        margin-bottom: 20px;
        transition: transform 0.3s;
    }}
    .news-card:hover {{
        transform: translateX(5px);
    }}

    /* Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
        background-color: {COLOR_SECONDARY};
        color: {COLOR_TEXT};
        border: 1px solid #333;
        border-radius: 0;
    }}
    .stTextInput>div>div>input:focus {{
        border-color: {COLOR_ACCENT};
    }}

    /* Links */
    a {{ color: {COLOR_TEXT} !important; text-decoration: none; font-weight: 600; }}
    a:hover {{ color: {COLOR_ACCENT} !important; text-decoration: underline; }}
    
    hr {{ border-color: #333; margin: 3rem 0; }}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. STATE & DATA
# -----------------------------------------------------------------------------
if 'songs' not in st.session_state:
    st.session_state.songs = [
        {"title": "System Failure (Original Mix)", "label": "House Keeping Rec", "cat": "HKR004"},
        {"title": "Analog Dreams", "label": "Tresor Records", "cat": "TR-291"},
        {"title": "Voltage Control", "label": "Ostgut Ton", "cat": "OSTGUT-55"}
    ]

# NEW IMAGES: Modular, Tech, Crowd (No Guitars/DJs)
if 'gallery' not in st.session_state:
    st.session_state.gallery = [
        {"caption": "MODULAR RIG SETUP A", "url": "https://images.unsplash.com/photo-1550291652-6ea9114a47b1?q=80&w=800&auto=format&fit=crop"},
        {"caption": "LIVE SIGNAL PATH", "url": "https://images.unsplash.com/photo-1598275529124-b1c4b786f1e2?q=80&w=800&auto=format&fit=crop"},
        {"caption": "WAREHOUSE CROWD", "url": "https://images.unsplash.com/photo-1571266028243-371695063ad6?q=80&w=800&auto=format&fit=crop"},
        {"caption": "OSCILLATOR DETAIL", "url": "https://images.unsplash.com/photo-1619967657960-983b6329c370?q=80&w=800&auto=format&fit=crop"}
    ]

if 'bookings' not in st.session_state:
    st.session_state.bookings = []

# -----------------------------------------------------------------------------
# 4. NAVIGATION (Clean, Top-Bar)
# -----------------------------------------------------------------------------
selected = option_menu(
    menu_title=None,
    options=["HOME", "MUSIC", "EVENTS", "STORE", "ABOUT"],
    icons=["house-fill", "disc-fill", "calendar-event-fill", "bag-fill", "info-circle-fill"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": COLOR_BG, "border-bottom": "1px solid #333"},
        "icon": {"color": "#666", "font-size": "12px"}, 
        "nav-link": {
            "font-size": "14px", "text-align": "center", "margin": "0px", 
            "color": "#888", "font-family": "Inter, sans-serif", "text-transform": "uppercase", "font-weight": "600"
        },
        "nav-link-selected": {"background-color": COLOR_BG, "color": COLOR_TEXT, "border-bottom": f"2px solid {COLOR_ACCENT}"},
    }
)

# -----------------------------------------------------------------------------
# 5. PAGE CONTENT
# -----------------------------------------------------------------------------

# --- HOME PAGE ---
if selected == "HOME":
    # HERO SECTION: Big Image, Bold Text
    # Replacing DJ image with Modular/Abstract Tech image
    st.image("https://images.unsplash.com/photo-1517457375825-e578c799a74f?q=80&w=1400&auto=format&fit=crop", use_column_width=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"## TUESDAYNIGHTFREAK {TNF_LOGO_SVG}", unsafe_allow_html=True)
        st.markdown("#### DEFINING THE FUTURE OF LIVE HARDWARE ELECTRONICS")
        
        st.markdown("""
        Tuesdaynightfreak represents a new era in electronic music performance. 
        Bridging the gap between studio precision and live improvisation, we construct 
        immersive soundscapes using only modular synthesis and drum machines. 
        
        **No Laptops. No Sync. Pure Voltage.**
        """)
        st.button("LISTEN TO LATEST RELEASE")

    with col2:
        # LATEST NEWS / UPDATES (Defected Style "News Feed")
        st.markdown("#### LATEST NEWS")
        
        st.markdown(f"""
        <div class="news-card">
        <strong>NEW EP ANNOUNCED</strong><br>
        <span style="font-size:0.8rem; color:#888;">OCT 24, 2025</span><br>
        'Voltage Control' drops worldwide next Friday on House Keeping Records.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="news-card">
        <strong>EUROPEAN TOUR DATES</strong><br>
        <span style="font-size:0.8rem; color:#888;">OCT 10, 2025</span><br>
        We are hitting the road this winter. Check the Events page for details.
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    
    # FEATURED VIDEO (YouTube Embed Style)
    st.markdown("### LIVE SESSIONS")
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1510915364890-a7d41f02c611?q=80&w=800&auto=format&fit=crop", caption="LIVE FROM THE WAREHOUSE")
    with col2:
        st.markdown("""
        **SESSION 001: MODULAR IMPROV**
        
        Recorded live in one take. A journey through deep textures and driving rhythms.
        Hardware used: Eurorack system (Make Noise, Intellijel), TR-909.
        """)
        st.button("WATCH FULL SET")

# --- MUSIC ---
elif selected == "MUSIC":
    st.markdown("## DISCOGRAPHY")
    
    # Clean List View (Label Style)
    for track in st.session_state.songs:
        c1, c2, c3, c4 = st.columns([1, 4, 2, 2])
        with c1:
            # Small thumbnail placeholder
            st.markdown(f"<div style='width:50px; height:50px; background-color:{COLOR_ACCENT};'></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"**{track['title']}**")
        with c3:
            st.caption(track['label'])
        with c4:
            st.button("STREAM", key=track['title'])
        st.markdown(f"<hr style='margin: 10px 0; border-color: #222;'>", unsafe_allow_html=True)

    st.markdown("### HOUSE KEEPING RECORDS")
    st.image("https://images.unsplash.com/photo-1605218427306-022648d42d32?q=80&w=1200&auto=format&fit=crop", caption="HKR HQ")
    st.write("Our home for the raw and the deep. Establishing a new standard for vinyl releases.")

# --- EVENTS ---
elif selected == "EVENTS":
    st.markdown("## UPCOMING DATES")
    
    # Event List Table Style
    events = [
        {"date": "NOV 04", "city": "AMSTERDAM", "venue": "SHELTER", "status": "SELLING FAST"},
        {"date": "NOV 11", "city": "LONDON", "venue": "FOLD", "status": "TICKETS"},
        {"date": "NOV 18", "city": "MELBOURNE", "venue": "REVOLVER", "status": "SOLD OUT"},
        {"date": "DEC 02", "city": "PARIS", "venue": "REX CLUB", "status": "TICKETS"},
    ]
    
    for event in events:
        c1, c2, c3, c4 = st.columns([1, 2, 2, 2])
        with c1:
            st.markdown(f"<span style='color:{COLOR_ACCENT}; font-weight:900;'>{event['date']}</span>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"**{event['city']}**")
        with c3:
            st.markdown(event['venue'])
        with c4:
            if event['status'] == "SOLD OUT":
                st.markdown(f"<span style='color:#666;'>SOLD OUT</span>", unsafe_allow_html=True)
            else:
                st.button(f"BUY {event['status']}", key=event['city'])
        st.markdown(f"<hr style='margin: 10px 0; border-color: #222;'>", unsafe_allow_html=True)

# --- STORE ---
elif selected == "STORE":
    st.markdown("## SHOP MERCH & VINYL")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.image("https://images.unsplash.com/photo-1585227803927-2c24067b9416?q=80&w=600&auto=format&fit=crop", caption="HKR004 - VINYL 12\"")
        st.markdown("**SYSTEM FAILURE EP**")
        st.caption("€14.00")
        st.button("ADD TO CART", key="p1")
        
    with c2:
        st.image("https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?q=80&w=600&auto=format&fit=crop", caption="TNF LOGO TEE")
        st.markdown("**OFFICIAL T-SHIRT**")
        st.caption("€35.00")
        st.button("ADD TO CART", key="p2")
        
    with c3:
        st.image("https://images.unsplash.com/photo-1529339077446-df732dfa062c?q=80&w=600&auto=format&fit=crop", caption="PATCH CABLE SET")
        st.markdown("**TNF CABLE PACK**")
        st.caption("€20.00")
        st.button("ADD TO CART", key="p3")

# --- ABOUT / CONTACT ---
elif selected == "ABOUT":
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("## THE PROJECT")
        st.markdown("""
        **Tuesdaynightfreak** is a dedicated exploration of electronic sound. 
        Founded in Melbourne, the project focuses on the visceral experience of 
        live hardware performance.
        
        We believe in the power of the machine and the human error that brings it to life.
        Our sets are improvised, raw, and unique to every venue.
        """)
        
        st.markdown("#### CONTACT MANAGEMENT")
        st.code("mgmt@tuesdaynightfreak.com")
        
        st.markdown("#### DEMOS")
        st.code("demos@housekeeping-rec.com")

    with col2:
        st.markdown("## NEWSLETTER")
        st.write("Join our community for early access to vinyl drops and guestlist spots.")
        with st.form("newsletter"):
            st.text_input("EMAIL ADDRESS")
            st.form_submit_button("SUBSCRIBE")
            
        st.write("---")
        st.markdown("#### PRESS KIT")
        st.button("DOWNLOAD EPK (ZIP)")
