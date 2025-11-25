# app.py - Tuesdaynightfreak (Full Upgrade)
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import requests
import io
import validators
import time

# --- CONFIGURATION & PALETTE ---
CP_YELLOW = "#fcee0a"
CP_CYAN = "#00f0ff"
CP_RED = "#ff003c"
CP_BLACK = "#050a0e"
TT_CREAM = "#f2f2f2"  # Used for contrast borders

# --- DEFECTED-INSPIRED "PREMIUM UNDERGROUND" ---
COLOR_BG = "#080808"
COLOR_TEXT = "#F0F0F0"
COLOR_ACCENT = "#FF0033"
COLOR_SECONDARY = "#1A1A1A"

# Poster local image (developer uploaded file). Use as fallback for video.
POSTER_IMG_LOCAL = "/mnt/data/32b1d44b-a37c-4c95-acdd-0c4ef6a11a99.png"

# --- BRANDING: CUSTOM SVG LOGOS ---
TNF_STAMP_LOGO = f"""
<svg width="60" height="60" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="45" stroke="{CP_YELLOW}" stroke-width="5" fill="{CP_BLACK}"/>
  <path d="M20 50 L40 50 L40 80" stroke="{CP_CYAN}" stroke-width="8"/> 
  <path d="M50 80 L50 20 L80 80 L80 20" stroke="{CP_RED}" stroke-width="6"/>
  <text x="50%" y="50%" text-anchor="middle" stroke="{CP_YELLOW}" stroke-width="1" dy=".3em" font-family="monospace" font-weight="bold" font-size="20">TNF</text>
</svg>
"""

TNF_LOGO_SVG = f"""
<svg width="120" height="40" viewBox="0 0 120 40" fill="none" xmlns="http://www.w3.org/2000/svg">
  <text x="0" y="30" font-family="Helvetica, Arial, sans-serif" font-weight="900" font-size="32" fill="{COLOR_TEXT}" letter-spacing="-2">TNF</text>
  <circle cx="80" cy="20" r="8" fill="{COLOR_ACCENT}"/>
  <rect x="95" y="12" width="25" height="16" fill="{COLOR_TEXT}"/>
</svg>
"""

