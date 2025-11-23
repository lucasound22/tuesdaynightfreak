import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime, time
import random

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & CUSTOM CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Tuesdaynightfreak | Live Electronic",
    page_icon="🎹",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for that "Dark Techno" Aesthetic
st.markdown("""
<style>
    /* Main Background & Text */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #00ffcc !important; /* Neon Cyan */
        font-family: 'Helvetica Neue', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Buttons */
    .stButton>button {
        color: #0e1117;
        background-color: #00ffcc;
        border-radius: 20px;
        border: none;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #ff00ff; /* Neon Pink on hover */
        color: white;
        transform: scale(1.05);
    }

    /* Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #262730;
        color: white;
        border-radius: 10px;
    }

    /* Custom classes for layout */
    .highlight {
        color: #ff00ff;
        font-weight: bold;
    }
    
    .album-card {
        background-color: #1f1f1f;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #333;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. SESSION STATE (Simulated Database)
# -----------------------------------------------------------------------------
# In a real app, you would use SQLite, Firestore, or a JSON file for persistence.
# For this demo, we use session_state so the Admin panel updates the UI immediately.

if 'songs' not in st.session_state:
    st.session_state.songs = [
        {"title": "Midnight In Melbourne", "url": "https://soundcloud.com/example/midnight", "platform": "SoundCloud"},
        {"title": "Deep Groove Theory", "url": "https://open.spotify.com/track/example", "platform": "Spotify"},
        {"title": "Techno Slap (Live Edit)", "url": "https://youtube.com/watch?v=example", "platform": "YouTube"},
    ]

if 'gallery' not in st.session_state:
    # Using placeholder images for the demo
    st.session_state.gallery = [
        {"caption": "Live at The Warehouse", "url": "https://images.unsplash.com/photo-1571266028243-371695063ad6?auto=format&fit=crop&q=80&w=600"},
        {"caption": "Studio Session", "url": "https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?auto=format&fit=crop&q=80&w=600"},
        {"caption": "Modular Synthesis", "url": "https://images.unsplash.com/photo-1558584673-c834fb1cc3ca?auto=format&fit=crop&q=80&w=600"},
        {"caption": "Crowd Energy", "url": "https://images.unsplash.com/photo-1493225255756-d9584f8606e9?auto=format&fit=crop&q=80&w=600"},
    ]

if 'bookings' not in st.session_state:
    st.session_state.bookings = []

# -----------------------------------------------------------------------------
# 3. NAVIGATION
# -----------------------------------------------------------------------------
selected = option_menu(
    menu_title=None,
    options=["Home", "Music", "House Keeping Records", "Media", "Bookings", "Admin"],
    icons=["house", "music-note-beamed", "vinyl", "images", "calendar-event", "gear"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#0e1117"},
        "icon": {"color": "orange", "font-size": "18px"}, 
        "nav-link": {"font-size": "14px", "text-align": "center", "margin": "0px", "--hover-color": "#262730"},
        "nav-link-selected": {"background-color": "#00ffcc", "color": "black"},
    }
)

# -----------------------------------------------------------------------------
# 4. PAGE LOGIC
# -----------------------------------------------------------------------------

# --- HOME / BIO ---
if selected == "Home":
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("# TUESDAYNIGHTFREAK")
        st.markdown("### MELBOURNE // LIVE ELECTRONIC // PRODUCER")
        st.write("---")
        st.markdown("""
        **Tuesdaynightfreak** is a Melbourne-based electronic music force, bridging the gap between 
        the raw, unpredictable energy of live hardware performance and the surgical precision of studio production.
        
        Born from the underground warehouse scene, the sound is unmistakable: **Funky Techno grooves that slap**, 
        layered with soulful, underground Deep House influences. 
        
        Unlike the push-play DJs, Tuesdaynightfreak constructs the vibe in real-time, using drum machines, 
        modular synths, and FX loops to create a unique sonic journey every single night.
        """)
        
        st.write("---")
        st.markdown("##### 📅 UPCOMING GIGS")
        st.info("No public dates confirmed for next month. Check back soon.")

    with col2:
        # Hero Image (Simulated)
        st.image("https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&q=80&w=800", 
                 caption="Tuesdaynightfreak Live", use_column_width=True)

    # Socials Bar
    st.write("---")
    c1, c2, c3, c4 = st.columns(4)
    c1.link_button("Instagram", "https://instagram.com")
    c2.link_button("SoundCloud", "https://soundcloud.com")
    c3.link_button("Spotify", "https://spotify.com")
    c4.link_button("Resident Advisor", "https://ra.co")

# --- MUSIC ---
elif selected == "Music":
    st.title("The Sound")
    st.write("Latest releases, live sets, and underground edits.")
    
    # Featured Track (Mock Embedded Player)
    st.markdown("""
    <div style="background-color:#1E1E1E; padding:20px; border-radius:10px; border-left: 5px solid #00ffcc;">
        <h3>🔥 LATEST RELEASE: "Concrete Jungle"</h3>
        <p>Out now on House Keeping Records.</p>
    </div>
    """, unsafe_allow_html=True)
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3") # Placeholder Audio
    
    st.write("---")
    st.subheader("Discography & Links")
    
    # Display links from Session State
    for song in st.session_state.songs:
        with st.container():
            c1, c2 = st.columns([3, 1])
            c1.markdown(f"**{song['title']}**")
            c2.link_button(f"Listen on {song['platform']}", song['url'])
            st.write("")

# --- HOUSE KEEPING RECORDS ---
elif selected == "House Keeping Records":
    st.markdown("<h1 style='text-align: center; color: #ff00ff !important;'>HOUSE KEEPING RECORDS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>THE HOME OF UNDERGROUND GROOVES</p>", unsafe_allow_html=True)
    
    st.image("https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?auto=format&fit=crop&q=80&w=1200", caption="House Keeping HQ", use_column_width=True)
    
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### ABOUT THE LABEL
        House Keeping Records was established to provide a platform for the gritty, 
        lo-fi, and funk-infused side of techno. We don't do polished pop; 
        we do dusty drums and acid basslines.
        
        **Demo Policy:** We are currently accepting demos. 
        Please send private SoundCloud links to demo@housekeeping.com
        """)
    
    with col2:
        st.markdown("### LATEST CATALOGUE")
        st.info("HKR001 - Tuesdaynightfreak - The Beginning EP")
        st.info("HKR002 - Unknown Artist - White Label Vol 1")
        st.info("HKR003 - Tuesdaynightfreak - Acid Rain")

