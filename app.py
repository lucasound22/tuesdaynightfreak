import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime
import time

# --- CONFIGURATION & PALETTE ---
# Premium Underground (Black/Red) + Cyberpunk Splash (Cyan)
COLOR_BG = "#080808"
COLOR_TEXT = "#F0F0F0" 
COLOR_ACCENT = "#FF0033" # Acid Red (Primary Brand)
COLOR_CYAN = "#00f7ff"   # Cyberpunk Splash (Secondary/Tech)
COLOR_SECONDARY = "#141414" # Card Background

# --- BRANDING: TUESDAYNIGHTFREAK GLITCH LOGO ---
# FIXED: Removed duplicate 'x2' attribute in the line element to prevent rendering errors
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
    <line x1="0" y1="45" x2="140" y2="45" stroke="{COLOR_CYAN}" stroke-width="1"/>
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

# --- HELPER FUNCTION FOR ADDING TO CART ---
def add_to_cart(item_name):
    """Adds an item to the cart."""
    # We append to state but do NOT call st.rerun() here to avoid potential recursion loops.
    # The UI update happens naturally on the next interaction or can be forced in the button callback.
    st.session_state.cart.append(item_name)

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
# 2. SESSION STATE VALIDATION (UAT Tested)
# -----------------------------------------------------------------------------

# TNF MUSIC
if 'songs' not in st.session_state:
    st.session_state.songs = list([
        {"title": "System Failure (Original Mix)", "label": "House Keeping Rec", "cat": "HKR004"},
        {"title": "Analog Dreams", "label": "Tresor Records", "cat": "TR-291"},
        {"title": "Voltage Control", "label": "Ostgut Ton", "cat": "OSTGUT-55"},
        {"title": "Modular State", "label": "Klockworks", "cat": "KW-22"}
    ])

# HKR MUSIC (New separate list for the HKR page)
if 'hkr_releases' not in st.session_state:
    st.session_state.hkr_releases = list([
        {"title": "Rhythm Generator EP", "artist": "Various Artists", "cat": "HKR005"},
        {"title": "Modular Loop 01", "artist": "TUESDAYNIGHTFREAK", "cat": "HKR004"},
        {"title": "Grid Sequencer", "artist": "Acid Junkie", "cat": "HKR003"},
    ])

# GALLERY/VISUAL ARCHIVE (Fixed with new mock image IDs and fallback URLs)
if 'gallery' not in st.session_state:
    st.session_state.gallery = list([
        {"caption": "OSCILLATOR BANK A", "url": "https://images.unsplash.com/photo-1621360841012-2357d27e02a4?q=80&w=800&auto=format&fit=crop"},
        {"caption": "PATCH CABLE LOGIC", "url": "https://images.unsplash.com/photo-1598275529124-b1c4b786f1e2?q=80&w=800&auto=format&fit=crop"},
        {"caption": "LIVE TRANSMISSION MELBOURNE", "url": "https://images.unsplash.com/photo-1550291652-6ea9114a47b1?q=80&w=800&auto=format&fit=crop"},
        {"caption": "SEQUENCER ARRAY", "url": "https://images.unsplash.com/photo-1619967657960-983b6329c370?q=80&w=800&auto=format&fit=crop"},
        {"caption": "FILTER RESONANCE", "url": "https://images.unsplash.com/photo-1510915364890-a7d41f02c611?q=80&w=800&auto=format&fit=crop"}
    ])

if 'bookings' not in st.session_state:
    st.session_state.bookings = list([])

if 'cart' not in st.session_state:
    st.session_state.cart = list([])

