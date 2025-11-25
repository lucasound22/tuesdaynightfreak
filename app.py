import streamlit as st
import pandas as pd
import requests
import time
from io import StringIO
from typing import List, Dict

# -------------------- CONFIG --------------------
st.set_page_config(page_title="Tuesday Night Freak", layout="wide")

CP_YELLOW = "#fcee0a"
CP_CYAN = "#00f0ff"
CP_RED = "#ff003c"
COLOR_BG = "#080808"
COLOR_TEXT = "#F0F0F0"
COLOR_ACCENT = "#FF0033"
POSTER_IMG = "/mnt/data/32b1d44b-a37c-4c95-acdd-0c4ef6a11a99.png"  # developer-uploaded poster

# -------------------- NAV / PAGES --------------------
PAGES = ["home", "music", "gallery", "label", "events", "store", "admin", "about"]

# -------------------- STATE INIT --------------------
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'dark' not in st.session_state:
    st.session_state.dark = True
if 'perf_log' not in st.session_state:
    st.session_state.perf_log = []

# simple in-memory session lists
if 'songs' not in st.session_state:
    st.session_state.songs = [
        {"title":"UNTITLED_SEQ_04 [LIVE REC]","url":"#","platform":"SoundCloud"},
        {"title":"MODULAR EXCURSION B (RAW)","url":"#","platform":"Bandcamp"},
    ]
if 'gallery' not in st.session_state:
    st.session_state.gallery = [
        {"caption":"WAREHOUSE RAVE // BERLIN","url":"https://images.unsplash.com/photo-1517457375825-e578c799a74f?q=80&w=1200&auto=format&fit=crop"},
        {"caption":"LIVE MODULAR RIG","url":"https://images.unsplash.com/photo-1550291652-6ea9114a47b1?q=80&w=1200&auto=format&fit=crop"},
    ]

# -------------------- UTILITIES --------------------
def is_url(u: str) -> bool:
    return bool(u and (u.startswith('http://') or u.startswith('https://')))

@st.cache_data(ttl=300)
def http_status(u: str) -> int:
    try:
        r = requests.head(u, allow_redirects=True, timeout=6)
        if r.status_code >= 400:
            r = requests.get(u, allow_redirects=True, timeout=8)
        return int(r.status_code)
    except Exception:
        return 0

# sanitize gallery on startup: replace dead urls with POSTER_IMG
def sanitize_gallery():
    fixed = []
    for g in st.session_state.gallery:
        url = g.get('url','')
        if not is_url(url):
            g['url'] = POSTER_IMG
        else:
            status = http_status(url)
            if status == 0 or status >= 400:
                g['url'] = POSTER_IMG
        fixed.append(g)
    st.session_state.gallery = fixed

sanitize_gallery()

