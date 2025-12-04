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
# TNF Logo
TNF_LOGO_SVG = f"""
<svg width="100%" height="100%" viewBox="0 0 300 90" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
    <text x="4" y="65" font-family="Arial, sans-serif" font-weight="900" font-size="72" fill="{COLOR_CYAN}" opacity="0.6" letter-spacing="-4">TNF</text>
    <text x="-2" y="65" font-family="Arial, sans-serif" font-weight="900" font-size="72" fill="{COLOR_ACCENT}" opacity="0.7" letter-spacing="-4">TNF</text>
    <text x="0" y="65" font-family="Arial, sans-serif" font-weight="900" font-size="72" fill="{COLOR_TEXT}" letter-spacing="-4">TNF</text>
    <rect x="160" y="25" width="8" height="40" fill="{COLOR_ACCENT}"/>
    <rect x="175" y="25" width="8" height="40" fill="{COLOR_CYAN}"/>
    <circle cx="210" cy="45" r="12" stroke="{COLOR_TEXT}" stroke-width="3" fill="none"/>
    <line x1="0" y1="85" x2="300" y2="85" stroke="{COLOR_CYAN}" stroke-width="2" opacity="0.8"/>
</svg>
"""

# House Keeping Records Logo
HKR_LOGO_SVG = f"""
<svg width="100%" height="100%" viewBox="0 0 150 150" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
    <rect x="5" y="5" width="140" height="140" stroke="{COLOR_TEXT}" stroke-width="5" fill="none"/>
    <path d="M20 60 L75 20 L130 60" stroke="{COLOR_ACCENT}" stroke-width="5" fill="none"/>
    <circle cx="75" cy="95" r="30" stroke="{COLOR_CYAN}" stroke-width="4" fill="none"/>
    <rect x="72" y="85" width="6" height="20" fill="{COLOR_CYAN}"/>
    <text x="75" y="135" font-family="monospace" font-size="14" fill="#888" text-anchor="middle" font-weight="bold">EST. 2023</text>
</svg>
"""

# Slipmat Icon
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
# Using a dedicated key for the menu selection to prevent sync issues
if 'menu_selection' not in st.session_state:
    st.session_state.menu_selection = "HOME"

# --- NAVIGATION CALLBACK ---
# This function fixes the "double click" issue by updating the state directly
def set_page(index):
    st.session_state.page_index = index
    # Map index to menu option string
    options = ["HOME", "MUSIC", "HKR", "EVENTS", "STORE", "GALLERY", "ABOUT", "SYSTEM"]
    if 0 <= index < len(options):
        st.session_state.menu_selection = options[index]

def add_to_cart(item):
    st.session_state.cart.append(item)
    st.toast(f"Added {item} to cart!", icon="🛒")

# --- CUSTOM CSS ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Space+Mono:wght@400;700&display=swap');
    
    .stApp {{ background-color: {COLOR_BG}; color: {COLOR_TEXT}; font-family: 'Inter', sans-serif; }}
    
    /* REMOVE WHITE GAPS around content */
    .block-container {{
        padding-top: 0rem !important;
        padding-bottom: 5rem !important;
        max-width: 100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }}
    /* Add padding back to the main content area only */
    div[data-testid="stVerticalBlock"] > div:first-of-type {{
        padding-top: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }}
    
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
    .stButton>button:hover, .stLinkButton>a:hover {{
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
        height: 56.25vw; 
        min-height: 100vh;
        min-width: 177.77vh;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        opacity: 0.4; /* Darker opacity for readability */
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
        opacity: 0.8;
    }}
    .mockup-logo {{
        position: absolute;
        top: 50%; /* Perfectly centered vertically */
        left: 50%; /* Perfectly centered horizontally */
        transform: translate(-50%, -50%);
        z-index: 10;
        filter: drop-shadow(0 0 10px rgba(0,0,0,0.8));
        width: 120px; /* Adjusted size for better fit */
        height: auto;
    }}

    /* Cards */
    .content-card {{
        background-color: {COLOR_SECONDARY};
        padding: 25px;
        border-left: 3px solid {COLOR_ACCENT};
        margin-bottom: 20px;
        border: 1px solid #222;
    }}
    
</style>
""", unsafe_allow_html=True)

# --- BACKGROUND VIDEO & AUDIO ---
# Using a reliable abstract geometric loop
st.markdown("""
<div class="video-bg">
    <iframe src="https://www.youtube.com/embed/49bK4n449K4?controls=0&showinfo=0&rel=0&autoplay=1&loop=1&mute=1&playlist=49bK4n449K4" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
</div>
<div class="video-overlay"></div>
""", unsafe_allow_html=True)

# Audio Autostart
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
            Tone.Transport.bpm.value = 125;
            Tone.Transport.start();
        }
    });
</script>
""", height=0)


