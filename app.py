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

# Custom CSS: Brutalist, Monochrome, Raw
st.markdown("""
<style>
    /* 1. GLOBAL RESET & MONOCHROME THEME */
    .stApp {
        background-color: #000000;
        color: #e0e0e0;
        font-family: 'Courier New', Courier, monospace; /* Industrial/Terminal font */
    }

    /* 2. TYPOGRAPHY */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-family: 'Courier New', Courier, monospace;
        text-transform: uppercase;
        font-weight: 900;
        letter-spacing: -1px;
    }
    
    p, div, label, span {
        font-family: 'Courier New', Courier, monospace;
    }

    /* 3. IMAGERY - FORCE B&W & HIGH CONTRAST */
    img {
        filter: grayscale(100%) contrast(110%) brightness(90%);
        transition: filter 0.3s ease;
    }
    img:hover {
        filter: grayscale(0%) contrast(100%); /* Slight reveal on hover */
    }

    /* 4. UI ELEMENTS - BRUTALIST (NO ROUNDED CORNERS) */
    .stButton>button {
        color: #ffffff;
        background-color: #000000;
        border: 1px solid #ffffff;
        border-radius: 0px !important; /* Sharp edges */
        text-transform: uppercase;
        padding: 10px 20px;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #ffffff;
    }

    /* 5. INPUTS */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: #111111;
        color: #ffffff;
        border: 1px solid #333;
        border-radius: 0px;
        font-family: 'Courier New', monospace;
    }

    /* 6. CONTAINERS */
    .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }
    
    /* Remove default streamlit branding if possible/desired visually */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
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
        {"title": "UNTITLED_SEQ_01", "url": "https://soundcloud.com/example/seq01", "platform": "SoundCloud"},
        {"title": "MODULAR EXCURSION A", "url": "https://bandcamp.com", "platform": "Bandcamp"},
        {"title": "LIVE AT TRESOR (EXCERPT)", "url": "https://youtube.com", "platform": "YouTube"},
    ]

if 'gallery' not in st.session_state:
    # Generic images will be forced B&W by CSS
    st.session_state.gallery = [
        {"caption": "HARDWARE SETUP 2024", "url": "https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?auto=format&fit=crop&q=80&w=800"},
        {"caption": "BERLIN", "url": "https://images.unsplash.com/photo-1558584673-c834fb1cc3ca?auto=format&fit=crop&q=80&w=800"},
        {"caption": "LIVE IMPROVISATION", "url": "https://images.unsplash.com/photo-1514525253440-b393452e8d26?auto=format&fit=crop&q=80&w=800"},
    ]

if 'bookings' not in st.session_state:
    st.session_state.bookings = []

# -----------------------------------------------------------------------------
# 3. NAVIGATION
# -----------------------------------------------------------------------------
# Styling option_menu to be high contrast (White text on Black)
selected = option_menu(
    menu_title=None,
    options=["HOME", "MUSIC", "LABEL", "VISUALS", "CONTACT", "ADMIN"],
    icons=["circle-fill", "circle", "circle", "circle", "circle", "square"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#000000", "border-bottom": "1px solid #333"},
        "icon": {"color": "#666", "font-size": "12px"}, 
        "nav-link": {
            "font-size": "14px", 
            "text-align": "center", 
            "margin": "0px", 
            "color": "#e0e0e0", 
            "font-family": "Courier New",
            "text-transform": "uppercase"
        },
        "nav-link-selected": {
            "background-color": "#000000", 
            "color": "#ffffff", 
            "font-weight": "bold",
            "border-bottom": "2px solid #ffffff"
        },
    }
)

# -----------------------------------------------------------------------------
# 4. PAGE LOGIC
# -----------------------------------------------------------------------------

# --- HOME / BIO ---
if selected == "HOME":
    st.markdown("## TUESDAYNIGHTFREAK")
    st.caption("LIVE ELECTRONIC // MELBOURNE -- BERLIN")
    
    st.write("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ### BIOGRAPHY
        
        Operating on the fringes of Melbourne’s electronic underground, **Tuesdaynightfreak** rejects the polished predictability of modern club music. 
        
        Rooted in the tradition of live hardware improvisation, the project explores the tension between mechanical precision and human error. There are no pre-recorded sets here. Using a complex architecture of drum machines, modular synthesis, and feedback loops, Tuesdaynightfreak constructs soundscapes in real-time.
        
        The sound is raw, reductive, and texture-heavy—blending the hypnotic repetition of Berlin techno with the dust and grit of lo-fi house. It is music for dark rooms and loud systems.
        """)
        
        st.write("")
        st.markdown("##### UPCOMING DATES")
        st.code("NO PUBLIC DATES SCHEDULED.\nSTUDIO MODE ACTIVE.")

    with col2:
        # Image will be rendered B&W by CSS
        st.image("https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&q=80&w=800", 
                 caption="LIVE PERFORMANCE // 2024", use_column_width=True)

    # Minimal Text Links for Socials
    st.write("---")
    cols = st.columns(6)
    cols[0].markdown("[INSTAGRAM](https://instagram.com)")
    cols[1].markdown("[SOUNDCLOUD](https://soundcloud.com)")
    cols[2].markdown("[SPOTIFY](https://spotify.com)")
    cols[3].markdown("[RESIDENT ADVISOR](https://ra.co)")

