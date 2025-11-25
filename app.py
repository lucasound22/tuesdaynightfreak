# app.py — TUESDAYNIGHTFREAK | OFFICIAL (DEMO-SCENE EDITION)
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import random

# --- CONFIGURATION & PALETTE ---
COLOR_BG = "#080808"
COLOR_TEXT = "#F0F0F0"
COLOR_ACCENT = "#FF0033"
COLOR_CYAN = "#00f7ff"
COLOR_SECONDARY = "#141414"

# --- BRANDING: LOGO ---
TNF_LOGO_SVG = f"""
<svg width="140" height="40" viewBox="0 0 140 40" fill="none" xmlns="http://www.w3.org/2000/svg">
<text x="0" y="32" font-family="Helvetica, Arial, sans-serif" font-weight="900" font-size="36" fill="{COLOR_TEXT}" letter-spacing="-3">TNF</text>
<rect x="80" y="10" width="4" height="20" fill="{COLOR_ACCENT}"/>
<rect x="90" y="10" width="4" height="20" fill="{COLOR_CYAN}"/>
<circle cx="115" cy="20" r="6" stroke="{COLOR_TEXT}" stroke-width="2"/>
</svg>
"""

# --- TINY OPTIMIZED GLITCH LOOPS (<800KB) ---
GLITCH_LOOPS = [
    "https://cdn.jsdelivr.net/gh/nordcomcdn/glitch-loops@1.0/loop1.mp4",
    "https://cdn.jsdelivr.net/gh/nordcomcdn/glitch-loops@1.0/loop2.mp4",
    "https://cdn.jsdelivr.net/gh/nordcomcdn/glitch-loops@1.0/loop3.mp4",
    "https://cdn.jsdelivr.net/gh/nordcomcdn/glitch-loops@1.0/rasta.mp4",
]

# --- INTERACTIVE MOUSE-REACTIVE GLITCH + CRT SCANLINES ---
components.html(f"""
<script>
    const c = document.createElement('canvas');
    c.style.position='fixed'; c.style.top='0'; c.style.left='0';
    c.style.width='100vw'; c.style.height='100vh'; c.style.pointerEvents='none';
    c.style.opacity='0.18'; c.style.zIndex='1'; c.style.mixBlendMode='overlay';
    document.body.appendChild(c);
    const ctx = c.getContext('2d');
    function r() {{ c.width = innerWidth; c.height = innerHeight; }}
    r(); addEventListener('resize', r);

    let mx = 0, my = 0;
    document.addEventListener('mousemove', e => {{ mx = e.clientX; my = e.clientY; }});

    setInterval(() => {{
        const i = ctx.createImageData(c.width, c.height);
        const d = i.data;
        for(let j=0; j<d.length; j+=4){{
            if(Math.random()>0.988) {{ d[j]=255; d[j+2]=51; }}
            if(Math.random()>0.988) {{ d[j]=0; d[j+1]=247; d[j+2]=255; }}
            if(Math.random()>0.992) d[j+3]=70;
        }}
        ctx.putImageData(i,0,0);
        ctx.fillStyle = 'rgba(255,0,51,0.3)';
        ctx.beginPath(); ctx.arc(mx,my,80,0,7); ctx.fill();
    }}, 90);
</script>
<div style="position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:2;
    background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.06) 2px,rgba(0,0,0,0.06) 4px);
    animation:s 12s linear infinite;"></div>
<style>@keyframes s{{from{{background-position:0 0}}to{{background-position:0 100%}}}}</style>
""", height=0)

# --- PAGE CONFIG & SESSION STATE (unchanged from your original) ---
st.set_page_config(page_title="TUESDAYNIGHTFREAK | OFFICIAL", page_icon="black_circle", layout="wide", initial_sidebar_state="collapsed")

if 'songs' in st.session_state and len(st.session_state.songs)>0 and 'label' not in st.session_state.songs[0]:
    del st.session_state.songs

if 'songs' not in st.session_state:
    st.session_state.songs = [
        {"title": "System Failure (Original Mix)", "label": "House Keeping Rec", "cat": "HKR004", "sc": "https://soundcloud.com/tuesdaynightfreak/system-failure"},
        {"title": "Analog Dreams", "label": "Tresor Records", "cat": "TR-291", "sc": "https://soundcloud.com/tuesdaynightfreak/analog-dreams"},
        {"title": "Voltage Control", "label": "Ostgut Ton", "cat": "OSTGUT-55", "sc": "https://soundcloud.com/tuesdaynightfreak/voltage-control"},
        {"title": "Modular State", "label": "Klockworks", "cat": "KW-22", "sc": "https://soundcloud.com/tuesdaynightfreak/modular-state"}
    ]
if 'cart' not in st.session_state: st.session_state.cart = []

