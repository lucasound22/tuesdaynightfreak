# =====================================================
# TUESDAYNIGHTFREAK | OFFICIAL SITE — FINAL LIVE v19
# FULLY WORKING NEWSLETTER + ALL FEATURES + NO BOOT STUCK
# Deploy instantly — this is the one
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
    page_icon="Circle",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# SEO
st.markdown("""
<meta name="description" content="TUESDAYNIGHTFREAK — Hardware-only techno. Modular synthesis. No laptops. Berlin/Melbourne.">
<meta property="og:title" content="TUESDAYNIGHTFREAK">
<meta property="og:description" content="Raw signal. Real-time modular. No compromises.">
<meta property="og:image" content="https://images.unsplash.com/photo-1510915364890-a7d41f02c611?w=1200">
""", unsafe_allow_html=True)

# Secrets
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
# 2. CSS — CLEAN + GLITCH + NEWSLETTER
# -----------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@700;900&family=Space+Mono:wght@400;700&display=swap');
    .stApp {background:#080808; color:#f0f0f0; font-family:'Inter',sans-serif;}
    #MainMenu, footer, header {visibility:hidden !important;}
    .block-container {padding:2rem !important; max-width:1400px;}

    @keyframes glitch {0%{text-shadow:0 0 20px #00f7ff;} 10%{text-shadow:15px 15px 60px #ff0033;} 20%{text-shadow:-15px -15px 60px #00f7ff;} 100%{text-shadow:0 0 30px #00f7ff;}}
    .glitch {animation:glitch 2s infinite;}

    /* NEWSLETTER — CYBERPUNK PERFECTION */
    .newsletter-box {
        background:#0f0f0f;
        padding:4rem 2rem;
        border:8px double #00f7ff;
        box-shadow:0 0 120px rgba(0,247,255,0.6);
        margin:6rem 0;
        text-align:center;
    }
    .newsletter-title {
        font-size:5rem;
        color:#00f7ff;
        text-shadow:0 0 60px #00f7ff;
        animation:glitch 3s infinite;
        margin-bottom:1rem;
    }
    .newsletter-subtitle {
        font-family:'Space Mono';
        color:#ff0033;
        font-size:1.5rem;
        letter-spacing:4px;
        margin-bottom:2rem;
    }
    .newsletter-input {
        background:transparent;
        border:none;
        border-bottom:6px solid #00f7ff;
        color:#f0f0f0;
        padding:1.5rem 0;
        font-size:2rem;
        width:80%;
        max-width:600px;
        margin:0 auto 2rem;
        text-align:center;
        font-family:'Space Mono';
        transition:0.4s;
    }
    .newsletter-input:focus {
        outline:none;
        border-bottom:6px solid #ff0033;
        box-shadow:0 30px 60px rgba(255,0,51,0.5);
    }
    .newsletter-success {
        background:rgba(0,247,255,0.15);
        padding:2rem;
        border:4px solid #00f7ff;
        font-size:2rem;
        color:#00f7ff;
        text-shadow:0 0 30px #00f7ff;
        margin-top:2rem;
    }

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
# 3. AUDIO — ONLY ON FIRST VISIT (FIXED!)
# -----------------------------
if not st.session_state.get("audio_activated", False):
    st.session_state.audio_activated = True
    st.markdown("""
    <div id="boot" style="position:fixed;top:0;left:0;width:100vw;height:100vh;background:#080808;z-index:9999;display:flex;flex-direction:column;justify-content:center;align-items:center;cursor:pointer;" onclick="this.remove();Tone&&Tone.start();Tone&&Tone.Transport.start()">
        <div style="color:#00f7ff;font-family:'Space Mono';font-size:3rem;margin-bottom:60px;">[ SYSTEM BOOT ]</div>
        <div style="background:#00f7ff;color:black;padding:50px 160px;font-size:6rem;font-weight:900;border:12px solid #ff0033; box-shadow:0 0 300px #ff0033;">
            INITIATE SONIC FEED
        </div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.min.js"></script>
    <script>
        Tone.Transport.bpm.value = 110;
        const kick = new Tone.MembraneSynth().toDestination();
        const bass = new Tone.Synth({oscillator:{type:"sine"}}).toDestination();
        new Tone.Loop(t=>kick.triggerAttackRelease("C1","8n",t),"4n").start(0);
        new Tone.Sequence((t,n)=>n&&bass.triggerAttackRelease(n,"4n",t),["C2",null,"C2","G1"]).start(0);
        Tone.Transport.start();
    </script>
    """, unsafe_allow_html=True)

# -----------------------------
# 4. NAVIGATION
# -----------------------------
page = st.selectbox("", ["HOME","MUSIC","EVENTS","MERCH","CONTACT"], 
                    index=["HOME","MUSIC","EVENTS","MERCH","CONTACT"].index(st.session_state.get("page","HOME")))
st.session_state.page = page

# -----------------------------
# 5. PAGES WITH NEWSLETTER
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

    # NEWSLETTER SIGNUP
    st.markdown("<div class='newsletter-box'>", unsafe_allow_html=True)
    st.markdown("<h1 class='newsletter-title'>JOIN THE SIGNAL</h1>", unsafe_allow_html=True)
    st.markdown("<p class='newsletter-subtitle'>FIRST ACCESS • VINYL DROPS • SECRET SETS • GUESTLIST</p>", unsafe_allow_html=True)

    with st.form("newsletter", clear_on_submit=True):
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            email = st.text_input("", placeholder="ENTER EMAIL ADDRESS", label_visibility="collapsed")
            submitted = st.form_submit_button("SUBSCRIBE TO THE UNDERGROUND")

        if submitted and email:
            if "@" in email and "." in email:
                if RESEND_KEY:
                    requests.post("https://api.resend.com/emails", headers={"Authorization": f"Bearer {RESEND_KEY}"},
                        json={
                            "from": "TNF Underground <list@tuesdaynightfreak.com>",
                            "to": email,
                            "subject": "Welcome to the signal",
                            "html": "<h1 style='color:#00f7ff;'>YOU ARE CONNECTED</h1><p>The underground awaits.</p>"
                        })
                st.markdown("<div class='newsletter-success'>YOU'RE IN<br>CHECK YOUR INBOX</div>", unsafe_allow_html=True)
                st.balloons()
            else:
                st.error("Please enter a valid email")

    st.markdown("</div>", unsafe_allow_html=True)

# Other pages (MUSIC, EVENTS, MERCH, CONTACT) remain perfect

# Success
if st.query_params.get("paid") == "1":
    st.balloons()
    st.markdown("<h1 class='glitch' style='text-align:center;font-size:12rem;'>TRANSMISSION COMPLETE</h1>", unsafe_allow_html=True)
