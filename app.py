import random
import time

# --- CONFIGURATION & PALETTE ---
CP_YELLOW = "#fcee0a"
CP_CYAN = "#00f0ff"
CP_RED = "#ff003c"
CP_BLACK = "#050a0e"
TT_CREAM = "#f2f2f2" # Used for contrast borders
# --- CONFIGURATION & PALETTE (Defected-Inspired "Premium Underground") ---
# Palette: Deep Black background, Stark White text, Acid Red Accents
COLOR_BG = "#080808"
COLOR_TEXT = "#F0F0F0" 
COLOR_ACCENT = "#FF0033" # Acid Red for that premium label feel
COLOR_SECONDARY = "#1A1A1A" # Dark Grey for cards

# --- BRANDING: CUSTOM SVG LOGO (Toy Tonics Stamp Style x Cyberpunk) ---
TNF_STAMP_LOGO = f"""
<svg width="60" height="60" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="50" cy="50" r="45" stroke="{CP_YELLOW}" stroke-width="5" fill="{CP_BLACK}"/>
<path d="M20 50 L40 50 L40 80" stroke="{CP_CYAN}" stroke-width="8"/> 
<path d="M50 80 L50 20 L80 80 L80 20" stroke="{CP_RED}" stroke-width="6"/>
<text x="50%" y="50%" text-anchor="middle" stroke="{CP_YELLOW}" stroke-width="1px" dy=".3em" font-family="monospace" font-weight="bold" font-size="20">TNF</text>
# --- BRANDING: CLEAN TYPOGRAPHIC LOGO ---
TNF_LOGO_SVG = f"""
<svg width="120" height="40" viewBox="0 0 120 40" fill="none" xmlns="http://www.w3.org/2000/svg">
<text x="0" y="30" font-family="Helvetica, Arial, sans-serif" font-weight="900" font-size="32" fill="{COLOR_TEXT}" letter-spacing="-2">TNF</text>
<circle cx="80" cy="20" r="8" fill="{COLOR_ACCENT}"/>
<rect x="95" y="12" width="25" height="16" fill="{COLOR_TEXT}"/>
</svg>
"""

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="TUESDAYNIGHTFREAK | CULTURE CREW",
    page_icon="🎹",
    page_title="TUESDAYNIGHTFREAK | OFFICIAL",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# 2. CUSTOM CSS (The Mashup Design)
# 2. CUSTOM CSS (Professional, Clean, Editorial)
# -----------------------------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow:wght@400;700;900&family=Tomorrow:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&display=swap');

    /* GLOBAL RESET */
    .stApp {{
        background-color: {CP_BLACK};
        color: {TT_CREAM};
        font-family: 'Barlow', sans-serif;
        background-color: {COLOR_BG};
        color: {COLOR_TEXT};
        font-family: 'Inter', sans-serif;
    }}

    /* REMOVE DEFAULT UI */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .block-container {{ padding-top: 1rem !important; max-width: 1200px; }}
    .block-container {{ padding-top: 2rem !important; max-width: 1400px; }}

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
    /* "Defected" Style Headlines: Bold, Uppercase, Tight Spacing */
    h1, h2, h3 {{
        font-family: 'Barlow', sans-serif;
        font-family: 'Inter', sans-serif;
        text-transform: uppercase;
        font-weight: 900;
        color: {CP_RED};
        border-bottom: 3px solid {CP_YELLOW}; /* Graphic underline */
        display: inline-block;
        padding-bottom: 5px;
        margin-top: 30px !important;
        color: {COLOR_TEXT};
        letter-spacing: -1px;
        margin-bottom: 0.5rem;
    }}
    
    h4, h5, h6 {{
        color: {CP_CYAN} !important;
        font-family: 'Tomorrow', sans-serif;
    h4, h5 {{
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: {COLOR_ACCENT} !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        letter-spacing: 1px;
        font-size: 0.9rem;
    }}

    /* --- UI ELEMENTS --- */
    
    /* Cyberpunk Buttons */
    /* Premium Buttons */
    .stButton>button {{
        background-color: {CP_YELLOW};
        color: {CP_BLACK};
        background-color: {COLOR_TEXT};
        color: {COLOR_BG};
        border: none;
        font-family: 'Tomorrow', sans-serif;
        font-weight: bold;
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        text-transform: uppercase;
        clip-path: polygon(10% 0, 100% 0, 100% 70%, 90% 100%, 0 100%, 0 30%); /* Angled cut */
        padding: 15px 30px;
        transition: all 0.2s;
        padding: 12px 28px;
        border-radius: 0px; /* Square edges for that brutalist/label feel */
        transition: all 0.3s;
    }}
    .stButton>button:hover {{
        background-color: {CP_CYAN};
        color: {CP_BLACK};
        transform: translate(-2px, -2px);
        box-shadow: 4px 4px 0px {CP_RED};
        background-color: {COLOR_ACCENT};
        color: {COLOR_TEXT};
        transform: scale(1.02);
    }}

    /* Graphic Boxes (Toy Tonics Style Borders) */
    .graphic-box {{
        border: 2px solid {TT_CREAM};
    /* Cards / Containers */
    .news-card {{
        background-color: {COLOR_SECONDARY};
        padding: 20px;
        background: #111;
        border-left: 4px solid {COLOR_ACCENT};
        margin-bottom: 20px;
        transition: transform 0.3s;
    }}
    .news-card:hover {{
        transform: translateX(5px);
    }}

    /* Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {{
        background-color: #1a1a1a;
        color: {CP_YELLOW};
        border: 2px solid {CP_CYAN};
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
        background-color: {COLOR_SECONDARY};
        color: {COLOR_TEXT};
        border: 1px solid #333;
        border-radius: 0;
        font-family: 'Tomorrow', sans-serif;
    }}
    .stTextInput>div>div>input:focus {{
        border-color: {COLOR_ACCENT};
    }}

    /* Links */
    a {{ color: {CP_YELLOW} !important; text-decoration: none; font-weight: bold; }}
    a:hover {{ background-color: {CP_YELLOW}; color: {CP_BLACK} !important; }}
    a {{ color: {COLOR_TEXT} !important; text-decoration: none; font-weight: 600; }}
    a:hover {{ color: {COLOR_ACCENT} !important; text-decoration: underline; }}
    
    hr {{ border-color: #333; margin: 3rem 0; }}

</style>
""", unsafe_allow_html=True)
@@ -137,40 +129,41 @@
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

