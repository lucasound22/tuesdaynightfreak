import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import time

# --- CONFIGURATION & PALETTE ---
COLOR_BG = "#080808"
COLOR_TEXT = "#F0F0F0"
COLOR_ACCENT = "#FF0033"  # Acid Red
COLOR_CYAN = "#00f7ff"    # Cyberpunk Splash
COLOR_SECONDARY = "#141414"

# --- BRANDING SVGs (BIGGER & CLEANER) ---
# TNF Logo - Glitch/Cyberpunk Style
TNF_LOGO_SVG = f"""
<svg width="300" height="90" viewBox="0 0 300 90" xmlns="http://www.w3.org/2000/svg">
    <text x="4" y="65" font-family="Arial, sans-serif" font-weight="900" font-size="72" fill="{COLOR_CYAN}" opacity="0.6" letter-spacing="-4">TNF</text>
    <text x="-2" y="65" font-family="Arial, sans-serif" font-weight="900" font-size="72" fill="{COLOR_ACCENT}" opacity="0.7" letter-spacing="-4">TNF</text>
    <text x="0" y="65" font-family="Arial, sans-serif" font-weight="900" font-size="72" fill="{COLOR_TEXT}" letter-spacing="-4">TNF</text>
    <rect x="160" y="25" width="8" height="40" fill="{COLOR_ACCENT}"/>
    <rect x="175" y="25" width="8" height="40" fill="{COLOR_CYAN}"/>
    <circle cx="210" cy="45" r="12" stroke="{COLOR_TEXT}" stroke-width="3" fill="none"/>
    <line x1="0" y1="85" x2="300" y2="85" stroke="{COLOR_CYAN}" stroke-width="2" opacity="0.8"/>
</svg>
"""

# House Keeping Records Logo - Deep House/Minimal Style
HKR_LOGO_SVG = f"""
<svg width="150" height="150" viewBox="0 0 150 150" xmlns="http://www.w3.org/2000/svg">
    <rect x="5" y="5" width="140" height="140" stroke="{COLOR_TEXT}" stroke-width="5" fill="none"/>
    <path d="M20 60 L75 20 L130 60" stroke="{COLOR_ACCENT}" stroke-width="5" fill="none"/>
    <circle cx="75" cy="95" r="30" stroke="{COLOR_CYAN}" stroke-width="4" fill="none"/>
    <rect x="72" y="85" width="6" height="20" fill="{COLOR_CYAN}"/>
    <text x="75" y="135" font-family="monospace" font-size="14" fill="#888" text-anchor="middle" font-weight="bold">EST. 2023</text>
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

# Gallery/Visual Archive - Updated with robust Unsplash URLs
if 'gallery' not in st.session_state:
    st.session_state.gallery = [
        {"caption": "MODULAR RIG SETUP A", "url": "https://images.unsplash.com/photo-1550291652-6ea9114a47b1?q=80&w=800&auto=format&fit=crop"},
        {"caption": "LIVE SIGNAL PATH", "url": "https://images.unsplash.com/photo-1598275529124-b1c4b786f1e2?q=80&w=800&auto=format&fit=crop"},
        {"caption": "WAREHOUSE CROWD", "url": "https://images.unsplash.com/photo-1571266028243-371695063ad6?q=80&w=800&auto=format&fit=crop"},
        {"caption": "OSCILLATOR DETAIL", "url": "https://images.unsplash.com/photo-1619967657960-983b6329c370?q=80&w=800&auto=format&fit=crop"}
    ]

# Songs Data
if 'songs' not in st.session_state:
    st.session_state.songs = [
        {"title": "System Failure (Original Mix)", "label": "House Keeping Rec", "cat": "HKR004"},
        {"title": "Analog Dreams", "label": "Tresor Records", "cat": "TR-291"},
        {"title": "Voltage Control", "label": "Ostgut Ton", "cat": "OSTGUT-55"},
        {"title": "Modular State", "label": "Klockworks", "cat": "KW-22"}
    ]

# HKR Releases Data
if 'hkr_releases' not in st.session_state:
    st.session_state.hkr_releases = [
        {"title": "Rhythm Generator EP", "artist": "Various Artists", "cat": "HKR005"},
        {"title": "Modular Loop 01", "artist": "TUESDAYNIGHTFREAK", "cat": "HKR004"},
        {"title": "Grid Sequencer", "artist": "Acid Junkie", "cat": "HKR003"},
    ]

if 'bookings' not in st.session_state:
    st.session_state.bookings = []


# --- NAVIGATION CALLBACK ---
def set_page(index):
    st.session_state.page_index = index

# --- CUSTOM CSS ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Space+Mono:wght@400;700&display=swap');
    
    .stApp {{ background-color: {COLOR_BG}; color: {COLOR_TEXT}; font-family: 'Inter', sans-serif; }}
    
    /* Navigation Menu Font Override */
    div[data-testid="stHorizontalBlock"] button {{
        font-family: 'Inter', sans-serif !important;
    }}
    
    h1, h2, h3 {{ font-weight: 900; text-transform: uppercase; letter-spacing: -1px; }}
    h4, h5 {{ font-family: 'Space Mono', monospace; color: {COLOR_CYAN}; text-transform: uppercase; letter-spacing: 1px; }}
    
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
    }}
    .stButton>button:hover {{
        background: {COLOR_ACCENT};
        color: #fff;
        box-shadow: 0 0 15px {COLOR_ACCENT};
    }}
    
    /* Video Background - Full Screen & Behind Everything */
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
        height: 56.25vw; /* 16:9 */
        min-height: 100vh;
        min-width: 177.77vh;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        opacity: 0.6; /* Darken for readability */
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
    
    /* Mockup Container */
    .mockup-container {{
        position: relative;
        width: 100%;
        height: 300px;
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
        opacity: 0.6;
    }}
    .mockup-logo {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 10;
        filter: drop-shadow(0 0 10px rgba(0,0,0,0.8));
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
    
</style>
""", unsafe_allow_html=True)

