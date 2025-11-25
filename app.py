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

# --- BRANDING: NEW GLITCH LOGO ---
# Updated for a "Glitch" effect with offset layers
TNF_LOGO_SVG = f"""
<svg width="160" height="50" viewBox="0 0 160 50" fill="none" xmlns="http://www.w3.org/2000/svg">
    <!-- Glitch Layers -->
    <text x="2" y="32" font-family="Helvetica, Arial, sans-serif" font-weight="900" font-size="36" fill="{COLOR_CYAN}" opacity="0.7" letter-spacing="-3">TNF</text>
    <text x="-2" y="32" font-family="Helvetica, Arial, sans-serif" font-weight="900" font-size="36" fill="{COLOR_ACCENT}" opacity="0.7" letter-spacing="-3">TNF</text>
    <!-- Main Text -->
    <text x="0" y="32" font-family="Helvetica, Arial, sans-serif" font-weight="900" font-size="36" fill="{COLOR_TEXT}" letter-spacing="-3">TNF</text>
    
    <!-- Graphic Elements -->
    <rect x="85" y="10" width="4" height="20" fill="{COLOR_ACCENT}"/>
    <rect x="95" y="10" width="4" height="20" fill="{COLOR_CYAN}"/>
    <rect x="105" y="10" width="4" height="20" fill="{COLOR_TEXT}"/>
    <circle cx="130" cy="20" r="6" stroke="{COLOR_TEXT}" stroke-width="2"/>
    <line x1="0" y1="45" x2="140" x2="45" stroke="{COLOR_CYAN}" stroke-width="1"/>
</svg>
"""