# NEW IMAGES: Modular, Tech, Crowd (No Guitars/DJs)
if 'gallery' not in st.session_state:
    st.session_state.gallery = [
        {"caption": "WAREHOUSE RAVE // BERLIN", "url": "https://images.unsplash.com/photo-1574169208507-84376144848b?q=80&w=800&auto=format&fit=crop"},
        {"caption": "MODULAR SYSTEM // LIVE RIG", "url": "https://images.unsplash.com/photo-1550291652-6ea9114a47b1?q=80&w=800&auto=format&fit=crop"},
        {"caption": "CROWD ENERGY // 3AM", "url": "https://images.unsplash.com/photo-1571266028243-371695063ad6?q=80&w=800&auto=format&fit=crop"},
        {"caption": "ANALOG OSCILLATORS", "url": "https://images.unsplash.com/photo-1621360841012-2357d27e02a4?q=80&w=800&auto=format&fit=crop"}
        {"caption": "MODULAR RIG SETUP A", "url": "https://images.unsplash.com/photo-1550291652-6ea9114a47b1?q=80&w=800&auto=format&fit=crop"},
        {"caption": "LIVE SIGNAL PATH", "url": "https://images.unsplash.com/photo-1598275529124-b1c4b786f1e2?q=80&w=800&auto=format&fit=crop"},
        {"caption": "WAREHOUSE CROWD", "url": "https://images.unsplash.com/photo-1571266028243-371695063ad6?q=80&w=800&auto=format&fit=crop"},
        {"caption": "OSCILLATOR DETAIL", "url": "https://images.unsplash.com/photo-1619967657960-983b6329c370?q=80&w=800&auto=format&fit=crop"}
    ]

if 'bookings' not in st.session_state:
    st.session_state.bookings = []

# -----------------------------------------------------------------------------
# 4. NAVIGATION (Toy Tonics Style - Simple Top Bar)
# 4. NAVIGATION (Clean, Top-Bar)
# -----------------------------------------------------------------------------
selected = option_menu(
    menu_title=None,
    options=["HOME", "MUSIC", "LABEL", "MEDIA", "CONTACT", "SYSTEM"],
    icons=["house", "disc", "vinyl", "camera-reels", "envelope", "cpu"], 
    options=["HOME", "MUSIC", "EVENTS", "STORE", "ABOUT"],
    icons=["house-fill", "disc-fill", "calendar-event-fill", "bag-fill", "info-circle-fill"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": CP_BLACK, "border-bottom": f"1px solid {CP_CYAN}"},
        "icon": {"color": CP_YELLOW, "font-size": "14px"}, 
        "container": {"padding": "0!important", "background-color": COLOR_BG, "border-bottom": "1px solid #333"},
        "icon": {"color": "#666", "font-size": "12px"}, 
        "nav-link": {
            "font-size": "14px", "text-align": "center", "margin": "0px", 
            "color": TT_CREAM, "font-family": "Tomorrow, sans-serif", "text-transform": "uppercase"
            "color": "#888", "font-family": "Inter, sans-serif", "text-transform": "uppercase", "font-weight": "600"
        },
        "nav-link-selected": {"background-color": "#1a1a1a", "color": CP_CYAN, "border-top": f"3px solid {CP_RED}"},
        "nav-link-selected": {"background-color": COLOR_BG, "color": COLOR_TEXT, "border-bottom": f"2px solid {COLOR_ACCENT}"},
    }
)

