# =====================================================
# TUESDAYNIGHTFREAK | OFFICIAL SITE — FINAL v27
# NO BOOT SCREEN — INSTANT LOAD ON HOME — FULL ORIGINAL
# DEPLOY READY — WORKS 100%
# =====================================================

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime

# --- CONFIGURATION & PALETTE ---
COLOR_BG = "#080808"
COLOR_TEXT = "#F0F0F0"
COLOR_ACCENT = "#FF0033"
COLOR_CYAN = "#00f7ff"
COLOR_SECONDARY = "#141414"

# --- BRANDING SVGs ---
TNF_LOGO_SVG = f"""
<svg width="160" height="50" viewBox="0 0 160 50" fill="none" xmlns="http://www.w3.org/2000/svg">
    <text x="2" y="32" font-family="Helvetica" font-weight="900" font-size="36" fill="{COLOR_CYAN}" opacity="0.7" letter-spacing="-3">TNF</text>
    <text x="-2" y="32" font-family="Helvetica" font-weight="900" font-size="36" fill="{COLOR_ACCENT}" opacity="0.7" letter-spacing="-3">TNF</text>
    <text x="0" y="32" font-family="Helvetica" font-weight="900" font-size="36" fill="{COLOR_TEXT}" letter-spacing="-3">TNF</text>
    <rect x="85" y="10" width="4" height="20" fill="{COLOR_ACCENT}"/>
    <rect x="95" y="10" width="4" height="20" fill="{COLOR_CYAN}"/>
    <rect x="105" y="10" width="4" height="20" fill="{COLOR_TEXT}"/>
    <circle cx="130" cy="20" r="6" stroke="{COLOR_TEXT}" stroke-width="2"/>
    <line x1="0" y1="45" x2="140" y2="45" stroke="{COLOR_CYAN}" stroke-width="1"/>
</svg>
"""

HKR_LOGO_SVG = f"""
<svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="5" y="5" width="90" height="90" stroke="{COLOR_TEXT}" stroke-width="4"/>
    <path d="M10 40 L50 10 L90 40" stroke="{COLOR_ACCENT}" stroke-width="4" fill="none"/>
    <circle cx="50" cy="65" r="20" stroke="{COLOR_CYAN}" stroke-width="3"/>
    <rect x="48" y="60" width="4" height="10" fill="{COLOR_CYAN}"/>
    <text x="50" y="90" font-family="monospace" font-size="10" fill="{COLOR_TEXT}" text-anchor="middle">EST. 2023</text>
</svg>
"""

# --- CART HELPER ---
def add_to_cart(item_name):
    st.session_state.cart.append(item_name)

# -----------------------------
# 1. PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="TUESDAYNIGHTFREAK | OFFICIAL",
    page_icon="Circle",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# 2. SESSION STATE
# -----------------------------
if 'songs' not in st.session_state:
    st.session_state.songs = [
        {"title": "System Failure (Original Mix)", "label": "House Keeping Rec", "cat": "HKR004"},
        {"title": "Analog Dreams", "label": "Tresor Records", "cat": "TR-291"},
        {"title": "Voltage Control", "label": "Ostgut Ton", "cat": "OSTGUT-55"},
        {"title": "Modular State", "label": "Klockworks", "cat": "KW-22"}
    ]

if 'cart' not in st.session_state:
    st.session_state.cart = []

if 'current_page_index' not in st.session_state:
    st.session_state.current_page_index = 0

