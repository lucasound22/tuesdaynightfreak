import streamlit as st
from streamlit_option_menu import option_menu
import time

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
    
</style>
""", unsafe_allow_html=True)

# --- BACKGROUND VIDEO & AUDIO ---
st.markdown("""
<div class="video-bg">
    <iframe src="https://www.youtube.com/embed/qC0vDKVPCrw?controls=0&showinfo=0&rel=0&autoplay=1&loop=1&mute=1&playlist=qC0vDKVPCrw" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
</div>
<div class="video-overlay"></div>
""", unsafe_allow_html=True)

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
        We are an independent electronic music project and culture crew bridging the gap between 
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
    # Content remains the same as it was functional
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
    
    # Improved look for flyers using high-contrast mock images
    events_data = [
        {"date": "NOV 04", "city": "AMSTERDAM", "venue": "SHELTER", "image": "https://images.unsplash.com/photo-1517457371957-c7385e05a769?q=80&w=800&auto=format&fit=crop"},
        {"date": "NOV 11", "city": "LONDON", "venue": "FOLD", "image": "https://images.unsplash.com/photo-1543851505-18ff86725350?q=80&w=800&auto=format&fit=crop"},
        {"date": "NOV 18", "city": "MELBOURNE", "venue": "REVOLVER", "image": "https://images.unsplash.com/photo-1599321355410-0254c0af474a?q=80&w=800&auto=format&fit=crop"},
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
    
    # Merch 1: T-Shirt with BIGGER Logo Overlay
    with c1:
        st.markdown(f"""
        <div class="mockup-container">
            <img src="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=600&q=80" class="mockup-bg">
            <div class="mockup-logo" style="transform: translate(-50%, -50%) scale(0.6);">{TNF_LOGO_SVG}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**TNF CORE TEE**")
        st.caption("Heavyweight Cotton")
        if st.button("ADD TO CART €35", key="m1"):
            add_to_cart("TNF Core Tee")

    # Merch 2: Hoodie with HKR Logo
    with c2:
        st.markdown(f"""
        <div class="mockup-container">
            <img src="https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=600&q=80" class="mockup-bg">
            <div class="mockup-logo" style="transform: translate(-50%, -50%) scale(0.7);">{HKR_LOGO_SVG}</div>
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
            <img src="https://images.unsplash.com/photo-1603048588665-791ca8aea617?auto=format&fit=crop&w=600&q=80" class="mockup-bg">
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
    
    # Updated to be high-contrast and synth/club focused like Defected's content
    gallery_images = [
        {"url": "https://images.unsplash.com/photo-1506450682137-f4a471413a17?q=80&w=800&auto=format&fit=crop", "cap": "MODULAR SYNTHESIS"},
        {"url": "https://images.unsplash.com/photo-1510928230230-e837894ff54c?q=80&w=800&auto=format&fit=crop", "cap": "LIVE PERFORMANCE IN BERLIN"},
        {"url": "https://images.unsplash.com/photo-1534005888251-140a324032d8?q=80&w=800&auto=format&fit=crop", "cap": "DRUM MACHINE SEQUENCE"},
        {"url": "https://images.unsplash.com/photo-1543851505-18ff86725350?q=80&w=800&auto=format&fit=crop", "cap": "CROWD MOMENTS"},
        {"url": "https://images.unsplash.com/photo-1571266028243-371695063ad6?q=80&w=800&auto=format&fit=crop", "cap": "VINYL MIXING"},
        {"url": "https://images.unsplash.com/photo-1563841930606-67e26ce48428?q=80&w=800&auto=format&fit=crop", "cap": "STUDIO SESSION"}
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
        
        Drawing influence from the stark industrialism of Berlin and the soulful rhythms of Detroit, the project explores the boundaries of hardware sequencing. It is a reaction against the predictability of digital production—a celebration of the machine's inherent instability.
        
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
