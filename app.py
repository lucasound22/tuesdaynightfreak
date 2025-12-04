import streamlit as st
from streamlit_option_menu import option_menu
import time

# --- UPLOADED IMAGE MAPPINGS (Replaces Unsplash URLs) ---
# These Content IDs refer to your uploaded files
IMAGE_MAPPING = {
    # Events
    "EVENT_AMSTERDAM": "uploaded:image_1bc503.jpg-857b2deb-0348-4079-b5ae-7435256a80af", # DJ/Crowd shot 1
    "EVENT_LONDON": "uploaded:image_1bb6f5.jpg-434247b3-a427-4211-9669-fc465cd7b712",    # Crowd/Scene shot 2
    "EVENT_MELBOURNE": "uploaded:image_377bc1.jpg-bd1de4bb-ff91-42fc-bdc4-e40ecdda71fe", # Scene/Texture shot
    # Store Mockups (using PNGs for apparel mockups)
    "MERCH_TEE": "uploaded:image_20608f.png-54a97f38-0e2f-412b-864a-fe49523e31bc",
    "MERCH_HOODIE": "uploaded:image_831f9b.png-cebe82d7-d6b6-44cd-a376-0a36c263db05",
    "MERCH_SLIPMATS": "uploaded:image_205cd6.png-3bca7ad1-af70-44d0-961c-7d5c82c713c5",
    # Gallery
    "GALLERY_1": "uploaded:image_37de51.png-bd336e1f-aee3-41c9-ae31-d75b4df0cb48",
    "GALLERY_2": "uploaded:image_1a5cde.png-21ff920c-a784-44af-baf3-b86316c15967",
    "GALLERY_3": "uploaded:image_9deda8.png-8dbdce5e-0e20-43f9-a15f-277a03aa8c4f",
    "GALLERY_4": "uploaded:image_9dd73a.png-f3e52899-1fd9-4c67-9ad7-5707fd96bc9a",
    "GALLERY_5": "uploaded:image_1bab17.png-b46838e8-6d68-4332-98b2-515b0aefa899",
    "GALLERY_6": "uploaded:image_1bb25b.png-7161be77-115d-4c4c-ab7e-dabeeb3e79ab",
}

# --- CONFIGURATION & PALETTE ---
COLOR_BG = "#080808"
COLOR_TEXT = "#F0F0F0"
COLOR_ACCENT = "#FF0033"  # Acid Red
COLOR_CYAN = "#00f7ff"    # Cyberpunk Splash
COLOR_SECONDARY = "#141414"

# --- BRANDING SVGs (SCALABLE & CENTERED) ---
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

HKR_LOGO_SVG = f"""
<svg width="150" height="150" viewBox="0 0 150 150" xmlns="http://www.w3.org/2000/svg">
    <rect x="5" y="5" width="140" height="140" stroke="{COLOR_TEXT}" stroke-width="5" fill="none"/>
    <path d="M20 60 L75 20 L130 60" stroke="{COLOR_ACCENT}" stroke-width="5" fill="none"/>
    <circle cx="75" cy="95" r="30" stroke="{COLOR_CYAN}" stroke-width="4" fill="none"/>
    <rect x="72" y="85" width="6" height="20" fill="{COLOR_CYAN}"/>
    <text x="75" y="135" font-family="monospace" font-size="14" fill="#888" text-anchor="middle" font-weight="bold">HKR 2023</text>
</svg>
"""

SLIPMAT_ICON_SVG = f"""
<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <circle cx="50" cy="50" r="45" fill="#111" stroke="{COLOR_CYAN}" stroke-width="2"/>
    <circle cx="50" cy="50" r="15" fill="{COLOR_ACCENT}"/>
    <circle cx="50" cy="50" r="2" fill="#fff"/>
</svg>
"""

