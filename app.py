import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime
import random
import time

# --- CONFIGURATION & PALETTE ---
# Premium Underground (Black/Red) + Cyberpunk Splash (Cyan)
COLOR_BG = "#080808"
COLOR_TEXT = "#F0F0F0" 
COLOR_ACCENT = "#FF0033" # Acid Red (Primary Brand)
COLOR_CYAN = "#00f7ff"   # Cyberpunk Splash (Secondary/Tech)
COLOR_SECONDARY = "#141414" # Card Background

# --- BRANDING: LOGO ---
TNF_LOGO_SVG = f"""
<svg width="140" height="40" viewBox="0 0 140 40" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="0" y="0" width="140" height="40" fill="none"/>
<text x="0" y="32" font-family="Helvetica, Arial, sans-serif" font-weight="900" font-size="36" fill="{COLOR_TEXT}" letter-spacing="-3">TNF</text>
<rect x="80" y="10" width="4" height="20" fill="{COLOR_ACCENT}"/>
<rect x="90" y="10" width="4" height="20" fill="{COLOR_CYAN}"/>
<circle cx="115" cy="20" r="6" stroke="{COLOR_TEXT}" stroke-width="2"/>
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
# 2. SESSION STATE VALIDATION (Fixes KeyError)
# -----------------------------------------------------------------------------
# This block ensures that if old data exists in the browser cache without 
# the 'label' key, it gets overwritten with the new correct data.
if 'songs' in st.session_state:
    # Check if the first song has the 'label' key. If not, reset the data.
    if len(st.session_state.songs) > 0 and 'label' not in st.session_state.songs[0]:
        del st.session_state.songs

if 'songs' not in st.session_state:
    st.session_state.songs = [
        {"title": "System Failure (Original Mix)", "label": "House Keeping Rec", "cat": "HKR004"},
        {"title": "Analog Dreams", "label": "Tresor Records", "cat": "TR-291"},
        {"title": "Voltage Control", "label": "Ostgut Ton", "cat": "OSTGUT-55"},
        {"title": "Modular State", "label": "Klockworks", "cat": "KW-22"}
    ]

if 'gallery' not in st.session_state:
    st.session_state.gallery = [
        {"caption": "MODULAR RIG SETUP A", "url": "https://images.unsplash.com/photo-1550291652-6ea9114a47b1?q=80&w=800&auto=format&fit=crop"},
        {"caption": "LIVE SIGNAL PATH", "url": "https://images.unsplash.com/photo-1598275529124-b1c4b786f1e2?q=80&w=800&auto=format&fit=crop"},
        {"caption": "WAREHOUSE CROWD", "url": "https://images.unsplash.com/photo-1571266028243-371695063ad6?q=80&w=800&auto=format&fit=crop"},
        {"caption": "OSCILLATOR DETAIL", "url": "https://images.unsplash.com/photo-1619967657960-983b6329c370?q=80&w=800&auto=format&fit=crop"}
    ]

if 'bookings' not in st.session_state:
    st.session_state.bookings = []

if 'cart' not in st.session_state:
    st.session_state.cart = []

# -----------------------------------------------------------------------------
# 3. CUSTOM CSS
# -----------------------------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&family=Space+Mono:wght@400;700&display=swap');

    /* GLOBAL RESET */
    .stApp {{
        background-color: {COLOR_BG};
        color: {COLOR_TEXT};
        font-family: 'Inter', sans-serif;
    }}

    /* UI CLEANUP */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .block-container {{ padding-top: 2rem !important; max-width: 1400px; }}

    /* --- TYPOGRAPHY --- */
    h1, h2, h3 {{
        font-family: 'Inter', sans-serif;
        text-transform: uppercase;
        font-weight: 900;
        color: {COLOR_TEXT};
        letter-spacing: -1px;
        margin-bottom: 0.5rem;
    }}
    
    /* Subheaders with Cyberpunk Splash */
    h4, h5 {{
        font-family: 'Space Mono', monospace; /* Tech font */
        font-weight: 700;
        color: {COLOR_CYAN} !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.9rem;
    }}

    /* --- UI ELEMENTS --- */
    
    /* Primary Action Button (Red) */
    .stButton>button {{
        background-color: {COLOR_TEXT};
        color: {COLOR_BG};
        border: 1px solid {COLOR_TEXT};
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        text-transform: uppercase;
        padding: 12px 28px;
        border-radius: 0px;
        transition: all 0.3s;
    }}
    .stButton>button:hover {{
        background-color: {COLOR_ACCENT};
        color: {COLOR_TEXT};
        border-color: {COLOR_ACCENT};
        box-shadow: 0 0 15px rgba(255, 0, 51, 0.4);
    }}

    /* Cards / Containers */
    .content-card {{
        background-color: {COLOR_SECONDARY};
        padding: 25px;
        border-left: 3px solid {COLOR_ACCENT};
        margin-bottom: 20px;
        border-right: 1px solid #222;
        border-top: 1px solid #222;
        border-bottom: 1px solid #222;
    }}
    
    /* Tech/System Cards (Cyan Splash) */
    .tech-card {{
        background-color: #0f0f0f;
        padding: 15px;
        border: 1px solid #222;
        border-top: 3px solid {COLOR_CYAN};
        font-family: 'Space Mono', monospace;
        font-size: 0.85rem;
        color: #aaa;
    }}

    /* Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
        background-color: {COLOR_SECONDARY};
        color: {COLOR_TEXT};
        border: 1px solid #333;
        border-radius: 0;
    }}
    .stTextInput>div>div>input:focus {{
        border-color: {COLOR_CYAN};
        box-shadow: 0 0 8px rgba(0, 247, 255, 0.2);
    }}

    /* Links */
    a {{ color: {COLOR_TEXT} !important; text-decoration: none; font-weight: 600; transition: color 0.2s; }}
    a:hover {{ color: {COLOR_CYAN} !important; }}
    
    hr {{ border-color: #222; margin: 3rem 0; }}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. NAVIGATION
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
    # HERO IMAGE: Tech/Abstract
    st.image("https://images.unsplash.com/photo-1558584673-c834fb1cc3ca?q=80&w=1400&auto=format&fit=crop", use_column_width=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"## TUESDAYNIGHTFREAK {TNF_LOGO_SVG}", unsafe_allow_html=True)
        st.markdown("#### ARCHITECTS OF THE ANALOGUE SIGNAL")
        
        st.markdown("""
        <div style="font-size: 1.1rem; line-height: 1.6;">
        Tuesdaynightfreak operates at the intersection of <strong>studio precision</strong> and <strong>live improvisation</strong>. 
        We construct immersive sonic environments using modular synthesis, exploring the tension between mechanical repetition and human error.
        <br><br>
        A sonic movement born in Melbourne, refined in Berlin.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.button("LATEST RELEASE")
        with c2:
            st.button("VIEW TOUR DATES")

    with col2:
        st.markdown("#### SYSTEM UPDATES")
        
        st.markdown(f"""
        <div class="tech-card">
        <span style="color:{COLOR_ACCENT}">●</span> <strong>NEW RELEASE</strong><br>
        'VOLTAGE CONTROL' EP OUT NOW VIA OSTGUT TON.
        </div>
        <br>
        <div class="tech-card">
        <span style="color:{COLOR_CYAN}">●</span> <strong>TOUR ANNOUNCEMENT</strong><br>
        EUROPEAN DATES CONFIRMED FOR WINTER 2025.
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    
    # FEATURED VIDEO
    st.markdown("### LIVE TRANSMISSION")
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1550291652-6ea9114a47b1?q=80&w=800&auto=format&fit=crop", caption="LIVE RIG CONFIGURATION")
    with col2:
        st.markdown("""
        **SESSION 001: MODULAR IMPROV**
        
        Recorded live in one take at The Warehouse Project. 
        A journey through deep textures and driving rhythms.
        
        *Hardware: Eurorack system, TR-909, Moog Sub37.*
        """)
        st.button("WATCH FULL SET")

# --- MUSIC ---
elif selected == "MUSIC":
    st.markdown("## DISCOGRAPHY")
    
    # Track List
    for track in st.session_state.songs:
        c1, c2, c3, c4 = st.columns([1, 4, 2, 2])
        with c1:
            st.markdown(f"<div style='width:50px; height:50px; background-color:{COLOR_SECONDARY}; border:1px solid #333; display:flex; align-items:center; justify-content:center; color:#666; font-size:0.7rem;'>ART</div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"**{track['title']}**")
        with c3:
            st.caption(track['label'] + " // " + track['cat'])
        with c4:
            st.button("STREAM", key=track['title'])
        st.markdown(f"<hr style='margin: 10px 0; border-color: #1a1a1a;'>", unsafe_allow_html=True)

    st.markdown("### HOUSE KEEPING RECORDS")
    c1, c2 = st.columns([1, 1])
    with c1:
        st.image("https://images.unsplash.com/photo-1605218427306-022648d42d32?q=80&w=1200&auto=format&fit=crop", caption="HKR HQ")
    with c2:
        st.markdown("""
        <div class="content-card">
        Our dedicated platform for the raw and the deep.
        <br><br>
        House Keeping Records focuses on functional tools for DJs and sonic explorations for heads. 
        Strictly vinyl releases for select projects.
        </div>
        """, unsafe_allow_html=True)

# --- EVENTS ---
elif selected == "EVENTS":
    st.markdown("## UPCOMING DATES")
    
    events = [
        {"date": "NOV 04", "city": "AMSTERDAM", "venue": "SHELTER", "status": "SELLING FAST"},
        {"date": "NOV 11", "city": "LONDON", "venue": "FOLD", "status": "TICKETS"},
        {"date": "NOV 18", "city": "MELBOURNE", "venue": "REVOLVER", "status": "SOLD OUT"},
        {"date": "DEC 02", "city": "PARIS", "venue": "REX CLUB", "status": "TICKETS"},
    ]
    
    for event in events:
        c1, c2, c3, c4 = st.columns([1, 2, 2, 2])
        with c1:
            st.markdown(f"<span style='color:{COLOR_ACCENT}; font-family:Space Mono; font-weight:bold;'>{event['date']}</span>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"**{event['city']}**")
        with c3:
            st.markdown(event['venue'])
        with c4:
            if event['status'] == "SOLD OUT":
                st.markdown(f"<span style='color:#666; font-family:Space Mono;'>SOLD OUT</span>", unsafe_allow_html=True)
            else:
                st.button(f"BUY {event['status']}", key=event['city'])
        st.markdown(f"<hr style='margin: 10px 0; border-color: #1a1a1a;'>", unsafe_allow_html=True)

# --- STORE (MERCH) ---
elif selected == "STORE":
    st.markdown("## OFFICIAL MERCHANDISE")
    
    # Cart Summary
    if len(st.session_state.cart) > 0:
        st.info(f"CART: {len(st.session_state.cart)} ITEMS")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        # Merch Item 1
        st.markdown(f"""
        <div style="background:{COLOR_SECONDARY}; padding:10px; margin-bottom:10px;">
            <div style="height:200px; background:#000; display:flex; align-items:center; justify-content:center;">
                <span style="color:{COLOR_TEXT}; font-weight:900; font-size:2rem;">TNF</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**TNF CORE TEE [BLACK]**")
        st.caption("Heavyweight Cotton / Screen Print")
        st.markdown(f"**€35.00**")
        if st.button("ADD TO CART", key="m1"):
            st.session_state.cart.append("Tee")
            st.rerun()
        
    with c2:
        # Merch Item 2
        st.markdown(f"""
        <div style="background:{COLOR_SECONDARY}; padding:10px; margin-bottom:10px;">
            <div style="height:200px; background:#000; display:flex; align-items:center; justify-content:center;">
                <span style="color:{COLOR_ACCENT}; font-weight:900; font-size:2rem;">HKR</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**HKR LABEL HOODIE**")
        st.caption("Oversized Fit / Embroidered")
        st.markdown(f"**€65.00**")
        if st.button("ADD TO CART", key="m2"):
            st.session_state.cart.append("Hoodie")
            st.rerun()
        
    with c3:
        # Merch Item 3
        st.markdown(f"""
        <div style="background:{COLOR_SECONDARY}; padding:10px; margin-bottom:10px;">
            <div style="height:200px; background:#000; display:flex; align-items:center; justify-content:center;">
                <span style="color:{COLOR_CYAN}; font-weight:900; font-size:2rem;">◎</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**PROFESSIONAL SLIPMATS (PAIR)**")
        st.caption("High grade felt / Anti-static")
        st.markdown(f"**€20.00**")
        if st.button("ADD TO CART", key="m3"):
            st.session_state.cart.append("Slipmats")
            st.rerun()

# --- ABOUT / CONTACT ---
elif selected == "ABOUT":
    col1, col2 = st.columns([1.5, 1], gap="large")
    
    with col1:
        st.markdown("## BIOGRAPHY")
        st.markdown("""
        **Tuesdaynightfreak** is an electronic music project established in Melbourne, Australia.
        
        Drawing influence from the stark industrialism of Berlin and the soulful rhythms of Detroit, 
        the project explores the boundaries of hardware sequencing. It is a reaction against the 
        predictability of digital production—a celebration of the machine's inherent instability.
        
        From the smoky basements of *Revolver* to the concrete halls of *Tresor*, Tuesdaynightfreak 
        delivers a sound that is distinct, raw, and uncompromising. 
        
        Alongside the live act, the **House Keeping Records** imprint serves as a vessel for 
        like-minded artists pushing the envelope of functional dance music.
        """)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### CONTACT MANAGEMENT")
        st.markdown(f"<div class='tech-card'>mgmt@tuesdaynightfreak.com</div>", unsafe_allow_html=True)
        
        st.markdown("#### DEMO POLICY")
        st.markdown(f"<div class='tech-card'>demos@housekeeping-rec.com (Private SC Links Only)</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("## NEWSLETTER")
        st.write("Join our community for early access to vinyl drops and guestlist spots.")
        with st.form("newsletter"):
            st.text_input("EMAIL ADDRESS")
            st.form_submit_button("SUBSCRIBE")
            
        st.write("---")
        st.markdown("#### PRESS KIT")
        st.button("DOWNLOAD EPK (ZIP)")
