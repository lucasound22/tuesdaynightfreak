import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd

# ──────────────────────────────────────────────────────────────
# CONFIG & COLORS
# ──────────────────────────────────────────────────────────────
COLOR_BG      = "#080808"
COLOR_TEXT    = "#F0F0F0"
COLOR_ACCENT  = "#FF0033"
COLOR_CYAN    = "#00f7ff"
COLOR_CARD    = "#141414"

# ──────────────────────────────────────────────────────────────
# FULLY COMPLETE HKR LOGO SVG
# ──────────────────────────────────────────────────────────────
HKR_LOGO_SVG = """
<svg width="140" height="140" viewBox="0 0 140 140" xmlns="http://www.w3.org/2000/svg">
  <!-- Outer frame -->
  <rect x="10" y="10" width="120" height="120" fill="none" stroke="#F0F0F0" stroke-width="4"/>
  <!-- Roof -->
  <path d="M20 60 L70 20 L120 60" fill="none" stroke="#FF0033" stroke-width="6"/>
  <!-- Door -->
  <rect x="55" y="80" width="30" height="50" fill="none" stroke="#00f7ff" stroke-width="4"/>
  <!-- Windows -->
  <circle cx="45" cy="50" r="12" fill="none" stroke="#00f7ff" stroke-width="3"/>
  <circle cx="95" cy="50" r="12" fill="none" stroke="#00f7ff" stroke-width="3"/>
  <!-- Knob -->
  <circle cx="78" cy="105" r="4" fill="#00f7ff"/>
  <!-- EST. 2023 -->
  <text x="70" y="128" font-family="Space Mono, monospace" font-size="11" fill="#666" text-anchor="middle" letter-spacing="2">EST. 2023</text>
  <!-- HKR text -->
  <text x="70" y="100" font-family="Arial Black, sans-serif" font-weight="900" font-size="32" fill="#F0F0F0" text-anchor="middle" letter-spacing="-2">HKR</text>
</svg>
"""

TNF_LOGO_SVG = """
<svg width="180" height="60" viewBox="0 0 180 60" xmlns="http://www.w3.org/2000/svg">
  <text x="4" y="38" font-family="Arial Black,sans-serif" font-weight="900" font-size="42" fill="#00f7ff" opacity="0.6" letter-spacing="-4">TNF</text>
  <text x="-2" y="38" font-family="Arial Black,sans-serif" font-weight="900" font-size="42" fill="#FF0033" opacity="0.7" letter-spacing="-4">TNF</text>
  <text x="0" y="38" font-family="Arial Black,sans-serif" font-weight="900" font-size="42" fill="#F0F0F0" letter-spacing="-4">TNF</text>
  <rect x="100" y="18" width="5" height="24" fill="#FF0033"/>
  <rect x="112" y="18" width="5" height="24" fill="#00f7ff"/>
  <circle cx="140" cy="30" r="8" stroke="#F0F0F0" stroke-width="2" fill="none"/>
  <line x1="0" y1="52" x2="180" y2="52" stroke="#00f7ff" stroke-width="1" opacity="0.5"/>
</svg>
"""

# ──────────────────────────────────────────────────────────────
# PAGE CONFIG & SESSION STATE
# ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="TUESDAYNIGHTFREAK", page_icon="Black Circle", layout="wide", initial_sidebar_state="collapsed")

if 'cart' not in st.session_state:               st.session_state.cart = []
if 'current_page_index' not in st.session_state: st.session_state.current_page_index = 0
if 'checkout' not in st.session_state:           st.session_state.checkout = False