# --- PAGE SETUP & STATE ---
st.set_page_config(
    page_title="TUESDAYNIGHTFREAK | OFFICIAL",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'page_index' not in st.session_state:
    st.session_state.page_index = 0

def set_page(index):
    st.session_state.page_index = index

def add_to_cart(item):
    st.session_state.cart.append(item)
    st.toast(f"Added {item} to cart!", icon="🛒")

# --- CUSTOM CSS (STREAMLIT UI REMOVAL & STYLING) ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Space+Mono:wght@400;700&display=swap');
    
    .stApp {{ background-color: {COLOR_BG}; color: {COLOR_TEXT}; font-family: 'Inter', sans-serif; }}
    
    /* 1. REMOVE ALL STREAMLIT UI (Header, Menu Button, Footer) */
    header, footer, [data-testid="stToolbar"] {{ visibility: hidden; height: 0; }}

    /* 2. REMOVE WHITE BARS & PADDING */
    .block-container {{
        padding-top: 0rem !important;
        padding-bottom: 5rem !important;
        max-width: 100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }}
    /* Add padding back ONLY to the main content area below the menu */
    div[data-testid="stVerticalBlock"] > div:first-of-type {{
        padding-top: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }}
    
    h1, h2, h3 {{ font-weight: 900; text-transform: uppercase; letter-spacing: -1px; }}
    
    /* Buttons */
    .stButton>button {{
        background: {COLOR_CYAN}; 
        color: {COLOR_BG}; 
        font-weight: 900; 
        border-radius: 0;
        transition: 0.3s;
        width: 100%;
        border: 2px solid {COLOR_CYAN};
    }}
    .stButton>button:hover {{
        background: {COLOR_ACCENT};
        color: {COLOR_TEXT};
        border: 2px solid {COLOR_ACCENT};
        box-shadow: 0 0 15px {COLOR_ACCENT};
    }}

    /* Menu Styling */
    .st-emotion-cache-163lq9m {{ /* Target the option_menu container */
        border-bottom: 3px solid {COLOR_CYAN};
        padding: 0 2rem;
    }}
    
    /* Mockup Container */
    .mockup-container {{
        position: relative;
        width: 100%;
        height: 400px;
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
        opacity: 0.8;
    }}
    .mockup-logo {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 10;
        filter: drop-shadow(0 0 10px rgba(0,0,0,0.8));
    }}

    /* --- MARQUEE STYLING --- */
    .marquee-container {{
        width: 100%;
        overflow: hidden;
        background: rgba(0, 0, 0, 0.9);
        border-top: 2px solid {COLOR_ACCENT};
        border-bottom: 2px solid {COLOR_ACCENT};
        padding: 8px 0;
        position: relative;
        z-index: 1000;
        box-shadow: 0 0 10px rgba(255, 0, 51, 0.4); /* Subtle glow */
    }}
    .marquee-content {{
        display: inline-block;
        white-space: nowrap;
        animation: marquee 20s linear infinite;
        font-family: 'Space Mono', monospace;
        color: {COLOR_CYAN}; 
        font-size: 1.1rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 4px;
        text-shadow: 0 0 5px rgba(0, 247, 255, 0.6);
    }}
    @keyframes marquee {{
        0% {{ transform: translate(100%, 0); }}
        100% {{ transform: translate(-100%, 0); }}
    }}
    
    /* --- HIDE YOUTUBE/TONE.JS ELEMENTS --- */
    .video-bg, .video-overlay, .mixcloud-bg-spacer {{ display: none !important; }}

    /* --- MIXCLOUD EMBED (Hidden but functional for background audio) --- */
    .mixcloud-bg {{
        position: fixed;
        top: 0;
        left: 0;
        width: 1px;
        height: 1px;
        opacity: 0; 
        overflow: hidden;
        z-index: -999; /* Place far in background */
    }}
    
</style>
""", unsafe_allow_html=True)

# --- BACKGROUND AUDIO (Mixcloud) & MARQUEE ---

# 1. Mixcloud Player (Hidden)
st.markdown(f"""
<div class="mixcloud-bg">
    <!-- Using a simplified widget URL for autoplay/background purposes. User must click on the page once to enable audio. -->
    <iframe width="100%" height="120" src="https://www.mixcloud.com/House_Keeping/stargazing/embed/?autoplay=1&amp;hide_cover=1&amp;light=1&amp;mini=1" frameborder="0" allow="autoplay" loading="eager"></iframe>
</div>
""", unsafe_allow_html=True)

# 2. Marquee Text
st.markdown("""
<div class="marquee-container">
    <div class="marquee-content">
        TUESDAYNIGHTFREAK LIVE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;TUESDAYNIGHTFREAK LIVE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;TUESDAYNIGHTFREAK LIVE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;TUESDAYNIGHTFREAK LIVE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    </div>