# 2. HOUSE KEEPING RECORDS LOGO (Industrial, Bold)
HKR_LOGO_SVG = f"""
<svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="5" y="5" width="90" height="90" stroke="{COLOR_TEXT}" stroke-width="4"/>
    <path d="M10 40 L50 10 L90 40" stroke="{COLOR_ACCENT}" stroke-width="4" fill="none"/>
    <circle cx="50" cy="65" r="20" stroke="{COLOR_CYAN}" stroke-width="3"/>
    <rect x="48" y="60" width="4" height="10" fill="{COLOR_CYAN}"/>
    <text x="50" y="90" font-family="monospace" font-size="10" fill="{COLOR_TEXT}" text-anchor="middle">EST. 2023</text>
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
# 2. SESSION STATE VALIDATION (Unchanged from previous turn)
# -----------------------------------------------------------------------------
if 'songs' in st.session_state:
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
        {"caption": "OSCILLATOR BANK A", "url": "https://images.unsplash.com/photo-1621360841012-2357d27e02a4?q=80&w=800&auto=format&fit=crop"},
        {"caption": "PATCH CABLE LOGIC", "url": "https://images.unsplash.com/photo-1598275529124-b1c4b786f1e2?q=80&w=800&auto=format&fit=crop"},
        {"caption": "SEQUENCER ARRAY", "url": "https://images.unsplash.com/photo-1619967657960-983b6329c370?q=80&w=800&auto=format&fit=crop"},
        {"caption": "FILTER RESONANCE", "url": "https://images.unsplash.com/photo-1510915364890-a7d41f02c611?q=80&w=800&auto=format&fit=crop"}
    ]

if 'bookings' not in st.session_state:
    st.session_state.bookings = []

if 'cart' not in st.session_state:
    st.session_state.cart = []

# -----------------------------------------------------------------------------
# 3. CUSTOM CSS & TONE.JS AUDIO SETUP
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
    
    /* --- FULL-SCREEN VIDEO BACKGROUND (New) --- */
    .video-background-fixed {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        z-index: -999; /* Push behind all content */
    }}
    .video-background-fixed iframe {{
        width: 100%;
        height: 100%;
        /* Ensure it covers the viewport, even if aspect ratios don't match */
        min-width: 100vw; 
        min-height: 100vh;
        transform: scale(1.1); /* Zoom slightly to remove iframe borders */
    }}
    
    /* Overlay to darken video and ensure readability */
    .video-overlay-fixed {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(8,8,8, 0.85); /* Darker overlay for text contrast */
        pointer-events: none;
        z-index: -998;
    }}

    /* Audio Activation Button (Hidden after click) */
    #audio-activation {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: {COLOR_BG};
        color: {COLOR_CYAN};
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 1.5rem;
        font-family: 'Space Mono', monospace;
        text-transform: uppercase;
        cursor: pointer;
        z-index: 1000;
        transition: opacity 0.5s;
    }}
    #audio-activation:hover {{
        background: #111;
    }}

</style>

<!-- TONE.JS AND BACKGROUND AUDIO SCRIPT -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.min.js"></script>

<div id="audio-activation" onclick="startAudio()">
    [SYSTEM ACTIVE] CLICK TO INITIATE SONIC FEED
</div>

<script>
    function startAudio() {{
        // Check if Tone is ready
        if (typeof Tone !== 'undefined') {{
            // 1. Set the low, slow techno BPM
            Tone.Transport.bpm.value = 110;
            
            // 2. Deep Kick Drum
            const kick = new Tone.MembraneSynth({{
                pitchDecay: 0.05,
                octaves: 2,
                envelope: {{
                    attack: 0.001,
                    decay: 0.4,
                    sustain: 0.01,
                    release: 0.8,
                }}
            }}).toDestination();

            // 3. Dark, simple Sub Bass (Sine wave)
            const bass = new Tone.Synth({{
                oscillator: {{ type: "sine" }},
                envelope: {{
                    attack: 0.1,
                    decay: 0.2,
                    sustain: 0.8,
                    release: 0.5
                }}
            }}).toDestination();
            bass.volume.value = -12; // Keep bass subtle

            // 4. Create the loops
            // Kick loop: every beat
            new Tone.Loop(time => {{
                kick.triggerAttackRelease("C1", "8n", time);
            }}, "4n").start(0);

            // Bassline loop: simple, deep rhythm
            new Tone.Sequence((time, note) => {{
                bass.triggerAttackRelease(note, "4n", time);
            }}, ["C2", ["C2", "G1"], "C2", "G1"], "4n").start(0);

            // 5. Start the transport (sequencer) and context
            Tone.Transport.start();
            
            // Hide the activation overlay after audio starts
            const activationDiv = document.getElementById('audio-activation');
            activationDiv.style.opacity = '0';
            setTimeout(() => {{
                activationDiv.style.display = 'none';
            }}, 500); // Wait for transition
        }}
    }}
</script>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 4. NAVIGATION (Menu styling preserved)
# -----------------------------------------------------------------------------
selected = option_menu(
    menu_title=None,
    options=["HOME", "MUSIC", "EVENTS", "STORE", "ABOUT", "SYSTEM"],
    icons=["house-fill", "disc-fill", "calendar-event-fill", "bag-fill", "info-circle-fill", "cpu-fill"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "rgba(8,8,8,0.95)", "border-bottom": "1px solid #333"},
        "icon": {"color": "#fff", "font-size": "14px"}, 
        "nav-link": {
            "font-size": "20px", # Increased size
            "text-align": "center", 
            "margin": "0px", 
            "color": "#ffffff", # Brighter white
            "font-family": "Inter, sans-serif", 
            "text-transform": "uppercase", 
            "font-weight": "700"
        },
        "nav-link-selected": {
            "background-color": "rgba(255,255,255,0.1)", 
            "color": COLOR_CYAN, # Cyberpunk Cyan highlight
            "border-bottom": f"3px solid {COLOR_CYAN}",
            "text-shadow": f"0 0 10px {COLOR_CYAN}" # Glow effect
        },
    }
)

# -----------------------------------------------------------------------------
# 5. PAGE CONTENT
# -----------------------------------------------------------------------------

# --- HOME PAGE ---
if selected == "HOME":
    # --- FIXED FULL-SCREEN BACKGROUND VIDEO ---
    # This element is fixed behind all content by CSS and remains across all pages.
    st.markdown(f"""
        <div class="video-background-fixed">
            <iframe 
                src="https://www.youtube.com/embed/qC0vDKVPCrw?controls=0&showinfo=0&rel=0&autoplay=1&loop=1&mute=1&playlist=qC0vDKVPCrw" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
            </iframe>
        </div>
        <div class="video-overlay-fixed"></div>
    """, unsafe_allow_html=True)
    
    # --- MAIN CONTENT ---
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"## TUESDAYNIGHTFREAK {TNF_LOGO_SVG}", unsafe_allow_html=True)
        st.markdown("#### ARCHITECTS OF THE ANALOGUE SIGNAL")
        
        st.markdown("""
        <div style="font-size: 1.1rem; line-height: 1.6; text-shadow: 0 2px 4px rgba(0,0,0,0.8);">
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
        <div class="tech-card" style="background: rgba(15,15,15,0.8);">
        <span style="color:{COLOR_ACCENT}">●</span> <strong>NEW RELEASE</strong><br>
        'VOLTAGE CONTROL' EP OUT NOW VIA OSTGUT TON.
        </div>
        <br>
        <div class="tech-card" style="background: rgba(15,15,15,0.8);">
        <span style="color:{COLOR_CYAN}">●</span> <strong>TOUR ANNOUNCEMENT</strong><br>
        EUROPEAN DATES CONFIRMED FOR WINTER 2025.
        </div>
        """, unsafe_allow_html=True)

    # The entire "LIVE TRANSMISSION" section has been removed as requested.

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
            lbl = track.get('label', 'HKR')
            cat = track.get('cat', '000')
            st.caption(f"{lbl} // {cat}")
        with c4:
            st.button("STREAM", key=track['title'])
        st.markdown(f"<hr style='margin: 10px 0; border-color: #1a1a1a;'>", unsafe_allow_html=True)

    st.markdown("### HOUSE KEEPING RECORDS")
    c1, c2 = st.columns([1, 3])
    with c1:
        st.markdown(HKR_LOGO_SVG, unsafe_allow_html=True)
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

# --- SYSTEM (ADMIN) ---
elif selected == "SYSTEM":
    st.markdown("## SYSTEM ACCESS")
    st.caption("SECURE AREA. AUTHORIZED PERSONNEL ONLY.")
    
    pwd = st.text_input("ENTER AUTH CODE", type="password")
    
    if pwd == "admin123":
        st.success("ACCESS GRANTED. WELCOME, OPERATOR.")
        
        # --- ADMIN TABS FOR UPLOADING CONTENT ---
        tab1, tab2, tab3 = st.tabs(["UPLOAD MUSIC", "UPLOAD VISUALS", "INCOMING DATA"])
        
        with tab1:
            st.markdown("### ADD AUDIO SOURCE")
            with st.form("add_song_admin"):
                new_title = st.text_input("SONG TITLE")
                new_label = st.text_input("LABEL")
                new_cat = st.text_input("CATALOGUE #")
                if st.form_submit_button("UPLOAD TRACK"):
                    st.session_state.songs.append({"title": new_title, "label": new_label, "cat": new_cat})
                    st.success(f"TRACK '{new_title}' ADDED TO ARCHIVE.")
            
            if st.button("PURGE AUDIO ARCHIVE"):
                st.session_state.songs = []
                st.warning("AUDIO ARCHIVE CLEARED.")
                st.rerun()

        with tab2:
            st.markdown("### ADD VISUAL ASSET")
            with st.form("add_photo_admin"):
                new_caption = st.text_input("CAPTION")
                new_img_url = st.text_input("IMAGE URL")
                if st.form_submit_button("UPLOAD VISUAL"):
                    st.session_state.gallery.append({"caption": new_caption, "url": new_img_url})
                    st.success("VISUAL ASSET ADDED TO FEED.")
                    st.rerun()

        with tab3:
            st.markdown("### INCOMING TRANSMISSIONS")
            if len(st.session_state.bookings) > 0:
                st.dataframe(pd.DataFrame(st.session_state.bookings))
            else:
                st.info("NO NEW MESSAGES.")
