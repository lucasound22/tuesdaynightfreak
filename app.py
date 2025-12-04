import streamlit as st
from streamlit_option_menu import option_menu
import time
import requests
import stripe

# --- CONFIGURATION & PALETTE ---
COLOR_BG = "#080808"
COLOR_TEXT = "#F0F0F0"
COLOR_ACCENT = "#FF0033"  # Acid Red
COLOR_CYAN = "#00f7ff"    # Cyberpunk Splash
COLOR_SECONDARY = "#141414"

# --- BRANDING SVGs (Optimized) ---
TNF_LOGO_SVG = f"""
<svg width="80%" height="80%" viewBox="0 0 300 90" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
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
<svg width="100%" height="100%" viewBox="0 0 150 150" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
    <rect x="5" y="5" width="140" height="140" stroke="{COLOR_TEXT}" stroke-width="5" fill="none"/>
    <path d="M20 60 L75 20 L130 60" stroke="{COLOR_ACCENT}" stroke-width="5" fill="none"/>
    <circle cx="75" cy="95" r="30" stroke="{COLOR_CYAN}" stroke-width="4" fill="none"/>
    <rect x="72" y="85" width="6" height="20" fill="{COLOR_CYAN}"/>
    <text x="75" y="135" font-family="monospace" font-size="14" fill="#888" text-anchor="middle" font-weight="bold">EST. 2023</text>
</svg>
"""

SLIPMAT_ICON_SVG = f"""
<svg width="100%" height="100%" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
    <circle cx="50" cy="50" r="45" fill="#111" stroke="{COLOR_CYAN}" stroke-width="2"/>
    <circle cx="50" cy="50" r="15" fill="{COLOR_ACCENT}"/>
    <circle cx="50" cy="50" r="2" fill="#fff"/>
</svg>
"""

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
if 'expanded_image' not in st.session_state:
    st.session_state.expanded_image = None

# --- NAVIGATION CALLBACK ---
def set_page(index):
    st.session_state.page_index = index
    st.session_state.expanded_image = None  # Reset expanded image on page change
    
def add_to_cart(item):
    st.session_state.cart.append(item)
    st.toast(f"Added {item} to cart!", icon="🛒")

# --- CUSTOM CSS ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Space+Mono:wght@400;700&display=swap');
    
    .stApp {{ background-color: {COLOR_BG}; color: {COLOR_TEXT}; font-family: 'Inter', sans-serif; }}
    
    /* Remove Streamlit branding */
    [data-testid="stToolbar"] {{ visibility: hidden !important; }}
    footer {{ visibility: hidden !important; }}
    header {{ visibility: hidden !important; }}
    .css-1y4p8pa {{ display: none !important; }} /* Hide main menu */
    .css-18e3th9 {{ padding-top: 0 !important; }} /* Remove top padding */
    
    /* NAVIGATION FIXES - No white gaps */
    div[data-testid="stHorizontalBlock"] {{
        background-color: {COLOR_BG} !important;
        padding: 0 !important;
        margin: 0 !important;
    }}
    div[data-testid="stHorizontalBlock"] button {{
        font-family: 'Inter', sans-serif !important;
        background-color: {COLOR_BG} !important;
        color: {COLOR_TEXT} !important;
        border: none !important;
        padding: 8px 16px !important;
    }}
    div[data-testid="stHorizontalBlock"] button:hover {{
        color: {COLOR_CYAN} !important;
    }}
    
    /* LAYOUT FIXES */
    .block-container {{
        padding-top: 0 !important;
        padding-bottom: 5rem !important;
        max-width: 100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }}
    div[data-testid="stVerticalBlock"] > div:first-of-type {{
        padding-left: 1rem;
        padding-right: 1rem;
    }}
    
    h1, h2, h3 {{ font-weight: 900; text-transform: uppercase; letter-spacing: -1px; }}
    h4, h5 {{ font-family: 'Space Mono', monospace; color: {COLOR_CYAN}; text-transform: uppercase; letter-spacing: 1px; }}
    
    /* BUTTONS */
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
    
    /* VIDEO BACKGROUND */
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
        opacity: 0.5; 
    }}
    .video-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0,0,0,0.85);
        z-index: -1;
    }}
    
    /* STORE MOCKUPS - Centered logos, larger on t-shirt */
    .mockup-container {{
        position: relative;
        width: 100%;
        height: 400px;
        background-color: #111;
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
        opacity: 0.7;
    }}
    .mockup-logo {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 10;
        width: 200px;
        filter: drop-shadow(0 0 10px rgba(0,0,0,0.8));
    }}
    .tee-logo {{ width: 250px !important; }}  /* Larger on t-shirt */
    
    /* CARDS */
    .content-card {{
        background-color: {COLOR_SECONDARY};
        padding: 25px;
        border-left: 3px solid {COLOR_ACCENT};
        margin-bottom: 20px;
        border: 1px solid #222;
    }}
    .news-item {{
        padding: 15px 0;
        border-bottom: 1px solid #333;
        color: #ADD8E6;
        font-family: 'Space Mono', monospace;
        font-size: 0.9rem;
    }}
    /* Gallery expanded */
    .expanded-image {{ width: 100%; max-height: 80vh; object-fit: contain; }}