# --- MUSIC ---
elif selected == "MUSIC":
    st.markdown("### DISCOGRAPHY")
    st.write("Explorations in rhythm and noise.")
    
    st.write("---")
    
    # Text-based list layout (Brutalist style)
    for song in st.session_state.songs:
        col1, col2, col3 = st.columns([4, 2, 2])
        with col1:
            st.markdown(f"**{song['title']}**")
        with col2:
            st.caption(f"[{song['platform']}]")
        with col3:
            st.markdown(f"[LISTEN]({song['url']})")
        st.markdown("<hr style='margin: 5px 0; border-top: 1px dashed #333;'>", unsafe_allow_html=True)

# --- LABEL ---
elif selected == "LABEL":
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("## HOUSE KEEPING RECORDS")
        st.markdown("**EST. 2023**")
        st.write("---")
        st.markdown("""
        House Keeping Records exists to document the output of the local hardware community. 
        
        We are not interested in trends. We focus on the functional, the raw, and the deep. 
        Vinyl only releases for select projects. Digital archives available via Bandcamp.
        
        **DEMO POLICY**
        We listen. Send private streams only.
        """)
        st.code("demo@housekeeping.com")
    
    with col2:
        # A placeholder image that looks like a white label vinyl or studio gear
        st.image("https://images.unsplash.com/photo-1605218427306-022648d42d32?auto=format&fit=crop&q=80&w=800", caption="HKR CATALOGUE", use_column_width=True)

    st.write("---")
    st.markdown("### RECENT OUTPUT")
    st.text("HKR001 // TUESDAYNIGHTFREAK // STATIC INTERFERENCE EP")
    st.text("HKR002 // VARIOUS ARTISTS // TOOLS FOR DJs VOL. 1")

# --- VISUALS ---
elif selected == "VISUALS":
    st.markdown("### VISUAL ARCHIVE")
    
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
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### BOOKING")
        st.write("Representation: Independent.")
        st.write("Region: Worldwide.")
        st.write("")
        st.code("tuesdaynightfreak@gmail.com")
        st.write("")
        st.markdown("""
        **REQUIREMENTS**
        * 2x meters table space
        * 2x stereo DI boxes
        * Quality monitoring system
        """)

    with col2:
        st.markdown("### INQUIRY")
        with st.form("booking_form"):
            st.markdown("**DATE / VENUE / OFFER**")
            name = st.text_input("PROMOTER", placeholder="Name or Organization")
            email = st.text_input("EMAIL", placeholder="contact@domain.com")
            details = st.text_area("DETAILS", placeholder="Include date, venue, and fee offer.")
            
            # Custom styled button via CSS above
            submitted = st.form_submit_button("TRANSMIT")
            
            if submitted:
                if name and email:
                    new_booking = {
                        "name": name, 
                        "email": email, 
                        "details": details,
                        "timestamp": str(datetime.now())
                    }
                    st.session_state.bookings.append(new_booking)
                    st.success("TRANSMISSION RECEIVED.")
                else:
                    st.error("MISSING DATA.")

# --- ADMIN ---
elif selected == "ADMIN":
    st.markdown("### SYSTEM ACCESS")
    
    password = st.text_input("PASSWORD", type="password")
    
    if password == "admin123":
        st.success("AUTHENTICATED")
        
        tab1, tab2, tab3 = st.tabs(["AUDIO", "VISUAL", "DATA"])
        
        with tab1:
            st.markdown("**ADD NEW AUDIO SOURCE**")
            with st.form("add_song"):
                new_title = st.text_input("TITLE")
                new_url = st.text_input("URL")
                new_platform = st.selectbox("PLATFORM", ["SoundCloud", "Bandcamp", "Spotify", "YouTube"])
                if st.form_submit_button("UPLOAD"):
                    st.session_state.songs.append({"title": new_title, "url": new_url, "platform": new_platform})
                    st.rerun()
            
            if st.button("CLEAR ALL SONGS"):
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