</div>
""", unsafe_allow_html=True)


# --- NAVIGATION (Fixed Double-Click) ---
menu_options = ["HOME", "MUSIC", "HKR", "EVENTS", "STORE", "GALLERY", "ABOUT", "SYSTEM"]
selected = option_menu(
    menu_title=None,
    options=menu_options,
    icons=["house", "disc", "vinyl", "calendar3", "bag", "images", "info-circle", "cpu"],
    default_index=st.session_state.page_index,
    orientation="horizontal",
    styles={
        "container": {"padding": "0", "background-color": "rgba(0,0,0,0.8)"},
        "nav-link": {"font-size": "16px", "text-transform": "uppercase", "font-weight": "bold", "color": "#fff", "border-radius": "0px"},
        "nav-link-selected": {"background-color": "transparent", "color": COLOR_CYAN, "border-bottom": f"3px solid {COLOR_CYAN}"}
    }
)

# Update page index on selection change to fix double-click issue
if menu_options.index(selected) != st.session_state.page_index:
   set_page(menu_options.index(selected))
   st.rerun()

# --- CONTENT PAGES ---

if selected == "HOME":
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"<div style='width: 300px; height: 90px; margin-bottom: 20px;'>{TNF_LOGO_SVG}</div>", unsafe_allow_html=True)
        st.markdown("### THE SOUND OF HARDWARE SOUL")
        st.markdown("""
        <div style="font-size: 1.2rem; line-height: 1.6; color: #ddd;">
        We are an independent electronic music project and culture crew bridging the gap between <br>
        Berlin's concrete basements and Melbourne's warehouse soul. We embrace the **analogue error**.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        with b1:
            st.button("LATEST RELEASE", on_click=set_page, args=(1,))
        with b2:
            st.button("TOUR DATES", on_click=set_page, args=(3,))

    with col2:
        st.markdown("#### SYSTEM UPDATES")
        st.info("**NEW RELEASE:** 'VOLTAGE CONTROL' EP OUT NOW VIA OSTGUT TON.")
        st.info("**TOUR ANNOUNCEMENT:** EUROPEAN DATES CONFIRMED FOR WINTER 2025.")

elif selected == "MUSIC":
    st.title("DISCOGRAPHY")
    releases = [
        {"title": "System Failure", "label": "House Keeping Rec", "cat": "HKR004"},
        {"title": "Analog Dreams", "label": "Tresor Records", "cat": "TR-291"},
        {"title": "Voltage Control", "label": "Ostgut Ton", "cat": "OSTGUT-55"}
    ]
    
    for r in releases:
        c1, c2, c3, c4 = st.columns([1, 4, 2, 2])
        with c1:
            st.markdown(f"<div style='width:60px;height:60px;background:#222;border:1px solid #444;border-radius: 4px;'></div>", unsafe_allow_html=True)
        with c2:
            st.subheader(r['title'])
        with c3:
            st.caption(f"{r['label']} // {r['cat']}")
        with c4:
            st.button("STREAM / BUY", key=r['cat'])
        st.divider()

elif selected == "HKR":
    c1, c2 = st.columns([1, 3])
    with c1:
        st.markdown(f"<div style='width: 120px; height: 120px; margin: auto;'>{HKR_LOGO_SVG}</div>", unsafe_allow_html=True)
    with c2:
        st.title("HOUSE KEEPING RECORDS")
        st.markdown("#### EST. 2023 // DEEP HOUSE & TECHNO // VINYL ONLY")
        st.write("House Keeping Records is the dedicated platform for the raw and the deep. Focusing on functional tools for DJs and sonic explorations for heads.")
    
    st.divider()
    st.subheader("CATALOGUE")
    
    hkr_releases = [
        {"cat": "HKR005", "artist": "VARIOUS", "title": "RHYTHM GENERATOR EP"},
        {"cat": "HKR004", "artist": "TUESDAYNIGHTFREAK", "title": "MODULAR LOOP 01"},
        {"cat": "HKR003", "artist": "ACID JUNKIE", "title": "GRID SEQUENCER"}
    ]
    
    for item in hkr_releases:
        c1, c2, c3 = st.columns([1, 3, 1])
        with c1:
            st.markdown(f"**{item['cat']}**")
        with c2:
            st.markdown(f"**{item['artist']}** — {item['title']}")
        with c3:
            st.button("PURCHASE VINYL", key=item['cat'])
        st.divider()

elif selected == "EVENTS":
    st.title("UPCOMING DATES")
    
    # Updated to use MAPPED IMAGE IDs
    events_data = [
        {"date": "NOV 04", "city": "AMSTERDAM", "venue": "SHELTER", "image": IMAGE_MAPPING['EVENT_AMSTERDAM']},
        {"date": "NOV 11", "city": "LONDON", "venue": "FOLD", "image": IMAGE_MAPPING['EVENT_LONDON']},
        {"date": "NOV 18", "city": "MELBOURNE", "venue": "REVOLVER", "image": IMAGE_MAPPING['EVENT_MELBOURNE']},
    ]
    
    for event in events_data:
        c1, c2, c3 = st.columns([2, 3, 1])
        with c1:
            st.image(event['image'], caption=f"{event['city']} - {event['venue']}", use_column_width=True)
        with c2:
            st.markdown(f"### {event['date']}")
            st.markdown(f"**{event['city']}** // {event['venue']}")
        with c3:
            st.button("TICKETS", key=event['city'])
        st.divider()