# -------------------------------------------------------------------------
# Page config
# -------------------------------------------------------------------------
st.set_page_config(
    page_title="TUESDAYNIGHTFREAK | OFFICIAL",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------------------------------------------------------------
# CSS template (placeholders replaced to avoid f-string brace problems)
# -------------------------------------------------------------------------
css_template = """
<style>
:root{
  --bg: %%COLOR_BG%%;
  --text: %%COLOR_TEXT%%;
  --accent: %%COLOR_ACCENT%%;
  --yellow: %%CP_YELLOW%%;
  --cyan: %%CP_CYAN%%;
  --red: %%CP_RED%%;
  --cream: %%TT_CREAM%%;
  --secondary: %%COLOR_SECONDARY%%;
}

/* base */
body, .stApp {
  background: var(--bg);
  color: var(--text);
  font-family: Inter, sans-serif;
}

/* hide default chrome */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* container */
.block-container { padding-top: 1.25rem !important; max-width: 1230px; }

/* hero typography */
.artist-title { font-family: 'Tomorrow', sans-serif; font-size: clamp(2rem, 5vw, 4rem); font-weight: 900; text-transform: uppercase; color: var(--yellow); text-shadow: 4px 4px 0px var(--cyan); line-height: 0.9; letter-spacing: -2px; transform: skew(-5deg); margin-bottom: .6rem; }

/* head styles */
h1,h2,h3 { font-family: Barlow, sans-serif; text-transform: uppercase; font-weight: 900; color: var(--text); border-bottom: 3px solid var(--yellow); display: inline-block; padding-bottom: .4rem; margin-top: 1.6rem !important; letter-spacing: -1px; margin-bottom: .5rem; }

h4,h5,h6 { color: var(--cyan) !important; font-family: Tomorrow, sans-serif; }

/* buttons */
.stButton > button {
  background-color: var(--text);
  color: var(--bg);
  border: none;
  font-weight: 900;
  text-transform: uppercase;
  padding: 10px 22px;
  border-radius: 0;
  transition: transform .18s ease, box-shadow .18s ease;
}
.stButton > button:hover {
  background-color: var(--accent);
  color: var(--text);
  transform: translate(-2px,-2px) scale(1.02);
  box-shadow: 4px 4px 0px var(--red);
}

/* cards */
.graphic-box { border: 2px solid var(--cream); padding: 16px; background: linear-gradient(180deg, rgba(0,0,0,0.35), transparent); }
.news-card { background-color: var(--secondary); padding: 14px; border-left: 4px solid var(--accent); margin-bottom: 14px; transition: transform .2s ease; }
.news-card:hover { transform: translateX(6px); }

/* inputs */
.stTextInput input, .stTextArea textarea { background-color: #121212; color: var(--yellow); border: 1px solid #2b2b2b; border-radius: 2px; }

/* links */
a { color: var(--yellow) !important; text-decoration: none; font-weight: 600; }
a:hover { color: var(--accent) !important; text-decoration: underline; }

/* utility */
.muted { color: #888; font-size: 0.9rem; }

/* bg video */
.bg-video-wrap {
  position: fixed;
  inset: 0;
  z-index: -1;
  overflow: hidden;
  pointer-events: none;
}
.bg-video-wrap video {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%,-50%);
  min-width: 100%;
  min-height: 100%;
  width: auto; height: auto;
  object-fit: cover;
  filter: brightness(.45) contrast(1.05);
  will-change: transform;
}

/* content overlay spacing helper */
.content-overlay { position: relative; z-index: 2; padding-top: 2rem; }

/* responsive tweaks */
@media (max-width: 600px) {
  .artist-title { font-size: 2.1rem; transform: none; }
  .bg-video-wrap { display: none; } /* mobile browsers often block background autoplay */
}
</style>
"""

css = (css_template
       .replace('%%CP_YELLOW%%', CP_YELLOW)
       .replace('%%CP_CYAN%%', CP_CYAN)
       .replace('%%CP_RED%%', CP_RED)
       .replace('%%CP_BLACK%%', CP_BLACK)
       .replace('%%TT_CREAM%%', TT_CREAM)
       .replace('%%COLOR_BG%%', COLOR_BG)
       .replace('%%COLOR_TEXT%%', COLOR_TEXT)
       .replace('%%COLOR_ACCENT%%', COLOR_ACCENT)
       .replace('%%COLOR_SECONDARY%%', COLOR_SECONDARY)
)

st.markdown(css, unsafe_allow_html=True)

# -------------------------------------------------------------------------
# Helper utilities & initial state
# -------------------------------------------------------------------------
def sanitize_url(url: str) -> str:
    if not url:
        return ""
    url = url.strip()
    if url.startswith("http"):
        return url
    return url

if 'songs' not in st.session_state:
    st.session_state.songs = [
        {"title": "UNTITLED_SEQ_04 [LIVE REC]", "url": "#", "platform": "SoundCloud"},
        {"title": "MODULAR EXCURSION B (RAW)", "url": "#", "platform": "Bandcamp"},
        {"title": "RESIDENT ADVISOR PODCAST 892", "url": "#", "platform": "RA"},
        {"title": "System Failure (Original Mix)", "label": "House Keeping Rec", "cat": "HKR004"},
        {"title": "Analog Dreams", "label": "Tresor Records", "cat": "TR-291"},
        {"title": "Voltage Control", "label": "Ostgut Ton", "cat": "OSTGUT-55"}
    ]

# curated techno-related media (Unsplash / Mixkit placeholders)
if 'gallery' not in st.session_state:
    st.session_state.gallery = [
        {"caption": "WAREHOUSE RAVE // BERLIN", "url": "https://images.unsplash.com/photo-1517457375825-e578c799a74f?q=80&w=1200&auto=format&fit=crop"},
        {"caption": "LIVE MODULAR RIG", "url": "https://images.unsplash.com/photo-1550291652-6ea9114a47b1?q=80&w=1200&auto=format&fit=crop"},
        {"caption": "CROWD ENERGY // 3AM", "url": "https://images.pexels.com/photos/1190293/pexels-photo-1190293.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"},
        {"caption": "ANALOG OSCILLATORS", "url": "https://images.unsplash.com/photo-1621360841012-2357d27e02a4?q=80&w=1200&auto=format&fit=crop"},
        {"caption": "MODULAR RIG SETUP", "url": "https://images.unsplash.com/photo-1510915364890-a7d41f02c611?q=80&w=1200&auto=format&fit=crop"},
        {"caption": "LIVE SIGNAL PATH", "url": "https://images.unsplash.com/photo-1598275529124-b1c4b786f1e2?q=80&w=1200&auto=format&fit=crop"},
        {"caption": "WAREHOUSE CROWD", "url": "https://images.unsplash.com/photo-1571266028243-371695063ad6?q=80&w=1200&auto=format&fit=crop"},
        {"caption": "OSCILLATOR DETAIL", "url": "https://images.unsplash.com/photo-1619967657960-983b6329c370?q=80&w=1200&auto=format&fit=crop"}
    ]

if 'bookings' not in st.session_state:
    st.session_state.bookings = []

# -------------------------------------------------------------------------
# Background video HTML (insert once)
# -------------------------------------------------------------------------
# Placeholder / example MP4. Replace VIDEO_SRC with your production video URL (CDN).
# Mixkit / Mixdrive / Pexels offer free short loops; host on CDN for reliability.
VIDEO_SRC = "https://assets.mixkit.co/videos/preview/mixkit-clubbing-dancers-loop-2387-large.mp4"
# Use local poster image as fallback (from developer uploaded file). See developer note.
POSTER_IMG = POSTER_IMG_LOCAL  # "/mnt/data/32b1d44b-a37c-4c95-acdd-0c4ef6a11a99.png"

bg_video_html = f"""
<div class="bg-video-wrap">
  <video autoplay muted loop playsinline poster="{POSTER_IMG}" id="hero-bg">
    <source src="{VIDEO_SRC}" type="video/mp4">
    <!-- fallback: poster image will show -->
  </video>
</div>
<div class="content-overlay"></div>
"""
st.markdown(bg_video_html, unsafe_allow_html=True)

# -------------------------------------------------------------------------
# Navigation
# -------------------------------------------------------------------------
selected = option_menu(
    menu_title=None,
    options=["HOME", "MUSIC", "LABEL", "MEDIA", "EVENTS", "STORE", "CONTACT", "SYSTEM", "ABOUT"],
    icons=["house", "music-note-list", "tag", "camera-reels", "calendar-event", "bag", "envelope", "gear", "info-circle"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": COLOR_BG, "border-bottom": "1px solid #222"},
        "icon": {"color": "#999", "font-size": "12px"},
        "nav-link": {"font-size": "14px", "text-align": "center", "margin": "0px", "color": TT_CREAM, "font-family": "Inter, sans-serif", "text-transform": "uppercase", "font-weight": "600"},
        "nav-link-selected": {"background-color": COLOR_BG, "color": COLOR_TEXT, "border-bottom": f"2px solid {COLOR_ACCENT}"},
    }
)

# -------------------------------------------------------------------------
# Shared components
# -------------------------------------------------------------------------
def render_hero():
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown('<div class="artist-title">TUESDAY<br>NIGHT<br>FREAK</div>', unsafe_allow_html=True)
        st.markdown(f"### LIVE HARDWARE ELECTRONICS {TNF_STAMP_LOGO}", unsafe_allow_html=True)
        st.markdown(f"<h5 style='color:{TT_CREAM} !important'>MELBOURNE // BERLIN // UNDERGROUND</h5>", unsafe_allow_html=True)
        st.markdown(f"## TUESDAYNIGHTFREAK {TNF_LOGO_SVG}", unsafe_allow_html=True)
        st.markdown("#### DEFINING THE FUTURE OF LIVE HARDWARE ELECTRONICS")
        st.markdown("""
        Tuesdaynightfreak is a new era in electronic music performance.
        Bridging studio precision and live improvisation, crafting immersive soundscapes using only modular synthesis and drum machines.

        **No Laptops. No Sync. Pure Voltage.**
        """)
        cols = st.columns([1,1,1])
        with cols[0]:
            st.button("LISTEN", key="cta_listen")
        with cols[1]:
            st.button("SHOP VINYL", key="cta_shop")
        with cols[2]:
            st.button("TOUR DATES", key="cta_tour")
    with c2:
        st.markdown("#### LATEST NEWS")
        st.markdown(f"""
        <div class="graphic-box">
        Tuesdaynightfreak is not just an artist; it's a <strong>sonic movement</strong>.
        <div class="news-card">
        <strong>NEW EP ANNOUNCED</strong><br>
        <span class="muted">OCT 24, 2025</span><br>
        'Voltage Control' drops worldwide next Friday on House Keeping Records.
        </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"**CURRENT SYSTEM STATUS:** <span style='color:{CP_YELLOW}; font-family:monospace;'>ONLINE // STUDIO MODE</span>", unsafe_allow_html=True)

def render_gallery_grid(count=6):
    st.markdown("### VISUAL FEED")
    cols = st.columns(3)
    for i, item in enumerate(st.session_state.gallery[:count]):
        with cols[i % 3]:
            # streamlit will lazy-load images by default when not used with use_column_width
            st.image(item['url'], caption=item['caption'], use_column_width=True)

def render_discography():
    st.markdown("### DISCOGRAPHY")
    for track in st.session_state.songs:
        c1, c2, c3 = st.columns([1, 4, 2])
        with c1:
            st.markdown(f"<div style='width:42px;height:42px;background:{COLOR_ACCENT};border-radius:4px;'></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"**{track['title']}**")
            if track.get("label"):
                st.caption(track.get("label"))
        with c3:
            if track.get("url") and track["url"].startswith("http"):
                st.markdown(f"[Listen ▶]({track['url']})")
            else:
                st.button("STREAM", key=track['title'])

# -------------------------------------------------------------------------
# Simple broken link checker (admin)
# -------------------------------------------------------------------------
def check_links(links):
    results = []
    for u in links:
        if not u:
            continue
        u = u.strip()
        try:
            # prefer HEAD then GET fallback
            r = requests.head(u, allow_redirects=True, timeout=8)
            status = r.status_code
            if status >= 400:
                # try full GET (some servers block HEAD)
                r2 = requests.get(u, allow_redirects=True, timeout=8)
                status = r2.status_code
        except Exception as e:
            status = f"ERR: {str(e)[:80]}"
        results.append({"url": u, "status": status})
    return results

# -------------------------------------------------------------------------
# PAGE ROUTES
# -------------------------------------------------------------------------
if selected == "HOME":
    render_hero()
    st.write("---")
    render_gallery_grid(count=4)
    st.write("---")
    st.markdown("### FEATURED RELEASE")
    c1, c2 = st.columns([2,1])
    with c1:
        st.image(st.session_state.gallery[0]['url'], caption="STATIC INTERFERENCE EP [12\" VINYL]", use_column_width=True)
    with c2:
        st.markdown("**STATIC INTERFERENCE EP**")
        st.markdown("A limited pressing. Pressing available worldwide.")
        st.button("BUY VINYL / DIGITAL", key="buy_vinyl")

elif selected == "MUSIC":
    st.markdown("## SONIC ARCHIVE")
    st.markdown("### LIVE JAMS & STUDIO CUTS")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### UNTITLED_SEQ_04")
        st.image("https://images.unsplash.com/photo-1493225255756-d9584f8606e9?q=80&w=800&auto=format&fit=crop", caption="Live Recording")
        # embed soundcloud example (if url exists)
        if st.session_state.songs and st.session_state.songs[0].get("url", "").startswith("http"):
            url = st.session_state.songs[0]["url"]
            # embed as link if not embedable
            st.markdown(f"[Open track ▶]({url})")
    with c2:
        st.markdown("#### ACID RAIN (DUB)")
        st.image("https://images.unsplash.com/photo-1514525253440-b393452e8d26?q=80&w=800&auto=format&fit=crop", caption="Studio Cut")
        st.markdown("[BUY ON BANDCAMP](#)")
    st.write("---")
    render_discography()

elif selected == "LABEL":
    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown("## HOUSE KEEPING RECORDS")
        st.markdown("**EST. 2023 // VINYL ONLY**")
        st.write("---")
        st.markdown("""
        <div class="graphic-box">
        House Keeping Records is our platform for the raw, the deep, and the functional.
        We release tools for DJs and explorations for heads.
        <br><br>
        <strong>PHILOSOPHY:</strong><br>
        1. Respect the groove.<br>
        2. Hardware over software.<br>
        3. Community over clout.
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("### SUBMIT DEMO")
        with st.form("demo_form"):
            alias = st.text_input("ARTIST ALIAS")
            link = st.text_input("SOUNDCLOUD / PRIVATE LINK (PRIVATE ONLY)")
            submitted = st.form_submit_button("TRANSMIT DATA")
            if submitted:
                valid = validators.url(link) if link else True
                if not valid:
                    st.error("Please provide a valid URL or leave blank for private SoundCloud.")
                else:
                    st.success("Demo transmitted. We'll review and respond.")

elif selected == "MEDIA":
    st.markdown("## VISUAL FEED")
    render_gallery_grid(count=9)
    st.write("---")
    st.markdown("#### Press / Mixes")
    # example embed placeholder for RA or SoundCloud
    st.markdown("Embedded mixes and press links will appear here.")

elif selected == "EVENTS":
    st.markdown("## UPCOMING DATES")
    events = [
        {"date": "NOV 04", "city": "AMSTERDAM", "venue": "SHELTER", "status": "SELLING FAST", "link": "#"},
        {"date": "NOV 11", "city": "LONDON", "venue": "FOLD", "status": "TICKETS", "link": "#"},
        {"date": "NOV 18", "city": "MELBOURNE", "venue": "REVOLVER", "status": "SOLD OUT", "link": "#"},
        {"date": "DEC 02", "city": "PARIS", "venue": "REX CLUB", "status": "TICKETS", "link": "#"},
    ]
    for event in events:
        c1, c2, c3, c4 = st.columns([1, 2, 2, 2])
        with c1:
            st.markdown(f"<span style='color:{COLOR_ACCENT}; font-weight:900;'>{event['date']}</span>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"**{event['city']}**")
            st.caption(event['venue'])
        with c3:
            st.markdown(event['venue'])
        with c4:
            if event['status'] == "SOLD OUT":
                st.markdown("<span class='muted'>SOLD OUT</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"[Buy Tickets ▶]({event['link']})")
    st.write("---")
    st.info("Add events via SYSTEM > UPLOAD VISUALS or contact management to list shows.")

elif selected == "STORE":
    st.markdown("## SHOP MERCH & VINYL")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("## BOOKING & PRESS")
        st.markdown("### WORLDWIDE")
        st.write("Direct Management")
        st.markdown(f"<h2 style='border:none; color:{CP_YELLOW};'>tuesdaynightfreak@gmail.com</h2>", unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1585227803927-2c24067b9416?q=80&w=600&auto=format&fit=crop", caption='HKR004 - VINYL 12\"')
        st.markdown("**SYSTEM FAILURE EP**")
        st.caption("€14.00")
        st.button("ADD TO CART", key="p1")
        st.write("---")
        st.markdown("### MEDIA KIT")
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

elif selected == "SYSTEM":
    st.markdown("## SYSTEM ACCESS")
    st.caption("SECURE AREA. AUTHORIZED PERSONNEL ONLY.")
    pwd = st.text_input("ENTER AUTH CODE", type="password")
    if pwd == "admin123":
        st.success("ACCESS GRANTED. WELCOME, OPERATOR.")
        tab1, tab2, tab3 = st.tabs(["UPLOAD MUSIC", "UPLOAD VISUALS", "INCOMING DATA"])
        with tab1:
            st.markdown("### ADD AUDIO SOURCE")
            with st.form("add_song_admin"):
                new_title = st.text_input("SONG TITLE")
                new_url = st.text_input("URL (SoundCloud/Bandcamp/Spotify)")
                new_platform = st.selectbox("PLATFORM", ["SoundCloud", "Bandcamp", "Spotify", "RA", "Other"])
                submitted = st.form_submit_button("UPLOAD TRACK")
                if submitted:
                    if not new_title:
                        st.error("Please provide a song title.")
                    else:
                        if new_url and not validators.url(new_url):
                            st.error("Please provide a valid URL or leave blank.")
                        else:
                            st.session_state.songs.append({"title": new_title, "url": new_url or "#", "platform": new_platform})
                            st.success(f"TRACK '{new_title}' ADDED TO ARCHIVE.")
            if st.button("PURGE AUDIO ARCHIVE"):
                st.session_state.songs = []
                st.warning("AUDIO ARCHIVE CLEARED.")

        with tab2:
            st.markdown("### ADD VISUAL ASSET")
            with st.form("add_photo_admin"):
                new_caption = st.text_input("CAPTION")
                new_img_url = st.text_input("IMAGE URL")
                uploaded = st.form_submit_button("UPLOAD VISUAL")
                if uploaded:
                    # allow either valid URL or local path
                    if new_img_url and not validators.url(new_img_url) and not new_img_url.startswith("/mnt/"):
                        st.error("Provide a valid http(s) URL or local server path (/mnt/...)")
                    else:
                        st.session_state.gallery.append({"caption": new_caption or "Untitled", "url": new_img_url or POSTER_IMG})
                        st.success("VISUAL ASSET ADDED TO FEED.")
            st.write("---")
            st.markdown("### SITE DIAGNOSTICS")
            if st.button("Run Broken Link Check"):
                with st.spinner("Scanning links..."):
                    links = []
                    # collect images & song urls
                    for s in st.session_state.songs:
                        u = s.get("url")
                        if u and u != "#":
                            links.append(u)
                    for g in st.session_state.gallery:
                        links.append(g.get("url"))
                    # dedupe
                    links = list(dict.fromkeys([l for l in links if l]))
                    results = check_links(links)
                    df = pd.DataFrame(results)
                    st.dataframe(df)
                    csv_buf = io.StringIO()
                    df.to_csv(csv_buf, index=False)
                    st.download_button("Download link report", csv_buf.getvalue(), file_name="link_report.csv")
        with tab3:
            st.markdown("### INCOMING TRANSMISSIONS")
            if len(st.session_state.bookings) > 0:
                st.dataframe(pd.DataFrame(st.session_state.bookings))
            else:
                st.info("NO NEW MESSAGES.")
    else:
        st.info("Enter operator auth code to manage content (admin123).")

elif selected == "ABOUT":
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.markdown("## THE PROJECT")
        st.markdown("""
        **Tuesdaynightfreak** is a dedicated exploration of electronic sound.
        Founded in Melbourne, the project focuses on the visceral experience of live hardware performance.
        """)
        st.markdown("## CONTACT MANAGEMENT")
        st.code("mgmt@tuesdaynightfreak.com")
        st.markdown("## DEMOS")
        st.code("demos@housekeeping-rec.com")
    with col2:
        st.markdown("## NEWSLETTER")
        with st.form("newsletter"):
            email = st.text_input("EMAIL ADDRESS")
            sub = st.form_submit_button("SUBSCRIBE")
            if sub:
                if not email or "@" not in email:
                    st.error("Please provide a valid email address.")
                else:
                    st.success("Thanks — you're on the list.")
        st.write("---")
        st.markdown("#### PRESS KIT")
        st.button("DOWNLOAD EPK (ZIP)")

# -------------------------------------------------------------------------
# End of file
# -------------------------------------------------------------------------
