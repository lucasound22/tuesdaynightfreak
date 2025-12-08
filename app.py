import streamlit as st
from streamlit_option_menu import option_menu
import time

# --- CONFIGURATION & PALETTE ---
COLOR_BG = "#080808"
COLOR_TEXT = "#F0F0F0"
COLOR_ACCENT = "#FF0033"  # Acid Red
COLOR_CYAN = "#00f7ff"    # Cyberpunk Splash
COLOR_SECONDARY = "#141414"

# --- PAGE SETUP ---
st.set_page_config(
    page_title="TUESDAYNIGHTFREAK | OFFICIAL",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- STATE MANAGEMENT (THE CMS DATABASE) ---
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'page_index' not in st.session_state:
    st.session_state.page_index = 0

# 1. CMS TEXT CONTENT
if 'site_content' not in st.session_state:
    st.session_state.site_content = {
        "home_headline": "THE SOUND OF HARDWARE SOUL",
        "home_body": "We are an independent electronic music project and culture crew bridging the gap between Berlin's concrete basements and Melbourne's warehouse soul. We embrace the analogue error.",
        "about_bio": "Tuesdaynightfreak is an electronic music project established in Melbourne, Australia.\n\nDrawing influence from the stark industrialism of Berlin and the soulful rhythms of Detroit, the project explores the boundaries of hardware sequencing. It is a reaction against the predictability of digital production—a celebration of the machine's inherent instability.",
        "system_update_1": "**NEW RELEASE:** 'VOLTAGE CONTROL' EP OUT NOW VIA OSTGUT TON.",
        "system_update_2": "**TOUR ANNOUNCEMENT:** EUROPEAN DATES CONFIRMED FOR WINTER 2025."
    }

# 2. MIXCLOUD SETTINGS
if 'mixcloud_url' not in st.session_state:
    # Default is a placeholder; Admin will overwrite this
    st.session_state.mixcloud_url = "https://www.mixcloud.com/widget/iframe/?hide_cover=1&mini=1&light=0&feed=%2Fcarlcox%2Fcarl-cox-global-722%2F"

# 3. GALLERY DATA
if 'gallery_data' not in st.session_state:
    st.session_state.gallery_data = [
        {"type": "image", "src": "https://images.unsplash.com/photo-1506450682137-f4a471413a17?q=80&w=800&auto=format&fit=crop", "cap": "MODULAR SYNTHESIS"},
        {"type": "image", "src": "https://images.unsplash.com/photo-1510928230230-e837894ff54c?q=80&w=800&auto=format&fit=crop", "cap": "LIVE PERFORMANCE"},
        {"type": "image", "src": "https://images.unsplash.com/photo-1534005888251-140a324032d8?q=80&w=800&auto=format&fit=crop", "cap": "DRUM SEQUENCES"},
        {"type": "image", "src": "https://images.unsplash.com/photo-1543851505-18ff86725350?q=80&w=800&auto=format&fit=crop", "cap": "CROWD"},
        {"type": "image", "src": "https://images.unsplash.com/photo-1571266028243-371695063ad6?q=80&w=800&auto=format&fit=crop", "cap": "VINYL"},
        {"type": "image", "src": "https://images.unsplash.com/photo-1563841930606-67e26ce48428?q=80&w=800&auto=format&fit=crop", "cap": "STUDIO"}
    ]

# 4. EVENTS DATA (NEW)
if 'events_data' not in st.session_state:
    st.session_state.events_data = [
        {"date":"NOV 04","city":"AMSTERDAM","venue":"SHELTER"},
        {"date":"NOV 11","city":"LONDON","venue":"FOLD"},
        {"date":"NOV 18","city":"MELBOURNE","venue":"REVOLVER"}
    ]

def set_page(index):
    st.session_state.page_index = index

def add_to_cart(item):
    st.session_state.cart.append(item)
    st.toast(f"Added {item} to cart!", icon="🛒")

# --- BRANDING SVGs ---
TNF_LOGO_SVG = f"""<svg width="300" height="90" viewBox="0 0 300 90" xmlns="http://www.w3.org/2000/svg"><text x="4" y="65" font-family="Arial" font-weight="900" font-size="72" fill="{COLOR_CYAN}" opacity="0.6" letter-spacing="-4">TNF</text><text x="-2" y="65" font-family="Arial" font-weight="900" font-size="72" fill="{COLOR_ACCENT}" opacity="0.7" letter-spacing="-4">TNF</text><text x="0" y="65" font-family="Arial" font-weight="900" font-size="72" fill="{COLOR_TEXT}" letter-spacing="-4">TNF</text><rect x="160" y="25" width="8" height="40" fill="{COLOR_ACCENT}"/><rect x="175" y="25" width="8" height="40" fill="{COLOR_CYAN}"/></svg>"""
HKR_LOGO_SVG = f"""<svg width="150" height="150" viewBox="0 0 150 150" xmlns="http://www.w3.org/2000/svg"><rect x="5" y="5" width="140" height="140" stroke="{COLOR_TEXT}" stroke-width="5" fill="none"/><path d="M20 60 L75 20 L130 60" stroke="{COLOR_ACCENT}" stroke-width="5" fill="none"/><circle cx="75" cy="95" r="30" stroke="{COLOR_CYAN}" stroke-width="4" fill="none"/></svg>"""
SLIPMAT_ICON_SVG = f"""<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="45" fill="#111" stroke="{COLOR_CYAN}" stroke-width="2"/><circle cx="50" cy="50" r="15" fill="{COLOR_ACCENT}"/></svg>"""


# --- CUSTOM CSS (FIXING VISIBILITY) ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Space+Mono:wght@400;700&display=swap');
    
    .stApp {{ background-color: {COLOR_BG}; color: {COLOR_TEXT}; font-family: 'Inter', sans-serif; }}
    
    /* REMOVE UI */
    header, footer, [data-testid="stToolbar"] {{ visibility: hidden; height: 0; }}
    
    /* LAYOUT FIXES */
    .block-container {{
        padding-top: 0rem !important;
        padding-bottom: 5rem !important;
        max-width: 100% !important;
    }}
    div[data-testid="stVerticalBlock"] > div:first-of-type {{
        padding: 2rem;
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

    /* ADMIN PANEL STYLING */
    .admin-box {{
        background-color: #1a1a1a;
        padding: 20px;
        border: 1px solid #333;
        border-radius: 5px;
        margin-bottom: 20px;
    }}
    
    /* Ensure input text is visible in Dark Mode */
    input, textarea {{
        color: #fff !important; 
        background-color: #222 !important;
        border: 1px solid #444 !important;
    }}
    
    /* NAVIGATION FIXES (Main Menu Visibility) */
    .st-emotion-cache-163lq9m {{ border-bottom: 3px solid {COLOR_CYAN}; padding: 0 2rem; }}
    .st-emotion-cache-163lq9m a {{ color: {COLOR_TEXT}; }} /* Non-selected menu text color */
    .st-emotion-cache-163lq9m .st-emotion-cache-1n76hnz {{ color: {COLOR_CYAN}; }} /* Selected menu item */

    /* ADMIN TABS FIXES (Tab Label Visibility) */
    [data-testid="stTabs"] button {{
        color: {COLOR_TEXT}; /* Unselected tab text color */
        background-color: #1a1a1a;
        border-bottom: 3px solid #333;
        margin-right: 5px;
        transition: 0.3s;
    }}
    [data-testid="stTabs"] button[aria-selected="true"] {{
        color: {COLOR_CYAN}; /* Selected tab text color */
        border-bottom-color: {COLOR_CYAN};
        background-color: {COLOR_BG};
    }}
    
    /* Video Background (Restoring video functionality) */
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
        opacity: 0.3; /* Added opacity to ensure text is visible */
    }}
    .video-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7); 
        z-index: -1;
    }}
    
