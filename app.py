import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime
import random
import time

# --- CONFIGURATION & PALETTE ---
CP_YELLOW = "#fcee0a"
CP_CYAN = "#00f0ff"
CP_RED = "#ff003c"
CP_BLACK = "#050a0e"
TT_CREAM = "#f2f2f2" # Used for contrast borders

# --- BRANDING: CUSTOM SVG LOGO (Toy Tonics Stamp Style x Cyberpunk) ---
TNF_STAMP_LOGO = f"""
<svg width="60" height="60" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="50" cy="50" r="45" stroke="{CP_YELLOW}" stroke-width="5" fill="{CP_BLACK}"/>
<path d="M20 50 L40 50 L40 80" stroke="{CP_CYAN}" stroke-width="8"/> 
<path d="M50 80 L50 20 L80 80 L80 20" stroke="{CP_RED}" stroke-width="6"/>
<text x="50%" y="50%" text-anchor="middle" stroke="{CP_YELLOW}" stroke-width="1px" dy=".3em" font-family="monospace" font-weight="bold" font-size="20">TNF</text>
</svg>
"""

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="TUESDAYNIGHTFREAK | CULTURE CREW",
    page_icon="🎹",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# 2. CUSTOM CSS (The Mashup Design)
# -----------------------------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow:wght@400;700;900&family=Tomorrow:wght@400;700&display=swap');

    /* GLOBAL RESET */
    .stApp {{
        background-color: {CP_BLACK};
        color: {TT_CREAM};
        font-family: 'Barlow', sans-serif;
    }}

    /* REMOVE DEFAULT UI */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .block-container {{ padding-top: 1rem !important; max-width: 1200px; }}

    /* --- TYPOGRAPHY --- */
    
    /* Cyberpunk Artist Name Style */
    .artist-title {{
        font-family: 'Tomorrow', sans-serif;
        font-size: 4rem; /* Responsive scaling needed usually, but huge for impact */
        font-weight: 900;
        text-transform: uppercase;
        color: {CP_YELLOW};
        text-shadow: 4px 4px 0px {CP_CYAN};
        line-height: 0.9;
        letter-spacing: -2px;
        transform: skew(-5deg);
        margin-bottom: 10px;
    }}
    
    /* Toy Tonics Style Headers (Bold, Graphic) */
    h1, h2, h3 {{
        font-family: 'Barlow', sans-serif;
        text-transform: uppercase;
        font-weight: 900;
        color: {CP_RED};
        border-bottom: 3px solid {CP_YELLOW}; /* Graphic underline */
        display: inline-block;
        padding-bottom: 5px;
        margin-top: 30px !important;
    }}
    
    h4, h5, h6 {{
        color: {CP_CYAN} !important;
        font-family: 'Tomorrow', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}

    /* --- UI ELEMENTS --- */
    
    /* Cyberpunk Buttons */
    .stButton>button {{
        background-color: {CP_YELLOW};
        color: {CP_BLACK};
        border: none;
        font-family: 'Tomorrow', sans-serif;
        font-weight: bold;
        text-transform: uppercase;
        clip-path: polygon(10% 0, 100% 0, 100% 70%, 90% 100%, 0 100%, 0 30%); /* Angled cut */
        padding: 15px 30px;
        transition: all 0.2s;
    }}
    .stButton>button:hover {{
        background-color: {CP_CYAN};
        color: {CP_BLACK};
        transform: translate(-2px, -2px);
        box-shadow: 4px 4px 0px {CP_RED};
    }}

    /* Graphic Boxes (Toy Tonics Style Borders) */
    .graphic-box {{
        border: 2px solid {TT_CREAM};
        padding: 20px;
        background: #111;
        margin-bottom: 20px;
    }}

    /* Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {{
        background-color: #1a1a1a;
        color: {CP_YELLOW};
        border: 2px solid {CP_CYAN};
        border-radius: 0;
        font-family: 'Tomorrow', sans-serif;
    }}

    /* Links */
    a {{ color: {CP_YELLOW} !important; text-decoration: none; font-weight: bold; }}
    a:hover {{ background-color: {CP_YELLOW}; color: {CP_BLACK} !important; }}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. STATE & DATA
# -----------------------------------------------------------------------------
if 'songs' not in st.session_state:
    st.session_state.songs = [
        {"title": "UNTITLED_SEQ_04 [LIVE REC]", "url": "#", "platform": "SoundCloud"},
        {"title": "MODULAR EXCURSION B (RAW)", "url": "#", "platform": "Bandcamp"},
        {"title": "RESIDENT ADVISOR PODCAST 892", "url": "#", "platform": "RA"},
    ]

if 'gallery' not in st.session_state:
    st.session_state.gallery = [
        {"caption": "WAREHOUSE RAVE // BERLIN", "url": "https://images.unsplash.com/photo-1574169208507-84376144848b?q=80&w=800&auto=format&fit=crop"},
        {"caption": "MODULAR SYSTEM // LIVE RIG", "url": "https://images.unsplash.com/photo-1550291652-6ea9114a47b1?q=80&w=800&auto=format&fit=crop"},
        {"caption": "CROWD ENERGY // 3AM", "url": "https://images.unsplash.com/photo-1571266028243-371695063ad6?q=80&w=800&auto=format&fit=crop"},
        {"caption": "ANALOG OSCILLATORS", "url": "https://images.unsplash.com/photo-1621360841012-2357d27e02a4?q=80&w=800&auto=format&fit=crop"}
    ]

if 'bookings' not in st.session_state:
    st.session_state.bookings = []

# -----------------------------------------------------------------------------
# 4. NAVIGATION (Toy Tonics Style - Simple Top Bar)
# -----------------------------------------------------------------------------
selected = option_menu(
    menu_title=None,
    options=["HOME", "MUSIC", "LABEL", "MEDIA", "CONTACT", "SYSTEM"],
    icons=["house", "disc", "vinyl", "camera-reels", "envelope", "cpu"], 
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": CP_BLACK, "border-bottom": f"1px solid {CP_CYAN}"},
        "icon": {"color": CP_YELLOW, "font-size": "14px"}, 
        "nav-link": {
            "font-size": "14px", "text-align": "center", "margin": "0px", 
            "color": TT_CREAM, "font-family": "Tomorrow, sans-serif", "text-transform": "uppercase"
        },
        "nav-link-selected": {"background-color": "#1a1a1a", "color": CP_CYAN, "border-top": f"3px solid {CP_RED}"},
    }
)

