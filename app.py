import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import random
import time

# --- CONFIGURATION & PALETTE ---
CP_YELLOW = "#fcee0a"
CP_CYAN = "#00f0ff"
CP_RED = "#ff003c"
CP_BLACK = "#050a0e"
TT_CREAM = "#f2f2f2"  # Used for contrast borders

# --- DEFECTED-INSPIRED "PREMIUM UNDERGROUND" ---
COLOR_BG = "#080808"
COLOR_TEXT = "#F0F0F0"
COLOR_ACCENT = "#FF0033"
COLOR_SECONDARY = "#1A1A1A"

# --- BRANDING: CUSTOM SVG LOGOS ---
TNF_STAMP_LOGO = f"""
<svg width="60" height="60" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="45" stroke="{CP_YELLOW}" stroke-width="5" fill="{CP_BLACK}"/>
  <path d="M20 50 L40 50 L40 80" stroke="{CP_CYAN}" stroke-width="8"/> 
  <path d="M50 80 L50 20 L80 80 L80 20" stroke="{CP_RED}" stroke-width="6"/>
  <text x="50%" y="50%" text-anchor="middle" stroke="{CP_YELLOW}" stroke-width="1" dy=".3em" font-family="monospace" font-weight="bold" font-size="20">TNF</text>
</svg>
"""

TNF_LOGO_SVG = f"""
<svg width="120" height="40" viewBox="0 0 120 40" fill="none" xmlns="http://www.w3.org/2000/svg">
  <text x="0" y="30" font-family="Helvetica, Arial, sans-serif" font-weight="900" font-size="32" fill="{COLOR_TEXT}" letter-spacing="-2">TNF</text>
  <circle cx="80" cy="20" r="8" fill="{COLOR_ACCENT}"/>
  <rect x="95" y="12" width="25" height="16" fill="{COLOR_TEXT}"/>
</svg>
"""

