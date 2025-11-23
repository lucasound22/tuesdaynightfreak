import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime
import random
import time

# --- CONFIGURATION ---
NEON_CYAN = "#00f7ff" # Primary Neon color: Cyan
NEON_CYAN_RGB_SHADOW = "0, 247, 255"

# --- BRANDING: SIMPLE SVG LOGO FOR CONSISTENCY ---
TNF_LOGO_SVG = f"""
<svg width="40" height="20" viewBox="0 0 40 20" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="0" y="0" width="10" height="20" fill="{NEON_CYAN}"/>
<rect x="15" y="0" width="10" height="20" fill="{NEON_CYAN}"/>
<path d="M 30 0 L 40 0 L 40 20 L 30 20 L 30 0" fill="{NEON_CYAN}"/>
<path d="M 30 10 L 40 10" stroke="#000000" stroke-width="2"/>
</svg>
"""

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & BERLIN AESTHETIC CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="TUESDAYNIGHTFREAK",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS: Brutalist, Monochrome, Raw + New Cyan Neon Highlights
st.markdown(f"""
<style>
    /* 1. GLOBAL RESET & MONOCHROME THEME */
    @keyframes pulse-bg {{
        0% {{ background-color: #050505; }}
        50% {{ background-color: #080808; }}
        100% {{ background-color: #050505; }}
    }}

    .stApp {{
        background-color: #050505;
        color: #e0e0e0;
        font-family: 'Courier New', Courier, monospace;
        animation: pulse-bg 30s infinite alternate; /* Subtle background pulse flare */
    }}

    /* 2. REMOVE STREAMLIT BRANDING & HEADER */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* 3. FIX MENU CUT-OFF (Adjust Top Padding) */
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 5rem;
        max-width: 1200px;
    }}

    /* 4. BRANDING & TYPOGRAPHY */
    
    /* Custom Logo Style (New - Brutalist Stamped Block Font) */
    /* Simulates a low-res terminal block text or stamped text */
    .logo-text {{
        color: {NEON_CYAN} !important;
        font-family: 'monospace';
        font-size: 5rem;
        line-height: 0.8;
        text-transform: uppercase;
        font-weight: 900;
        letter-spacing: -5px; /* Tighter block look */
        display: block;
        padding-top: 1rem;
        padding-bottom: 1rem;
        text-shadow: 0 0 10px rgba({NEON_CYAN_RGB_SHADOW}, 0.5);
    }}

    h1, h2, h3, h4, h5, h6 {{
        color: {NEON_CYAN} !important; /* NEON CYAN */
        font-family: 'Courier New', Courier, monospace;
        text-transform: uppercase;
        font-weight: 900;
        letter-spacing: -1.5px;
        transition: text-shadow 0.3s ease-in-out;
    }}
    
    h1:hover, h2:hover, h3:hover {{
        text-shadow: 0 0 10px rgba({NEON_CYAN_RGB_SHADOW}, 0.5); /* Heading hover glow flare */
    }}
    
    p, div, label, span {{
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: -0.5px;
    }}
    
    /* Lighter and Bigger Text for items like LATEST PRESSINGS (stText) */
    div.stText p {{
        color: #ffffff !important;
        font-size: 1.1em;
        margin-bottom: 5px;
    }}

    a {{
        color: {NEON_CYAN} !important;
        text-decoration: none;
        transition: text-shadow 0.3s;
    }}
    a:hover {{
        text-decoration: underline;
        text-shadow: 0 0 10px {NEON_CYAN};
    }}

    /* 5. IMAGERY - FORCE B&W & HIGH CONTRAST */
    img {{
        filter: grayscale(100%) contrast(120%) brightness(85%);
        transition: all 0.4s ease;
        border: 1px solid #1a1a1a;
    }}
    img:hover {{
        filter: grayscale(0%) contrast(110%) brightness(100%); /* Color reveal on hover */
        border: 1px solid {NEON_CYAN};
        box-shadow: 0 0 15px rgba({NEON_CYAN_RGB_SHADOW}, 0.4);
    }}

    /* 6. UI ELEMENTS - BRUTALIST (NO ROUNDED CORNERS) */
    .stButton>button {{
        color: {NEON_CYAN};
        background-color: #000000;
        border: 1px solid {NEON_CYAN};
        border-radius: 0px !important;
        text-transform: uppercase;
        padding: 12px 24px;
        font-weight: bold;
        transition: all 0.2s;
    }}
    .stButton>button:hover {{
        background-color: {NEON_CYAN};
        color: #000000;
        box-shadow: 0 0 20px rgba({NEON_CYAN_RGB_SHADOW}, 0.8);
    }}

    /* 7. INPUTS & FORMS - Added borders for flare */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div, .stForm {{
        background-color: #0a0a0a;
        color: {NEON_CYAN};
        border: 1px solid #333;
        border-radius: 0px;
        font-family: 'Courier New', monospace;
    }}
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {{
        border-color: {NEON_CYAN};
        box-shadow: 0 0 5px {NEON_CYAN}; /* Input focus flare */
    }}
    
    /* Highlight form borders for better visual separation */
    .stForm > div:first-child {{
        border: 2px solid #1a1a1a;
        padding: 20px;
        margin-top: 10px;
        border-left: 5px solid {NEON_CYAN}; /* Brutalist accent border flare */
    }}

    hr {{
        border-top: 1px solid #333;
    }}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. SESSION STATE & DATA
# -----------------------------------------------------------------------------
if 'songs' not in st.session_state:
    st.session_state.songs = [
        {"title": "UNTITLED_SEQ_04 [LIVE REC]", "url": "#", "platform": "SoundCloud"},
        {"title": "MODULAR EXCURSION B (RAW)", "url": "#", "platform": "Bandcamp"},
        {"title": "RESIDENT ADVISOR PODCAST 892", "url": "#", "platform": "RA"},
    ]

# --- UPDATED STOCK IMAGES (More industrial/hardware focused) ---
if 'gallery' not in st.session_state or 'updated_images' not in st.session_state:
    st.session_state.gallery = [
        {"caption": "ANALOG SYNTHESIS HARDWARE", "url": "https://images.unsplash.com/photo-1510915364890-a7d41f02c611?q=80&w=800&auto=format&fit=crop"}, # Modular synth closeup
        {"caption": "RAW WAREHOUSE ATMOSPHERE", "url": "https://images.unsplash.com/photo-1543167156-f6d89262f270?q=80&w=800&auto=format&fit=crop"}, # Stark tunnel/warehouse light
        {"caption": "PATCH CABLE MATRIX", "url": "https://images.unsplash.com/photo-1598275529124-b1c4b786f1e2?q=80&w=800&auto=format&fit=crop"}, # Patch cables/close up connections
        {"caption": "HIGH-CONTRAST MIXER VIEW", "url": "https://images.unsplash.com/photo-1619967657960-983b6329c370?q=80&w=800&auto=format&fit=crop"}, # Controller/mixer close up
    ]
    st.session_state.updated_images = True # Flag to avoid re-running image initialization

if 'bookings' not in st.session_state:
    st.session_state.bookings = []

# Initialize the time placeholder
if 'time_placeholder' not in st.session_state:
    st.session_state.time_placeholder = None

# -----------------------------------------------------------------------------
# 3. UTILITY FUNCTIONS
# -----------------------------------------------------------------------------

# --- Enhancement 3: Temporal Display (Debugged) ---
def display_running_time():
    """
    Displays the current time, giving a system/terminal aesthetic.
    Uses an initial placeholder and a safe rerun loop.
    """
    if st.session_state.time_placeholder is None:
        st.session_state.time_placeholder = st.empty()

    current_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    st.session_state.time_placeholder.markdown(f"""
        <div style="text-align: right; color: #888; font-size: 0.8em; margin-bottom: 20px;">
            SYSTEM TIME: {current_time_str} UTC
        </div>
        """, unsafe_allow_html=True)
        
    # Schedule a rerun every second if on one of the main pages
    if selected in ["HOME", "LABEL", "CONTACT"]:
        # Time.sleep() is crucial to make the update feel real and not cause excessive reruns
        time.sleep(1) 
        # Safely trigger a rerun for the time to update
        st.rerun() 
    # If on TRANSMISSIONS, MEDIA, or SYSTEM, do not call st.rerun()

# -----------------------------------------------------------------------------
# 4. NAVIGATION
# -----------------------------------------------------------------------------

# Styling option_menu
selected = option_menu(
    menu_title=None,
    options=["HOME", "TRANSMISSIONS", "LABEL", "MEDIA", "CONTACT", "SYSTEM"],
    icons=["circle-fill", "circle-fill", "circle-fill", "circle-fill", "circle-fill", "lock"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "0!important", 
            "background-color": "#000000", 
            "border-bottom": "1px solid #333",
            "margin-bottom": "2rem"
        },
        "icon": {"color": "#333", "font-size": "10px"}, 
        "nav-link": {
            "font-size": "16px",
            "text-align": "center", 
            "margin": "0px", 
            "color": "#fff",
            "font-family": "Courier New",
            "text-transform": "uppercase",
            "font-weight": "bold",
            "transition": "text-shadow 0.3s",
            "line-height": "1.2", 
            "min-height": "40px",
            "display": "flex",
            "align-items": "center",
            "justify-content": "center",
        },
        "nav-link:hover": { 
            "text-shadow": f"0 0 5px {NEON_CYAN}",
        },
        "nav-link-selected": {
            "background-color": "#000000", 
            "color": NEON_CYAN, 
            "border-bottom": f"2px solid {NEON_CYAN}"
        }, 
    }
)

# -----------------------------------------------------------------------------
# 5. PAGE LOGIC
# -----------------------------------------------------------------------------

# Run the running time display only on main pages
if selected in ["HOME", "LABEL", "CONTACT"]:
    # Display the time at the very top of the content area
    display_running_time()


# --- HOME / BIO ---
if selected == "HOME":
    # 3. New unique artist name/logo presentation
    st.markdown(f"<span class='logo-text'>TUESDAYNIGHTFREAK</span>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='color: #666 !important;'>LIVE HARDWARE ELECTRONICS // MELBOURNE -- BERLIN {TNF_LOGO_SVG}</h4>", unsafe_allow_html=True)
    
    # --- Enhancement 2: Interactive Live Feed Status ---
    # Randomly show a status for demonstration
    status = random.choice(["LIVE: TONE TESTING", "STANDBY", "OFFLINE"])
    status_color = NEON_CYAN if status.startswith("LIVE") else "#888"
    st.markdown(f"""
        <div style="
            display: inline-block; 
            padding: 5px 10px; 
            border: 1px solid {status_color}; 
            color: {status_color}; 
            font-size: 0.9em; 
            font-weight: bold; 
            margin-bottom: 20px;
            animation: {'blink 1s steps(1, end) infinite' if status.startswith('LIVE') else 'none'};
        ">
            FEED STATUS: {status}
        </div>
        <style>
            @keyframes blink {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}
        </style>
        """, unsafe_allow_html=True)
    # ----------------------------------------------------
    
    st.write("---")
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown(f"### BIOGRAPHY {TNF_LOGO_SVG}")
        
        st.markdown("""
        **Tuesdaynightfreak** operates in the void between mechanical precision and human error. Rejecting the safety of pre-recorded sets, the project is a study in live improvisation using a complex architecture of modular synthesis, drum machines, and feedback loops.
        
        Drawing from the austere industrialism of the Berlin school and the raw funk of Detroit's second wave, the sound is reductive and texture-heavy. It is music built for concrete rooms and high-pressure sound systems.
        
        No laptops. No presets. Just voltage and rhythm.
        """)
        
        st.write("")
        st.markdown("##### SCHEDULE")
        st.code("04.11 // TRESOR [BERLIN]\n11.11 // FOLD [LONDON]\n18.11 // REVOLVER [MELBOURNE]\n25.11 // STUDIO LOCKDOWN")

    with col2:
        # New Stock Image 1: Industrial Warehouse / Live
        st.image("https://images.unsplash.com/photo-1543167156-f6d89262f270?q=80&w=800&auto=format&fit=crop", 
                 caption="LIVE PERFORMANCE // 2024", use_column_width=True)
        st.caption("Image Source: Unsplash (Alistair Green)")
        
    st.write("---")
    # --- PROMOTIONAL FEATURE: FEATURED TRANSMISSION (EMBED) ---
    st.markdown("##### FEATURED TRANSMISSION (PROMINENT PLAYER)")
    st.html(f"""
    <iframe width="100%" height="166" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/1758580218&color=%23{'00f7ff'.lstrip('#')}&auto_play=false&hide_related=false&show_comments=false&show_user=true&show_reposts=false&show_teaser=true"></iframe>
    """)
    st.write("---")

    # Minimal Text Links for Socials
    cols = st.columns(4)
    cols[0].markdown("[INSTAGRAM](#)")
    cols[1].markdown("[SOUNDCLOUD](#)")
    cols[2].markdown("[SPOTIFY](#)")
    cols[3].markdown("[RESIDENT ADVISOR](#)")

# --- TRANSMISSIONS (MUSIC) ---
elif selected == "TRANSMISSIONS":
    st.markdown("### SONIC ARCHIVE")
    st.write("Live recordings and unreleased sketches.")
    
    st.write("---")
    
    # Text-based list layout (Brutalist style)
    for song in st.session_state.songs:
        col1, col2, col3 = st.columns([5, 2, 2])
        with col1:
            st.markdown(f"**{song['title']}**")
        with col2:
            st.caption(f"[{song['platform']}]")
        with col3:
            st.markdown(f"[>> LISTEN]({song['url']})")
        st.markdown("<hr style='margin: 10px 0; border-top: 1px dashed #333;'>", unsafe_allow_html=True)

# --- LABEL ---
elif selected == "LABEL":
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("## HOUSE KEEPING RECORDS")
        st.caption("EST. 2023 // PHYSICAL & DIGITAL")
        st.write("---")
        
        # --- LABEL FEATURE: MAILING LIST SIGNUP ---
        st.markdown("##### ACCESS PROTOCOL (MAILING LIST)")
        with st.form("mailing_list_form"):
            email_ml = st.text_input("ENTER FREQUENCY", placeholder="user@domain.com")
            if st.form_submit_button("SUBSCRIBE"):
                if email_ml:
                    st.success("FREQUENCY ACQUIRED. THANK YOU.")
                else:
                    st.error("INVALID FREQUENCY.")
        st.write("---")
        
        # --- Enhancement 1: Gated Download/Promo Section ---
        st.markdown("##### PROMO ACCESS (BETA TRACKS)")
        st.caption("ENTER PROMO KEY FOR UNRELEASED STEMS & DJ TOOLS")
        with st.form("promo_access_form"):
            promo_code = st.text_input("ENTER PROMO KEY", type="password", placeholder="e.g., HKR-BETA-003")
            if st.form_submit_button("UNLOCK ASSETS"):
                if promo_code == "HKR-BETA-003":
                    st.success("ACCESS GRANTED. [DOWNLOAD STICKERS & STEMS HERE](#) (Note: In a real app, this would require a backend.)")
                else:
                    st.warning("KEY INVALID. REQUIRES ADMIN OR PROMOTER CLEARANCE.")
        st.write("---")


        st.markdown("""
        **House Keeping Records** exists to document the output of the local hardware community. 
        
        We focus on the functional, the raw, and the deep. We release tools for DJs and explorations for heads. Vinyl pressing for select projects. 
        """)
        
    
    with col2:
        # New Stock Image 2: Patch Cables
        st.image("https://images.unsplash.com/photo-1598275529124-b1c4b786f1e2?q=80&w=800&auto=format&fit=crop", caption="HKR CATALOGUE", use_column_width=True)
        st.caption("Image Source: Unsplash (Ryan Hoffman)")
        st.write("---")
        
        # --- LABEL FEATURE: ARTIST ROSTER ---
        st.markdown("##### ARTIST ROSTER")
        st.code("TUESDAYNIGHTFREAK\nSYSTEM NOISE\nFUTURA DYNAMICS")
        
        # --- LABEL FEATURE: STOCKISTS ---
        st.markdown("##### PHYSICAL STOCKISTS (EUROPE)")
        st.code("HARDWAX [BERLIN]\nTECHNO IMPORT [PARIS]\nPHONICA [LONDON]")
        

    st.write("---")
    st.markdown("### DEMO SUBMISSION")
    st.write("We listen. Private SoundCloud links only. Do not send WeTransfer files.")
    st.code("demo@housekeeping-rec.com")
    
    st.write("---")
    st.markdown("### LATEST PRESSINGS")
    st.text("HKR001 // TUESDAYNIGHTFREAK // STATIC INTERFERENCE EP [12\"]")
    st.text("HKR002 // VARIOUS ARTISTS // TOOLS FOR DJs VOL. 1 [DIGITAL]")


# --- MEDIA (PHOTO / VIDEO) ---
elif selected == "MEDIA":
    st.markdown("### MEDIA ARCHIVE (PHOTO / VIDEO)")
    
    # Strict 2-column grid for visuals
    cols = st.columns(2)
    for i, item in enumerate(st.session_state.gallery):
        col_idx = i % 2
        with cols[col_idx]:
            st.image(item['url'], use_column_width=True)
            st.caption(f"// {item['caption']}")
            st.write("")

# --- CONTACT ---
elif selected == "CONTACT":
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### BOOKING")
        st.write("Representation: Independent.")
        st.write("Region: Worldwide.")
        st.write("")
        
        st.write("---")
        st.markdown("### MEDIA RELATIONS")
        # --- PROMOTIONAL FEATURE: PRESS KIT ---
        st.markdown("""
        **PRESS KIT (HIGH-RES ASSETS)**
        Download high-resolution press photos, full biography, and logo files.
        """)
        st.button("DOWNLOAD PKG [28MB]") 
        
        st.write("")
        st.markdown("**MANAGEMENT**")
        st.code("tuesdaynightfreak@gmail.com")
        st.write("")
        st.markdown("""
        **TECHNICAL RIDER**
        * 2x Meters table space (vibration free)
        * 2x Stereo DI boxes (Radial preferred)
        * 1x Monitor wedge (controllable from booth)
        * No smoke machines during performance
        """)

    with col2:
        st.markdown("### INQUIRY CHANNEL")
        with st.form("booking_form"):
            st.markdown("**DATE / VENUE / OFFER**")
            name = st.text_input("PROMOTER / AGENT", placeholder="Name or Organization")
            email = st.text_input("RETURN FREQUENCY (EMAIL)", placeholder="contact@domain.com")
            details = st.text_area("DETAILS", placeholder="Include date, venue, and fee offer.")
            
            submitted = st.form_submit_button("TRANSMIT REQUEST")
            
            if submitted:
                if name and email:
                    new_booking = {
                        "name": name, 
                        "email": email, 
                        "details": details,
                        "timestamp": str(datetime.now())
                    }
                    st.session_state.bookings.append(new_booking)
                    st.success("TRANSMISSION RECEIVED. WE WILL RESPOND IF ALIGNED.")
                else:
                    st.error("INCOMPLETE DATA.")

# --- SYSTEM (ADMIN) ---
elif selected == "SYSTEM":
    st.markdown("### RESTRICTED ACCESS")
    
    password = st.text_input("ACCESS CODE", type="password")
    
    if password == "admin123":
        st.success("AUTHENTICATED")
        
        tab1, tab2, tab3 = st.tabs(["AUDIO", "VISUAL", "LOGS"])
        
        with tab1:
            st.markdown("**ADD AUDIO SOURCE**")
            with st.form("add_song"):
                new_title = st.text_input("TITLE")
                new_url = st.text_input("URL")
                new_platform = st.selectbox("PLATFORM", ["SoundCloud", "Bandcamp", "Spotify", "RA"])
                if st.form_submit_button("UPLOAD"):
                    st.session_state.songs.append({"title": new_title, "url": new_url, "platform": new_platform})
                    st.rerun()
            
            if st.button("PURGE ALL SONGS"):
                st.session_state.songs = []
                st.rerun()

        with tab2:
            st.markdown("**ADD VISUAL ASSET**")
            with st.form("add_photo"):
                new_caption = st.text_input("CAPTION")
                new_img_url = st.text_input("IMAGE URL")
                if st.form_submit_button("UPLOAD"):
                    st.session_state.gallery.append({"caption": new_caption, "url": new_img_url})
                    st.rerun()

        with tab3:
            st.markdown("**INCOMING TRANSMISSIONS**")
            if len(st.session_state.bookings) > 0:
                st.table(pd.DataFrame(st.session_state.bookings))
            else:
                st.write("NO DATA.")