elif selected == "STORE":
    st.title("OFFICIAL MERCHANDISE")
    
    if st.session_state.cart:
        st.info(f"CART: {len(st.session_state.cart)} ITEMS")
        if st.button("CHECKOUT (EMAIL)"):
             st.markdown(f'<meta http-equiv="refresh" content="0;url=mailto:tuesdaynightfreak@gmail.com?subject=Merch%20Order&body=I%20would%20like%20to%20buy:%20{", ".join(st.session_state.cart)}">', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    
    # Merch 1: T-Shirt with BIGGER Logo Overlay - Updated to use MAPPED IMAGE ID
    with c1:
        st.markdown(f"""
        <div class="mockup-container">
            <img src="{IMAGE_MAPPING['MERCH_TEE']}" class="mockup-bg">
            <div class="mockup-logo" style="transform: translate(-50%, -50%) scale(0.6);">{TNF_LOGO_SVG}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**TNF CORE TEE**")
        st.caption("Heavyweight Cotton")
        if st.button("ADD TO CART €35", key="m1"):
            add_to_cart("TNF Core Tee")

    # Merch 2: Hoodie with HKR Logo - Updated to use MAPPED IMAGE ID
    with c2:
        st.markdown(f"""
        <div class="mockup-container">
            <img src="{IMAGE_MAPPING['MERCH_HOODIE']}" class="mockup-bg">
            <div class="mockup-logo" style="transform: translate(-50%, -50%) scale(0.7);">{HKR_LOGO_SVG}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**HKR LABEL HOODIE**")
        st.caption("Oversized Fit")
        if st.button("ADD TO CART €65", key="m2"):
            add_to_cart("HKR Hoodie")

    # Merch 3: Slipmats - Updated to use MAPPED IMAGE ID
    with c3:
        st.markdown(f"""
        <div class="mockup-container">
            <img src="{IMAGE_MAPPING['MERCH_SLIPMATS']}" class="mockup-bg">
            <div class="mockup-logo" style="transform: translate(-50%, -50%) scale(0.8);">{SLIPMAT_ICON_SVG}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**PRO SLIPMATS**")
        st.caption("Anti-static Pair")
        if st.button("ADD TO CART €20", key="m3"):
            add_to_cart("Slipmats")

elif selected == "GALLERY":
    st.title("VISUAL ARCHIVE // HARDWARE FOCUS")
    st.caption("RAW VOLTAGE. RAW RHYTHM.")
    
    # Updated to use MAPPED IMAGE IDs
    gallery_images = [
        {"url": IMAGE_MAPPING['GALLERY_1'], "cap": "MODULAR SYNTHESIS"},
        {"url": IMAGE_MAPPING['GALLERY_2'], "cap": "LIVE PERFORMANCE IN BERLIN"},
        {"url": IMAGE_MAPPING['GALLERY_3'], "cap": "DRUM MACHINE SEQUENCE"},
        {"url": IMAGE_MAPPING['GALLERY_4'], "cap": "CROWD MOMENTS"},
        {"url": IMAGE_MAPPING['GALLERY_5'], "cap": "VINYL MIXING"},
        {"url": IMAGE_MAPPING['GALLERY_6'], "cap": "STUDIO SESSION"}
    ]
    
    c1, c2, c3 = st.columns(3)
    cols = [c1, c2, c3]
    for i, item in enumerate(gallery_images):
        with cols[i % 3]:
            st.image(item['url'], caption=item['cap'], use_column_width=True)

elif selected == "ABOUT":
    # Content remains the same as it was functional
    c1, c2 = st.columns([2,1])
    with c1:
        st.title("BIOGRAPHY")
        st.write("""
        **Tuesdaynightfreak** is an electronic music project established in Melbourne, Australia.
        <br>
        Drawing influence from the stark industrialism of Berlin and the soulful rhythms of Detroit, the project explores the boundaries of hardware sequencing. It is a reaction against the predictability of digital production—a celebration of the machine's inherent instability.
        <br>
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
    pwd = st.text_input("ENTER AUTH CODE", type="password")
    if pwd == "admin123":
        st.success("ACCESS GRANTED")