# -----------------------------------------------------------------------------
# 5. PAGE CONTENT
# -----------------------------------------------------------------------------

# --- HOME PAGE ---
if selected == "HOME":
    # HERO SECTION
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown('<div class="artist-title">TUESDAY<br>NIGHT<br>FREAK</div>', unsafe_allow_html=True)
        st.markdown(f"### LIVE HARDWARE ELECTRONICS {TNF_STAMP_LOGO}", unsafe_allow_html=True)
        st.markdown(f"<h5 style='color:{TT_CREAM} !important'>MELBOURNE // BERLIN // UNDERGROUND</h5>", unsafe_allow_html=True)
        
        # Toy Tonics style copy: "Culture Crew", "Vibes", "Analogue"
        st.markdown(f"""
        <div class="graphic-box">
        Tuesdaynightfreak is not just an artist; it's a **sonic movement**. 
        We are an independent electronic music project and culture crew bridging the gap between 
        Berlin's concrete basements and Melbourne's warehouse soul.
        <br><br>
        We reject the digital perfection of modern EDM. We embrace the <strong>analogue error</strong>.
        We combine raw modular synthesis with the funk of Detroit's second wave to create 
        positive, high-pressure vibes. No laptops. Just voltage.
        </div>
        """, unsafe_allow_html=True)
        
        # Interactive Element: Status
        st.markdown(f"**CURRENT SYSTEM STATUS:** <span style='color:{CP_YELLOW}; font-family:monospace; animation: blink 1s infinite;'>ONLINE // STUDIO MODE</span>", unsafe_allow_html=True)

    with col2:
        # New Techno Image
        st.image("https://images.unsplash.com/photo-1594623930572-300a3011d9ae?q=80&w=800&auto=format&fit=crop", caption="LIVE AT TRESOR // 2024")

    st.write("---")
    
    # FEATURED RELEASE
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("### LATEST DROP")
        # Simulating a bold graphic card for a release
        st.image("https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?q=80&w=800&auto=format&fit=crop", caption="STATIC INTERFERENCE EP [12\" VINYL]")
        st.button("BUY VINYL / DIGITAL")

