import streamlit as st
from streamlit_option_menu import option_menu
import time

# --- CONFIGURATION & PALETTE ---
COLOR_BG = "#080808"
COLOR_TEXT = "#F0F0F0"
COLOR_ACCENT = "#FF0033"  # Acid Red
COLOR_CYAN = "#00f7ff"    # Cyberpunk Splash
COLOR_SECONDARY = "#141414"

# --- BRANDING SVGs ---
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

# --- PAGE SETUP & STATE MANAGEMENT (CMS DATA) ---
st.set_page_config(
    page_title="TUESDAYNIGHTFREAK | OFFICIAL",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session State
if 'page_index' not in st.session_state: st.session_state.page_index = 0
if 'cart' not in st.session_state: st.session_state.cart = []
if 'mixcloud_url' not in st.session_state: 
    # Mixcloud URL setup for autoplay (may still require user click due to browser policies)
    st.session_state.mixcloud_url = "https://www.mixcloud.com/widget/iframe/?hide_cover=1&mini=1&light=0&feed=%2Fcarlcox%2Fcarl-cox-global-722%2F&autoplay=1"

# 1. SITE COPY
if 'site_content' not in st.session_state:
    st.session_state.site_content = {
        "home_headline": "THE SOUND OF HARDWARE SOUL",
        "home_body": "We are an independent electronic music project and culture crew bridging the gap between Berlin's concrete basements and Melbourne's warehouse soul. We embrace the **analogue error**.",
        "about_bio": "**Tuesdaynightfreak** is an electronic music project established in Melbourne, Australia.\n\nDrawing influence from the stark industrialism of Berlin and the soulful rhythms of Detroit, the project explores the boundaries of hardware sequencing. It is a reaction against the predictability of digital production—a celebration of the machine's inherent instability.",
        "system_update_1": "**NEW RELEASE:** 'VOLTAGE CONTROL' EP OUT NOW VIA OSTGUT TON.",
        "system_update_2": "**TOUR ANNOUNCEMENT:** EUROPEAN DATES CONFIRMED FOR WINTER 2025."
    }

# 2. STORE ITEMS
if 'merch_data' not in st.session_state:
    st.session_state.merch_data = [
        {"name": "TNF CORE TEE", "desc": "Heavyweight Cotton", "price": 35, "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=600&q=80", "logo_svg": TNF_LOGO_SVG, "svg_scale": 0.6},
        {"name": "HKR LABEL HOODIE", "desc": "Oversized Fit", "price": 65, "image_url": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=600&q=80", "logo_svg": HKR_LOGO_SVG, "svg_scale": 0.7},
        {"name": "PRO SLIPMATS (PAIR)", "desc": "Anti-static Pair", "price": 20, "image_url": "https://images.unsplash.com/photo-1603048588665-791ca8aea617?auto=format&fit=crop&w=600&q=80", "logo_svg": SLIPMAT_ICON_SVG, "svg_scale": 0.8},
    ]

# 3. HKR RELEASES
if 'hkr_data' not in st.session_state:
    st.session_state.hkr_data = [
        {"cat": "HKR005", "artist": "VARIOUS", "title": "RHYTHM GENERATOR EP"},
        {"cat": "HKR004", "artist": "TUESDAYNIGHTFREAK", "title": "MODULAR LOOP 01"},
        {"cat": "HKR003", "artist": "ACID JUNKIE", "title": "GRID SEQUENCER"}
    ]

# 4. EVENTS (FIXED: Added 'image_url' to default structure)
if 'events_data' not in st.session_state:
    st.session_state.events_data = [
        {"date": "NOV 04", "city": "AMSTERDAM", "venue": "SHELTER", "image_url": "https://images.unsplash.com/photo-1517457371957-c7385e05a769?q=80&w=800&auto=format&fit=crop"},
        {"date": "NOV 11", "city": "LONDON", "venue": "FOLD", "image_url": "https://images.unsplash.com/photo-1543851505-18ff86725350?q=80&w=800&auto=format&fit=crop"},
        {"date": "NOV 18", "city": "MELBOURNE", "venue": "REVOLVER", "image_url": "https://images.unsplash.com/photo-1599321355410-0254c0af474a?q=80&w=800&auto=format&fit=crop"},
    ]

# 5. GALLERY (FIXED: Standardized key to 'url')
if 'gallery_data' not in st.session_state:
    st.session_state.gallery_data = [
        {"url": "https://images.unsplash.com/photo-1506450682137-f4a471413a17?q=80&w=800&auto=format&fit=crop", "cap": "MODULAR SYNTHESIS"},
        {"url": "https://images.unsplash.com/photo-1510928230230-e837894ff54c?q=80&w=800&auto=format&fit=crop", "cap": "LIVE PERFORMANCE IN BERLIN"},
        {"url": "https://images.unsplash.com/photo-1534005888251-140a324032d8?q=80&w=800&auto=format&fit=crop", "cap": "DRUM MACHINE SEQUENCE"},
    ]


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

    /* 2. LAYOUT & PADDING FIXES */
    .block-container {{
        padding-top: 0rem !important;
        padding-bottom: 5rem !important;
        max-width: 100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }}
    div[data-testid="stVerticalBlock"] > div:first-of-type {{
        padding-top: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }}
    
    /* TYPOGRAPHY */
    h1, h2, h3 {{ font-weight: 900; text-transform: uppercase; letter-spacing: -1px; }}
    
    /* BUTTONS */
    .stButton>button {{
        background: {COLOR_CYAN}; 
        color: {COLOR_BG}; 
        font-weight: 900; 
        border-radius: 0;
        border: 2px solid {COLOR_CYAN};
        transition: 0.3s;
        width: 100%;
    }}
    .stButton>button:hover {{
        background: {COLOR_ACCENT};
        color: {COLOR_TEXT};
        border-color: {COLOR_ACCENT};
        box-shadow: 0 0 15px {COLOR_ACCENT};
    }}

    /* MENU FIXES */
    .st-emotion-cache-163lq9m {{ 
        border-bottom: 3px solid {COLOR_CYAN};
        padding: 0 2rem;
    }}
    .st-emotion-cache-163lq9m a {{ color: {COLOR_TEXT}; }} /* Non-selected menu text color */
    .st-emotion-cache-163lq9m .st-emotion-cache-1n76hnz {{ color: {COLOR_CYAN}; }} /* Selected menu item */


    /* ADMIN PANEL FIXES (Input & Tab Visibility) */
    .admin-box {{
        background-color: #1a1a1a;
        padding: 20px;
        border: 1px solid #333;
        border-radius: 5px;
        margin-bottom: 20px;
    }}
    input, textarea {{
        color: #fff !important; 
        background-color: #222 !important;
        border: 1px solid #444 !important;
    }}
    [data-testid="stTabs"] button {{
        color: {COLOR_TEXT} !important; 
        background-color: #1a1a1a;
        border-bottom: 3px solid #333;
    }}
    [data-testid="stTabs"] button[aria-selected="true"] {{
        color: {COLOR_CYAN} !important; 
        border-bottom-color: {COLOR_CYAN};
        background-color: {COLOR_BG};
    }}


    /* VIDEO BACKGROUND FIX (Ensures it shows and is behind content) */
    .video-bg {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -2;
        overflow: hidden;
    }}
    .video-bg iframe {{
        width: 100vw;
        height: 56.25vw; /* 16:9 ratio */
        min-height: 100vh;
        min-width: 177.77vh; /* 16:9 ratio */
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        pointer-events: none;
        opacity: 0.2; /* Subtle background */
    }}
    .video-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.75); /* Darker overlay for text contrast */
        z-index: -1;
    }}

    /* Merch Mockup Container (Fixed for dynamic images) */
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
        top: 50%;
        left: 50%;
        z-index: 10;
        filter: drop-shadow(0 0 10px rgba(0,0,0,0.8));
    }}
    