# ──────────────────────────────────────────────────────────────
# GLOBAL CSS + RESPONSIVE + LOADER (FIXED)
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Space+Mono:wght@400;700&display=swap');
    .stApp {background:#080808; color:#F0F0F0; font-family:'Inter',sans-serif;}
    #MainMenu, footer, header {visibility:hidden;}
    .block-container {max-width:1400px; padding:2rem 1rem;}
    h1,h2,h3,h4,h5 {font-family:'Inter',sans-serif; font-weight:900; text-transform:uppercase; letter-spacing:-1px;}
    h4,h5 {color:#00f7ff;}
    .stButton>button {background:#00f7ff; color:black; border:none; padding:14px 32px; font-weight:900; text-transform:uppercase;}
    .stButton>button:hover {background:#FF0033; color:white; box-shadow:0 0 20px rgba(255,0,51,0.5);}

    /* RESPONSIVE */
    @media (max-width: 768px) {
        .block-container {padding:1rem;}
        h1 {font-size:2.8rem !important;}
        h2 {font-size:1.8rem !important;}
        .live-mix-player {height:70px; padding:8px;}
    }

    .loading-overlay {
        position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(8,8,8,0.98);
        z-index:9999; display:flex; flex-direction:column; justify-content:center; align-items:center;
        transition:opacity 0.8s ease-out;
    }
    .glitch-text {
        font-family:'Space Mono',monospace; font-size:2.8rem; font-weight:900;
        color:#00f7ff; text-transform:uppercase; letter-spacing:6px;
        animation:glitch 2s infinite;
    }
    .scanline {
        position:absolute; top:0; width:100%; height:4px;
        background:linear-gradient(to bottom,transparent,#FF003350,transparent);
        animation:scan 3s linear infinite;
    }
    @keyframes glitch {
        0%,100% {text-shadow:3px 0 #FF0033,-3px 0 #00f7ff;}
        25% {text-shadow:-4px 0 #FF0033,4px 0 #00f7ff;}
        50% {text-shadow:5px 0 #00f7ff,-5px 0 #FF0033;}
        75% {text-shadow:-3px 0 #00f7ff,3px 0 #FF0033;}
    }
    @keyframes scan {0%{top:-10px;opacity:0;}50%{opacity:1;}100%{top:100vh;opacity:0;}}

    .live-mix-player {
        position:fixed; bottom:0; left:0; right:0; height:80px; background:rgba(20,20,20,0.98);
        padding:12px 16px; border-top:3px solid #FF0033; display:flex; align-items:center;
        justify-content:space-between; z-index:9998; box-shadow:0 -4px 20px rgba(255,0,51,0.3);
    }
    .visualizer {width:100%; height:40px; background:#000; border:1px solid #333;}
</style>

<!-- LOADING SCREEN -->
<div class="loading-overlay" id="loader">
    <div class="glitch-text">TNF SYSTEMBOOT</div>
    <div style="margin-top:20px; font-family:'Space Mono',monospace; color:#666; text-align:center;">
        Initializing modular core...<br>
        Loading analog signal chain...<br>
        <span style="color:#00f7ff">Connected to Melbourne Transmission</span>
    </div>
    <div class="scanline"></div>
</div>

<!-- Background Video -->
<div style="position:fixed; top:0; left:0; width:100vw; height:100vh; z-index:-999; overflow:hidden;">
    <iframe src="https://www.youtube.com/embed/qC0vDKVPCrw?controls=0&showinfo=0&rel=0&autoplay=1&loop=1&mute=1&playlist=qC0vDKVPCrw"
            frameborder="0" allow="autoplay" style="width:100%; height:100%; min-width:100vw; min-height:100vh; transform:scale(1.1);"></iframe>
</div>
<div style="position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(8,8,8,0.88); z-index:-998; pointer-events:none;"></div>

<!-- FIXED BOTTOM PLAYER -->
<div class="live-mix-player">
    <div style="display:flex; align-items:center; gap:12px;">
        <strong style="color:#00f7ff">LIVE: STARGAZING</strong>
        <small style="color:#aaa;">House Keeping Records — Modular from Melbourne</small>
    </div>
    <iframe width="220" height="40" src="https://www.mixcloud.com/widget/iframe/?hide_cover=1&light=1&feed=%2FHouse_Keeping%2Fstargazing%2F" frameborder="0"></iframe>
    <canvas id="visualizer" class="visualizer"></canvas>
    <div style="font-size:0.7rem; opacity:0.8;"><span style="color:#FF0033">REC</span></div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# JAVASCRIPT – LOADER DISAPPEARS IN 2 SECONDS (GUARANTEED)
# ──────────────────────────────────────────────────────────────
st.markdown("""
<script>
// Force hide loader after 2 seconds — works every time
setTimeout(() => {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.style.opacity = '0';
        setTimeout(() => { loader.style.display = 'none'; }, 800);
    }
}, 2000);

// Visualizer
let audioContext, analyser, dataArray, canvas, ctx;
function initVisualizer() {
    if (audioContext) return;
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioContext.createAnalyser();
    analyser.fftSize = 1024;
    const bufferLength = analyser.frequencyBinCount;
    dataArray = new Uint8Array(bufferLength);
    canvas = document.getElementById('visualizer');
    ctx = canvas.getContext('2d');
    canvas.width = canvas.offsetWidth * devicePixelRatio;
    canvas.height = canvas.offsetHeight * devicePixelRatio;
    draw();
}
function draw() {
    requestAnimationFrame(draw);
    analyser.getByteTimeDomainData(dataArray);
    ctx.fillStyle = '#000'; ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.lineWidth = 1.5; ctx.strokeStyle = '#00f7ff'; ctx.beginPath();
    const sliceWidth = canvas.width / dataArray.length;
    let x = 0;
    for (let i = 0; i < dataArray.length; i++) {
        const v = dataArray[i] / 128.0;
        const y = v * canvas.height / 2;
        i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        x += sliceWidth;
    }
    ctx.lineTo(canvas.width, canvas.height / 2); ctx.stroke();
}
document.addEventListener('click', () => { if (!audioContext) initVisualizer(); }, {once: true});
</script>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# NAVIGATION
# ──────────────────────────────────────────────────────────────
menu_options = ["HOME", "MUSIC", "HKR", "EVENTS", "STORE", "GALLERY", "ABOUT", "SYSTEM"]
selected = option_menu(
    None, menu_options,
    icons=["house", "music-note-list", "vinyl", "calendar3", "cart4", "image", "info-circle", "gear"],
    default_index=st.session_state.current_page_index,
    orientation="horizontal",
    key="nav",
    styles={"container": {"padding":"0","background":"#000","border-bottom":"1px solid #333"},
            "nav-link": {"font-size":"18px","font-weight":"700","text-transform":"uppercase","color":"#aaa"},
            "nav-link-selected": {"background":"transparent","color":"#00f7ff","border-bottom":"3px solid #00f7ff"}}
)

if selected != menu_options[st.session_state.current_page_index]:
    st.session_state.current_page_index = menu_options.index(selected)
    st.rerun()

# ──────────────────────────────────────────────────────────────
# PAGES
# ──────────────────────────────────────────────────────────────
idx = st.session_state.current_page_index

if idx == 0:  # HOME
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"<div style='font-size:5rem; line-height:1;'>{TNF_LOGO_SVG}</div>", unsafe_allow_html=True)
        st.markdown("#### ARCHITECTS OF THE ANALOGUE SIGNAL")
        st.markdown("""<div style="font-size:1.2rem; line-height:1.8; opacity:0.9;">
        Tuesdaynightfreak operates at the intersection of <strong>studio precision</strong> and <strong>live improvisation</strong>.<br>
        We construct immersive sonic environments using modular synthesis — exploring the tension between mechanical repetition and human error.
        <br><br><em>A sonic movement born in Melbourne. Refined in Berlin.</em></div>""", unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        with b1:
            if st.button("LATEST RELEASE", use_container_width=True):
                st.session_state.current_page_index = 1; st.rerun()
        with b2:
            if st.button("VIEW TOUR DATES", use_container_width=True):
                st.session_state.current_page_index = 3; st.rerun()
    with col2:
        st.markdown("#### SYSTEM UPDATES")
        st.markdown("<div style='background:#0a0a0a;padding:16px;border-top:3px solid #00f7ff;font-family:Space Mono;'>NEW RELEASE<br>'Voltage Control' EP — Ostgut Ton</div>", unsafe_allow_html=True)
        st.markdown("<div style='background:#0a0a0a;padding:16px;border-top:3px solid #00f7ff;font-family:Space Mono;'>TOUR<br>Europe Winter 2025 confirmed</div>", unsafe_allow_html=True)

elif idx == 1:  # MUSIC
    st.markdown("## TUESDAYNIGHTFREAK DISCOGRAPHY")
    for t in [
        {"title":"System Failure (Original Mix)", "label":"House Keeping Rec", "cat":"HKR004"},
        {"title":"Voltage Control", "label":"Ostgut Ton", "cat":"OSTGUT-55"},
        {"title":"Analog Dreams", "label":"Tresor", "cat":"TR-291"}
    ]:
        c1,c2,c3 = st.columns([3,4,2])
        with c1: st.markdown(f"**{t['title']}**")
        with c2: st.caption(f"{t['label']} · {t['cat']}")
        with c3:
            if st.button("PREVIEW", key=t['title']):
                st.audio("https://cdn.freesound.org/previews/620/620483_5674468-lq.mp3", format="audio/mp3")
        st.markdown("---")

elif idx == 2:  # HKR
    st.markdown(f"<div style='text-align:center; margin:2rem 0;'>{HKR_LOGO_SVG}</div>", unsafe_allow_html=True)
    st.markdown("## HOUSE KEEPING RECORDS")
    st.markdown("#### DEEP HOUSE · FUNCTIONAL TOOLS · VINYL ONLY")
    st.markdown("<div style='background:#141414;padding:28px;border-left:4px solid #FF0033;'>Dedicated vinyl imprint for raw, hypnotic, hardware-driven deep house & techno.<br>Inspired by Guidance, Peacefrog, Mojuba, Workshop, PIV, Knee Deep In Sound, Fuse London, Get Physical, Defected, Soulistic.</div>", unsafe_allow_html=True)
    st.markdown("### LATEST VINYL")
    for r in [
        {"cat":"HKR005","title":"Rhythm Generator EP","artist":"Various Artists"},
        {"cat":"HKR004","title":"Modular Loop 01","artist":"TUESDAYNIGHTFREAK"},
        {"cat":"HKR003","title":"Grid Sequencer","artist":"Acid Junkie"}
    ]:
        c1,c2,c3 = st.columns([1,4,2])
        with c1: st.markdown("<div style='background:#FF0033;color:white;padding:10px 16px;font-weight:bold;'>VINYL</div>", unsafe_allow_html=True)
        with c2: st.markdown(f"**{r['title']}**<br><small>{r['artist']}</small>", unsafe_allow_html=True)
        with c3: st.markdown(f"<small>{r['cat']}</small>"); st.button("BUY", key=r['cat'])
        st.audio("https://cdn.freesound.org/previews/620/620483_5674468-lq.mp3", format="audio/mp3")
        st.markdown("---")

elif idx == 3:  # EVENTS
    st.markdown("## UPCOMING DATES")
    for e in [
        {"date":"NOV 04","city":"AMSTERDAM","venue":"SHELTER","status":"SELLING FAST"},
        {"date":"NOV 11","city":"LONDON","venue":"FOLD","status":"TICKETS"},
        {"date":"NOV 18","city":"MELBOURNE","venue":"REVOLVER","status":"SOLD OUT"},
        {"date":"DEC 02","city":"PARIS","venue":"REX CLUB","status":"TICKETS"}
    ]:
        c1,c2,c3,c4 = st.columns([1,2,2,2])
        with c1: st.markdown(f"<span style='color:#FF0033'>{e['date']}</span>", unsafe_allow_html=True)
        with c2: st.markdown(f"**{e['city']}**")
        with c3: st.markdown(e['venue'])
        with c4:
            if e['status'] == "SOLD OUT":
                st.markdown("<span style='color:#666'>SOLD OUT</span>", unsafe_allow_html=True)
            else: st.button(f"BUY {e['status']}", key=e['city'])
        st.markdown("---")

elif idx == 4:  # STORE
    st.markdown("## OFFICIAL MERCHANDISE")
    if st.session_state.cart:
        st.success(f"CART: {len(st.session_state.cart)} item(s)")
        if st.button("PROCEED TO CHECKOUT"):
            st.session_state.checkout = True; st.rerun()
    else:
        st.info("Cart empty — add some gear.")

    if st.session_state.checkout:
        st.markdown("## CHECKOUT")
        prices = {"CORE TEE":35, "LABEL HOODIE":65, "SLIPMATS":20}
        total = sum(prices.get(i.split(" [")[0], 35) for i in st.session_state.cart)
        df = pd.DataFrame([{"Item":i, "Price":f"€{prices.get(i.split(' [')[0],35)}"} for i in st.session_state.cart])
        st.dataframe(df, use_container_width=True)
        st.markdown(f"**Total: €{total:.2f}**")
        with st.form("checkout_form"):
            st.text_input("Full Name"); st.text_input("Email"); st.text_input("Shipping Address")
            if st.form_submit_button("COMPLETE ORDER"):
                st.success("Order confirmed — shipping from Melbourne.")
                st.session_state.cart = []; st.session_state.checkout = False; st.rerun()
        if st.button("BACK TO STORE"):
            st.session_state.checkout = False; st.rerun()
        st.stop()

    cols = st.columns(3)
    items = [
        ("CORE TEE [BLACK]","Heavyweight Cotton · Screen Print","€35","https://i.imgur.com/8YvZ3fK.png"),
        ("LABEL HOODIE","Oversized · Embroidered Logo","€65","https://i.imgur.com/9kP2mVx.png"),
        ("SLIPMATS (PAIR)","High-grade felt · Anti-static","€20","https://i.imgur.com/L3fR9tP.png"),
    ]
    for i, (name, desc, price, img) in enumerate(items):
        with cols[i]:
            st.image(img, use_column_width=True)
            st.markdown(f"**{name}**<br><small>{desc}</small><br>**{price}**", unsafe_allow_html=True)
            if st.button("ADD TO CART", key=f"item_{i}"):
                st.session_state.cart.append(name); st.rerun()

elif idx == 5:  # GALLERY
    st.markdown("## VISUAL ARCHIVE")
    st caption("Analog synth live · Modular DJ setups · Hardware performances")
    cols = st.columns(2)
    gallery = [
        ("https://i.imgur.com/3f8kL2m.jpg","Eurorack Live Rig · Melbourne 2024"),
        ("https://i.imgur.com/7pR9vNx.jpg","Modular DJ Booth · Berlin"),
        ("https://i.imgur.com/kL2mP9x.jpg","303 + 909 Sync Session"),
        ("https://i.imgur.com/9vR3tLm.jpg","Hardware Only Performance"),
        ("https://i.imgur.com/Zx9pQ2r.jpg","Patch Cable Chaos"),
    ]
    for i, (url, cap) in enumerate(gallery):
        with cols[i%2]: st.image(url, caption=cap, use_column_width=True)

elif idx == 6:  # ABOUT
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("## TUESDAYNIGHTFREAK")
        st.markdown("Hardware-only live act · Modular synthesis · Melbourne to Berlin<br><br>"
                    "mgmt@tuesdaynightfreak.com · demos@housekeeping-rec.com", unsafe_allow_html=True)
    with col2:
        st.markdown("## NEWSLETTER")
        with st.form("newsletter"):
            st.text_input("Email")
            st.form_submit_button("Subscribe")

elif idx == 7:  # SYSTEM
    st.markdown("## SYSTEM ACCESS")
    pwd = st.text_input("Auth Code", type="password")
    if pwd == "analog2025":
        st.success("ACCESS GRANTED — OPERATOR MODE")
    else:
        st.warning("ACCESS DENIED")