# --- MEDIA ---
elif selected == "Media":
    st.title("Visuals")
    st.write("Live moments and press shots.")
    
    # Responsive Grid Layout
    cols = st.columns(3) # Grid of 3
    
    # Iterate through gallery and place in columns
    for i, item in enumerate(st.session_state.gallery):
        col_idx = i % 3
        with cols[col_idx]:
            st.image(item['url'], caption=item['caption'], use_column_width=True)

# --- BOOKINGS ---
elif selected == "Bookings":
    st.title("Bookings")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ### GET IN TOUCH
        Tuesdaynightfreak is available for:
        * Live Club Sets (1-2 Hours)
        * Festival Slots
        * Remix Work
        
        **Management / Direct:** 📧 tuesdaynightfreak@gmail.com
        """)
        
        st.warning("Currently accepting bookings for Summer 2025.")

    with col2:
        st.markdown("### INQUIRY FORM")
        with st.form("booking_form"):
            name = st.text_input("Promoter / Venue Name")
            email = st.text_input("Contact Email")
            date = st.date_input("Proposed Date", min_value=datetime.today())
            offer_type = st.selectbox("Type", ["Club Night", "Festival", "Private Event", "Remix Request"])
            details = st.text_area("Event Details / Offer")
            
            submitted = st.form_submit_button("SEND INQUIRY")
            
            if submitted:
                if name and email and details:
                    # Logic to save mock booking and clear form (simulated email)
                    new_booking = {
                        "name": name, 
                        "email": email, 
                        "date": str(date), 
                        "details": details,
                        "timestamp": str(datetime.now())
                    }
                    st.session_state.bookings.append(new_booking)
                    st.success(f"Thanks {name}! Your inquiry for {date} has been sent to tuesdaynightfreak@gmail.com. We will be in touch shortly.")
                    st.balloons()
                else:
                    st.error("Please fill in all required fields.")

# --- ADMIN ---
elif selected == "Admin":
    st.title("Backstage Area")
    st.markdown("Please verify your identity to manage content.")
    
    password = st.text_input("Enter Password", type="password")
    
    if password == "admin123": # Simple hardcoded auth for demo
        st.success("Access Granted")
        
        tab1, tab2, tab3 = st.tabs(["Add Music", "Add Photos", "View Bookings"])
        
        # TAB 1: ADD MUSIC
        with tab1:
            st.subheader("Upload New Link")
            with st.form("add_song"):
                new_title = st.text_input("Song Title")
                new_url = st.text_input("URL (Spotify/SC/Mixcloud)")
                new_platform = st.selectbox("Platform", ["SoundCloud", "Spotify", "YouTube", "Mixcloud", "Bandcamp"])
                submit_song = st.form_submit_button("Add Song")
                
                if submit_song and new_title and new_url:
                    st.session_state.songs.append({"title": new_title, "url": new_url, "platform": new_platform})
                    st.success(f"Added {new_title}!")
            
            st.write("### Current Links")
            st.dataframe(pd.DataFrame(st.session_state.songs))

        # TAB 2: ADD PHOTOS
        with tab2:
            st.subheader("Add Gallery Image")
            st.info("Paste a direct image URL (e.g., from Unsplash or hosted file)")
            with st.form("add_photo"):
                new_caption = st.text_input("Caption")
                new_img_url = st.text_input("Image URL")
                submit_photo = st.form_submit_button("Add Photo")
                
                if submit_photo and new_img_url:
                    st.session_state.gallery.append({"caption": new_caption, "url": new_img_url})
                    st.success("Image added to gallery!")
            
            st.write("### Current Images")
            st.write(st.session_state.gallery)

        # TAB 3: VIEW BOOKINGS
        with tab3:
            st.subheader("Incoming Inquiries")
            if len(st.session_state.bookings) > 0:
                df = pd.DataFrame(st.session_state.bookings)
                st.dataframe(df)
            else:
                st.info("No new bookings yet.")
                
    elif password:
        st.error("Incorrect Password")