</style>
""", unsafe_allow_html=True)

# --- BACKGROUND VIDEO & AUDIO (FIXED POSITIONING) ---
# FIX: The video is placed here to ensure it's loaded as the background layer.
st.markdown("""
<div class="video-bg">
    <iframe src="https://www.youtube.com/embed/qC0vDKVPCrw?controls=0&showinfo=0&rel=0&autoplay=1&loop=1&mute=1&playlist=qC0vDKVPCrw" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
</div>
<div class="video-overlay"></div>
""", unsafe_allow_html=True)

# Tone.js for initial user activation cue
st.components.v1.html("""
<script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.min.js"></script>
<script>
    document.addEventListener('click', async () => {
        if (Tone.context.state !== 'running') {
            await Tone.start();
            // Start silent synth cue
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
        "nav-link": {"font-size": "16px", "text-transform": "uppercase", "font-weight": "bold", "color": COLOR_TEXT, "border-radius": "0px"},
        "nav-link-selected": {"background-color": "transparent", "color": COLOR_CYAN, "border-bottom": f"3px solid {COLOR_CYAN}"}
    }
)

# Update page index on selection change to fix double-click issue
if menu_options.index(selected) != st.session_state.page_index:
   set_page(menu_options.index(selected))
   st.rerun()

# ---------------------------------------------
## 🏠 CORE SITE PAGES
# ---------------------------------------------

if selected == "HOME":
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"<div style='width: 300px; height: 90px; margin-bottom: 20px;'>{TNF_LOGO_SVG}</div>", unsafe_allow_html=True)
        # Dynamic Content
        st.markdown(f"### {st.session_state.site_content['home_headline']}")
        st.markdown(f"""
        <div style="font-size: 1.2rem; line-height: 1.6; color: #ddd;">
        {st.session_state.site_content['home_body']}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        with b1: st.button("LATEST RELEASE", on_click=set_page, args=(1,))
        with b2: st.button("TOUR DATES", on_click=set_page, args=(3,))

    with col2:
        st.markdown("#### SYSTEM UPDATES")
        st.info(st.session_state.site_content['system_update_1'])
        st.info(st.session_state.site_content['system_update_2'])

elif selected == "MUSIC":
    st.title("MUSIC & MIXES")
    st.markdown("### LATEST TRANSMISSION")
    # Dynamic Mixcloud Player
    st.markdown(f"""<iframe width="100%" height="120" src="{st.session_state.mixcloud_url}" frameborder="0" ></iframe>""", unsafe_allow_html=True)
    st.divider()
    
    st.subheader("DISCOGRAPHY")
    releases = [
        {"title": "System Failure", "label": "House Keeping Rec", "cat": "HKR004"},
        {"title": "Analog Dreams", "label": "Tresor Records", "cat": "TR-291"},
        {"title": "Voltage Control", "label": "Ostgut Ton", "cat": "OSTGUT-55"}
    ]
    for r in releases:
        c1, c2, c3, c4 = st.columns([1, 4, 2, 2])
        with c1: st.markdown(f"<div style='width:60px;height:60px;background:#222;border:1px solid #444;border-radius: 4px;'></div>", unsafe_allow_html=True)
        with c2: st.subheader(r['title'])
        with c3: st.caption(f"{r['label']} // {r['cat']}")
        with c4: st.button("STREAM / BUY", key=r['cat'])
        st.divider()

elif selected == "HKR":
    c1, c2 = st.columns([1, 3])
    with c1: st.markdown(f"<div style='width: 120px; height: 120px; margin: auto;'>{HKR_LOGO_SVG}</div>", unsafe_allow_html=True)
    with c2: st.title("HOUSE KEEPING RECORDS"); st.markdown("#### EST. 2023 // DEEP HOUSE & TECHNO // VINYL ONLY"); st.write("House Keeping Records is the dedicated platform for the raw and the deep. Focusing on functional tools for DJs and sonic explorations for heads.")
    
    st.divider()
    st.subheader("CATALOGUE")
    
    for item in st.session_state.hkr_data:
        c1, c2, c3 = st.columns([1, 3, 1])
        with c1: st.markdown(f"**{item['cat']}**")
        with c2: st.markdown(f"**{item['artist']}** — {item['title']}")
        with c3: st.button("PURCHASE VINYL", key=item['cat'])
        st.divider()

elif selected == "EVENTS":
    st.title("UPCOMING DATES")
    
    if not st.session_state.events_data:
        st.info("No events scheduled at this time.")
    
    for event in st.session_state.events_data:
        c1, c2, c3 = st.columns([2, 3, 1])
        with c1:
            # FIX: Using 'image_url' key
            st.image(event['image_url'], caption=f"{event['city']} - {event['venue']}", use_column_width=True)
        with c2:
            st.markdown(f"### {event['date']}")
            st.markdown(f"**{event['city']}** // {event['venue']}")
        with c3:
            st.button("TICKETS", key=event['city'] + event['date'])
        st.divider()

elif selected == "STORE":
    st.title("OFFICIAL MERCHANDISE")
    
    # Cart logic
    if st.session_state.cart:
        st.info(f"🛒 CART: {len(st.session_state.cart)} ITEMS: {', '.join(st.session_state.cart)}")
        if st.button("CHECKOUT (EMAIL ORDER)", type="primary"):
            # Simple mailto link for checkout
            cart_items = ", ".join(st.session_state.cart)
            st.markdown(f'<meta http-equiv="refresh" content="0;url=mailto:tuesdaynightfreak@gmail.com?subject=Merch%20Order&body=I%20would%20like%20to%20buy:%20{cart_items}%0A%0APlease%20send%20payment%20details%20and%20shipping%20information.">', unsafe_allow_html=True)
    
    cols = st.columns(3)
    
    # Dynamic Merch Rendering
    for i, item in enumerate(st.session_state.merch_data):
        with cols[i % 3]:
            # Mockup HTML structure
            st.markdown(f"""
            <div class="mockup-container">
                <img src="{item['image_url']}" class="mockup-bg">
                <div class="mockup-logo" style="transform: translate(-50%, -50%) scale({item['svg_scale']});">{item['logo_svg']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"**{item['name']}**")
            st.caption(item['desc'])
            
            if st.button(f"ADD TO CART €{item['price']}", key=f"m_btn_{i}"):
                st.session_state.cart.append(item['name'])
                st.toast(f"Added {item['name']} to cart!", icon="🛒")

elif selected == "GALLERY":
    st.title("VISUAL ARCHIVE // HARDWARE FOCUS")
    st.caption("RAW VOLTAGE. RAW RHYTHM.")
    
    cols = st.columns(3)
    for i, item in enumerate(st.session_state.gallery_data):
        with cols[i % 3]:
            # FIX: Using 'url' key
            st.image(item['url'], caption=item['cap'], use_column_width=True)
            st.markdown("<br>", unsafe_allow_html=True)

elif selected == "ABOUT":
    st.title("BIOGRAPHY & CONTACT")
    
    c1, c2 = st.columns([2,1])
    with c1:
        st.subheader("PROJECT BIO")
        st.write(st.session_state.site_content['about_bio'])
        st.markdown("<br>")
        st.button("DOWNLOAD PRESS KIT")
    with c2:
        st.subheader("CONTACT US")
        
        # Professional Email Form
        with st.form("contact_form"):
            st.markdown("##### SEND A DIRECT MESSAGE")
            sender_name = st.text_input("Your Name", key="contact_name")
            sender_email = st.text_input("Your Email", key="contact_email")
            message_type = st.selectbox("Message Type", ["Management/Booking", "Demo Submission", "General Inquiry"], key="contact_type")
            message = st.text_area("Your Message", height=150, key="contact_message")
            
            submit_button = st.form_submit_button("SEND TRANSMISSION", type="primary")

            if submit_button:
                if sender_name and sender_email and message:
                    # Construct mailto link
                    subject = f"[{message_type.upper()}] Message from {sender_name}"
                    body = f"Name: {sender_name}\nEmail: {sender_email}\n\nMessage:\n{message}"
                    mailto_link = f"mailto:tuesdaynightfreak@gmail.com?subject={subject}&body={body}"
                    
                    st.success("Message compiled! Click the link below to send via your email client.")
                    st.markdown(f'[Click here to open email client]({mailto_link})', unsafe_allow_html=True)
                    st.caption("We aim to respond within 48 hours.")
                else:
                    st.error("Please fill in your Name, Email, and Message.")
        
        st.markdown("#### DIRECT EMAILS")
        st.code("tuesdaynightfreak@gmail.com (Management & Demos)")


elif selected == "SYSTEM":
    st.title("SYSTEM ACCESS")
    pwd = st.text_input("ENTER AUTH CODE", type="password")
    
    if pwd == "admin123":
        st.success("ACCESS GRANTED. WELCOME, ADMINISTRATOR.")
        st.markdown("---")
        
        # --- ADMIN DASHBOARD ---
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📝 SITE COPY", "🎵 MIXCLOUD", "🖼️ GALLERY", "📅 EVENTS", "👕 MERCH", "🎧 HKR RELEASES"])
        
        # --- TAB 1: SITE COPY ---
        with tab1:
            st.markdown('<div class="admin-box">', unsafe_allow_html=True)
            st.subheader("HOME PAGE TEXT")
            st.session_state.site_content['home_headline'] = st.text_input("Headline", st.session_state.site_content['home_headline'], key="admin_home_headline")
            st.session_state.site_content['home_body'] = st.text_area("Body Text", st.session_state.site_content['home_body'], height=100, key="admin_home_body")
            
            c_up1, c_up2 = st.columns(2)
            st.session_state.site_content['system_update_1'] = c_up1.text_input("System Update 1", st.session_state.site_content['system_update_1'], key="admin_up1")
            st.session_state.site_content['system_update_2'] = c_up2.text_input("System Update 2", st.session_state.site_content['system_update_2'], key="admin_up2")
            
            st.subheader("ABOUT PAGE TEXT")
            st.session_state.site_content['about_bio'] = st.text_area("Biography Text", st.session_state.site_content['about_bio'], height=150, key="admin_bio")
            
            if st.button("💾 SAVE ALL TEXT CHANGES", key="save_text", type="primary"):
                st.toast("Content Updated Successfully!", icon="💾")
                st.rerun() 
            st.markdown('</div>', unsafe_allow_html=True)
            
        # --- TAB 2: MIXCLOUD MANAGER ---
        with tab2:
            st.markdown('<div class="admin-box">', unsafe_allow_html=True)
            st.subheader("UPDATE LATEST MIX")
            st.warning("You must paste the **Embed SRC URL**. Find it here: Go to Mixcloud -> Share -> Embed Player -> Copy the **URL inside the src='...'** part of the code.")
            
            curr_mix = st.text_input("Mixcloud Embed SRC URL", st.session_state.mixcloud_url, key="admin_mixcloud_url")
            
            if st.button("🎵 UPDATE MIX PLAYER", key="update_mix_player", type="primary"):
                st.session_state.mixcloud_url = curr_mix
                st.toast("Mixcloud Player Updated! Check the MUSIC tab.", icon="✅")
                
            st.markdown("---")
            st.markdown("#### CURRENT MIX PREVIEW")
            st.markdown(f"""<iframe width="100%" height="120" src="{curr_mix}" frameborder="0" ></iframe>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # --- TAB 3: GALLERY MANAGER ---
        with tab3:
            st.markdown('<div class="admin-box">', unsafe_allow_html=True)
            st.subheader("ADD NEW IMAGE/VIDEO")
            new_url = st.text_input("Image/Video URL (e.g., Unsplash link, YouTube link)", key="admin_new_url")
            new_cap = st.text_input("Caption", key="admin_new_cap")
            
            if st.button("⚡ ADD TO GALLERY", key="add_gallery", type="primary"):
                if new_url and new_cap:
                    # FIX: Ensuring key is 'url'
                    st.session_state.gallery_data.insert(0, {"url": new_url, "cap": new_cap})
                    st.toast("Item Added!")
                    st.rerun()
                else:
                    st.error("Please provide both URL and Caption.")
            st.divider()

            st.subheader("CURRENT ITEMS")
            for i, item in enumerate(st.session_state.gallery_data):
                col_i, col_c, col_d = st.columns([1, 4, 1])
                col_i.image(item['url'], width=100)
                col_c.write(f"**{item['cap']}**")
                if col_d.button("🔴 DELETE", key=f"del_g_{i}"):
                    st.session_state.gallery_data.pop(i)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # --- TAB 4: EVENTS MANAGER ---
        with tab4:
            st.markdown('<div class="admin-box">', unsafe_allow_html=True)
            st.subheader("ADD NEW EVENT")
            col_e1, col_e2, col_e3 = st.columns(3)
            new_date = col_e1.text_input("Date (e.g. SEP 05)", key="admin_new_date")
            new_city = col_e2.text_input("City (e.g. BERLIN)", key="admin_new_city")
            new_venue = col_e3.text_input("Venue (e.g. TRESOR)", key="admin_new_venue")
            new_image = st.text_input("Image URL (Flyer/Venue Photo)", key="admin_new_event_img")
            
            if st.button("➕ ADD EVENT", key="add_event", type="primary"):
                if new_date and new_city and new_venue and new_image:
                    st.session_state.events_data.insert(0, {"date": new_date, "city": new_city, "venue": new_venue, "image_url": new_image})
                    st.toast("Event Added!")
                    st.rerun()
                else:
                    st.error("Please fill in all event details.")
            
            st.divider()
            st.subheader("CURRENT EVENTS")
            
            for i, event in enumerate(st.session_state.events_data):
                col_i, col_d, col_v, col_del = st.columns([0.5, 1, 3, 1])
                col_i.write(f"**{i+1}.**")
                col_d.write(f"**{event['date']}**")
                col_v.write(f"{event['city']} // {event['venue']}")
                if col_del.button("REMOVE", key=f"event_del_{i}"):
                    st.session_state.events_data.pop(i)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # --- TAB 5: MERCH MANAGER ---
        with tab5:
            st.markdown('<div class="admin-box">', unsafe_allow_html=True)
            st.subheader("ADD NEW MERCH ITEM")
            col_m1, col_m2 = st.columns(2)
            new_m_name = col_m1.text_input("Item Name", key="admin_new_m_name")
            new_m_price = col_m2.number_input("Price (€)", min_value=1, key="admin_new_m_price")
            new_m_desc = st.text_input("Description", key="admin_new_m_desc")
            new_m_img = st.text_input("Product Image URL", key="admin_new_m_img")
            
            if st.button("➕ ADD MERCH", key="add_merch", type="primary"):
                if new_m_name and new_m_price and new_m_img:
                    # Using a generic SVG for new items; Admin can update manually if needed
                    new_item = {"name": new_m_name, "desc": new_m_desc, "price": new_m_price, "image_url": new_m_img, "logo_svg": TNF_LOGO_SVG, "svg_scale": 0.5}
                    st.session_state.merch_data.insert(0, new_item)
                    st.toast("Merch Item Added!")
                    st.rerun()
                else:
                    st.error("Please fill in Name, Price, and Image URL.")
            
            st.divider()
            st.subheader("CURRENT MERCH ITEMS")
            
            for i, item in enumerate(st.session_state.merch_data):
                col_i, col_n, col_p, col_del = st.columns([1, 4, 1, 1])
                col_i.image(item['image_url'], width=50)
                col_n.write(f"**{item['name']}** - *{item['desc']}*")
                col_p.write(f"€{item['price']}")
                if col_del.button("REMOVE", key=f"merch_del_{i}"):
                    st.session_state.merch_data.pop(i)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        # --- TAB 6: HKR RELEASES MANAGER ---
        with tab6:
            st.markdown('<div class="admin-box">', unsafe_allow_html=True)
            st.subheader("ADD NEW HKR RELEASE")
            col_h1, col_h2 = st.columns(2)
            new_h_cat = col_h1.text_input("Catalogue Number (e.g. HKR006)", key="admin_new_h_cat")
            new_h_artist = col_h2.text_input("Artist", key="admin_new_h_artist")
            new_h_title = st.text_input("Release Title", key="admin_new_h_title")
            
            if st.button("➕ ADD HKR RELEASE", key="add_hkr", type="primary"):
                if new_h_cat and new_h_artist and new_h_title:
                    st.session_state.hkr_data.insert(0, {"cat": new_h_cat, "artist": new_h_artist, "title": new_h_title})
                    st.toast("HKR Release Added!")
                    st.rerun()
                else:
                    st.error("Please fill in all release details.")
            
            st.divider()
            st.subheader("CURRENT HKR CATALOGUE")
            
            for i, item in enumerate(st.session_state.hkr_data):
                col_c, col_a, col_t, col_del = st.columns([1, 2, 3, 1])
                col_c.write(f"**{item['cat']}**")
                col_a.write(f"*{item['artist']}*")
                col_t.write(item['title'])
                if col_del.button("REMOVE", key=f"hkr_del_{i}"):
                    st.session_state.hkr_data.pop(i)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