</style>
""", unsafe_allow_html=True)

# --- BACKGROUND MEDIA (Video + Hidden Audio Tone) ---
# Ensure this block is high up to render the background properly
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
            // Simple synth for an initial sound cue
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
        "container": {"background-color": "rgba(0,0,0,0.8)", "padding": "0!important"}, 
        "nav-link-selected": {"color": COLOR_CYAN, "border-bottom": f"3px solid {COLOR_CYAN}"},
        "nav-link": {"color": COLOR_TEXT} # Explicitly setting color for non-selected links
    }
)

# Sync state
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
        # LOAD DYNAMIC CONTENT
        st.markdown(f"### {st.session_state.site_content['home_headline']}")
        st.markdown(f"""<div style="font-size: 1.2rem; line-height: 1.6; color: #ddd;">{st.session_state.site_content['home_body']}</div>""", unsafe_allow_html=True)
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
    releases = [{"title": "System Failure", "label": "HKR004"}, {"title": "Analog Dreams", "label": "TR-291"}, {"title": "Voltage Control", "label": "OSTGUT-55"}]
    for r in releases:
        c1, c2, c3 = st.columns([1, 4, 2])
        with c1: st.markdown("<div style='width:60px;height:60px;background:#222;border:1px solid #444;'></div>", unsafe_allow_html=True)
        with c2: st.subheader(r['title']); st.caption(r['label'])
        with c3: st.button("STREAM / BUY", key=r['label'])
        st.divider()

elif selected == "HKR":
    c1, c2 = st.columns([1, 3])
    with c1: st.markdown(f"<div style='width: 120px; height: 120px; margin: auto;'>{HKR_LOGO_SVG}</div>", unsafe_allow_html=True)
    with c2: st.title("HOUSE KEEPING RECORDS"); st.markdown("#### EST. 2023 // DEEP HOUSE & TECHNO // VINYL ONLY"); st.write("House Keeping Records is the dedicated platform for the raw and the deep. Focusing on functional tools for DJs and sonic explorations for heads.")
    st.divider()
    st.subheader("CATALOGUE")
    hkr = [{"cat":"HKR005","t":"RHYTHM GENERATOR EP"},{"cat":"HKR004","t":"MODULAR LOOP 01"},{"cat":"HKR003","t":"GRID SEQUENCER"}]
    for i in hkr:
        c1, c2, c3 = st.columns([1,3,1])
        c1.write(f"**{i['cat']}**"); c2.write(f"**{i['t']}**"); c3.button("PURCHASE VINYL", key=i['cat'])
        st.divider()

elif selected == "EVENTS":
    st.title("UPCOMING DATES")
    
    events = st.session_state.events_data
    if not events:
        st.info("No events scheduled at this time. Check back soon!")
    
    for e in events:
        c1, c2, c3 = st.columns([1, 3, 1])
        with c1: st.markdown(f"### {e['date']}")
        with c2: st.markdown(f"**{e['city']}** // {e['venue']}"); st.caption("Techno / House")
        with c3: st.button("TICKETS", key=e['city'] + e['date'])
        st.divider()

elif selected == "STORE":
    st.title("OFFICIAL MERCHANDISE")
    if st.session_state.cart: st.info(f"CART: {len(st.session_state.cart)} ITEMS")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='mockup-container'><div class='mockup-logo' style='transform: translate(-50%, -50%) scale(0.6);'>{TNF_LOGO_SVG}</div></div>", unsafe_allow_html=True)
        st.markdown("**TNF CORE TEE**"); st.caption("Heavyweight Cotton")
        st.button("ADD TO CART €35", key="m1", on_click=add_to_cart, args=("TNF Tee",))
    with c2:
        st.markdown(f"<div class='mockup-container'><div class='mockup-logo' style='transform: translate(-50%, -50%) scale(0.7);'>{HKR_LOGO_SVG}</div></div>", unsafe_allow_html=True)
        st.markdown("**HKR LABEL HOODIE**"); st.caption("Oversized Fit")
        st.button("ADD TO CART €65", key="m2", on_click=add_to_cart, args=("HKR Hoodie",))
    with c3:
        st.markdown(f"<div class='mockup-container'><div class='mockup-logo' style='transform: translate(-50%, -50%) scale(0.8);'>{SLIPMAT_ICON_SVG}</div></div>", unsafe_allow_html=True)
        st.markdown("**PRO SLIPMATS**"); st.caption("Anti-static Pair")
        st.button("ADD TO CART €20", key="m3", on_click=add_to_cart, args=("Slipmats",))

elif selected == "GALLERY":
    st.title("VISUAL ARCHIVE")
    st.caption("RAW VOLTAGE. RAW RHYTHM.")
    
    # 4-column grid for smaller images
    gallery_items = st.session_state.gallery_data
    cols = st.columns(4) 
    
    for i, item in enumerate(gallery_items):
        with cols[i % 4]:
            if item['type'] == 'video':
                st.video(item['src'])
            else:
                st.image(item['src'], use_column_width=True)
            if item.get('cap'): st.caption(item['cap'])
            st.markdown("<br>", unsafe_allow_html=True)

elif selected == "ABOUT":
    c1, c2 = st.columns([2,1])
    with c1:
        st.title("BIOGRAPHY")
        # Load Dynamic Bio
        st.write(st.session_state.site_content['about_bio'])
    with c2:
        st.markdown("#### CONTACT")
        st.code("mgmt@tuesdaynightfreak.com")
        st.markdown("#### DEMOS")
        st.code("demos@housekeeping-rec.com")
        st.button("DOWNLOAD PRESS KIT")

# ---------------------------------------------
## 💻 SYSTEM ACCESS (ADMIN)
# ---------------------------------------------

elif selected == "SYSTEM":
    st.title("SYSTEM ACCESS")
    
    # Simple Auth
    pwd = st.text_input("ENTER SYSTEM PASSWORD", type="password")
    
    if pwd == "admin123":
        st.success("AUTHENTICATED. WELCOME, ADMINISTRATOR.")
        st.markdown("---")
        
        # --- ADMIN DASHBOARD ---
        tab1, tab2, tab3, tab4 = st.tabs(["📝 SITE COPY", "🖼️ GALLERY", "📅 EVENTS", "☁️ MIXCLOUD"])
        
        # --- TAB 1: CONTENT MANAGER (SITE COPY) ---
        with tab1:
            st.markdown('<div class="admin-box">', unsafe_allow_html=True)
            st.subheader("HOME PAGE TEXT")
            st.caption("The Home Page copy is editable here.")
            new_headline = st.text_input("Headline (H3)", st.session_state.site_content['home_headline'])
            new_body = st.text_area("Body Text", st.session_state.site_content['home_body'], height=100)
            
            c_up1, c_up2 = st.columns(2)
            new_up1 = c_up1.text_input("System Update 1 (Info Box)", st.session_state.site_content['system_update_1'])
            new_up2 = c_up2.text_input("System Update 2 (Info Box)", st.session_state.site_content['system_update_2'])
            
            st.subheader("ABOUT PAGE TEXT")
            new_bio = st.text_area("Biography Text", st.session_state.site_content['about_bio'], height=150)
            
            if st.button("💾 SAVE ALL TEXT CHANGES"):
                st.session_state.site_content.update({
                    "home_headline": new_headline,
                    "home_body": new_body,
                    "about_bio": new_bio,
                    "system_update_1": new_up1,
                    "system_update_2": new_up2
                })
                st.toast("Content Updated Successfully!", icon="💾")
                st.rerun() 
            st.markdown('</div>', unsafe_allow_html=True)

        # --- TAB 2: GALLERY MANAGER ---
        with tab2:
            st.markdown('<div class="admin-box">', unsafe_allow_html=True)
            
            # Upload Section
            st.markdown("#### ADD NEW ITEM")
            col_add1, col_add2 = st.columns(2)
            with col_add1:
                new_img_url = st.text_input("Image URL (Paste URL)")
                new_vid_url = st.text_input("Video URL (YouTube/MP4)")
            with col_add2:
                new_cap = st.text_input("Caption (e.g. 'Studio Session 2025')")
                if st.button("⚡ ADD TO GALLERY", type="primary"):
                    if new_img_url:
                        st.session_state.gallery_data.insert(0, {"type": "image", "src": new_img_url, "cap": new_cap})
                        st.toast("Image Linked")
                        st.rerun()
                    elif new_vid_url:
                        st.session_state.gallery_data.insert(0, {"type": "video", "src": new_vid_url, "cap": new_cap})
                        st.toast("Video Linked")
                        st.rerun()
                    else:
                        st.error("Please provide either an image or a video URL.")

            st.divider()
            
            # Management Grid (Thumbnails + Delete)
            st.markdown("#### CURRENT ITEMS (4 Column Grid for Management)")
            
            mgr_cols = st.columns(4)
            for i, item in enumerate(st.session_state.gallery_data):
                with mgr_cols[i % 4]:
                    st.markdown(f"<div style='border:1px solid #333; padding:5px; background:#000;'>", unsafe_allow_html=True)
                    if item['type'] == 'image':
                        st.image(item['src'], use_column_width=True)
                    else:
                        st.markdown(f"🎥 **VIDEO**")
                    
                    st.caption(f"**{i+1}.** {item.get('cap', 'No Caption')}")
                    
                    if st.button("🔴 DELETE", key=f"del_{i}", type="secondary"):
                        st.session_state.gallery_data.pop(i)
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        # --- TAB 3: EVENTS MANAGER (NEW) ---
        with tab3:
            st.markdown('<div class="admin-box">', unsafe_allow_html=True)
            st.subheader("ADD NEW EVENT")
            col_e1, col_e2, col_e3 = st.columns(3)
            new_date = col_e1.text_input("Date (e.g. SEP 05)")
            new_city = col_e2.text_input("City (e.g. BERLIN)")
            new_venue = col_e3.text_input("Venue (e.g. TRESOR)")
            
            if st.button("➕ ADD EVENT TO SCHEDULE", type="primary"):
                if new_date and new_city and new_venue:
                    st.session_state.events_data.insert(0, {"date": new_date, "city": new_city, "venue": new_venue})
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

        # --- TAB 4: MIXCLOUD MANAGER ---
        with tab4:
            st.markdown('<div class="admin-box">', unsafe_allow_html=True)
            st.subheader("UPDATE LATEST MIX")
            # Clear instruction for Mixcloud Fix
            st.warning("FIX: You must paste the **Embed SRC URL**. Find it here: Go to Mixcloud -> Share -> Embed Player -> Copy the **URL inside the src='...'** part of the code.")
            
            curr_mix = st.text_input("Mixcloud Embed SRC URL", st.session_state.mixcloud_url)
            
            if st.button("🎵 UPDATE MIX PLAYER", type="primary"):
                st.session_state.mixcloud_url = curr_mix
                st.toast("Mixcloud Player Updated! Check the MUSIC tab.", icon="✅")
                # Removed rerun here to allow the preview to update without immediately reloading the whole page
                
            st.markdown("---")
            st.markdown("#### CURRENT MIX PREVIEW")
            # Preview uses the current input value, fixing the preview error
            st.markdown(f"""<iframe width="100%" height="120" src="{curr_mix}" frameborder="0" ></iframe>""", unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
