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
# BRANDING SVGs
# ──────────────────────────────────────────────────────────────
TNF_LOGO_SVG = """
<svg width="180" height="60" viewBox="0 0 180 60" xmlns="http://www.w3.org/2000/svg">
  <text x="4" y="38" font-family="Arial Black, sans-serif" font-weight="900" font-size="42" fill="#00f7ff" opacity="0.6" letter-spacing="-4">TNF</text>
  <text x="-2" y="38" font-family="Arial Black, sans-serif" font-weight="900" font-size="42" fill="#FF0033" opacity="0.7" letter-spacing="-4">TNF</text>
  <text x="0" y="38" font-family="Arial Black, sans-serif" font-weight="900" font-size="42" fill="#F0F0F0" letter-spacing="-4">TNF</text>
  <rect x="100" y="18" width="5" height="24" fill="#FF0033"/>
  <rect x="112" y="18" width="5" height="24" fill="#00f7ff"/>
  <circle cx="140" cy="30" r="8" stroke="#F0F0F0" stroke-width="2" fill="none"/>
  <line x1="0" y1="52" x2="180" y2="52" stroke="#00f7ff" stroke-width="1" opacity="0.5"/>
</svg>
"""

HKR_LOGO_SVG = """
<svg width="110" height="110" viewBox="0 0 110 110" xmlns="http://www.w3.org/2000/svg">
  <rect x="8" y="8" width="94" height="94" stroke="#F0F0F0" stroke-width="4" fill="none"/>
  <path d="M15 45 L55 15 L95 45" stroke="#FF0033" stroke-width="5" fill="none"/>
  <circle cx="55" cy="70" r="22" stroke="#00f7ff" stroke-width="4" fill="none"/>
  <rect x="53" y="64" width="4" height="12" fill="#00f7ff"/>
  <text x="55" y="100" font-family="monospace" font-size="10" fill="#888" text-anchor="middle">EST. 2023</text>
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
# GLOBAL CSS + WEB AUDIO API SYNTH + MOBILE OPTIMIZATION
# ──────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Space+Mono:wght@400;700&display=swap');
    .stApp {{background:{COLOR_BG}; color:{COLOR_TEXT}; font-family:'Inter',sans-serif;}}
    #MainMenu, footer, header {{visibility:hidden;}}
    .block-container {{max-width:1400px; padding-top:2rem; padding-left:1rem; padding-right:1rem;}}
    h1,h2,h3,h4,h5 {{font-family:'Inter',sans-serif; font-weight:900; text-transform:uppercase; letter-spacing:-1px;}}
    h4,h5 {{color:{COLOR_CYAN};}}
    .stButton>button {{background:{COLOR_CYAN}; color:black; border:none; padding:14px 32px; font-weight:900; text-transform:uppercase;}}
    .stButton>button:hover {{background:{COLOR_ACCENT}; color:white; box-shadow:0 0 20px rgba(255,0,51,0.5);}}
    .content-card {{background:{COLOR_CARD}; padding:28px; border-left:4px solid {COLOR_ACCENT};}}
    .tech-card {{background:#0a0a0a; padding:16px; border-top:3px solid {COLOR_CYAN}; font-family:'Space Mono',monospace;}}
    .live-mix-player {{
        position:fixed; bottom:16px; left:16px; right:16px; z-index:9999;
        background:rgba(20,20,20,0.97); padding:12px 16px; border-left:5px solid {COLOR_ACCENT};
        box-shadow:0 0 30px rgba(255,0,51,0.4); border-radius:0;
    }}
    .visualizer {{width:100%; height:180px; background:#000; margin:10px 0; border:1px solid #333;}}
    .video-bg {{position:fixed; top:0; left:0; width:100vw; height:100vh; z-index:-999; overflow:hidden;}}
    .video-bg iframe {{width:100%; height:100%; min-width:100vw; min-height:100vh; transform:scale(1.1);}}
    .overlay {{position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(8,8,8,0.88); z-index:-998; pointer-events:none;}}
    @media (max-width: 768px) {{
        .block-container {{padding-top:1rem;}}
        h1 {{font-size:2.5rem !important;}}
        .live-mix-player {{bottom:8px; left:8px; right:8px;}}
    }}
</style>

<!-- Ambient Background Video -->
<div class="video-bg">
    <iframe src="https://www.youtube.com/embed/qC0vDKVPCrw?controls=0&showinfo=0&rel=0&autoplay=1&loop=1&mute=1&playlist=qC0vDKVPCrw"
            frameborder="0" allow="autoplay"></iframe>
</div>
<div class="overlay"></div>

<!-- LIVE 24/7 MIX + WEB AUDIO API MODULAR VISUALIZER -->
<div class="live-mix-player">
    <strong style="color:{COLOR_CYAN};">LIVE TRANSMISSION</strong>
    <small> — Modular Synth 24/7 from Berlin</small>
    <audio controls autoplay style="width:100%; margin:8px 0;">
        <source src="https://stream.zeno.fm/6x9q7v3k1k8uv" type="audio/mpeg">
    </audio>
    <canvas id="visualizer" class="visualizer"></canvas>
    <div style="font-size:0.7rem; opacity:0.8;">
        <span style="color:{COLOR_ACCENT};">REC</span> Tuesdaynightfreak — Hardware Only
    </div>
</div>

<script>
// Web Audio API Modular Visualizer (Oscilloscope + Frequency Bars)
let audioContext, analyser, source, dataArray, canvas, ctx, animationId;

function initVisualizer() {{
    if (audioContext) return;
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioContext.createAnalyser();
    analyser.fftSize = 2048;
    const bufferLength = analyser.frequencyBinCount;
    dataArray = new Uint8Array(bufferLength);

    const audio = document.querySelector('audio');
    source = audioContext.createMediaElementSource(audio);
    source.connect(analyser);
    analyser.connect(audioContext.destination);

    canvas = document.getElementById('visualizer');
    ctx = canvas.getContext('2d');
    canvas.width = canvas.offsetWidth * devicePixelRatio;
    canvas.height = canvas.offsetHeight * devicePixelRatio;

    draw();
}}

function draw() {{
    animationId = requestAnimationFrame(draw);
    analyser.getByteTimeDomainData(dataArray);

    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.lineWidth = 2;
    ctx.strokeStyle = '{COLOR_CYAN}';
    ctx.beginPath();

    const sliceWidth = canvas.width / dataArray.length;
    let x = 0;

    for (let i = 0; i < dataArray.length; i++) {{
        const v = dataArray[i] / 128.0;
        const y = v * canvas.height / 2;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
        x += sliceWidth;
    }}

    ctx.lineTo(canvas.width, canvas.height / 2);
    ctx.stroke();

    // Add frequency bars at bottom
    analyser.getByteFrequencyData(dataArray);
    const barWidth = (canvas.width / 64);
    let barX = 0;
    ctx.fillStyle = '{COLOR_ACCENT}';
    for (let i = 0; i < 64; i++) {{
        const barHeight = (dataArray[i] / 255) * 40;
        ctx.fillRect(barX, canvas.height - barHeight, barWidth - 2, barHeight);
        barX += barWidth;
    }}
}}

document.addEventListener('click', () => {{
    if (!audioContext) initVisualizer();
}}, {{once: true}});
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
    styles={
        "container": {"padding":"0","background":"#000","border-bottom":"1px solid #333"},
        "nav-link": {"font-size":"18px","font-weight":"700","text-transform":"uppercase","color":"#aaa"},
        "nav-link-selected": {"background":"transparent","color":COLOR_CYAN,"border-bottom":f"3px solid {COLOR_CYAN}"}
    }
)
st.session_state.current_page_index = menu_options.index(selected)

# ──────────────────────────────────────────────────────────────
# PAGES
# ──────────────────────────────────────────────────────────────
if selected == "HOME":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"<div style='font-size:5rem; line-height:1;'>{TNF_LOGO_SVG}</div>", unsafe_allow_html=True)
        st.markdown("#### ARCHITECTS OF THE ANALOGUE SIGNAL", unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:1.2rem; line-height:1.8; opacity:0.9;">
        Tuesdaynightfreak operates at the intersection of <strong>studio precision</strong> and <strong>live improvisation</strong>.<br>
        We construct immersive sonic environments using modular synthesis — exploring the tension between mechanical repetition and human error.
        <br><br><em>A sonic movement born in Melbourne. Refined in Berlin.</em>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        with b1:
            if st.button("LATEST RELEASE", use_container_width=True):
                st.session_state.current_page_index = 1; st.rerun()
        with b2:
            if st.button("VIEW TOUR DATES", use_container_width=True):
                st.session_state.current_page_index = 3; st.rerun()
    with col2:
        st.markdown("#### SYSTEM UPDATES")
        st.markdown(f"<div class='tech-card'>NEW RELEASE<br>'Voltage Control' EP — Ostgut Ton</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='tech-card'>TOUR<br>Europe Winter 2025 confirmed</div>", unsafe_allow_html=True)

elif selected == "MUSIC":
    st.markdown("## TUESDAYNIGHTFREAK DISCOGRAPHY")
    for t in [
        {"title":"System Failure (Original Mix)", "label":"House Keeping Rec", "cat":"HKR004"},
        {"title":"Voltage Control", "label":"Ostgut Ton", "cat":"OSTGUT-55"},
        {"title":"Analog Dreams", "label":"Tresor", "cat":"TR-291"},
    ]:
        c1, c2, c3 = st.columns([3, 4, 2])
        with c1: st.markdown(f"**{t['title']}**")
        with c2: st.caption(f"{t['label']} · {t['cat']}")
        with c3:
            if st.button("PREVIEW", key=t['title']):
                st.audio("https://cdn.freesound.org/previews/620/620483_5674468-lq.mp3", format="audio/mp3")
        st.markdown("---")

elif selected == "HKR":
    st.markdown(f"<div style='text-align:center;'>{HKR_LOGO_SVG}</div>", unsafe_allow_html=True)
    st.markdown("## HOUSE KEEPING RECORDS")
    st.markdown("#### DEEP HOUSE · FUNCTIONAL TOOLS · VINYL ONLY")
    st.markdown("""
    <div class="content-card">
    Dedicated vinyl imprint for raw, hypnotic, hardware-driven deep house & techno.<br>
    Inspired by Guidance, Peacefrog, Mojuba, Workshop, PIV, Knee Deep In Sound, Fuse London, Get Physical, Defected, Soulistic.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### LATEST VINYL")
    for r in [
        {"cat":"HKR005","title":"Rhythm Generator EP","artist":"Various Artists"},
        {"cat":"HKR004","title":"Modular Loop 01","artist":"TUESDAYNIGHTFREAK"},
        {"cat":"HKR003","title":"Grid Sequencer","artist":"Acid Junkie"},
    ]:
        c1,c2,c3 = st.columns([1,4,2])
        with c1: st.markdown(f"<div style='background:{COLOR_ACCENT};color:white;padding:10px 16px;font-weight:bold;'>VINYL</div>", unsafe_allow_html=True)
        with c2: st.markdown(f"**{r['title']}**<br><small>{r['artist']}</small>", unsafe_allow_html=True)
        with c3: st.markdown(f"<small>{r['cat']}</small>"); st.button("BUY", key=r['cat'])
        st.audio("https://cdn.freesound.org/previews/620/620483_5674468-lq.mp3", format="audio/mp3")
        st.markdown("---")