# --- NAVIGATION ---
menu_options = ["HOME", "MUSIC", "HKR", "EVENTS", "STORE", "GALLERY", "ABOUT", "SYSTEM"]

# Explicitly set styles to remove padding
menu_styles = {
    "container": {"padding": "0", "background-color": COLOR_BG, "border-bottom": "1px solid #333"},
    "nav-link": {"font-size": "14px", "text-transform": "uppercase", "font-weight": "bold", "color": "#fff", "margin":"0px"},
    "nav-link-selected": {"background-color": "transparent", "color": COLOR_CYAN, "border-bottom": f"2px solid {COLOR_CYAN}"}
}

# Ensure session state matches selection if updated elsewhere
default_index = st.session_state.page_index

selected = option_menu(
    menu_title=None,
    options=menu_options,
    icons=["house", "disc", "vinyl", "calendar3", "bag", "images", "info-circle", "cpu"],
    default_index=default_index,
    orientation="horizontal",
    styles=menu_styles,
    key="main_menu" # Key is important for state stability
)

# Update state based on menu selection
if selected != menu_options[st.session_state.page_index]:
   st.session_state.page_index = menu_options.index(selected)
   st.rerun()

# --- CONTENT ---

if selected == "HOME":
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        # Smaller logo on Home Page
        st.markdown(f"<div style='width: 200px;'>{TNF_LOGO_SVG}</div>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:white; margin-top:-10px;'>TUESDAY NIGHT FREAK</h2>", unsafe_allow_html=True)
        st.markdown("### DEFINING THE FUTURE OF ANALOGUE HOUSE")
        st.markdown("""
        <div style="font-size: 1.1rem; line-height: 1.6; color: #ddd;">
        Established in the underground, Tuesdaynightfreak is a global electronic music project dedicated to the preservation and evolution of hardware-based performance. 
        <br><br>
        We exist at the intersection of machine precision and human improvisation. No laptops, no sync buttons—just raw voltage and rhythm. 
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
        <div style="padding: 15px 0; border-bottom: 1px solid #333; color: #ADD8E6;">
            <strong>NEW EP 'VOLTAGE CONTROL'</strong><br>
            Available now on all streaming platforms and limited 12" vinyl.
        </div>
        <div style="padding: 15px 0; border-bottom: 1px solid #333; color: #ADD8E6;">
            <strong>EUROPEAN TOUR CONFIRMED</strong><br>
            Winter 2025 dates announced for London, Berlin, and Amsterdam.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### JOIN THE FAMILY")
        with st.form("home_signup"):
            email = st.text_input("EMAIL ADDRESS")
            if st.form_submit_button("SIGN UP"):
                 st.markdown(f'<meta http-equiv="refresh" content="0;url=mailto:tuesdaynightfreak@gmail.com?subject=Newsletter%20Signup&body=Sign%20me%20up!%20Email:%20{email}">', unsafe_allow_html=True)

elif selected == "MUSIC":
    st.title("DISCOGRAPHY")
    
    # Mock Data
    songs_data = [
        {"title": "System Failure", "label": "House Keeping Rec", "cat": "HKR004", "cover": "https://placehold.co/400x400/111/FFF?text=HKR004"},
        {"title": "Analog Dreams", "label": "Tresor Records", "cat": "TR-291", "cover": "https://placehold.co/400x400/000/00f7ff?text=TR-291"},
        {"title": "Voltage Control", "label": "Ostgut Ton", "cat": "OSTGUT-55", "cover": "https://placehold.co/400x400/222/FF0033?text=OSTGUT"},
        {"title": "Modular State", "label": "Klockworks", "cat": "KW-22", "cover": "https://placehold.co/400x400/000/FFF?text=KW-22"}
    ]
    
    for track in songs_data:
        c1, c2, c3 = st.columns([1, 3, 1])
        with c1:
            st.image(track['cover'], width=150)
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
        # Smaller logo for HKR page
        st.markdown(f"<div style='width: 150px;'>{HKR_LOGO_SVG}</div>", unsafe_allow_html=True)
    with c2:
        st.title("HOUSE KEEPING RECORDS")
        st.markdown("#### EST. 2023 // DEEP HOUSE & TECHNO // VINYL ONLY")
        st.write("House Keeping Records is a sanctuary for authentic deep house and raw techno. We are dedicated to the craft of vinyl and the culture of the underground. Quality over quantity, always.")
    
    st.divider()
    st.subheader("CATALOGUE")
    
    hkr_releases = [
        {"cat": "HKR005", "artist": "VARIOUS", "title": "RHYTHM GENERATOR EP", "cover": "https://placehold.co/400x400/000/FFF?text=HKR005"},
        {"cat": "HKR004", "artist": "TUESDAYNIGHTFREAK", "title": "MODULAR LOOP 01", "cover": "https://placehold.co/400x400/111/00f7ff?text=HKR004"},
        {"cat": "HKR003", "artist": "ACID JUNKIE", "title": "GRID SEQUENCER", "cover": "https://placehold.co/400x400/222/FF0033?text=HKR003"}
    ]
    
    for item in hkr_releases:
        c1, c2, c3 = st.columns([1, 3, 1])
        with c1:
            st.image(item['cover'], width=120)
        with c2:
            st.markdown(f"**{item['cat']}**")
            st.markdown(f"**{item['artist']}** — {item['title']}")
        with c3:
            st.button("PURCHASE VINYL", key=item['cat'])

elif selected == "EVENTS":
    st.title("TOUR DATES")
    
    events_data = [
        {"date": "NOV 04", "city": "AMSTERDAM", "venue": "SHELTER", "flyer": "https://placehold.co/600x300/000/FFF?text=ADE+2025"},
        {"date": "NOV 11", "city": "LONDON", "venue": "FOLD", "flyer": "https://placehold.co/600x300/111/FF0033?text=LONDON+RAVE"},
        {"date": "NOV 18", "city": "MELBOURNE", "venue": "REVOLVER", "flyer": "https://placehold.co/600x300/000/00f7ff?text=REVOLVER+SUNDAYS"},
        {"date": "DEC 02", "city": "PARIS", "venue": "REX CLUB", "flyer": "https://placehold.co/600x300/222/FFF?text=REX+CLUB"}
    ]
    
    for event in events_data:
        c1, c2, c3 = st.columns([2, 3, 1])
        with c1:
            st.image(event['flyer'], use_column_width=True)
        with c2:
            st.markdown(f"### {event['date']}")
            st.markdown(f"**{event['city']}** // {event['venue']}")
        with c3:
            # Use st.link_button for reliable navigation or mock action
            st.button("TICKETS", key=event['city'])
        st.divider()

elif selected == "STORE":
    st.title("OFFICIAL MERCHANDISE")
    
    if st.session_state.cart:
        st.info(f"CART: {len(st.session_state.cart)} ITEMS")
        if st.button("CHECKOUT (EMAIL)"):
             st.markdown(f'<meta http-equiv="refresh" content="0;url=mailto:tuesdaynightfreak@gmail.com?subject=Merch%20Order&body=I%20would%20like%20to%20buy:%20{", ".join(st.session_state.cart)}">', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    
    # Merch 1: T-Shirt (Better Centering)
    with c1:
        st.markdown(f"""
        <div class="mockup-container">
            <img src="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=600&q=80" class="mockup-bg">
            <div class="mockup-logo" style="transform: translate(-50%, -50%) scale(0.4); top: 40%;">{TNF_LOGO_SVG}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**TNF CORE TEE**")
        st.caption("Heavyweight Cotton")
        if st.button("ADD TO CART €35", key="m1"):
            add_to_cart("TNF Core Tee")

    # Merch 2: Hoodie (Better Centering)
    with c2:
        st.markdown(f"""
        <div class="mockup-container">
            <img src="https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=600&q=80" class="mockup-bg">
            <div class="mockup-logo" style="transform: translate(-50%, -50%) scale(0.6); top: 40%;">{HKR_LOGO_SVG}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**HKR LABEL HOODIE**")
        st.caption("Oversized Fit")
        if st.button("ADD TO CART €65", key="m2"):
            add_to_cart("HKR Hoodie")

    # Merch 3: Slipmats (Better Centering)
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
    st.title("VISUAL ARCHIVE")
    st.caption("CAPTURED LIVE AND IN STUDIO")
    
    # Replaced all internal image references with robust Unsplash URLs
    gallery_images = [
        {"url": "https://images.unsplash.com/photo-1598275529124-b1c4b786f1e2?q=80&w=800&auto=format&fit=crop", "cap": "EURORACK PATCHING"},
        {"url": "https://images.unsplash.com/photo-1571266028243-371695063ad6?q=80&w=800&auto=format&fit=crop", "cap": "WAREHOUSE CROWD"},
        {"url": "https://images.unsplash.com/photo-1550291652-6ea9114a47b1?q=80&w=800&auto=format&fit=crop", "cap": "LIVE RIG"},
        {"url": "https://images.unsplash.com/photo-1619967657960-983b6329c370?q=80&w=800&auto=format&fit=crop", "cap": "SEQUENCER DETAIL"},
        {"url": "https://images.unsplash.com/photo-1514525253440-b393452e8d26?q=80&w=800&auto=format&fit=crop", "cap": "CLUB ATMOSPHERE"},
        {"url": "https://images.unsplash.com/photo-1563841930606-67e26ce48428?q=80&w=800&auto=format&fit=crop", "cap": "VINYL SELECTION"}
    ]
    
    c1, c2 = st.columns(2)
    for i, item in enumerate(gallery_images):
        with (c1 if i % 2 == 0 else c2):
            st.image(item['url'], caption=item['cap'], use_column_width=True)

elif selected == "ABOUT":
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