</style>
""", unsafe_allow_html=True)

# --- BACKGROUND VIDEO ---
st.markdown("""
<div class="video-bg">
    <iframe src="https://www.youtube.com/embed/ZeFchP2PrW0?controls=0&showinfo=0&rel=0&autoplay=1&loop=1&mute=1&playlist=ZeFchP2PrW0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
</div>
<div class="video-overlay"></div>
""", unsafe_allow_html=True)

# --- AUDIO (Tone.js) ---
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
            Tone.Transport.bpm.value = 124;
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
        "container": {"padding": "0", "background-color": "rgba(0,0,0,0.9)", "border-bottom": f"1px solid {COLOR_ACCENT}"},
        "nav-link": {"font-size": "15px", "text-transform": "uppercase", "font-weight": "bold", "color": "#fff", "margin":"0px"},
        "nav-link-selected": {"background-color": "transparent", "color": COLOR_CYAN, "border-bottom": f"3px solid {COLOR_CYAN}"}
    }
)

# Sync session state
if menu_options.index(selected) != st.session_state.page_index:
    st.session_state.page_index = menu_options.index(selected)
    st.session_state.expanded_gallery = None

# --- CONTENT ---

if selected == "HOME":
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"<div>{TNF_LOGO_SVG}</div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='color:{COLOR_TEXT}; margin-top:-20px; letter-spacing: 2px;'>TUESDAY NIGHT FREAK</h2>", unsafe_allow_html=True)
        st.markdown("### ARCHITECTS OF THE ANALOGUE SIGNAL")
        st.markdown("""
        <div style="font-size: 1.1rem; line-height: 1.6; color: #ddd; border-left: 2px solid #00f7ff; padding-left: 15px;">
        **Tuesdaynightfreak** is a sonic movement dedicated to the preservation of hardware-based performance. 
        <br><br>
        We exist at the intersection of machine precision and human improvisation. 
        We reject the digital perfection of modern EDM in favor of the analogue error.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        with b1:
            st.button("LATEST RELEASE", on_click=set_page, args=(1,))
        with b2:
            st.button("TOUR DATES", on_click=set_page, args=(3,))

    with col2:
        st.markdown("### LATEST NEWS")
        st.markdown("""
        <div class="news-item">
            <strong>NEW EP 'VOLTAGE CONTROL'</strong><br>
            Available now on all streaming platforms and limited 12" vinyl.
        </div>
        <div class="news-item">
            <strong>EUROPEAN TOUR CONFIRMED</strong><br>
            Winter 2025 dates announced for London, Berlin, and Amsterdam.
        </div>
        <div class="news-item">
            <strong>HKR LABEL NIGHT</strong><br>
            Join us at Panorama Bar for the official label showcase.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### JOIN THE FAMILY")
        with st.form("home_signup"):
            email = st.text_input("EMAIL ADDRESS")
            if st.form_submit_button("SIGN UP"):
                st.markdown(f'<meta http-equiv="refresh" content="0;url=mailto:tuesdaynightfreak@gmail.com?subject=Newsletter%20Signup&body=Add%20me:%20{email}">', unsafe_allow_html=True)

elif selected == "MUSIC":
    st.title("DISCOGRAPHY")
    
    # Improved artwork from search
    songs = [
        {"title": "System Failure", "label": "House Keeping Rec", "cat": "HKR004", "cover": "https://thumbs.dreamstime.com/b/overgrown-modular-synth-enchanted-forest-setting-s-ai-masterpiece-vintage-synthesizer-covered-lush-moss-delicate-408915293.jpg"},
        {"title": "Analog Dreams", "label": "Tresor Records", "cat": "TR-291", "cover": "https://thumbs.dreamstime.com/b/futuristic-modular-synthesizer-transparent-casing-striking-image-cutting-edge-featuring-reveals-its-intricate-inner-347695422.jpg"},
        {"title": "Voltage Control", "label": "Ostgut Ton", "cat": "OSTGUT-55", "cover": "https://thumbs.dreamstime.com/b/abstract-pop-art-neon-illustration-mosaic-pixel-vibrant-futuristic-d-artwork-techno-house-album-art-depicting-people-400762655.jpg"},
        {"title": "Modular State", "label": "Klockworks", "cat": "KW-22", "cover": "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=122231043668119738"}
    ]
    
    for track in songs:
        c1, c2, c3 = st.columns([1, 3, 1])
        with c1:
            st.image(track['cover'], width=150, alt=track['title'] + " album cover")
        with c2:
            st.subheader(track['title'])
            st.caption(f"{track['label']} // {track['cat']}")
            st.write("Deep, driving, analog rhythms designed for the floor.")
        with c3:
            st.button("STREAM / BUY", key=track['cat'])
        st.divider()

elif selected == "HKR":
    c1, c2 = st.columns([1, 3])
    with c1:
        st.markdown(HKR_LOGO_SVG, unsafe_allow_html=True)
    with c2:
        st.title("HOUSE KEEPING RECORDS")
        st.markdown("#### EST. 2023 // DEEP HOUSE & TECHNO // VINYL ONLY")
        st.write("House Keeping Records is a sanctuary for authentic deep house and raw techno. Dedicated to the craft of vinyl and the culture of the underground.")
    
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

elif selected == "EVENTS":
    st.title("TOUR DATES")
    
    # Improved flyers from search
    events = [
        {"date": "NOV 04", "city": "AMSTERDAM", "venue": "SHELTER", "flyer": "https://imgproxy.ra.co/_/quality:66/aHR0cHM6Ly9pbWFnZXMucmEuY28vOGQyNjE1OTFiOTg1N2JhMDlmZDMzY2NkYmViZWY3OWM5ODlkYWQwNS5qcGc="},
        {"date": "NOV 11", "city": "LONDON", "venue": "FOLD", "flyer": "https://imgproxy.ra.co/_/quality:66/aHR0cHM6Ly9pbWFnZXMucmEuY28vYmNiOTcwMzAwYjQ1MWY3Njc3NzUzYTdiNjAxODU4NjY0NmU0OTA1Yy5qcGc="},
        {"date": "NOV 18", "city": "MELBOURNE", "venue": "REVOLVER", "flyer": "https://imgproxy.ra.co/_/quality:50/aHR0cHM6Ly9pbWFnZXMucmEuY28vMTNmNzNjMTBkMWJlMDRiODA5YWQ4ZTU0ODc1ZjM2M2Q3YThlY2Y5Zi5wbmc="},
        {"date": "DEC 02", "city": "PARIS", "venue": "REX CLUB", "flyer": "https://imgproxy.ra.co/_/quality:66/aHR0cHM6Ly9pbWFnZXMucmEuY28vZTgxMzJkZWNkODA5MzMzMTc4ODRhMDhjYjQwOTY0ZjE2NzZiMDYzOC5wbmc="}
    ]
    
    for event in events:
        c1, c2, c3 = st.columns([2, 3, 1])
        with c1:
            st.image(event['flyer'], use_column_width=True, alt=event['venue'] + " event flyer")
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
        if st.button("CHECKOUT (EMAIL INQUIRY)"):
             st.markdown(f'<meta http-equiv="refresh" content="0;url=mailto:tuesdaynightfreak@gmail.com?subject=Merch%20Order&body=I%20would%20like%20to%20buy:%20{", ".join(st.session_state.cart)}">', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    
    # Merch 1: T-Shirt (Larger logo)
    with c1:
        st.markdown(f"""
        <div class="mockup-container">
            <img src="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=600&q=80" class="mockup-bg" alt="TNF Core Tee">
            <div class="mockup-logo tee-logo" style="transform: translate(-50%, -50%) scale(0.4);">{TNF_LOGO_SVG}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**TNF CORE TEE**")
        st.caption("Heavyweight Cotton")
        if st.button("ADD TO CART €35", key="m1"):
            add_to_cart("TNF Core Tee")

    # Merch 2: Hoodie
    with c2:
        st.markdown(f"""
        <div class="mockup-container">
            <img src="https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=600&q=80" class="mockup-bg" alt="HKR Label Hoodie">
            <div class="mockup-logo" style="transform: translate(-50%, -50%) scale(0.5);">{HKR_LOGO_SVG}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**HKR LABEL HOODIE**")
        st.caption("Oversized Fit")
        if st.button("ADD TO CART €65", key="m2"):
            add_to_cart("HKR Hoodie")

    # Merch 3: Slipmats
    with c3:
        st.markdown(f"""
        <div class="mockup-container">
            <img src="https://images.unsplash.com/photo-1603048588665-791ca8aea617?auto=format&fit=crop&w=600&q=80" class="mockup-bg" alt="Pro Slipmats">
            <div class="mockup-logo" style="transform: translate(-50%, -50%) scale(0.6);">{SLIPMAT_ICON_SVG}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**PRO SLIPMATS**")
        st.caption("Anti-static Pair")
        if st.button("ADD TO CART €20", key="m3"):
            add_to_cart("Slipmats")

elif selected == "GALLERY":
    st.title("VISUAL ARCHIVE")
    
    # Using VALID Unsplash URLs to fix broken image error
    images = [
        {"url": "https://images.unsplash.com/photo-1598275529124-b1c4b786f1e2?q=80&w=800&auto=format&fit=crop", "cap": "EURORACK PATCHING"},
        {"url": "https://images.unsplash.com/photo-1571266028243-371695063ad6?q=80&w=800&auto=format&fit=crop", "cap": "WAREHOUSE CROWD"},
        {"url": "https://images.unsplash.com/photo-1550291652-6ea9114a47b1?q=80&w=800&auto=format&fit=crop", "cap": "LIVE RIG"},
        {"url": "https://images.unsplash.com/photo-1619967657960-983b6329c370?q=80&w=800&auto=format&fit=crop", "cap": "SEQUENCER DETAIL"},
    ]
    
    # Fixed gallery with back button
    if 'expanded_gallery' in st.session_state and st.session_state.expanded_gallery is not None:
        idx = st.session_state.expanded_gallery
        st.image(images[idx]['url'] + "?w=1600", caption=images[idx]['cap'], use_column_width=True, alt=images[idx]['cap'])
        if st.button("← BACK TO GALLERY"):
            st.session_state.expanded_gallery = None
    else:
        c1, c2 = st.columns(2)
        for i, item in enumerate(images):
            with (c1 if i % 2 == 0 else c2):
                st.image(item['url'], caption=item['cap'], use_column_width=True, alt=item['cap'])
                if st.button("ENLARGE", key=f"enlarge_{i}"):
                    st.session_state.expanded_gallery = i

elif selected == "ABOUT":
    c1, c2 = st.columns([2,1])
    with c1:
        st.title("BIOGRAPHY")
        st.write("""
        **Tuesdaynightfreak** is an electronic music project established in Melbourne, Australia.
        
        Drawing influence from the stark industrialism of Berlin and the soulful rhythms of Detroit, the project explores the boundaries of hardware sequencing. It is a reaction against the predictability of digital production.
        
        From the smoky basements of Revolver to the concrete halls of Tresor, Tuesdaynightfreak delivers a sound that is distinct, raw, and uncompromising.
        """)
    with c2:
        st.markdown("#### CONTACT")
        st.code("tuesdaynightfreak@gmail.com")
        
        with st.form("contact_form"):
            email = st.text_input("Your Email")
            msg = st.text_area("Message")
            if st.form_submit_button("SEND"):
                st.markdown(f'<meta http-equiv="refresh" content="0;url=mailto:tuesdaynightfreak@gmail.com?subject=General%20Inquiry&body={msg}">', unsafe_allow_html=True)

elif selected == "SYSTEM":
    st.title("SYSTEM ACCESS")
    pwd = st.text_input("ENTER AUTH CODE", type="password")
    if pwd == "admin123":
        st.success("ACCESS GRANTED")

# Advanced SEO: JSON-LD structured data
st.markdown("""
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "MusicGroup",
  "name": "Tuesdaynightfreak",
  "url": "https://tuesdaynightfreak.streamlit.app/",
  "genre": "Techno",
  "foundingLocation": {
    "@type": "Place",
    "name": "Melbourne, Australia"
  },
  "member": {
    "@type": "Person",
    "name": "Tuesdaynightfreak"
  },
  "album": [
    {"@type": "MusicAlbum", "name": "Voltage Control"},
    {"@type": "MusicAlbum", "name": "System Failure"}
  ]
}
</script>
""", unsafe_allow_html=True)