# --- BACKGROUND VIDEO & AUDIO ---
# Muted, Autoplay, Loop, Controls Hidden
st.markdown("""
<div class="video-bg">
    <iframe src="https://www.youtube.com/embed/qC0vDKVPCrw?controls=0&showinfo=0&rel=0&autoplay=1&loop=1&mute=1&playlist=qC0vDKVPCrw" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
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
            const synth = new Tone.MembraneSynth().toDestination();
            const loop = new Tone.Loop(time => {
                synth.triggerAttackRelease("C1", "8n", time);
            }, "4n").start(0);
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
        "container": {"padding": "0", "background-color": "rgba(0,0,0,0.8)"},
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
        st.markdown("#### SYSTEM UPDATES")
        st.info("**NEW RELEASE:** 'VOLTAGE CONTROL' EP OUT NOW VIA OSTGUT TON.")
        st.info("**TOUR ANNOUNCEMENT:** EUROPEAN DATES CONFIRMED FOR WINTER 2025.")

elif selected == "MUSIC":
    st.title("DISCOGRAPHY")
    
    # Track List
    for track in st.session_state.songs:
        c1, c2, c3, c4 = st.columns([1, 4, 2, 2])
        with c1:
            # Placeholder for track artwork
            st.markdown(f"<div style='width:60px;height:60px;background:#222;border:1px solid #444;'></div>", unsafe_allow_html=True)
        with c2:
            st.subheader(track['title'])
        with c3:
            st.caption(f"{track.get('label', 'Unknown Label')} // {track.get('cat', 'Unknown Cat')}")
        with c4:
            st.button("STREAM", key=track['title'])
        st.divider()

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
            st.markdown(f"**{item['artist']}** — {item['title']}")
        with c3:
            st.button("BUY VINYL", key=item['cat'])

elif selected == "EVENTS":
    st.title("UPCOMING DATES")
    events = [
        {"date": "NOV 04", "city": "AMSTERDAM", "venue": "SHELTER"},
        {"date": "NOV 11", "city": "LONDON", "venue": "FOLD"},
        {"date": "NOV 18", "city": "MELBOURNE", "venue": "REVOLVER"},
        {"date": "DEC 02", "city": "PARIS", "venue": "REX CLUB"},
    ]
    for e in events:
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f"**{e['date']}**")
        with c2: st.markdown(e['city'])
        with c3: st.markdown(e['venue'])
        with c4: st.button("TICKETS", key=e['date']+e['city'])
        st.divider()

elif selected == "STORE":
    st.title("OFFICIAL MERCHANDISE")
    
    # Cart Summary
    if len(st.session_state.cart) > 0:
        st.info(f"CART: {len(st.session_state.cart)} ITEMS")

    c1, c2, c3 = st.columns(3)
    
    # Merch 1: T-Shirt with Logo Overlay
    with c1:
        st.markdown(f"""
        <div class="mockup-container">
            <img src="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=600&q=80" class="mockup-bg">
            <div class="mockup-logo" style="transform: translate(-50%, -50%) scale(0.5);">{TNF_LOGO_SVG}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**TNF CORE TEE**")
        st.caption("Heavyweight Cotton")
        st.button("ADD TO CART €35", key="m1", on_click=add_to_cart, args=("TNF CORE TEE",))

    # Merch 2: Hoodie with Logo Overlay
    with c2:
        st.markdown(f"""
        <div class="mockup-container">
            <img src="https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=600&q=80" class="mockup-bg">
            <div class="mockup-logo" style="transform: translate(-50%, -50%) scale(0.6);">{HKR_LOGO_SVG}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**HKR LABEL HOODIE**")
        st.caption("Oversized Fit")
        st.button("ADD TO CART €65", key="m2", on_click=add_to_cart, args=("HKR LABEL HOODIE",))

    # Merch 3: Slipmats
    with c3:
        st.markdown(f"""
        <div class="mockup-container">
            <img src="https://images.unsplash.com/photo-1603048588665-791ca8aea617?auto=format&fit=crop&w=600&q=80" class="mockup-bg">
            <div class="mockup-logo" style="transform: translate(-50%, -50%) scale(0.8);">{SLIPMAT_ICON_SVG}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**PRO SLIPMATS**")
        st.caption("Anti-static Pair")
        st.button("ADD TO CART €20", key="m3", on_click=add_to_cart, args=("PRO SLIPMATS",))

elif selected == "GALLERY":
    st.title("VISUAL ARCHIVE")
    
    c1, c2 = st.columns(2)
    for i, item in enumerate(st.session_state.gallery):
        with (c1 if i % 2 == 0 else c2):
            st.image(item['url'], caption=item['caption'], use_column_width=True)

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
                if st.form_submit_button("UPLOAD TRACK"):
                    st.session_state.songs.append({"title": new_title, "label": new_label, "cat": new_cat})
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
                new_img_url = st.text_input("IMAGE URL (Unsplash or similar)")
                if st.form_submit_button("UPLOAD VISUAL"):
                    st.session_state.gallery.append({"caption": new_caption, "url": new_img_url})
                    st.success("VISUAL ASSET ADDED TO FEED.")
                    st.rerun()

        with tab3:
            st.markdown("### INCOMING TRANSMISSIONS (Bookings/Demos)")
            # Currently, there's no way for users to submit data to this list
            # We'll display a placeholder to show where that data would go.
            if len(st.session_state.bookings) > 0:
                st.dataframe(pd.DataFrame(st.session_state.bookings))
            else:
                st.info("NO NEW MESSAGES.")