elif selected == "EVENTS":
    st.markdown("## UPCOMING DATES")
    for e in [
        {"date":"NOV 04","city":"AMSTERDAM","venue":"SHELTER","status":"SELLING FAST"},
        {"date":"NOV 11","city":"LONDON","venue":"FOLD","status":"TICKETS"},
        {"date":"NOV 18","city":"MELBOURNE","venue":"REVOLVER","status":"SOLD OUT"},
        {"date":"DEC 02","city":"PARIS","venue":"REX CLUB","status":"TICKETS"},
    ]:
        c1,c2,c3,c4 = st.columns([1,2,2,2])
        with c1: st.markdown(f"<span style='color:{COLOR_ACCENT}'>{e['date']}</span>", unsafe_allow_html=True)
        with c2: st.markdown(f"**{e['city']}**")
        with c3: st.markdown(e['venue'])
        with c4:
            if e['status'] == "SOLD OUT":
                st.markdown("<span style='color:#666'>SOLD OUT</span>", unsafe_allow_html=True)
            else: st.button(f"BUY {e['status']}", key=e['city'])
        st.markdown("---")

elif selected == "STORE":
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
        total = sum(prices.get(i.split(" [")[0].replace("CORE TEE","CORE TEE"), 35) for i in st.session_state.cart)
        df = pd.DataFrame([{"Item":i, "Price":f"€{prices.get(i.split(' [')[0].replace('CORE TEE','CORE TEE'),35)}"} for i in st.session_state.cart])
        st.dataframe(df, use_container_width=True)
        st.markdown(f"**Total: €{total:.2f}**")
        with st.form("checkout_form"):
            st.text_input("Full Name"); st.text_input("Email"); st.text_input("Shipping Address")
            if st.form_submit_button("COMPLETE ORDER"):
                st.success("Order confirmed — shipping from Berlin warehouse.")
                st.session_state.cart = []; st.session_state.checkout = False; st.rerun()
        if st.button("BACK TO STORE"):
            st.session_state.checkout = False; st.rerun()
        st.stop()

    cols = st.columns([1,1,1])
    items = [
        ("CORE TEE [BLACK]","Heavyweight Cotton · Screen Print","€35","https://images.unsplash.com/photo-1521577352947-9bb58764b69a?w=800&q=80"),
        ("LABEL HOODIE","Oversized · Embroidered Logo","€65","https://images.unsplash.com/photo-1556821845-8c5e2a6f58c1?w=800&q=80"),
        ("SLIPMATS (PAIR)","High-grade felt · Anti-static","€20","https://images.unsplash.com/photo-1622446287910-4e31f2f0c8db?w=800&q=80"),
    ]
    for i, (name, desc, price, img) in enumerate(items):
        with cols[i]:
            st.image(img, use_column_width=True)
            st.markdown(f"**{name}**<br><small>{desc}</small><br>**{price}**", unsafe_allow_html=True)
            if st.button("ADD TO CART", key=f"item{i}"):
                st.session_state.cart.append(name); st.rerun()