# --- MUSIC ---
elif selected == "MUSIC":
    st.markdown("## SONIC ARCHIVE")
    st.markdown("### LIVE JAMS & STUDIO CUTS")
    
    # Layout inspired by Toy Tonics "Music" page - Grid of releases
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### UNTITLED_SEQ_04")
        st.image("https://images.unsplash.com/photo-1493225255756-d9584f8606e9?q=80&w=800&auto=format&fit=crop", caption="Live Recording")
        st.markdown(f"[STREAM ON SOUNDCLOUD]({ '#'})")

    with col2:
        st.markdown(f"#### ACID RAIN (DUB)")
        st.image("https://images.unsplash.com/photo-1514525253440-b393452e8d26?q=80&w=800&auto=format&fit=crop", caption="Studio Cut")
        st.markdown(f"[BUY ON BANDCAMP]({ '#'})")
        
    st.write("---")
    st.markdown("### DISCOGRAPHY LIST")
    for song in st.session_state.songs:
        st.markdown(f"**{song['title']}** // {song['platform']}")

# --- LABEL ---
elif selected == "LABEL":
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("## HOUSE KEEPING RECORDS")
        st.markdown("**EST. 2023 // VINYL ONLY**")
        st.write("---")
        st.markdown(f"""
        <div class="graphic-box">
        House Keeping Records is our platform for the raw, the deep, and the functional. 
        We release tools for DJs and explorations for heads. 
        <br><br>
        **PHILOSOPHY:**<br>
        1. Respect the groove.<br>
        2. Hardware over software.<br>
        3. Community over clout.
        </div>
        """, unsafe_allow_html=True)
        
        # Demo Submission with "Cyberpunk" form style
        st.markdown("### SUBMIT DEMO")
        with st.form("demo_form"):
            st.text_input("ARTIST ALIAS")
            st.text_input("SOUNDCLOUD LINK (PRIVATE ONLY)")
            st.form_submit_button("TRANSMIT DATA")

    with col2:
        st.image("https://images.unsplash.com/photo-1603048588665-791ca8aea617?q=80&w=800&auto=format&fit=crop", caption="HKR HEADQUARTERS")
        
        # Physical Stockists List
        st.markdown("#### STOCKISTS")
        st.markdown(f"""
        * <span style="color:{CP_CYAN}">HARDWAX</span> [BERLIN]
        * <span style="color:{CP_CYAN}">PHONICA</span> [LONDON]
        * <span style="color:{CP_CYAN}">RUSH HOUR</span> [AMSTERDAM]
        """, unsafe_allow_html=True)

# --- MEDIA ---
elif selected == "MEDIA":
    st.markdown("## VISUAL FEED")
    
    # Masonry-style grid (Toy Tonics often has eclectic layouts)
    c1, c2 = st.columns(2)
    for i, item in enumerate(st.session_state.gallery):
        if i % 2 == 0:
            with c1:
                st.image(item["url"], caption=item["caption"])
        else:
            with c2:
                st.image(item["url"], caption=item["caption"])

# --- CONTACT ---
elif selected == "CONTACT":
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("## BOOKING & PRESS")
        st.markdown("### WORLDWIDE")
        st.write("Direct Management")
        st.markdown(f"<h2 style='border:none; color:{CP_YELLOW};'>tuesdaynightfreak@gmail.com</h2>", unsafe_allow_html=True)
        
        st.write("---")
        st.markdown("### MEDIA KIT")
        # Downloadable Rider/Press Kit
        st.download_button("DOWNLOAD TECH RIDER (PDF)", "Rider Content", file_name="TNF_Rider_2025.pdf")
        st.download_button("DOWNLOAD PRESS PHOTOS (ZIP)", "Photo Content", file_name="TNF_Press_Photos.zip")

    with c2:
        st.markdown("### TRANSMIT MESSAGE")
        with st.form("contact_form"):
            st.text_input("IDENTIFIER (NAME)")
            st.text_input("RETURN FREQUENCY (EMAIL)")
            st.text_area("MESSAGE PACKET")
            st.form_submit_button("SEND TRANSMISSION")

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
                new_url = st.text_input("URL (SoundCloud/Bandcamp)")
                new_platform = st.selectbox("PLATFORM", ["SoundCloud", "Bandcamp", "Spotify", "RA"])
                if st.form_submit_button("UPLOAD TRACK"):
                    st.session_state.songs.append({"title": new_title, "url": new_url, "platform": new_platform})
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