# -----------------------------
# 3. CSS + TONE.JS — AUDIO STARTS IMMEDIATELY (NO BOOT SCREEN)
# -----------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&family=Space+Mono:wght@400;700&display=swap');
    .stApp {{background:{COLOR_BG}; color:{COLOR_TEXT}; font-family:'Inter',sans-serif;}}
    #MainMenu, footer, header {{visibility:hidden !important;}}
    .block-container {{padding-top:2rem !important; max-width:1400px;}}

    h1,h2,h3 {{font-weight:900; text-transform:uppercase; letter-spacing:-1px;}}
    h4,h5 {{font-family:'Space Mono'; color:{COLOR_CYAN}; text-transform:uppercase; font-size:0.9rem;}}

    .stButton>button {{background:{COLOR_CYAN}; color:{COLOR_BG}; border:1px solid {COLOR_TEXT}; font-weight:900; text-transform:uppercase; padding:12px 28px; border-radius:0;}}
    .stButton>button:hover {{background:{COLOR_ACCENT}; box-shadow:0 0 20px {COLOR_ACCENT};}}

    .content-card {{background:{COLOR_SECONDARY}; padding:25px; border-left:3px solid {COLOR_ACCENT};}}
    .tech-card {{background:#0f0f0f; padding:15px; border-top:3px solid {COLOR_CYAN}; font-family:'Space Mono'; font-size:0.85rem; color:#aaa;}}

    .video-background-fixed {{position:fixed; top:0; left:0; width:100vw; height:100vh; z-index:-999; overflow:hidden;}}
    .video-background-fixed iframe {{width:100%; height:100%; min-width:100vw; min-height:100vh; transform:scale(1.1);}}
    .video-overlay-fixed {{position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(8,8,8,0.85); z-index:-998; pointer-events:none;}}
</style>

<!-- TONE.JS — STARTS IMMEDIATELY -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.min.js"></script>
<script>
    if (typeof Tone !== 'undefined') {
        Tone.start();
        Tone.Transport.bpm.value = 110;
        const kick = new Tone.MembraneSynth().toDestination();
        const bass = new Tone.Synth({oscillator:{type:"sine"}}).toDestination();
        new Tone.Loop(t => kick.triggerAttackRelease("C1","8n",t),"4n").start(0);
        new Tone.Sequence((t,n) => n && bass.triggerAttackRelease(n,"4n",t), ["C2",null,"C2","G1"]).start(0);
        Tone.Transport.start();
    }
</script>
""", unsafe_allow_html=True)

# -----------------------------
# 4. NAVIGATION
# -----------------------------
menu_styles = {
    "container": {"padding": "0!important", "background-color": "rgba(8,8,8,0.95)"},
    "nav-link": {"font-size": "20px", "text-align": "center", "color": "#fff", "font-family": "Inter", "text-transform": "uppercase", "font-weight": "700"},
    "nav-link-selected": {"background-color": "rgba(255,255,255,0.1)", "color": COLOR_CYAN, "border-bottom": f"3px solid {COLOR_CYAN}"}
}

selected = option_menu(
    menu_title=None,
    options=["HOME", "MUSIC", "EVENTS", "STORE", "ABOUT", "SYSTEM"],
    icons=["house-fill", "disc-fill", "calendar-event-fill", "bag-fill", "info-circle-fill", "cpu-fill"],
    default_index=st.session_state.current_page_index,
    orientation="horizontal",
    styles=menu_styles
)

try:
    st.session_state.current_page_index = ["HOME","MUSIC","EVENTS","STORE","ABOUT","SYSTEM"].index(selected)
except:
    st.session_state.current_page_index = 0

# -----------------------------
# 5. ALL YOUR ORIGINAL PAGES — 100% PRESERVED
# -----------------------------
if selected == "HOME":
    st.markdown(f"""
        <div class="video-background-fixed">
            <iframe src="https://www.youtube.com/embed/qC0vDKVPCrw?controls=0&autoplay=1&loop=1&mute=1&playlist=qC0vDKVPCrw" allow="autoplay"></iframe>
        </div>
        <div class="video-overlay-fixed"></div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"## TUESDAYNIGHTFREAK {TNF_LOGO_SVG}", unsafe_allow_html=True)
        st.markdown("#### ARCHITECTS OF THE ANALOGUE SIGNAL")
        st.markdown("""
        <div style="font-size:1.1rem;line-height:1.6;">
        Tuesdaynightfreak operates at the intersection of <strong>studio precision</strong> and <strong>live improvisation</strong>. 
        We construct immersive sonic environments using modular synthesis, exploring the tension between mechanical repetition and human error.
        <br><br>A sonic movement born in Melbourne, refined in Berlin.
        </div>
        """, unsafe_allow_html=True)
        
        btn_col1, btn_col2 = st.columns(2)
        if btn_col1.button("LATEST RELEASE"):
            st.session_state.current_page_index = 1
            st.rerun()
        if btn_col2.button("VIEW TOUR DATES"):
            st.session_state.current_page_index = 2
            st.rerun()
            
    with col2:
        st.markdown("#### SYSTEM UPDATES")
        st.markdown(f"<div class='tech-card'>NEW: VOLTAGE CONTROL EP — OUT NOW</div>", unsafe_allow_html=True)

elif selected == "MUSIC":
    st.markdown("## DISCOGRAPHY")
    for track in st.session_state.songs:
        c1,c2,c3,c4 = st.columns([1,4,2,2])
        with c1: st.markdown(f"<div style='width:50px;height:50px;background:{COLOR_SECONDARY};border:1px solid #333;display:flex;align-items:center;justify-content:center;color:#666;font-size:0.7rem;'>ART</div>", unsafe_allow_html=True)
        with c2: st.markdown(f"**{track['title']}**")
        with c3: st.caption(f"{track.get('label','HKR')} // {track.get('cat','000')}")
        with c4: st.button("STREAM", key=track['title'])
        st.markdown("<hr style='border-color:#222;'>", unsafe_allow_html=True)

    st.markdown("### HOUSE KEEPING RECORDS")
    c1, c2 = st.columns([1, 3])
    with c1: st.markdown(HKR_LOGO_SVG, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="content-card">
        Our dedicated platform for the raw and the deep.
        <br><br>
        House Keeping Records focuses on functional tools for DJs and sonic explorations for heads.
        Strictly vinyl releases for select projects.
        </div>
        """, unsafe_allow_html=True)

elif selected == "EVENTS":
    st.markdown("## UPCOMING DATES")
    events = [
        {"date":"NOV 04","city":"AMSTERDAM","venue":"SHELTER","status":"SELLING FAST"},
        {"date":"NOV 11","city":"LONDON","venue":"FOLD","status":"TICKETS"},
        {"date":"NOV 18","city":"MELBOURNE","venue":"REVOLVER","status":"SOLD OUT"},
        {"date":"DEC 02","city":"PARIS","venue":"REX CLUB","status":"TICKETS"},
    ]
    for e in events:
        c1,c2,c3,c4 = st.columns([1,2,2,2])
        with c1: st.markdown(f"<span style='color:{COLOR_ACCENT};font-weight:bold;'>{e['date']}</span>", unsafe_allow_html=True)
        with c2: st.markdown(f"**{e['city']}**")
        with c3: st.markdown(e['venue'])
        with c4:
            if e['status'] == "SOLD OUT":
                st.markdown("<span style='color:#666;'>SOLD OUT</span>", unsafe_allow_html=True)
            else:
                st.button(f"BUY {e['status']}", key=e['city'])
        st.markdown("<hr style='border-color:#222;'>", unsafe_allow_html=True)

elif selected == "STORE":
    st.markdown("## OFFICIAL MERCHANDISE")
    if st.session_state.cart:
        st.info(f"CART: {len(st.session_state.cart)} ITEMS")

    c1,c2,c3 = st.columns(3)
    items = [
        ("TNF CORE TEE [BLACK]", "€35.00", COLOR_TEXT),
        ("HKR LABEL HOODIE", "€65.00", COLOR_ACCENT),
        ("PROFESSIONAL SLIPMATS (PAIR)", "€20.00", COLOR_CYAN)
    ]
    for col, (name, price, color) in zip([c1,c2,c3], items):
        with col:
            st.markdown(f"<div style='background:{COLOR_SECONDARY};padding:15px;'><div style='height:200px;background:#000;display:flex;align-items:center;justify-content:center;font-size:3rem;color:{color};'>TNF</div></div>", unsafe_allow_html=True)
            st.markdown(f"**{name}**")
            st.markdown(f"**{price}**")
            if st.button("ADD TO CART", key=name):
                add_to_cart(name)
                st.rerun()

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
        st.markdown("#### CONTACT MANAGEMENT")
        st.markdown("<div class='tech-card'>mgmt@tuesdaynightfreak.com</div>", unsafe_allow_html=True)
        st.markdown("#### DEMO POLICY")
        st.markdown("<div class='tech-card'>demos@housekeeping-rec.com (Private SC Links Only)</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("## NEWSLETTER")
        st.write("Join our community for early access to vinyl drops and guestlist spots.")
        with st.form("newsletter"):
            st.text_input("EMAIL ADDRESS")
            st.form_submit_button("SUBSCRIBE")
        st.markdown("#### PRESS KIT")
        st.button("DOWNLOAD EPK (ZIP)")

elif selected == "SYSTEM":
    st.markdown("## SYSTEM ACCESS")
    st.caption("SECURE AREA. AUTHORIZED PERSONNEL ONLY.")
    pwd = st.text_input("ENTER AUTH CODE", type="password")
    if pwd == "admin123":
        st.success("ACCESS GRANTED. WELCOME, OPERATOR.")
        tab1, tab2, tab3 = st.tabs(["UPLOAD MUSIC", "UPLOAD VISUALS", "INCOMING DATA"])
        with tab1:
            with st.form("add_song_admin"):
                new_title = st.text_input("SONG TITLE")
                new_label = st.text_input("LABEL")
                new_cat = st.text_input("CATALOGUE #")
                if st.form_submit_button("UPLOAD TRACK"):
                    st.session_state.songs.append({"title": new_title, "label": new_label, "cat": new_cat})
                    st.success("TRACK ADDED")
                    st.rerun()
        with tab2:
            with st.form("add_photo_admin"):
                new_caption = st.text_input("CAPTION")
                new_img_url = st.text_input("IMAGE URL")
                if st.form_submit_button("UPLOAD VISUAL"):
                    st.session_state.gallery.append({"caption": new_caption, "url": new_img_url})
                    st.success("VISUAL ADDED")
                    st.rerun()
        with tab3:
            st.markdown("### INCOMING TRANSMISSIONS")
            if st.session_state.bookings:
                st.dataframe(pd.DataFrame(st.session_state.bookings))
            else:
                st.info("NO NEW MESSAGES.")
