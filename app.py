import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import time

# --- CONFIGURATION & PALETTE ---
COLOR_BG = "#080808"
COLOR_TEXT = "#F0F0F0"
COLOR_ACCENT = "#FF0033"  # Acid Red (Primary Highlight)
COLOR_CYAN = "#00f7ff"    # Cyberpunk Splash (Secondary Highlight)
COLOR_SECONDARY = "#141414"

# --- BRANDING SVGs (BIGGER & CLEANER) ---
# TNF Logo - Glitch/Cyberpunk Style
TNF_LOGO_SVG = f"""
<svg width="400" height="110" viewBox="0 0 400 110" xmlns="http://www.w3.org/2000/svg">
    <text x="6" y="85" font-family="Arial, sans-serif" font-weight="900" font-size="96" fill="{COLOR_CYAN}" opacity="0.6" letter-spacing="-6">TNF</text>
    <text x="-3" y="85" font-family="Arial, sans-serif" font-weight="900" font-size="96" fill="{COLOR_ACCENT}" opacity="0.7" letter-spacing="-6">TNF</text>
    <text x="0" y="85" font-family="Arial, sans-serif" font-weight="900" font-size="96" fill="{COLOR_TEXT}" letter-spacing="-6">TNF</text>
    <rect x="230" y="35" width="10" height="50" fill="{COLOR_ACCENT}"/>
    <rect x="250" y="35" width="10" height="50" fill="{COLOR_CYAN}"/>
    <circle cx="290" cy="60" r="16" stroke="{COLOR_TEXT}" stroke-width="4" fill="none"/>
    <line x1="0" y1="105" x2="400" y2="105" stroke="{COLOR_CYAN}" stroke-width="3" opacity="0.8"/>
</svg>
"""

# House Keeping Records Logo - Deep House/Minimal Style
HKR_LOGO_SVG = f"""
<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
    <rect x="10" y="10" width="180" height="180" stroke="{COLOR_TEXT}" stroke-width="6" fill="none"/>
    <path d="M25 80 L100 25 L175 80" stroke="{COLOR_ACCENT}" stroke-width="6" fill="none"/>
    <circle cx="100" cy="130" r="40" stroke="{COLOR_CYAN}" stroke-width="5" fill="none"/>
    <rect x="96" y="115" width="8" height="30" fill="{COLOR_CYAN}"/>
    <text x="100" y="185" font-family="monospace" font-size="20" fill="#888" text-anchor="middle" font-weight="bold">EST. 2023</text>
</svg>
"""

# Slipmat Icon - Simple Geometric
SLIPMAT_ICON_SVG = f"""
<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <circle cx="50" cy="50" r="45" fill="#111" stroke="{COLOR_CYAN}" stroke-width="2"/>
    <circle cx="50" cy="50" r="15" fill="{COLOR_ACCENT}"/>
    <circle cx="50" cy="50" r="2" fill="#fff"/>
</svg>
"""

# --- HELPER FUNCTION FOR ADDING TO CART ---
def add_to_cart(item_name):
    """Adds an item to the cart."""
    st.session_state.cart.append(item_name)
    st.toast(f"🛒 Added {item_name} to cart!", icon="✅")

