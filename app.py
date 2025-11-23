import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime
import random

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & BERLIN AESTHETIC CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="TUESDAYNIGHTFREAK",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS: Brutalist, Monochrome, Raw + Neon Green Highlights
st.markdown("""
<style>
    /* 1. GLOBAL RESET & MONOCHROME THEME */
    .stApp {
        background-color: #050505;
        color: #e0e0e0;
        font-family: 'Courier New', Courier, monospace; /* Industrial/Terminal font */
    }

    /* 2. REMOVE STREAMLIT BRANDING & HEADER */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;} /* Hides the top colored bar and hamburger menu */
    
    /* 3. FIX MENU CUT-OFF (Adjust Top Padding) */
    .block-container {
        padding-top: 1rem !important; /* Reduced to bring menu up, but ensures visibility */
        padding-bottom: 5rem;
        max-width: 1200px;
    }

    /* 4. TYPOGRAPHY & NEON HIGHLIGHTS */
    h1, h2, h3, h4, h5, h6 {
        color: #39ff14 !important; /* NEON GREEN RESTORED */
        font-family: 'Courier New', Courier, monospace;
        text-transform: uppercase;
        font-weight: 900;
        letter-spacing: -1.5px;
    }
    
    p, div, label, span {
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: -0.5px;
    }
    
    a {
        color: #39ff14 !important;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
        text-shadow: 0 0 10px #39ff14;
    }

    /* 5. IMAGERY - FORCE B&W & HIGH CONTRAST */
    img {
        filter: grayscale(100%) contrast(120%) brightness(85%);
        transition: all 0.4s ease;
        border: 1px solid #1a1a1a;
    }
    img:hover {
        filter: grayscale(0%) contrast(110%) brightness(100%); /* Color reveal on hover */
        border: 1px solid #39ff14;
        box-shadow: 0 0 15px rgba(57, 255, 20, 0.2);
    }

    /* 6. UI ELEMENTS - BRUTALIST (NO ROUNDED CORNERS) */
    .stButton>button {
        color: #39ff14;
        background-color: #000000;
        border: 1px solid #39ff14;
        border-radius: 0px !important; /* Sharp edges */
        text-transform: uppercase;
        padding: 12px 24px;
        font-weight: bold;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #39ff14;
        color: #000000;
        box-shadow: 0 0 20px rgba(57, 255, 20, 0.6);
    }

    /* 7. INPUTS */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: #0a0a0a;
        color: #39ff14;
        border: 1px solid #333;
        border-radius: 0px;
        font-family: 'Courier New', monospace;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #39ff14;
    }
    
    hr {
        border-top: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. SESSION STATE
# -----------------------------------------------------------------------------
if 'songs' not in st.session_state:
    st.session_state.songs = [
        {"title": "UNTITLED_SEQ_04 [LIVE REC]", "url": "#", "platform": "SoundCloud"},
        {"title": "MODULAR EXCURSION B (RAW)", "url": "#", "platform": "Bandcamp"},
        {"title": "RESIDENT ADVISOR PODCAST 892", "url": "#", "platform": "RA"},
    ]

if 'gallery' not in st.session_state:
    # Updated to reflect modular, crowd, and gig aesthetics (as requested)
    st.session_state.gallery = [
        {"caption": "LIVE RITUAL / DANCEFLOOR", "url": "https://images.unsplash.com/photo-1588975850980-8798e2850949?q=80&w=800&auto=format&fit=crop"}, # Crowd
        {"caption": "EURORACK & PATCH CABLES", "url": "https://images.unsplash.com/photo-1610427926868-685b5a26e828?q=80&w=800&auto=format&fit=crop"}, # Modular Synth
        {"caption": "BERLIN WAREHOUSE ATMOSPHERE", "url": "https://images.unsplash.com/photo-1628171092520-279611b7d52f?q=80&w=800&auto=format&fit=crop"}, # Gig/Atmosphere
        {"caption": "ANALOG DRUM MACHINE", "url": "https://images.unsplash.com/photo-1616147413695-1f912257224f?q=80&w=800&auto=format&fit=crop"}, # Hardware
    ]

if 'bookings' not in st.session_state:
    st.session_state.bookings = []

# -----------------------------------------------------------------------------
# 3. NAVIGATION
# -----------------------------------------------------------------------------
# Styling option_menu to be high contrast with Neon Green
selected = option_menu(
    menu_title=None,
    # Renamed VISUALS to MEDIA
    options=["HOME", "TRANSMISSIONS", "LABEL", "MEDIA", "CONTACT", "SYSTEM"],
    # Changed "dot" to "circle-fill" because "dot" is not a valid Bootstrap icon
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
            "font-size": "14px", 
            "text-align": "center", 
            "margin": "0px", 
            "color": "#888", 
            "font-family": "Courier New",
            "text-transform": "uppercase",
            "font-weight": "bold"
        },
        "nav-link-selected": {
            "background-color": "#000000", 
            "color": "#39ff14", # Fixed: Changed from CSS comment to Python comment
            "border-bottom": "2px solid #39ff14"
        },
    }
)

# -----------------------------------------------------------------------------
# 4. PAGE LOGIC
# -----------------------------------------------------------------------------

# --- HOME / BIO ---
if selected == "HOME":
    st.markdown("## TUESDAYNIGHTFREAK")
    st.markdown("<h4 style='color: #666 !important;'>LIVE HARDWARE ELECTRONICS // MELBOURNE -- BERLIN</h4>", unsafe_allow_html=True)
    
    st.write("---")
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        ### BIOGRAPHY
        
        **Tuesdaynightfreak** operates in the void between mechanical precision and human error. Rejecting the safety of pre-recorded sets, the project is a study in live improvisation using a complex architecture of modular synthesis, drum machines, and feedback loops.
        
        Drawing from the austere industrialism of the Berlin school and the raw funk of Detroit's second wave, the sound is reductive and texture-heavy. It is music built for concrete rooms and high-pressure sound systems.
        
        No laptops. No presets. Just voltage and rhythm.
        """)
        
        st.write("")
        st.markdown("##### SCHEDULE")
        st.code("04.11 // TRESOR [BERLIN]\n11.11 // FOLD [LONDON]\n18.11 // REVOLVER [MELBOURNE]\n25.11 // STUDIO LOCKDOWN")

    with col2:
        # Image will be rendered B&W by CSS, revealing color on hover
        st.image("https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?q=80&w=800&auto=format&fit=crop", 
                 caption="LIVE PERFORMANCE // 2024", use_column_width=True)

    st.write("---")
    # --- PROMOTIONAL FEATURE: FEATURED TRANSMISSION (EMBED) ---
    st.markdown("##### FEATURED TRANSMISSION (PROMINENT PLAYER)")
    # Simulating a prominent music player embed
    st.html("""
    <iframe width="100%" height="166" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/1758580218&color=%2339ff14&auto_play=false&hide_related=false&show_comments=false&show_user=true&show_reposts=false&show_teaser=true"></iframe>
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

        st.markdown("""
        **House Keeping Records** exists to document the output of the local hardware community. 
        
        We focus on the functional, the raw, and the deep. We release tools for DJs and explorations for heads. Vinyl pressing for select projects. 
        """)
        
    
    with col2:
        # Image: Vinyl / Studio aesthetic
        st.image("https://images.unsplash.com/photo-1605218427306-022648d42d32?q=80&w=800&auto=format&fit=crop", caption="HKR CATALOGUE", use_column_width=True)
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


# --- MEDIA (formerly VISUALS) ---
elif selected == "MEDIA":
    st.markdown("### MEDIA ARCHIVE (PHOTO / VIDEO)") # Updated Title
    
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
        # Simulate a button for file download (cannot actually download, but shows the feature)
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
            
            # Custom styled button via CSS above
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