# performance logging (append to /mnt/data/perf_log.csv)
def log_perf(event: str, meta: Dict = None):
    ts = time.time()
    entry = {'timestamp': ts, 'event': event, 'meta': str(meta or {})}
    st.session_state.perf_log.append(entry)
    try:
        # append to local CSV for persistence across sessions on Streamlit Cloud deploys
        with open('/mnt/data/perf_log.csv','a') as f:
            f.write(f"{ts},{event},{str(meta or {})}
")
    except Exception:
        pass

# -------------------- STYLES: dark/light + bg video responsive --------------------
def render_styles():
    dark = st.session_state.dark
    bg = COLOR_BG if dark else '#ffffff'
    text = COLOR_TEXT if dark else '#111111'
    accent = COLOR_ACCENT if dark else '#ff4400'
    # two background video sources: desktop (higher quality) + mobile (480p) — both shown/hidden by CSS
    VIDEO_DESKTOP = "https://assets.mixkit.co/videos/preview/mixkit-clubbing-dancers-loop-2387-large.mp4"
    VIDEO_MOBILE = "https://assets.mixkit.co/videos/preview/mixkit-clubbing-dancers-loop-2387-small.mp4"

    css = f"""
    <style>
    :root{{--bg:{bg}; --text:{text}; --accent:{accent}; --yellow:{CP_YELLOW};}}
    body, .stApp{{background:var(--bg); color:var(--text);}}
    .artist-title{{font-family:Tomorrow, sans-serif; font-size:clamp(2rem,5vw,4rem); font-weight:900; color:var(--yellow); text-shadow:4px 4px 0 #00f0ff;}}
    .logo-anim{{width:80px;height:80px;}}
    .bg-video-wrap{{position:fixed; inset:0; z-index:-1; overflow:hidden; pointer-events:none}}
    .bg-desktop{{display:block; min-width:100%; min-height:100%; object-fit:cover; filter:brightness(.45) contrast(1.05)}}
    .bg-mobile{{display:none; min-width:100%; min-height:100%; object-fit:cover; filter:brightness(.45) contrast(1.05)}}
    @media (max-width:700px){{ .bg-desktop{{display:none}}; .bg-mobile{{display:block}}; }}
    </style>
    <div class="bg-video-wrap">
      <video autoplay muted loop playsinline class="bg-desktop" poster="{POSTER_IMG}">
        <source src="{VIDEO_DESKTOP}" type="video/mp4">
      </video>
      <video autoplay muted loop playsinline class="bg-mobile" poster="{POSTER_IMG}">
        <source src="{VIDEO_MOBILE}" type="video/mp4">
      </video>
    </div>
    """
    st.markdown(css, unsafe_allow_html=True)

render_styles()

# -------------------- Animated SVG logo --------------------
ANIM_SVG = '''
<svg class="logo-anim" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="40" stroke="#fcee0a" stroke-width="4" fill="none">
    <animate attributeName="r" from="35" to="40" dur="1s" repeatCount="indefinite" />
  </circle>
  <text x="50%" y="55%" text-anchor="middle" font-family="monospace" font-weight="700" font-size="18" fill="#fcee0a">TNF</text>
</svg>
'''

# -------------------- Header / Navigation UI --------------------
cols = st.columns([1,4,1])
with cols[0]:
    st.markdown(ANIM_SVG, unsafe_allow_html=True)
with cols[1]:
    st.markdown('<div style="text-align:center"><h1 style="margin:0">TUESDAY NIGHT FREAK</h1><div style="font-size:12px">Live Hardware Electronics — Melbourne // Berlin</div></div>', unsafe_allow_html=True)
with cols[2]:
    toggle = st.checkbox('Dark mode', value=st.session_state.dark, key='dark_toggle')
    if toggle != st.session_state.dark:
        st.session_state.dark = toggle
        render_styles()

# breadcrumbs / page selector
page = st.selectbox('Navigate', PAGES, index=PAGES.index(st.session_state.page))
st.session_state.page = page
log_perf('navigate', {'page': page})

# -------------------- HOME --------------------
if st.session_state.page == 'home':
    st.markdown('''
    <div style="display:flex;gap:12px;align-items:center">
      <div class="artist-title">TUESDAY<br/>NIGHT<br/>FREAK</div>
      <div style="margin-left:18px">'''+ANIM_SVG+'''</div>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('### Immersive live modular sets — no laptops, pure voltage.')
    st.button('Listen — Latest Release')
    st.write('---')
    # featured media
    if st.session_state.gallery:
        g = st.session_state.gallery[0]
        st.image(g.get('url', POSTER_IMG), caption=g.get('caption'))

# -------------------- MUSIC (Dedicated player) --------------------
elif st.session_state.page == 'music':
    st.header('Music Player')
    st.markdown('A dedicated player for mp3/wav and SoundCloud embeds.')
    for idx, track in enumerate(st.session_state.songs):
        st.subheader(track.get('title','Untitled'))
        url = track.get('url','')
        if url.endswith('.mp3') or url.endswith('.wav'):
            st.audio(url)
        elif 'soundcloud.com' in url:
            embed = f"<iframe width='100%' height='140' scrolling='no' frameborder='no' allow='autoplay' src='https://w.soundcloud.com/player/?url={url}&auto_play=false'></iframe>"
            st.components.v1.html(embed, height=160)
        elif 'open.spotify.com' in url:
            # spotify embed
            sp = url.replace('open.spotify.com','open.spotify.com/embed')
            iframe = f"<iframe src='{sp}' width='100%' height='152' frameborder='0' allowtransparency='true' allow='encrypted-media'></iframe>"
            st.components.v1.html(iframe, height=160)
        else:
            st.write('No embeddable source. Provide mp3/wav/SoundCloud/Spotify link in ADMIN.')
        st.write('---')

# -------------------- GALLERY (AI visuals + grid) --------------------
elif st.session_state.page == 'gallery':
    st.header('Visual Feed — AI visuals & Live photos')
    col1, col2 = st.columns([3,1])
    with col2:
        st.markdown('### AI Visuals')
        if st.button('Add 6 AI visuals (sample)'):
            # In place of real AI generation we add curated techno-style images (user can replace later)
            sample = [
                'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?q=80&w=1200&auto=format&fit=crop',
                'https://images.unsplash.com/photo-1542736667-069246bdbc76?q=80&w=1200&auto=format&fit=crop',
                'https://images.unsplash.com/photo-1504384308090-c894fdcc538d?q=80&w=1200&auto=format&fit=crop',
            ]
            for s in sample:
                st.session_state.gallery.append({'caption':'AI VISUAL', 'url': s})
            sanitize_gallery()
            st.success('Sample AI visuals added to gallery (replace with your generated images as desired).')
    # grid
    cols = st.columns(3)
    for i, g in enumerate(st.session_state.gallery):
        with cols[i % 3]:
            st.image(g.get('url', POSTER_IMG), caption=g.get('caption',''), use_column_width=True)

# -------------------- LABEL --------------------
elif st.session_state.page == 'label':
    st.header('House Keeping Records')
    st.markdown('Vinyl-first label — releases, promos, demos.')
    with st.expander('Submit Demo'):
        alias = st.text_input('Artist alias')
        link = st.text_input('SoundCloud / Private link')
        if st.button('Submit demo'):
            st.success('Demo received — we will review.')

# -------------------- EVENTS --------------------
elif st.session_state.page == 'events':
    st.header('Tour Dates')
    events = [
        {'date':'2025-11-04','city':'AMSTERDAM','venue':'SHELTER','tickets':'https://example.com'},
        {'date':'2025-11-11','city':'LONDON','venue':'FOLD','tickets':'https://example.com'},
    ]
    for e in events:
        c1,c2,c3 = st.columns([1,3,2])
        with c1: st.markdown(f"**{e['date']}**")
        with c2:
            st.markdown(f"**{e['city']} — {e['venue']}**")
        with c3:
            st.markdown(f"[Buy Tickets ▶]({e['tickets']})")

# -------------------- STORE --------------------
elif st.session_state.page == 'store':
    st.header('Shop — Vinyl & Merch')
    st.markdown('Contact for wholesale and stockists.')

# -------------------- ADMIN (uploads + spotify/beatport embeds) --------------------
elif st.session_state.page == 'admin':
    st.header('Admin — Uploads & Embeds')
    with st.form('add_track'):
        t = st.text_input('Title')
        u = st.text_input('URL (mp3/wav/SoundCloud/Spotify)')
        submit = st.form_submit_button('Add track')
        if submit:
            st.session_state.songs.append({'title':t,'url':u})
            st.success('Track added')
            log_perf('add_track', {'title': t})
    with st.form('add_visual'):
        cap = st.text_input('Caption')
        img = st.text_input('Image URL (http(s) or /mnt/...)')
        addv = st.form_submit_button('Add visual')
        if addv:
            if img and not is_url(img) and not img.startswith('/mnt/'):
                st.error('Provide a valid http(s) URL or /mnt/... path')
            else:
                st.session_state.gallery.append({'caption':cap or 'Untitled','url': img or POSTER_IMG})
                sanitize_gallery()
                st.success('Visual added')
    st.write('---')
    st.markdown('### Embed Beatport release (link)')
    beat = st.text_input('Beatport release URL (optional)')
    if beat and is_url(beat):
        # Beatport doesn't offer a consistent public embed; provide link and try iframe fallback
        st.markdown(f"[Open on Beatport]({beat})")
        try:
            iframe = f"<iframe src='{beat}' width='100%' height='300'></iframe>"
            st.components.v1.html(iframe, height=320)
        except Exception:
            st.info('Beatport embed may not be supported — link provided.')

# -------------------- ABOUT / DOMAIN & SSL INSTRUCTIONS --------------------
elif st.session_state.page == 'about':
    st.header('About & Deployment Notes')
    st.markdown('''
    ### Custom domain & SSL (quick guide)
    1. Deploy your app on Streamlit Cloud (or any VPS).  
    2. Add your custom domain in the hosting provider settings (e.g., Cloudflare) and point DNS to Streamlit's provided CNAME / A records.  
    3. Enable Cloudflare (optional) and turn on "Always Use HTTPS". Streamlit Cloud provides HTTPS automatically for apps deployed there.  
    4. If self-hosting: configure a reverse proxy (Nginx) and obtain certificates with Let's Encrypt (certbot) — serve on port 443.  

    If you'd like I can produce exact DNS records for your registrar and a sample Nginx config.
    ''')
    st.write('---')
    st.markdown('### Performance logging')
    st.markdown('We log lightweight interactions to `/mnt/data/perf_log.csv` for offline analysis. Request the file if you need it.')
    try:
        with open('/mnt/data/perf_log.csv','r') as f:
            st.download_button('Download perf log', f.read(), file_name='perf_log.csv')
    except Exception:
        st.info('No perf log present yet.')

# -------------------- Diagnostics: quick link scanner available on admin page --------------------

# final perf entry
log_perf('page_view', {'page': st.session_state.page})

# EOF