elif selected == "GALLERY":
    st.markdown("## VISUAL ARCHIVE")
    st.caption("Modular rigs · Berlin warehouses · Melbourne nights")
    cols = st.columns(2)
    gallery = [
        ("https://images.unsplash.com/photo-1593795899638-4a7e97d7a97b?w=1200&q=80","Patch Cable Logic · 2024"),
        ("https://images.unsplash.com/photo-1511376777868-611b54f68947?w=1200&q=80","Revolver · Melbourne"),
        ("https://images.unsplash.com/photo-1582719193157-2438e20e2e39?w=1200&q=80","Oscillator Bank"),
        ("https://images.unsplash.com/photo-1574269909862-6e3c32a8e2e9?w=1200&q=80","Tresor 4AM"),
        ("https://images.unsplash.com/photo-1511671786110-4d9573c02006?w=1200&q=80","303 + 909 Sync"),
    ]
    for i, (url, cap) in enumerate(gallery):
        with cols[i%2]: st.image(url, caption=cap, use_column_width=True)

elif selected == "ABOUT":
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

elif selected == "SYSTEM":
    st.markdown("## SYSTEM ACCESS")
    pwd = st.text_input("Auth Code", type="password")
    if pwd == "analog2025":
        st.success("ACCESS GRANTED — OPERATOR MODE")
    else:
        st.warning("ACCESS DENIED")