if 'current_page_index' not in st.session_state:
    st.session_state.current_page_index = 0

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

    /* Primary Action Button (Cyan) */
    .stButton>button {{
        background-color: {COLOR_CYAN};
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
        background-color: {COLOR_ACCENT}; /* Red on hover */
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

    /* --- FULL-SCREEN VIDEO BACKGROUND --- */
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

</style>

<!-- TONE.JS AND BACKGROUND AUDIO SCRIPT -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.min.js"></script>

<script>
    // Auto-start audio on first user interaction (click)
    document.addEventListener('click', async () => {{
        if (typeof Tone !== 'undefined' && Tone.context.state !== 'running') {{
            await Tone.start();
            
            Tone.Transport.bpm.value = 110;
            const kick = new Tone.MembraneSynth({{
                pitchDecay: 0.05,
                octaves: 2,
                envelope: {{ attack: 0.001, decay: 0.4, sustain: 0.01, release: 0.8 }}
            }}).toDestination();

            const bass = new Tone.Synth({{
                oscillator: {{ type: "sine" }},
                envelope: {{ attack: 0.1, decay: 0.2, sustain: 0.8, release: 0.5 }}
            }}).toDestination();
            bass.volume.value = -12;

            new Tone.Loop(time => {{
                kick.triggerAttackRelease("C1", "8n", time);
            }}, "4n").start(0);

            new Tone.Sequence((time, note) => {{
                bass.triggerAttackRelease(note, "4n", time);
            }}, ["C2", ["C2", "G1"], "C2", "G1"], "4n").start(0);

            Tone.Transport.start();
            console.log("Audio initiated.");
        }}
    }}, {{ once: true }});
</script>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 4. NAVIGATION (UAT Tested)
# -----------------------------------------------------------------------------
# UPDATE: Added HKR to the main menu
menu_options = ["HOME", "MUSIC", "HKR", "EVENTS", "STORE", "GALLERY", "ABOUT", "SYSTEM"]

menu_styles = {
    "container": {"padding": "0!important", "background-color": "rgba(8,8,8,0.95)", "border-bottom": "1px solid #333"},
    "icon": {"color": "#fff", "font-size": "14px"},
    "nav-link": {
        "font-size": "20px",
        "text-align": "center",
        "margin": "0px",
        "color": "#ffffff",
        "font-family": "Inter",
        "text-transform": "uppercase",
        "font-weight": "700"
    },
    "nav-link-selected": {
        "background-color": "rgba(255,255,255,0.1)",
        "color": COLOR_CYAN,
        "border-bottom": "3px solid " + COLOR_CYAN,
        "text-shadow": "0 0 10px " + COLOR_CYAN
    },
}

selected = option_menu(
    menu_title=None,
    options=menu_options,
    icons=["house-fill", "disc-fill", "vinyl-fill", "calendar-event-fill", "bag-fill", "images-fill", "info-circle-fill", "cpu-fill"],
    menu_icon="cast",
    default_index=st.session_state.current_page_index,
    orientation="horizontal",
    styles=menu_styles 
)

try:
    st.session_state.current_page_index = menu_options.index(selected)
except Exception:
    st.session_state.current_page_index = 0


# -----------------------------------------------------------------------------
# 5. PAGE CONTENT
# -----------------------------------------------------------------------------

# --- HOME PAGE (UAT Tested) ---
if selected == "HOME":
    # --- FIXED FULL-SCREEN BACKGROUND VIDEO ---
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
            if st.button("LATEST RELEASE"):
                st.session_state.current_page_index = menu_options.index("MUSIC")
                st.rerun()
        with c2:
            if st.button("VIEW TOUR DATES"):
                st.session_state.current_page_index = menu_options.index("EVENTS")
                st.rerun()

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

# --- MUSIC (TNF Artist Discography) ---
elif selected == "MUSIC":
    st.markdown("## TUESDAYNIGHTFREAK DISCOGRAPHY")
    st.caption("ALL RELEASES EXCLUDING HKR")

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
            if st.button("STREAM", key=track['title']):
                st.info(f"Initiating stream for **{track['title']}**. Please wait for transmission handshake.")
        st.markdown(f"<hr style='margin: 10px 0; border-color: #1a1a1a;'>", unsafe_allow_html=True)

# --- HOUSE KEEPING RECORDS (New Dedicated Page) ---
elif selected == "HKR":
    st.markdown(f"## HOUSE KEEPING RECORDS {HKR_LOGO_SVG}", unsafe_allow_html=True)
    st.markdown("#### DEEP HOUSE & FUNCTIONAL TOOLS")

    st.markdown("""
    <div class="content-card" style="border-left: 3px solid #00f7ff;">
    House Keeping Records is TUESDAYNIGHTFREAK's dedicated platform for the raw and the deep. 
    The label operates on a principle of utility and sonic purity, focusing on hardware-driven deep house 
    and techno, strictly for vinyl releases for select projects. Our mission is to provide functional, 
    timeless tools for DJs and maintain the analogue signal chain.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ARTIST ROSTER")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### TUESDAYNIGHTFREAK")
        st.caption("Founder & Resident. Deep Modular Techno.")
    with c2:
        st.markdown("#### ACID JUNKIE")
        st.caption("Acidic Rhythms. Roland 303 Devotion.")
    with c3:
        st.markdown("#### D-PHASE")
        st.caption("Minimal & Hypnotic. Berlin Influence.")

    st.markdown("### HKR RELEASE CATALOGUE")
    for release in st.session_state.hkr_releases:
        r1, r2, r3, r4 = st.columns([1, 3, 2, 2])
        with r1:
            st.markdown(f"<div style='width:50px; height:50px; background-color:{COLOR_ACCENT}; border:1px solid #333; display:flex; align-items:center; justify-content:center; color:{COLOR_TEXT}; font-size:0.9rem;'>VINYL</div>", unsafe_allow_html=True)
        with r2:
            st.markdown(f"**{release['title']}**")
            st.caption(f"Artist: {release['artist']}")
        with r3:
            st.caption(f"CATALOGUE: {release['cat']}")
        with r4:
            st.button("BUY VINYL", key=release['cat'])
        st.markdown(f"<hr style='margin: 10px 0; border-color: #1a1a1a;'>", unsafe_allow_html=True)

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

# --- STORE (MERCH) (Fixed with mock images and logos) ---
elif selected == "STORE":
    st.markdown("## OFFICIAL MERCHANDISE")

    # Cart Summary - Rendered first for immediate feedback
    if len(st.session_state.cart) > 0:
        st.info(f"CART: {len(st.session_state.cart)} ITEMS")

    c1, c2, c3 = st.columns(3)

    # Merch Item 1 - TNF TEE
    with c1:
        st.markdown(f"<div style='margin-bottom: 15px; margin-top: -10px; text-align: center;'>{TNF_LOGO_SVG}</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:{COLOR_SECONDARY}; padding:10px; margin-bottom:10px;">
            <img src="uploaded:image_20608f.png-54a97f38-0e2f-412b-864a-fe49523e31bc" style="width:100%; height:250px; object-fit:cover; border: 1px solid {COLOR_ACCENT};" onerror="this.onerror=null;this.src='https://placehold.co/400x250/141414/F0F0F0?text=TNF+TEE+MOCK'">
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**CORE TEE [BLACK]**")
        st.caption("Heavyweight Cotton / Screen Print")
        st.markdown(f"**€35.00**")
        if st.button("ADD TO CART", key="m1"):
            add_to_cart("Tee")
            st.rerun() 

    # Merch Item 2 - HKR HOODIE
    with c2:
        st.markdown(f"<div style='margin-bottom: 5px; margin-top: -10px; text-align: center;'>{HKR_LOGO_SVG}</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:{COLOR_SECONDARY}; padding:10px; margin-bottom:10px;">
            <img src="uploaded:image_205d6e.png-557f8429-a75a-403a-9dbd-391d18da851b" style="width:100%; height:250px; object-fit:cover; border: 1px solid {COLOR_CYAN};" onerror="this.onerror=null;this.src='https://placehold.co/400x250/141414/F0F0F0?text=HKR+HOODIE+MOCK'">
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**LABEL HOODIE**")
        st.caption("Oversized Fit / Embroidered")
        st.markdown(f"**€65.00**")
        if st.button("ADD TO CART", key="m2"):
            add_to_cart("Hoodie")
            st.rerun() 

    # Merch Item 3 - SLIPMATS
    with c3:
        st.markdown(f"<div style='margin-bottom: 5px; margin-top: 10px; text-align: center; font-size: 2rem; color: {COLOR_ACCENT};'>🎧</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:{COLOR_SECONDARY}; padding:10px; margin-bottom:10px;">
            <img src="uploaded:image_205cd6.png-3bca7ad1-af70-44d0-961c-7d5c82c713c5" style="width:100%; height:250px; object-fit:cover; border: 1px solid {COLOR_TEXT};" onerror="this.onerror=null;this.src='https://placehold.co/400x250/141414/F0F0F0?text=SLIPMATS+MOCK'">
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**PROFESSIONAL SLIPMATS (PAIR)**")
        st.caption("High grade felt / Anti-static")
        st.markdown(f"**€20.00**")
        if st.button("ADD TO CART", key="m3"):
            add_to_cart("Slipmats")
            st.rerun() 

# --- GALLERY (Visual Archive Fixed) ---
elif selected == "GALLERY":
    st.markdown("## VISUAL ARCHIVE")
    st.caption("CAPTURED LIVE AND IN STUDIO")

    # Display gallery items in a 2-column grid
    cols = st.columns(2)
    
    # Using the updated, relevant image IDs
    for i, item in enumerate(st.session_state.gallery):
        with cols[i % 2]:
            # Check if url is an uploaded ID or a standard URL
            img_src = item['url']
            st.image(img_src, caption=item['caption'], use_column_width=True)
            st.markdown("---") # Separator between items

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
                    st.rerun()

            if st.button("PURGE AUDIO ARCHIVE"):
                st.session_state.songs = list([])
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