# --- PAGE SETUP ---
st.set_page_config(
    page_title="TUESDAYNIGHTFREAK | OFFICIAL",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- SESSION STATE INIT ---
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'page_index' not in st.session_state:
    st.session_state.page_index = 0
if 'bookings' not in st.session_state:
    st.session_state.bookings = []

# Gallery/Visual Archive - Updated with relevant, non-guitar images and a video
if 'gallery' not in st.session_state:
    st.session_state.gallery = [
        {"type": "image", "caption": "LIVE HARDWARE RIG", "url": "https://images.unsplash.com/photo-1598275529124-b1c4b786f1e2?q=80&w=800&auto=format&fit=crop"}, 
        {"type": "video", "caption": "Live Visual Excerpt: 'Fractal Echo'", "url": "https://www.youtube.com/watch?v=1F_s8f413wQ"}, # Abstract/Geometric Visuals
        {"type": "image", "caption": "WAREHOUSE CROWD V2", "url": "https://images.unsplash.com/photo-1571266028243-371695063ad6?q=80&w=800&auto=format&fit=crop"},
        {"type": "image", "caption": "OSCILLATOR DETAIL", "url": "https://images.unsplash.com/photo-1619967657960-983b6329c370?q=80&w=800&auto=format&fit=crop"}, 
        {"type": "image", "caption": "MIXER CHANNELS", "url": "https://images.unsplash.com/photo-1550291652-6ea9114a47b1?q=80&w=800&auto=format&fit=crop"}, 
        {"type": "image", "caption": "CABLE CHAOS", "url": "https://images.unsplash.com/photo-1554181961-45a727d8ce6b?q=80&w=800&auto=format&fit=crop"},
    ]

# Songs Data - Added 'cover_url' and 'format'
if 'songs' not in st.session_state:
    st.session_state.songs = [
        {"title": "System Failure (Original Mix)", "label": "House Keeping Rec", "cat": "HKR004", "format": "DIGITAL/VINYL", "cover_url": "https://placehold.co/600x600/FF0033/000?text=SYSTEM+FAILURE"},
        {"title": "Analog Dreams", "label": "Tresor Records", "cat": "TR-291", "format": "DIGITAL", "cover_url": "https://placehold.co/600x600/00f7ff/000?text=ANALOG+DREAMS"},
        {"title": "Voltage Control", "label": "Ostgut Ton", "cat": "OSTGUT-55", "format": "VINYL", "cover_url": "https://placehold.co/600x600/080808/FFF?text=VOLTAGE+CONTROL"},
        {"title": "Modular State", "label": "Klockworks", "cat": "KW-22", "format": "DIGITAL/VINYL", "cover_url": "https://placehold.co/600x600/141414/FF0033?text=MODULAR+STATE"}
    ]

# HKR Releases Data - Added 'format'
if 'hkr_releases' not in st.session_state:
    st.session_state.hkr_releases = [
        {"title": "Rhythm Generator EP", "artist": "Various Artists", "cat": "HKR005", "format": "VINYL ONLY"},
        {"title": "Modular Loop 01", "artist": "TUESDAYNIGHTFREAK", "cat": "HKR004", "format": "VINYL ONLY"},
        {"title": "Grid Sequencer", "artist": "Acid Junkie", "cat": "HKR003", "format": "VINYL ONLY"},
    ]

# Events Data - Added ticket links and flyer placeholders
if 'events' not in st.session_state:
    st.session_state.events = [
        {"date": "NOV 04", "city": "AMSTERDAM", "venue": "SHELTER", "ticket_link": "https://ticketco.io/shelter", "flyer_url": "https://placehold.co/600x300/1a1a1a/FF0033?text=AMSTERDAM+NOV+04"},
        {"date": "NOV 11", "city": "LONDON", "venue": "FOLD", "ticket_link": "https://ra.co/events/london/fold", "flyer_url": "https://placehold.co/600x300/1a1a1a/00f7ff?text=LONDON+NOV+11"},
        {"date": "NOV 18", "city": "MELBOURNE", "venue": "REVOLVER", "ticket_link": "https://moshtix.com.au/revolver", "flyer_url": "https://placehold.co/600x300/1a1a1a/FFF?text=MELBOURNE+NOV+18"},
        {"date": "DEC 02", "city": "PARIS", "venue": "REX CLUB", "ticket_link": "https://dice.fm/rexclub", "flyer_url": "https://placehold.co/600x300/1a1a1a/FF0033?text=PARIS+DEC+02"},
    ]


# --- NAVIGATION CALLBACK ---
def set_page(index):
    st.session_state.page_index = index

# --- CUSTOM CSS ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Space+Mono:wght@400;700&display=swap');
    
    .stApp {{ 
        background-color: {COLOR_BG}; 
        color: {COLOR_TEXT}; 
        font-family: 'Inter', sans-serif; 
    }}
    
    /* 1. LAYOUT FIXES: Remove white gaps next to the menu */
    /* Target the main block container to maximize width and remove default padding */
    .st-emotion-cache-18ni5f0 {{
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }}
    /* This targets the main content wrapper's padding */
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 2rem;
        padding-right: 2rem;
    }}

    /* Navigation Menu Font Override */
    div[data-testid="stHorizontalBlock"] button {{
        font-family: 'Inter', sans-serif !important;
    }}
    
    /* 2. TEXT READABILITY: Increased white text size and fixed color contrast */
    h1, h2, h3 {{ 
        font-weight: 900; 
        text-transform: uppercase; 
        letter-spacing: -1px; 
        color: {COLOR_TEXT};
    }}
    h4, h5 {{ 
        font-family: 'Space Mono', monospace; 
        color: {COLOR_TEXT}; /* Changed from CYAN to TEXT for better readability on dark BG */
        text-transform: uppercase; 
        letter-spacing: 1px; 
        font-size: 1.1rem; 
        font-weight: 700;
    }}
    
    /* General content text size increase */
    .stMarkdown p, .stMarkdown li, .stMarkdown > div > p:not(:first-child) {{
        font-size: 1.1rem; 
        line-height: 1.7;
    }}

    /* Buttons */
    .stButton>button {{
        background: {COLOR_CYAN}; 
        color: #000; 
        border: none; 
        padding: 12px 24px; 
        font-weight: 900; 
        text-transform: uppercase;
        border-radius: 0;
        transition: 0.3s;
        width: 100%;
        font-size: 1.1rem;
    }}
    .stButton>button:hover, .stLinkButton>a {{
        background: {COLOR_ACCENT};
        color: #fff;
        box-shadow: 0 0 15px {COLOR_ACCENT};
    }}
    
    /* 3. BACKGROUND VIDEO: Geometric/Amiga Vibe (Glitchy Abstract) */
    .video-bg {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        overflow: hidden;
    }}
    .video-bg iframe {{
        width: 100vw;
        height: 56.25vw; 
        min-height: 100vh;
        min-width: 177.77vh;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        opacity: 0.4; /* Darker opacity for content contrast */
    }}
    .video-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0,0,0,0.85); /* Heavy overlay */
        z-index: -1;
    }}
    
    /* Mockup Container (Merchandise) */
    .mockup-container {{
        position: relative;
        width: 100%;
        height: 350px;
        background-color: #1a1a1a;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #333;
    }}
    .mockup-bg {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        opacity: 0.8; /* Increased opacity for better product view */
    }}
    /* 4. MERCH LOGO CENTERING FIX */
    .mockup-logo {{
        position: absolute;
        top: 40%; /* Moved up slightly to center on chest */
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 10;
        filter: drop-shadow(0 0 10px rgba(0,0,0,0.5));
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
    
    /* Latest News Card (Contrast Fix) */
    .stAlert {{
        background-color: #222 !important;
        color: {COLOR_TEXT} !important;
        border-left: 5px solid {COLOR_ACCENT} !important;
        font-size: 1.05rem;
    }}

    /* Footer Style */
    .footer-bar {{
        position: fixed; 
        bottom: 0; 
        left: 0; 
        width: 100%; 
        background: {COLOR_SECONDARY}; 
        padding: 10px; 
        text-align: center; 
        font-family: "Space Mono", monospace; 
        font-size: 0.8rem; 
        color: #888; 
        border-top: 1px solid #333;
        z-index: 100;
    }}
    
</style>
""", unsafe_allow_html=True)

# --- BACKGROUND VIDEO & AUDIO ---
# Muted, Autoplay, Loop, Controls Hidden (Geometric, Amiga 90s Demo Scene Style)
st.markdown("""
<div class="video-bg">
    <iframe src="https://www.youtube.com/embed/49bK4n449K4?controls=0&showinfo=0&rel=0&autoplay=1&loop=1&mute=1&playlist=49bK4n449K4" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
</div>
<div class="video-overlay"></div>
""", unsafe_allow_html=True)

# Non-blocking Audio Autostart (Tone.js)
st.components.v1.html("""
<script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.min.js"></script>
<script>
    document.addEventListener('click', async () => {
        if (Tone.context.state !== 'running') {
            await Tone.start();
            // Simple low-frequency kick drum loop (a common deep house element)
            const kick = new Tone.MembraneSynth({
                pitchDecay: 0.05,
                octaves: 8,
                envelope: { attack: 0.001, decay: 0.4, sustain: 0.01, release: 0.8 }
            }).toDestination();
            
            const loop = new Tone.Loop(time => {
                kick.triggerAttackRelease("C1", "8n", time);
            }, "4n").start(0);
            
            Tone.Transport.bpm.value = 125;
            Tone.Transport.start();
        }
    });
</script>
""", height=0)


# --- NAVIGATION ---
menu_options = ["HOME", "MUSIC", "HKR", "EVENTS", "STORE", "GALLERY", "ABOUT", "SYSTEM"]
selected = option_menu(
    menu_title=None,
    options=menu_options,
    icons=["house", "disc", "vinyl", "calendar3", "bag", "images", "info-circle", "cpu"],
    default_index=st.session_state.page_index,
    orientation="horizontal",
    styles={
        "container": {"padding": "0", "background-color": "rgba(0,0,0,0.8)", "border-bottom": f"1px solid {COLOR_ACCENT}"},
        "nav-link": {"font-size": "16px", "text-transform": "uppercase", "font-weight": "bold", "color": "#fff"},
        "nav-link-selected": {"background-color": "transparent", "color": COLOR_CYAN, "border-bottom": f"3px solid {COLOR_CYAN}"}
    }
)

# --- CONTENT ---

if selected == "HOME":
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(TNF_LOGO_SVG, unsafe_allow_html=True)
        # Added full name beneath the logo
        st.markdown(f"<h1 style='font-size: 2.5rem; color: {COLOR_TEXT}; margin-top: -30px;'>Tuesday Night Freak</h1>", unsafe_allow_html=True)
        st.markdown("### ARCHITECTS OF THE ANALOGUE SIGNAL")
        st.markdown("""
        <div style="font-size: 1.2rem; line-height: 1.6;">
        Tuesdaynightfreak is not just an artist; it's a **sonic movement**. 
        We are an independent electronic music project and culture crew bridging the gap between 
        Berlin's concrete basements and Melbourne's warehouse soul.
        <br><br>
        We reject the digital perfection of modern EDM. We embrace the <strong>analogue error</strong>.
        No laptops. Just voltage.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        with b1:
            st.button("LATEST RELEASE", on_click=set_page, args=(1,))
        with b2:
            st.button("VIEW TOUR DATES", on_click=set_page, args=(3,))

    with col2:
        # Changed heading to LATEST NEWS
        st.markdown("#### LATEST NEWS")
        st.info("**NEW RELEASE:** 'VOLTAGE CONTROL' EP OUT NOW VIA OSTGUT TON.")
        st.info("**TOUR ANNOUNCEMENT:** EUROPEAN DATES CONFIRMED FOR WINTER 2025.")
        
        # Research-based improvement: Mailing List (UK labels prioritize community)
        st.markdown("<br>---<br>", unsafe_allow_html=True)
        st.markdown("#### JOIN THE CIRCUIT")
        with st.form("mailing_list_form"):
            st.markdown(f"<p style='font-size: 1rem; color: #888;'>Get early access to tickets & vinyl pre-orders.</p>", unsafe_allow_html=True)
            email = st.text_input("EMAIL ADDRESS", placeholder="circuit@tnf.com")
            if st.form_submit_button("CONNECT", type="primary"):
                st.success(f"CONNECTION ESTABLISHED. Welcome, {email.split('@')[0]}!")


elif selected == "MUSIC":
    st.title("DISCOGRAPHY")
    
    # HKR Section (Moved to Top)
    st.markdown("### HOUSE KEEPING RECORDS")
    c1, c2 = st.columns([1, 3])
    with c1:
        st.markdown(HKR_LOGO_SVG, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="content-card" style='border-left: 3px solid #00f7ff;'>
        HKR is our dedicated platform for the raw and the deep. Focusing on functional tools for DJs and sonic explorations for heads. 
        Strictly limited vinyl runs for select projects.
        </div>
        """, unsafe_allow_html=True)
    st.divider()
    
    st.markdown("### RELEASES")
    
    # Track List (With Image and Format)
    for track in st.session_state.songs:
        col_img, col_info, col_btn = st.columns([1, 5, 2])
        with col_img:
            # Clickable image enlarges natively in Streamlit (Interactive Album Cover)
            st.image(track['cover_url'], width=100)
        with col_info:
            # Increased text size for track title
            st.markdown(f"<p style='font-size: 1.5rem; font-weight: 700; margin-bottom: -0.5rem;'>{track['title']}</p>", unsafe_allow_html=True)
            st.caption(f"**{track.get('label', 'Unknown Label')}** // {track.get('cat', 'Unknown Cat')} | Format: {track.get('format', 'N/A')}")
        with col_btn:
            st.button("STREAM / BUY", key=track['title'])
        st.divider()


elif selected == "HKR":
    c1, c2 = st.columns([1, 3])
    with c1:
        st.markdown(HKR_LOGO_SVG, unsafe_allow_html=True)
    with c2:
        st.title("HOUSE KEEPING RECORDS")
        st.markdown("#### EST. 2023 // DEEP HOUSE & TECHNO // VINYL ONLY")
        st.write("House Keeping Records is the dedicated platform for the raw and the deep. Focusing on functional tools for DJs and sonic explorations for heads.")
    
    st.divider()
    st.subheader("LATEST PRESSINGS")
    
    for item in st.session_state.hkr_releases:
        c1, c2, c3 = st.columns([1, 3, 1])
        with c1:
            st.markdown(f"**{item['cat']}**")
        with c2:
            st.markdown(f"**{item['artist']}** — {item['title']} | {item['format']}")
        with c3:
            st.button("BUY VINYL", key=item['cat'])


elif selected == "EVENTS":
    st.title("TOUR DATES") # Changed title
    
    # Increased text size for events is handled by general CSS
    for e in st.session_state.events:
        col_flyer, col_info, col_btn = st.columns([2, 3, 1])
        with col_flyer:
             # Flyer Image
             st.image(e['flyer_url'], caption=f"{e['city']} - {e['venue']}", use_column_width=True)
        with col_info:
            # Increased text size for info
            st.markdown(f"<p style='font-size: 1.5rem; font-weight: 900; color: {COLOR_TEXT};'>{e['date']} // {e['city']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 1.2rem; color: {COLOR_CYAN};'>{e['venue']}</p>", unsafe_allow_html=True)
        with col_btn:
            # Working Ticket Purchase Link (using st.link_button)
            st.link_button("TICKETS", url=e['ticket_link'], key=e['date']+e['city'])
        st.divider()

elif selected == "STORE":
    st.title("OFFICIAL MERCHANDISE")
    
    # Cart Summary
    if len(st.session_state.cart) > 0:
        st.info(f"🛒 CART: {len(st.session_state.cart)} ITEMS")
    else:
        st.markdown(f"<p style='font-size: 1.1rem; color: #888;'>Your cart is currently empty. Voltage required.</p>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    
    # Merch 1: T-Shirt with Logo Overlay
    with c1:
        st.markdown(f"""
        <div class="mockup-container">
            <img src="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=600&q=80" class="mockup-bg">
            <div class="mockup-logo" style="transform: translate(-50%, -50%) scale(0.65);">{TNF_LOGO_SVG}</div>
        </div>
        """, unsafe_allow_html=True) # Logo scale increased to 0.65
        st.markdown(f"<p style='font-size: 1.4rem; font-weight: 700;'>TNF CORE TEE</p>", unsafe_allow_html=True) # Text size increased
        st.caption("Heavyweight Cotton // All Sizes")
        # Purchase link works via add_to_cart helper
        st.button("ADD TO CART €35", key="m1", on_click=add_to_cart, args=("TNF CORE TEE",))

    # Merch 2: Hoodie with Logo Overlay
    with c2:
        st.markdown(f"""
        <div class="mockup-container">
            <img src="https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=600&q=80" class="mockup-bg">
            <div class="mockup-logo" style="transform: translate(-50%, -50%) scale(0.8);">{HKR_LOGO_SVG}</div>
        </div>
        """, unsafe_allow_html=True) # Logo scale increased to 0.8
        st.markdown(f"<p style='font-size: 1.4rem; font-weight: 700;'>HKR LABEL HOODIE</p>", unsafe_allow_html=True) # Text size increased
        st.caption("Oversized Fit // Limited Run")
        # Purchase link works via add_to_cart helper
        st.button("ADD TO CART €65", key="m2", on_click=add_to_cart, args=("HKR LABEL HOODIE",))

    # Merch 3: Slipmats
    with c3:
        st.markdown(f"""
        <div class="mockup-container">
            <img src="https://images.unsplash.com/photo-1603048588665-791ca8aea617?auto=format&fit=crop&w=600&q=80" class="mockup-bg">
            <div class="mockup-logo" style="transform: translate(-50%, -50%) scale(1.0);">{SLIPMAT_ICON_SVG}</div>
        </div>
        """, unsafe_allow_html=True) # Logo scale increased to 1.0
        st.markdown(f"<p style='font-size: 1.4rem; font-weight: 700;'>PRO SLIPMATS</p>", unsafe_allow_html=True) # Text size increased
        st.caption("Anti-static Pair // Essential DJ Tool")
        # Purchase link works via add_to_cart helper
        st.button("ADD TO CART €20", key="m3", on_click=add_to_cart, args=("PRO SLIPMATS",))

elif selected == "GALLERY":
    st.title("VISUAL ARCHIVE")
    st.markdown("#### DOCUMENTATION OF THE FREAK ENCOUNTERS")
    
    c1, c2 = st.columns(2)
    # The gallery is now populated with relevant images and a video
    for i, item in enumerate(st.session_state.gallery):
        col = c1 if i % 2 == 0 else c2
        with col:
            if item['type'] == 'image':
                st.image(item['url'], caption=item['caption'], use_column_width=True)
            elif item['type'] == 'video':
                 st.video(item['url'])
                 st.caption(item['caption'])
        st.markdown("<br>", unsafe_allow_html=True) # Add some spacing

elif selected == "ABOUT":
    c1, c2 = st.columns([2,1])
    with c1:
        st.title("BIOGRAPHY")
        st.write("""
        **Tuesdaynightfreak** is an electronic music project established in Melbourne, Australia.
        Drawing influence from the stark industrialism of Berlin and the soulful rhythms of Detroit,
        the project explores the boundaries of hardware sequencing. 
        
        It is a reaction against the predictability of digital production—a celebration of the machine's inherent instability.
        From the smoky basements of Revolver to the concrete halls of Tresor, Tuesdaynightfreak delivers a sound that is distinct, raw, and uncompromising.
        """)
        
        st.markdown("#### DEMO SUBMISSION PROTOCOL") # Research-based improvement: structured demo section
        st.markdown(f"""
        <div class="tech-card">
        // HKR ONLY ACCEPTS DEEP & INDUSTRIAL TEMPO TRACKS (130-140 BPM).<br>
        // NO UNMASTERED FILES. NO CLOUD LINKS (Send private SoundCloud/Bandcamp link only).<br>
        // SUBJECT LINE MUST CONTAIN: [HKR DEMO] - ARTIST NAME - EP TITLE
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("#### CONTACT")
        st.code("mgmt@tuesdaynightfreak.com")
        st.markdown("#### DEMOS")
        st.code("demos@housekeeping-rec.com")
        st.button("DOWNLOAD PRESS KIT")

elif selected == "SYSTEM":
    st.title("SYSTEM ACCESS")
    
    # Mock Admin Login
    pwd = st.text_input("ENTER AUTH CODE", type="password")
    
    if pwd == "admin123":
        st.success("ACCESS GRANTED")
        
        # --- ADMIN TABS FOR UPLOADING CONTENT ---
        tab1, tab2, tab3 = st.tabs(["UPLOAD MUSIC", "UPLOAD VISUALS", "INCOMING DATA"])
        
        with tab1:
            st.markdown("### ADD AUDIO SOURCE")
            with st.form("add_song_admin"):
                new_title = st.text_input("SONG TITLE")
                new_label = st.text_input("LABEL")
                new_cat = st.text_input("CATALOGUE #")
                new_format = st.selectbox("FORMAT", ["DIGITAL/VINYL", "DIGITAL", "VINYL"])
                new_cover = st.text_input("COVER URL (Placeholder)")
                if st.form_submit_button("UPLOAD TRACK"):
                    st.session_state.songs.append({"title": new_title, "label": new_label, "cat": new_cat, "format": new_format, "cover_url": new_cover})
                    st.success(f"TRACK '{new_title}' ADDED TO ARCHIVE.")
                    st.rerun()
            
            if st.button("PURGE AUDIO ARCHIVE"):
                st.session_state.songs = []
                st.warning("AUDIO ARCHIVE CLEARED.")
                st.rerun()

        with tab2:
            st.markdown("### ADD VISUAL ASSET")
            with st.form("add_photo_admin"):
                new_caption = st.text_input("CAPTION")
                new_type = st.selectbox("ASSET TYPE", ["image", "video"])
                new_url = st.text_input("URL (Image or YouTube link)")
                if st.form_submit_button("UPLOAD VISUAL"):
                    st.session_state.gallery.append({"caption": new_caption, "url": new_url, "type": new_type})
                    st.success("VISUAL ASSET ADDED TO FEED.")
                    st.rerun()

        with tab3:
            st.markdown("### INCOMING TRANSMISSIONS (Bookings/Demos)")
            if len(st.session_state.bookings) > 0:
                st.dataframe(pd.DataFrame(st.session_state.bookings))
            else:
                st.info("NO NEW MESSAGES.")

# --- FOOTER (Always visible) ---
st.markdown(f"""
<div class="footer-bar">
    TUESDAYNIGHTFREAK &copy; 2024 // HKR-ARCHIVE V1.1 // DESIGNED FOR ANALOGUE MINDS
</div>
""", unsafe_allow_html=True)