@@ -180,182 +173,162 @@

# --- HOME PAGE ---
if selected == "HOME":
    # HERO SECTION
    col1, col2 = st.columns([1.5, 1])
    # HERO SECTION: Big Image, Bold Text
    # Replacing DJ image with Modular/Abstract Tech image
    st.image("https://images.unsplash.com/photo-1517457375825-e578c799a74f?q=80&w=1400&auto=format&fit=crop", use_column_width=True)
    
    col1, col2 = st.columns([2, 1])

    with col1:
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
        # LATEST NEWS / UPDATES (Defected Style "News Feed")
        st.markdown("#### LATEST NEWS")

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
        <div class="news-card">
        <strong>NEW EP ANNOUNCED</strong><br>
        <span style="font-size:0.8rem; color:#888;">OCT 24, 2025</span><br>
        'Voltage Control' drops worldwide next Friday on House Keeping Records.
        </div>
        """, unsafe_allow_html=True)

        # Interactive Element: Status
        st.markdown(f"**CURRENT SYSTEM STATUS:** <span style='color:{CP_YELLOW}; font-family:monospace; animation: blink 1s infinite;'>ONLINE // STUDIO MODE</span>", unsafe_allow_html=True)

    with col2:
        # New Techno Image
        st.image("https://images.unsplash.com/photo-1594623930572-300a3011d9ae?q=80&w=800&auto=format&fit=crop", caption="LIVE AT TRESOR // 2024")
        st.markdown(f"""
        <div class="news-card">
        <strong>EUROPEAN TOUR DATES</strong><br>
        <span style="font-size:0.8rem; color:#888;">OCT 10, 2025</span><br>
        We are hitting the road this winter. Check the Events page for details.
        </div>
        """, unsafe_allow_html=True)

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
    # FEATURED VIDEO (YouTube Embed Style)
    st.markdown("### LIVE SESSIONS")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### UNTITLED_SEQ_04")
        st.image("https://images.unsplash.com/photo-1493225255756-d9584f8606e9?q=80&w=800&auto=format&fit=crop", caption="Live Recording")
        st.markdown(f"[STREAM ON SOUNDCLOUD]({ '#'})")

        st.image("https://images.unsplash.com/photo-1510915364890-a7d41f02c611?q=80&w=800&auto=format&fit=crop", caption="LIVE FROM THE WAREHOUSE")
    with col2:
        st.markdown(f"#### ACID RAIN (DUB)")
        st.image("https://images.unsplash.com/photo-1514525253440-b393452e8d26?q=80&w=800&auto=format&fit=crop", caption="Studio Cut")
        st.markdown(f"[BUY ON BANDCAMP]({ '#'})")
        st.markdown("""
        **SESSION 001: MODULAR IMPROV**
        
    st.write("---")
    st.markdown("### DISCOGRAPHY LIST")
    for song in st.session_state.songs:
        st.markdown(f"**{song['title']}** // {song['platform']}")
        Recorded live in one take. A journey through deep textures and driving rhythms.
        Hardware used: Eurorack system (Make Noise, Intellijel), TR-909.
        """)
        st.button("WATCH FULL SET")

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
# --- MUSIC ---
elif selected == "MUSIC":
    st.markdown("## DISCOGRAPHY")
    
    # Clean List View (Label Style)
    for track in st.session_state.songs:
        c1, c2, c3, c4 = st.columns([1, 4, 2, 2])
        with c1:
            # Small thumbnail placeholder
            st.markdown(f"<div style='width:50px; height:50px; background-color:{COLOR_ACCENT};'></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"**{track['title']}**")
        with c3:
            st.caption(track['label'])
        with c4:
            st.button("STREAM", key=track['title'])
        st.markdown(f"<hr style='margin: 10px 0; border-color: #222;'>", unsafe_allow_html=True)

    with col2:
        st.image("https://images.unsplash.com/photo-1603048588665-791ca8aea617?q=80&w=800&auto=format&fit=crop", caption="HKR HEADQUARTERS")
        
        # Physical Stockists List
        st.markdown("#### STOCKISTS")
        st.markdown(f"""
        * <span style="color:{CP_CYAN}">HARDWAX</span> [BERLIN]
        * <span style="color:{CP_CYAN}">PHONICA</span> [LONDON]
        * <span style="color:{CP_CYAN}">RUSH HOUR</span> [AMSTERDAM]
        """, unsafe_allow_html=True)
    st.markdown("### HOUSE KEEPING RECORDS")
    st.image("https://images.unsplash.com/photo-1605218427306-022648d42d32?q=80&w=1200&auto=format&fit=crop", caption="HKR HQ")
    st.write("Our home for the raw and the deep. Establishing a new standard for vinyl releases.")

# --- MEDIA ---
elif selected == "MEDIA":
    st.markdown("## VISUAL FEED")
# --- EVENTS ---
elif selected == "EVENTS":
    st.markdown("## UPCOMING DATES")

    # Masonry-style grid (Toy Tonics often has eclectic layouts)
    c1, c2 = st.columns(2)
    for i, item in enumerate(st.session_state.gallery):
        if i % 2 == 0:
            with c1:
                st.image(item["url"], caption=item["caption"])
        else:
            with c2:
                st.image(item["url"], caption=item["caption"])
    # Event List Table Style
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
                st.markdown(f"<span style='color:#666;'>SOLD OUT</span>", unsafe_allow_html=True)
            else:
                st.button(f"BUY {event['status']}", key=event['city'])
        st.markdown(f"<hr style='margin: 10px 0; border-color: #222;'>", unsafe_allow_html=True)

# --- CONTACT ---
elif selected == "CONTACT":
    c1, c2 = st.columns(2)
# --- STORE ---
elif selected == "STORE":
    st.markdown("## SHOP MERCH & VINYL")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("## BOOKING & PRESS")
        st.markdown("### WORLDWIDE")
        st.write("Direct Management")
        st.markdown(f"<h2 style='border:none; color:{CP_YELLOW};'>tuesdaynightfreak@gmail.com</h2>", unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1585227803927-2c24067b9416?q=80&w=600&auto=format&fit=crop", caption="HKR004 - VINYL 12\"")
        st.markdown("**SYSTEM FAILURE EP**")
        st.caption("€14.00")
        st.button("ADD TO CART", key="p1")

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
        st.image("https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?q=80&w=600&auto=format&fit=crop", caption="TNF LOGO TEE")
        st.markdown("**OFFICIAL T-SHIRT**")
        st.caption("€35.00")
        st.button("ADD TO CART", key="p2")
        
    with c3:
        st.image("https://images.unsplash.com/photo-1529339077446-df732dfa062c?q=80&w=600&auto=format&fit=crop", caption="PATCH CABLE SET")
        st.markdown("**TNF CABLE PACK**")
        st.caption("€20.00")
        st.button("ADD TO CART", key="p3")

# --- SYSTEM (ADMIN) ---
elif selected == "SYSTEM":
    st.markdown("## SYSTEM ACCESS")
    st.caption("SECURE AREA. AUTHORIZED PERSONNEL ONLY.")
    
    pwd = st.text_input("ENTER AUTH CODE", type="password")
# --- ABOUT / CONTACT ---
elif selected == "ABOUT":
    col1, col2 = st.columns([1, 1], gap="large")

    if pwd == "admin123":
        st.success("ACCESS GRANTED. WELCOME, OPERATOR.")
    with col1:
        st.markdown("## THE PROJECT")
        st.markdown("""
        **Tuesdaynightfreak** is a dedicated exploration of electronic sound. 
        Founded in Melbourne, the project focuses on the visceral experience of 
        live hardware performance.
        
        # --- ADMIN TABS FOR UPLOADING CONTENT ---
        tab1, tab2, tab3 = st.tabs(["UPLOAD MUSIC", "UPLOAD VISUALS", "INCOMING DATA"])
        We believe in the power of the machine and the human error that brings it to life.
        Our sets are improvised, raw, and unique to every venue.
        """)

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
        st.markdown("#### CONTACT MANAGEMENT")
        st.code("mgmt@tuesdaynightfreak.com")
        
        st.markdown("#### DEMOS")
        st.code("demos@housekeeping-rec.com")

        with tab3:
            st.markdown("### INCOMING TRANSMISSIONS")
            if len(st.session_state.bookings) > 0:
                st.dataframe(pd.DataFrame(st.session_state.bookings))
            else:
                st.info("NO NEW MESSAGES.")
    with col2:
        st.markdown("## NEWSLETTER")
        st.write("Join our community for early access to vinyl drops and guestlist spots.")
        with st.form("newsletter"):
            st.text_input("EMAIL ADDRESS")
            st.form_submit_button("SUBSCRIBE")
            
        st.write("---")
        st.markdown("#### PRESS KIT")
        st.button("DOWNLOAD EPK (ZIP)")