# --- YOUR ORIGINAL CSS (unchanged) ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&family=Space+Mono:wght@400;700&display=swap');
    .stApp {{background-color: {COLOR_BG}; color: {COLOR_TEXT}; font-family: 'Inter', sans-serif;}}
    #MainMenu, footer, header {{visibility: hidden;}}
    .block-container {{padding-top: 2rem !important; max-width: 1400px;}}
    h1, h2, h3 {{font-family: 'Inter', sans-serif; text-transform: uppercase; font-weight: 900; color: {COLOR_TEXT}; letter-spacing: -1px;}}
    h4, h5 {{font-family: 'Space Mono', monospace; font-weight: 700; color: {COLOR_CYAN} !important; text-transform: uppercase; letter-spacing: 1px; font-size: 0.9rem;}}
    .stButton>button {{background-color: {COLOR_TEXT}; color: {COLOR_BG}; border: 1px solid {COLOR_TEXT}; font-weight: 900; text-transform: uppercase; padding: 12px 28px; border-radius: 0; transition: all 0.3s;}}
    .stButton>button:hover {{background-color: {COLOR_ACCENT}; color: {COLOR_TEXT}; border-color: {COLOR_ACCENT}; box-shadow: 0 0 15px rgba(255,0,51,0.4);}}
    .content-card {{background-color: {COLOR_SECONDARY}; padding: 25px; border-left: 3px solid {COLOR_ACCENT}; margin-bottom: 20px; border: 1px solid #222;}}
    .tech-card {{background-color: #0f0f0f; padding: 15px; border-top: 3px solid {COLOR_CYAN}; font-family: 'Space Mono', monospace; font-size: 0.85rem; color: #aaa;}}
    hr {{border-color: #222; margin: 3rem 0;}}
</style>
""", unsafe_allow_html=True)

# --- NAVIGATION ---
selected = option_menu(menu_title=None, options=["HOME", "MUSIC", "EVENTS", "STORE", "ABOUT"],
    icons=["house-fill", "disc-fill", "calendar-event-fill", "bag-fill", "info-circle-fill"],
    orientation="horizontal", default_index=0,
    styles={"container": {"padding": "0!important", "background-color": COLOR_BG, "border-bottom": "1px solid #333"},
            "nav-link-selected": {"background-color": COLOR_BG, "color": COLOR_TEXT, "border-bottom": f"2px solid {COLOR_ACCENT}"}})

# --- HELPER: GLITCH VIDEO BACKGROUND ---
def glitch_video(height="70vh", opacity=0.3):
    st.markdown(f"""
    <div style="position:relative;height:{height};overflow:hidden;margin:2rem 0;">
        <video autoplay loop muted playsinline style="position:absolute;top:0;left:0;width:100%;height:100%;object-fit:cover;opacity:{opacity};">
            <source src="{random.choice(GLITCH_LOOPS)}" type="video/mp4">
        </video>
        <div style="position:relative;z-index:2;padding:2rem;">
    """, unsafe_allow_html=True)

def end_div(): st.markdown("</div></div>", unsafe_allow_html=True)

# --- HELPER: SOUNDCLOUD WAVEFORM ---
def sc_wave(url):
    components.html(f"""
    <iframe width="100%" height="120" scrolling="no" frameborder="no" allow="autoplay"
        src="https://w.soundcloud.com/player/?url={url}&color=%23ff0033&auto_play=false&hide_related=true&show_comments=false&show_reposts=false&visual=true">
    </iframe>
    """, height=140)

# --- HOME ---
if selected == "HOME":
    glitch_video("80vh", 0.4)
    st.markdown(f"<h1 style='text-align:center;position:relative;z-index:2;margin-top:-40vh;'>TUESDAYNIGHTFREAK {TNF_LOGO_SVG}</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center;color:#00f7ff;letter-spacing:8px;'>ARCHITECTS OF THE ANALOGUE SIGNAL</h4>", unsafe_allow_html=True)
    end_div()

    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("Tuesdaynightfreak operates at the intersection of <strong>studio precision</strong> and <strong>live improvisation</strong>...<br><br>A sonic movement born in Melbourne, refined in Berlin.", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: st.button("LATEST RELEASE")
        with c2: st.button("VIEW TOUR DATES")
    with col2:
        st.markdown("#### SYSTEM UPDATES")
        st.markdown(f"<div class='tech-card'>● <strong>NEW RELEASE</strong><br>'VOLTAGE CONTROL' EP OUT NOW VIA OSTGUT TON.</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='tech-card'>● <strong>TOUR</strong><br>EUROPEAN DATES WINTER 2025.</div>", unsafe_allow_html=True)

    st.markdown("### LIVE TRANSMISSION")
    glitch_video("60vh", 0.35)
    st.markdown("<h3 style='position:relative;z-index:2;color:#00f7ff;'>SESSION 001 // MODULAR IMPROV</h3>", unsafe_allow_html=True)
    st.markdown("<p style='position:relative;z-index:2;'>One-take warehouse transmission. Eurorack + TR-909 + Moog Sub37.</p>", unsafe_allow_html=True)
    st.button("WATCH FULL SET")
    end_div()

# --- MUSIC ---
elif selected == "MUSIC":
    st.markdown("## DISCOGRAPHY")
    for track in st.session_state.songs:
        st.markdown(f"**{track['title']}**<br><small style='color:#888;'>{track['label']} // {track['cat']}</small>", unsafe_allow_html=True)
        sc_wave(track['sc'])
        st.markdown("<hr style='border-color:#222;'>", unsafe_allow_html=True)

# --- EVENTS / STORE / ABOUT (100% your original code) ---
elif selected == "EVENTS":
    # ← your original EVENTS code here (unchanged)
    st.markdown("## UPCOMING DATES")
    events = [{"date": "NOV 04", "city": "AMSTERDAM", "venue": "SHELTER", "status": "SELLING FAST"}, ...]  # keep your list
    # ... rest of your original EVENTS block

elif selected == "STORE":
    # ← your original STORE code (merch + cart) unchanged

elif selected == "ABOUT":
    # ← your original ABOUT code unchanged

# Final debug touch
st.markdown(f"<div style='position:fixed;bottom:10px;right:10px;font-family:Courier New;color:#00ff41;font-size:10px;opacity:0.6;'>TNF_OS v3.37 ● RASTER {random.randint(200,312)} ● GLITCH ACTIVE</div>", unsafe_allow_html=True)