# -----------------------------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="TUESDAYNIGHTFREAK | OFFICIAL",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# CUSTOM CSS: build with placeholders then replace to avoid f-string brace issues
# -----------------------------------------------------------------------------
css_template = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow:wght@400;700;900&family=Tomorrow:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&display=swap');

    /* GLOBAL RESET */
    .stApp { background-color: %%COLOR_BG%%; color: %%COLOR_TEXT%%; font-family: 'Inter', sans-serif; }

    /* HIDE DEFAULT UI */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    /* CONTAINER SIZING */
    .block-container { padding-top: 1rem !important; max-width: 1200px; }

    /* TYPOGRAPHY */
    .artist-title { font-family: 'Tomorrow', sans-serif; font-size: 4rem; font-weight: 900; text-transform: uppercase; color: %%CP_YELLOW%%; text-shadow: 4px 4px 0px %%CP_CYAN%%; line-height: 0.9; letter-spacing: -2px; transform: skew(-5deg); margin-bottom: 10px; }

    h1, h2, h3 { font-family: 'Barlow', sans-serif; text-transform: uppercase; font-weight: 900; color: %%COLOR_TEXT%%; border-bottom: 3px solid %%CP_YELLOW%%; display: inline-block; padding-bottom: 5px; margin-top: 30px !important; letter-spacing: -1px; margin-bottom: 0.5rem; }

    h4, h5, h6 { color: %%CP_CYAN%% !important; font-family: 'Tomorrow', sans-serif; }

    /* BUTTONS */
    .stButton > button { background-color: %%COLOR_TEXT%%; color: %%COLOR_BG%%; border: none; font-family: 'Inter', sans-serif; font-weight: 900; text-transform: uppercase; padding: 12px 28px; border-radius: 0px; transition: all 0.3s; }
    .stButton > button:hover { background-color: %%COLOR_ACCENT%%; color: %%COLOR_TEXT%%; transform: scale(1.02); box-shadow: 4px 4px 0px %%CP_RED%%; }

    /* CARDS */
    .graphic-box { border: 2px solid %%TT_CREAM%%; padding: 18px; }
    .news-card { background-color: %%COLOR_SECONDARY%%; padding: 18px; border-left: 4px solid %%COLOR_ACCENT%%; margin-bottom: 20px; transition: transform 0.3s; }
    .news-card:hover { transform: translateX(5px); }

    /* INPUTS */
    .stTextInput input, .stTextArea textarea, .stSelectbox div { background-color: #1a1a1a; color: %%CP_YELLOW%%; border: 2px solid %%CP_CYAN%%; }
    .stTextInput input:focus, .stTextArea textarea:focus { border-color: %%COLOR_ACCENT%%; }

    a { color: %%CP_YELLOW%% !important; text-decoration: none; font-weight: bold; }
    a:hover { background-color: %%CP_YELLOW%%; color: %%CP_BLACK%% !important; }

    hr { border-color: #333; margin: 3rem 0; }

    /* small utility */
    .muted { color: #888; font-size: 0.85rem; }

</style>
"""

css = (css_template
       .replace('%%CP_YELLOW%%', CP_YELLOW)
       .replace('%%CP_CYAN%%', CP_CYAN)
       .replace('%%CP_RED%%', CP_RED)
       .replace('%%CP_BLACK%%', CP_BLACK)
       .replace('%%TT_CREAM%%', TT_CREAM)
       .replace('%%COLOR_BG%%', COLOR_BG)
       .replace('%%COLOR_TEXT%%', COLOR_TEXT)
       .replace('%%COLOR_ACCENT%%', COLOR_ACCENT)
       .replace('%%COLOR_SECONDARY%%', COLOR_SECONDARY)
)

st.markdown(css, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# INITIALIZE SESSION STATE
# -----------------------------------------------------------------------------
if 'songs' not in st.session_state:
    st.session_state.songs = [
        {"title": "UNTITLED_SEQ_04 [LIVE REC]", "url": "#", "platform": "SoundCloud"},
        {"title": "MODULAR EXCURSION B (RAW)", "url": "#", "platform": "Bandcamp"},
        {"title": "RESIDENT ADVISOR PODCAST 892", "url": "#", "platform": "RA"},
        {"title": "System Failure (Original Mix)", "label": "House Keeping Rec", "cat": "HKR004"},
        {"title": "Analog Dreams", "label": "Tresor Records", "cat": "TR-291"},
        {"title": "Voltage Control", "label": "Ostgut Ton", "cat": "OSTGUT-55"}
    ]

if 'gallery' not in st.session_state:
    st.session_state.gallery = [
        {"caption": "WAREHOUSE RAVE // BERLIN", "url": "https://images.unsplash.com/photo-1574169208507-84376144848b?q=80&w=800&auto=format&fit=crop"},
        {"caption": "MODULAR SYSTEM // LIVE RIG", "url": "https://images.unsplash.com/photo-1550291652-6ea9114a47b1?q=80&w=800&auto=format&fit=crop"},
        {"caption": "CROWD ENERGY // 3AM", "url": "https://images.unsplash.com/photo-1571266028243-371695063ad6?q=80&w=800&auto=format&fit=crop"},
        {"caption": "ANALOG OSCILLATORS", "url": "https://images.unsplash.com/photo-1621360841012-2357d27e02a4?q=80&w=800&auto=format&fit=crop"},
        {"caption": "MODULAR RIG SETUP A", "url": "https://images.unsplash.com/photo-1550291652-6ea9114a47b1?q=80&w=800&auto=format&fit=crop"},
        {"caption": "LIVE SIGNAL PATH", "url": "https://images.unsplash.com/photo-1598275529124-b1c4b786f1e2?q=80&w=800&auto=format&fit=crop"},
        {"caption": "WAREHOUSE CROWD", "url": "https://images.unsplash.com/photo-1571266028243-371695063ad6?q=80&w=800&auto=format&fit=crop"},
        {"caption": "OSCILLATOR DETAIL", "url": "https://images.unsplash.com/photo-1619967657960-983b6329c370?q=80&w=800&auto=format&fit=crop"}
    ]

if 'bookings' not in st.session_state:
    st.session_state.bookings = []

# -----------------------------------------------------------------------------
# NAVIGATION
# -----------------------------------------------------------------------------
selected = option_menu(
    menu_title=None,
    options=["HOME", "MUSIC", "LABEL", "MEDIA", "EVENTS", "STORE", "CONTACT", "SYSTEM", "ABOUT"],
    icons=["house", "music-note-list", "tag", "camera-reels", "calendar-event", "bag", "envelope", "gear", "info-circle"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": COLOR_BG, "border-bottom": "1px solid #333"},
        "icon": {"color": "#666", "font-size": "12px"},
        "nav-link": {"font-size": "14px", "text-align": "center", "margin": "0px", "color": TT_CREAM, "font-family": "Inter, sans-serif", "text-transform": "uppercase", "font-weight": "600"},
        "nav-link-selected": {"background-color": COLOR_BG, "color": COLOR_TEXT, "border-bottom": f"2px solid {COLOR_ACCENT}"},
    }
)

# -----------------------------------------------------------------------------
# PAGES
# -----------------------------------------------------------------------------

# HOME
if selected == "HOME":
    col1, col2 = st.columns([2, 1])

    with col1:
        st.image("https://images.unsplash.com/photo-1517457375825-e578c799a74f?q=80&w=1400&auto=format&fit=crop", use_column_width=True)
        st.markdown('<div class="artist-title">TUESDAY<br>NIGHT<br>FREAK</div>', unsafe_allow_html=True)
        st.markdown(f"### LIVE HARDWARE ELECTRONICS {TNF_STAMP_LOGO}", unsafe_allow_html=True)
        st.markdown(f"<h5 style='color:{TT_CREAM} !important'>MELBOURNE // BERLIN // UNDERGROUND</h5>", unsafe_allow_html=True)
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
        st.markdown("#### LATEST NEWS")
        st.markdown(f"""
        <div class="graphic-box">
        Tuesdaynightfreak is not just an artist; it's a <strong>sonic movement</strong>.
        We are an independent electronic music project and culture crew bridging the gap between 
        Berlin's concrete basements and Melbourne's warehouse soul.
        <div class="news-card">
        <strong>NEW EP ANNOUNCED</strong><br>
        <span class="muted">OCT 24, 2025</span><br>
        'Voltage Control' drops worldwide next Friday on House Keeping Records.
        </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"**CURRENT SYSTEM STATUS:** <span style='color:{CP_YELLOW}; font-family:monospace;'>ONLINE // STUDIO MODE</span>", unsafe_allow_html=True)

    st.write("---")

# MUSIC
elif selected == "MUSIC":
    st.markdown("## SONIC ARCHIVE")
    st.markdown("### LIVE JAMS & STUDIO CUTS")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### UNTITLED_SEQ_04")
        st.image("https://images.unsplash.com/photo-1493225255756-d9584f8606e9?q=80&w=800&auto=format&fit=crop", caption="Live Recording")
        st.markdown("[STREAM ON SOUNDCLOUD](#)")

    with col2:
        st.markdown("#### ACID RAIN (DUB)")
        st.image("https://images.unsplash.com/photo-1514525253440-b393452e8d26?q=80&w=800&auto=format&fit=crop", caption="Studio Cut")
        st.markdown("[BUY ON BANDCAMP](#)")

    st.write("---")
    st.markdown("### DISCOGRAPHY LIST")
    for song in st.session_state.songs:
        st.markdown(f"**{song['title']}** // {song.get('platform', song.get('label',''))}")

# LABEL
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

    with col2:
        st.markdown("### SUBMIT DEMO")
        with st.form("demo_form"):
            st.text_input("ARTIST ALIAS")
            st.text_input("SOUNDCLOUD LINK (PRIVATE ONLY)")
            st.form_submit_button("TRANSMIT DATA")

# MEDIA
elif selected == "MEDIA":
    st.markdown("## VISUAL FEED")
    for item in st.session_state.gallery[:6]:
        st.image(item['url'], caption=item['caption'])

# EVENTS
elif selected == "EVENTS":
    st.markdown("## UPCOMING DATES")
    c1, c2 = st.columns(2)
    for i, item in enumerate(st.session_state.gallery):
        if i % 2 == 0:
            with c1:
                st.image(item['url'], caption=item['caption'])
        else:
            with c2:
                st.image(item['url'], caption=item['caption'])

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
                st.markdown("<span class='muted'>SOLD OUT</span>", unsafe_allow_html=True)
            else:
                st.button(f"BUY {event['status']}", key=event['city'])

# STORE
elif selected == "STORE":
    st.markdown("## SHOP MERCH & VINYL")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("## BOOKING & PRESS")
        st.markdown("### WORLDWIDE")
        st.write("Direct Management")
        st.markdown(f"<h2 style='border:none; color:{CP_YELLOW};'>tuesdaynightfreak@gmail.com</h2>", unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1585227803927-2c24067b9416?q=80&w=600&auto=format&fit=crop", caption='HKR004 - VINYL 12"')
        st.markdown("**SYSTEM FAILURE EP**")
        st.caption("€14.00")
        st.button("ADD TO CART", key="p1")

        st.write("---")
        st.markdown("### MEDIA KIT")
        st.download_button("DOWNLOAD TECH RIDER (PDF)", "Rider Content", file_name="TNF_Rider_2025.pdf")
        st.download_button("DOWNLOAD PRESS PHOTOS (ZIP)", "Photo Content", file_name="TNF_Press_Photos.zip")

    with c2:
        st.markdown("### TRANSMIT MESSAGE")
        with st.form("contact_form"):
            st.text_input("IDENTIFIER (NAME)")
            st.text_input("RETURN FREQUENCY (EMAIL)")
            st.text_area("MESSAGE PACKET")
            st.form_submit_button("SEND TRANSMISSION")
        st.image("https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?q=80&w=600&auto=format&fit=crop", caption="TNF LOGO TEE")
        st.markdown("**OFFICIAL T-SHIRT**")
        st.caption("€35.00")
        st.button("ADD TO CART", key="p2")

    with c3:
        st.image("https://images.unsplash.com/photo-1529339077446-df732dfa062c?q=80&w=600&auto=format&fit=crop", caption="PATCH CABLE SET")
        st.markdown("**TNF CABLE PACK**")
        st.caption("€20.00")
        st.button("ADD TO CART", key="p3")

# SYSTEM (ADMIN)
elif selected == "SYSTEM":
    st.markdown("## SYSTEM ACCESS")
    st.caption("SECURE AREA. AUTHORIZED PERSONNEL ONLY.")
    pwd = st.text_input("ENTER AUTH CODE", type="password")
    if pwd == "admin123":
        st.success("ACCESS GRANTED. WELCOME, OPERATOR.")
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

        with tab2:
            st.markdown("### ADD VISUAL ASSET")
            with st.form("add_photo_admin"):
                new_caption = st.text_input("CAPTION")
                new_img_url = st.text_input("IMAGE URL")
                if st.form_submit_button("UPLOAD VISUAL"):
                    st.session_state.gallery.append({"caption": new_caption, "url": new_img_url})
                    st.success("VISUAL ASSET ADDED TO FEED.")

        with tab3:
            st.markdown("### INCOMING TRANSMISSIONS")
            if len(st.session_state.bookings) > 0:
                st.dataframe(pd.DataFrame(st.session_state.bookings))
            else:
                st.info("NO NEW MESSAGES.")

# ABOUT / CONTACT
elif selected == "ABOUT":
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.markdown("## THE PROJECT")
        st.markdown("""
        **Tuesdaynightfreak** is a dedicated exploration of electronic sound. 
        Founded in Melbourne, the project focuses on the visceral experience of 
        live hardware performance.
        """)
        st.markdown("## CONTACT MANAGEMENT")
        st.code("mgmt@tuesdaynightfreak.com")
        st.markdown("## DEMOS")
        st.code("demos@housekeeping-rec.com")

    with col2:
        st.markdown("## NEWSLETTER")
        with st.form("newsletter"):
            st.text_input("EMAIL ADDRESS")
            st.form_submit_button("SUBSCRIBE")
        st.write("---")
        st.markdown("#### PRESS KIT")
        st.button("DOWNLOAD EPK (ZIP)")

# -----------------------------------------------------------------------------
# END
# -----------------------------------------------------------------------------
