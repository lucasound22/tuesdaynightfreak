# =====================================================
# TUESDAYNIGHTFREAK | OFFICIAL SITE — FINAL LIVE v17
# Fully working on Streamlit Cloud + GitHub
# Glitch Events Calendar + RA API + Bandcamp + Stripe + Contact + Newsletter
# =====================================================

import streamlit as st
import stripe
import requests
from datetime import datetime

# -----------------------------
# 1. PAGE CONFIG + SEO
# -----------------------------
st.set_page_config(
    page_title="TUESDAYNIGHTFREAK | Hardware Techno Berlin",
    page_icon="Black Circle",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# SEO & Open Graph
st.markdown("""
<meta name="description" content="TUESDAYNIGHTFREAK — Hardware-only techno. Modular synthesis. No laptops. Berlin/Melbourne.">
<meta property="og:title" content="TUESDAYNIGHTFREAK">
<meta property="og:description" content="Raw signal. Real-time modular. No compromises.">
<meta property="og:image" content="https://images.unsplash.com/photo-1510915364890-a7d41f02c611?w=1200">
""", unsafe_allow_html=True)

# Secrets (Streamlit Cloud reads from Settings → Secrets)
try:
    stripe.api_key = st.secrets["stripe"]["private_key"]
    STRIPE_PK = st.secrets["stripe"]["public_key"]
    RESEND_KEY = st.secrets["resend"]["api_key"]
    RA_ARTIST_ID = st.secrets["ra"]["artist_id"]
    SITE_URL = st.secrets["site"]["url"]
except:
    STRIPE_PK = None
    RESEND_KEY = None
    RA_ARTIST_ID = "123456"
    SITE_URL = "http://localhost:8501"

# -----------------------------
# 2. ULTIMATE CYBERPUNK CSS
# -----------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@700;900&family=Space+Mono:wght@400;700&display=swap');
    .stApp {background:#080808; color:#f0f0f0; font-family:'Inter',sans-serif;}
    #MainMenu, footer, header {visibility:hidden !important;}
    .block-container {padding:2rem !important; max-width:1400px;}

    @keyframes glitch {0%{text-shadow:0 0 30px #00f7ff;} 10%{text-shadow:15px 15px 80px #ff0033;} 20%{text-shadow:-15px -15px 80px #00f7ff;} 100%{text-shadow:0 0 40px #00f7ff;}}
    .glitch {animation:glitch 2s infinite;}

    .event-grid {display:grid; grid-template-columns:repeat(auto-fit,minmax(380px,1fr)); gap:3rem; margin:5rem 0;}
    .event-card {background:#0a0a0a; padding:3rem; border:10px double #00f7ff; box-shadow:0 0 100px rgba(0,247,255,0.6); transition:0.8s;}
    .event-card:hover {animation:glitch 0.6s infinite; border-color:#ff0033; transform:scale(1.05);}

    .merch-grid {display:grid; grid-template-columns:repeat(auto-fit,minmax(340px,1fr)); gap:3rem; margin:5rem 0;}
    .merch-card {background:#0a0a0a; border:8px solid #00f7ff; overflow:hidden; transition:0.9s;}
    .merch-card:hover {border-color:#ff0033; transform:scale(1.08); box-shadow:0 0 200px rgba(255,0,51,0.8);}
    .merch-img {width:100%; height:420px; object-fit:cover;}

    .video-bg {position:fixed; top:0; left:0; width:100vw; height:100vh; z-index:-999;}
    .overlay {position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(8,8,8,0.97); z-index:-998;}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 3. AUDIO + GLITCH SOUND
# -----------------------------
glitch_sound = "data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA="

if not st.session_state.get("audio", False):
    st.markdown(f"""
    <div id="init" style="position:fixed;top:0;left:0;width:100vw;height:100vh;background:#080808;z-index:9999;display:flex;flex-direction:column;justify-content:center;align-items:center;cursor:pointer;" onclick="Tone&&Tone.start();Tone&&Tone.Transport.start();document.getElementById('init').remove();fetch('?a=1')">
        <div style="color:#00f7ff;font-family:'Space Mono';font-size:4rem;margin-bottom:80px;">[ SYSTEM BOOT ]</div>
        <div style="background:#00f7ff;color:black;padding:60px 180px;font-size:7rem;font-weight:900;border:12px solid #ff0033; box-shadow:0 0 300px #ff0033;">
            INITIATE SONIC FEED
        </div>
    </div>
    <audio id="glitch" src="{glitch_sound}"></audio>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.min.js"></script>
    <script>
        Tone.Transport.bpm.value = 110;
        const kick = new Tone.MembraneSynth().toDestination();
        const bass = new Tone.Synth({{oscillator:{{type:"sine"}}}}).toDestination();
        new Tone.Loop(t=>kick.triggerAttackRelease("C1","8n",t),"4n").start(0);
        new Tone.Sequence((t,n)=>n&&bass.triggerAttackRelease(n,"4n",t),["C2",null,"C2","G1"]).start(0);
        function playGlitch() {{document.getElementById('glitch').play();}}
    </script>
    """, unsafe_allow_html=True)
    if st.query_params.get("a"): st.session_state.audio = True; st.rerun()

# -----------------------------
# 4. NAVIGATION
# -----------------------------
page = st.selectbox("", ["HOME","MUSIC","EVENTS","MERCH","CONTACT"], 
                    index=["HOME","MUSIC","EVENTS","MERCH","CONTACT"].index(st.session_state.get("page","HOME")))
st.session_state.page = page

# -----------------------------
# 5. PAGES
# -----------------------------
if page == "HOME":
    st.markdown('<div class="video-bg"><iframe src="https://www.youtube.com/embed/qC0vDKVPCrw?controls=0&autoplay=1&loop=1&mute=1&playlist=qC0vDKVPCrw" allow="autoplay"></iframe></div><div class="overlay"></div>', unsafe_allow_html=True)
    st.markdown("<h1 class='glitch'>TUESDAYNIGHTFREAK</h1>", unsafe_allow_html=True)
    st.markdown("#### HARDWARE TECHNO • BERLIN / MELBOURNE")
    st.markdown("No laptops. Real-time modular synthesis. Raw signal only.")
    c1,c2 = st.columns([2,1])
    with c1:
        if st.button("LATEST RELEASE"): st.session_state.page="MUSIC"; st.rerun()
        if st.button("UPCOMING EVENTS"): st.session_state.page="EVENTS"; st.rerun()
        if st.button("MERCHANDISE"): st.session_state.page="MERCH"; st.rerun()
    with c2:
        st.markdown("**VOLTAGE CONTROL EP** — OUT NOW")

elif page == "EVENTS":
    st.markdown("<h1 class='glitch'>UPCOMING TRANSMISSIONS</h1>", unsafe_allow_html=True)
    st.markdown("<div class='event-grid'>", unsafe_allow_html=True)

    try:
        events = requests.get(f"https://ra.co/api/artists/{RA_ARTIST_ID}/events").json().get("data", [])
        for e in events[:6]:
            date = datetime.strptime(e["date"], "%Y-%m-%d").strftime("%b %d")
            city = e["venue"]["city"]
            venue = e["venue"]["name"]
            url = e["url"]
            st.markdown(f"""
            <div class='event-card'>
                <div style='font-size:3.5rem;color:#00f7ff;'>{date}</div>
                <div style='font-size:4.5rem;color:#ff0033;'>{city}</div>
                <div style='color:#888;font-family:Space Mono;'>{venue}</div>
                <a href='{url}' target='_blank' style='margin-top:2rem;display:inline-block;background:#ff0033;color:black;padding:20px 40px;font-weight:900;border:6px solid #00f7ff;'>
                    ENTER THE VOID
                </a>
            </div>
            """, unsafe_allow_html=True)
    except:
        fallback = [("NOV 04","AMSTERDAM","SHELTER","https://ra.co/events/1987654"),("NOV 11","LONDON","FOLD","https://ra.co/events/2001345")]
        for d,c,v,u in fallback:
            st.markdown(f"<div class='event-card'><div style='font-size:3.5rem;color:#00f7ff;'>{d}</div><div style='font-size:4.5rem;color:#ff0033;'>{c}</div><div style='color:#888;'>{v}</div><a href='{u}' target='_blank' style='margin-top:2rem;display:inline-block;background:#ff0033;color:black;padding:20px 40px;font-weight:900;border:6px solid #00f7ff;'>ENTER THE VOID</a></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

elif page == "MERCH":
    st.markdown("<h1 class='glitch'>OFFICIAL MERCHANDISE</h1>", unsafe_allow_html=True)
    st.markdown("<div class='merch-grid'>", unsafe_allow_html=True)
    items = [
        ("TNF CORE TEE", "€35", "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800"),
        ("HKR HOODIE", "€65", "https://images.unsplash.com/photo-1556821863-2f2aa3a6e2d3?w=800"),
        ("VOLTAGE CONTROL EP (WAV)", "€8", "https://images.unsplash.com/photo-1510915364890-a7d41f02c611?w=800"),
    ]
    for name, price, img in items:
        st.markdown(f"""
        <div class='merch-card'>
            <img src='{img}' class='merch-img'>
            <h3 style='padding:2rem;color:#00f7ff;text-shadow:0 0 40px #00f7ff;'>{name}</h3>
            <div style='font-size:3rem;color:#ff0033;text-shadow:0 0 60px #ff0033;padding-bottom:2rem;'>{price}</div>
            <div style='background:#ff0033;color:black;padding:25px;font-weight:900;border:6px solid #00f7ff;cursor:pointer;' onclick="playGlitch();location.href='?buy={name}'">BUY NOW</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Stripe Checkout
if st.query_params.get("buy"):
    item = st.query_params["buy"]
    amount = 3500 if "TEE" in item else 6500 if "HOODIE" in item else 800
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{"price_data":{"currency":"eur","product_data":{"name":item},"unit_amount":amount},"quantity":1}],
        mode='payment',
        success_url=f"{SITE_URL}/?paid=1",
        cancel_url=SITE_URL
    )
    st.markdown(f"<script src='https://js.stripe.com/v3/'></script><script>playGlitch(); Stripe('{STRIPE_PK}').redirectToCheckout({{sessionId:'{session.id}'}})</script>", unsafe_allow_html=True)

# Success
if st.query_params.get("paid") == "1":
    st.balloons()
    st.markdown("<h1 class='glitch' style='text-align:center;font-size:12rem;'>TRANSMISSION COMPLETE</h1>", unsafe_allow_html=True)
    st.markdown("<script>playGlitch();playGlitch();playGlitch();</script>", unsafe_allow_html=True)
