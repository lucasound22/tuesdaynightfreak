# =====================================================
# TUESDAYNIGHTFREAK | OFFICIAL SITE v4.0 (FINAL)
# Features: Stripe + PayPal + Email Receipts + SoundCloud + Downloads
# Copy-paste ready — deploy to Streamlit Cloud now
# =====================================================

import streamlit as st
from streamlit_option_menu import option_menu
import stripe
import json
import requests
from datetime import datetime

# -----------------------------
# 1. CONFIG & SECRETS
# -----------------------------
st.set_page_config(
    page_title="TUESDAYNIGHTFREAK",
    page_icon="Black Circle",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === SECRETS (Add to .streamlit/secrets.toml) ===
try:
    stripe.api_key = st.secrets["stripe"]["private_key"]
    STRIPE_PK = st.secrets["stripe"]["public_key"]
    PAYPAL_CLIENT_ID = st.secrets["paypal"]["client_id"]
    RESEND_API_KEY = st.secrets["resend"]["api_key"]
    SITE_URL = st.secrets["site"]["url"]
    ADMIN_EMAIL = st.secrets["site"]["admin_email"]  # Your email
except Exception as e:
    st.error("Missing secrets. Check .streamlit/secrets.toml")
    st.stop()

# -----------------------------
# 2. DESIGN SYSTEM (Mobile-First)
# -----------------------------
COLOR_BG = "#080808"
COLOR_TEXT = "#F0F0F0"
COLOR_ACCENT = "#FF0033"
COLOR_CYAN = "#00f7ff"
COLOR_SECONDARY = "#141414"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&family=Space+Mono:wght@400;700&display=swap');
    .stApp {{background: {COLOR_BG}; color: {COLOR_TEXT}; font-family: 'Inter', sans-serif;}}
    #MainMenu, footer, header {{visibility: hidden !important;}}
    .block-container {{padding: 1rem !important; max-width: 1400px; margin: 0 auto;}}
    
    h1 {{font-size: 2.8rem; font-weight: 900; text-transform: uppercase; letter-spacing: -2px;}}
    h2 {{font-size: 2rem;}}
    .stButton>button {{background: {COLOR_CYAN}; color: black; border: 2px solid {COLOR_TEXT}; font-weight: 900; text-transform: uppercase; padding: 16px; width: 100%; border-radius: 0;}}
    .stButton>button:hover {{background: {COLOR_ACCENT}; box-shadow: 0 0 20px rgba(255,0,51,0.6);}}
    .product-card {{background: {COLOR_SECONDARY}; padding: 1.5rem; border-left: 5px solid {COLOR_ACCENT}; margin-bottom: 1.5rem;}}
    .cart-badge {{background: {COLOR_ACCENT}; color: white; padding: 6px 14px; border-radius: 30px; font-weight: bold;}}
    .video-bg {{position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -999; overflow: hidden;}}
    .overlay {{position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(8,8,8,0.92); z-index: -998; pointer-events: none;}}
    @media (max-width: 768px) {{
        h1 {{font-size: 2.2rem;}}
        .stColumns > div {{width: 100% !important;}}
    }}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 3. SESSION STATE
# -----------------------------
if 'cart' not in st.session_state:
    st.session_state.cart = []  # [{"name": "...", "price": 35.00, "type": "merch"|"digital", "download_url": "..."}]
if 'current_page_index' not in st.session_state:
    st.session_state.current_page_index = 0

# -----------------------------
# 4. AUDIO ACTIVATION
# -----------------------------
st.markdown(f"""
<script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.min.js"></script>
<div id="audio-overlay" onclick="startAudio()" style="position:fixed;top:0;left:0;width:100vw;height:100vh;background:{COLOR_BG};z-index:9999;display:flex;flex-direction:column;justify-content:center;align-items:center;cursor:pointer;">
    <div style="color:{COLOR_CYAN};font-family:'Space Mono';font-size:1.6rem;">[ AUDIO INACTIVE ]</div>
    <div style="background:{COLOR_CYAN};color:black;padding:20px 60px;margin-top:20px;font-size:2.2rem;font-weight:900;border:3px solid {COLOR_ACCENT};">INITIATE SONIC FEED</div>
</div>
<script>
    function startAudio() {{
        if (Tone) {{
            Tone.start();
            Tone.Transport.bpm.value = 110;
            const kick = new Tone.MembraneSynth().toDestination();
            const bass = new Tone.Synth({{oscillator:{{type:"sine"}}}}).toDestination();
            new Tone.Loop(t => kick.triggerAttackRelease("C1","8n",t),"4n").start(0);
            new Tone.Sequence((t,n) => n && bass.triggerAttackRelease(n,"4n",t), ["C2",null,"C2","G1"]).start(0);
            Tone.Transport.start();
            document.getElementById('audio-overlay').remove();
        }}
    }}
</script>
""", unsafe_allow_html=True)

# -----------------------------
# 5. NAVIGATION
# -----------------------------
menu_styles = {
    "container": {"padding": "0!important", "background-color": "rgba(8,8,8,0.95)"},
    "nav-link": {"font-size": "16px", "text-align": "center", "padding": "14px", "color": "#fff", "font-family": "Inter", "text-transform": "uppercase", "font-weight": "700"},
    "nav-link-selected": {"background-color": "rgba(255,255,255,0.1)", "color": COLOR_CYAN, "border-bottom": f"4px solid {COLOR_CYAN}"}
}

selected = option_menu(
    menu_title=None,
    options=["HOME", "MUSIC", "EVENTS", "STORE", "ABOUT"],
    icons=["house-fill", "disc-fill", "calendar-event-fill", "bag-fill", "info-circle-fill"],
    default_index=st.session_state.current_page_index,
    orientation="horizontal",
    styles=menu_styles
)
st.session_state.current_page_index = ["HOME", "MUSIC", "EVENTS", "STORE", "ABOUT"].index(selected)

# -----------------------------
# 6. HOME PAGE
# -----------------------------
if selected == "HOME":
    st.markdown(f'<div class="video-bg"><iframe src="https://www.youtube.com/embed/qC0vDKVPCrw?controls=0&autoplay=1&loop=1&mute=1&playlist=qC0vDKVPCrw" frameborder="0" allow="autoplay"></iframe></div><div class="overlay"></div>', unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("# TUESDAYNIGHTFREAK")
        st.markdown("#### ARCHITECTS OF THE ANALOGUE SIGNAL")
        st.markdown("Hardware techno. Melbourne → Berlin. No laptops on stage.")
        b1, b2 = st.columns(2)
        with b1: 
            if st.button("LATEST RELEASE"): st.session_state.current_page_index = 1; st.rerun()
        with b2: 
            if st.button("TOUR DATES"): st.session_state.current_page_index = 2; st.rerun()
    with c2:
        st.markdown("#### SYSTEM STATUS")
        st.markdown(f"<div style='background:#0f0f0f;padding:15px;border-top:4px solid {COLOR_ACCENT};font-family:Space Mono;'>VOLTAGE CONTROL EP – OUT NOW</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:#0f0f0f;padding:15px;border-top:4px solid {COLOR_CYAN};font-family:Space Mono;'>WINTER 2025 EU TOUR</div>", unsafe_allow_html=True)

# -----------------------------
# 7. MUSIC PAGE — SOUNDCLOUD PLAYER
# -----------------------------
elif selected == "MUSIC":
    st.markdown("## DISCOGRAPHY")
    st.markdown("""
    <iframe width="100%" height="400" scrolling="no" frameborder="no" allow="autoplay"
    src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/playlists/1792034045&color=%23ff0033&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true">
    </iframe>
    <div style="font-size:0.8rem;color:#666;">Latest TNF Mix — Live at Tresor, Berlin</div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    for t in [
        {"title": "System Failure (Original Mix)", "label": "House Keeping Rec", "cat": "HKR004"},
        {"title": "Voltage Control", "label": "Ostgut Ton", "cat": "OSTGUT-55"},
    ]:
        st.markdown(f"**{t['title']}** — {t['label']} // {t['cat']}")
        st.button("STREAM", key=t['title'])

# -----------------------------
# 8. STORE — PAYPAL + STRIPE + DIGITAL DOWNLOADS
# -----------------------------
elif selected == "STORE":
    st.markdown("## STORE")

    # Cart
    if st.session_state.cart:
        total = sum(item["price"] for item in st.session_state.cart)
        st.markdown(f"### Cart <span class='cart-badge'>{len(st.session_state.cart)} items</span> → **€{total:.2f}**", unsafe_allow_html=True)
        payment_method = st.radio("Pay with", ["Stripe (Card)", "PayPal"], horizontal=True)

        if st.button("CHECKOUT NOW", type="primary"):
            # === SEND EMAIL NOTIFICATION FUNCTION ===
            def send_receipt_email():
                items_list = "<br>".join([f"• {i['name']} — €{i['price']:.2f}" for i in st.session_state.cart])
                html = f"""
                <h2>New Order — Tuesdaynightfreak</h2>
                <p><strong>Total:</strong> €{total:.2f}</p>
                <p><strong>Items:</strong></p>
                {items_list}
                <hr>
                <p>Thank you for supporting underground techno.</p>
                """
                requests.post(
                    "https://api.resend.com/emails",
                    headers={"Authorization": f"Bearer {RESEND_API_KEY}"},
                    json={
                        "from": "TNF Store <store@tuesdaynightfreak.com>",
                        "to": [ADMIN_EMAIL],
                        "subject": f"New Order — €{total:.2f}",
                        "html": html
                    }
                )

            if payment_method == "Stripe (Card)":
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        "price_data": {
                            "currency": "eur",
                            "product_data": {"name": i["name"]},
                            "unit_amount": int(i["price"] * 100),
                        },
                        "quantity": 1,
                    } for i in st.session_state.cart],
                    mode='payment',
                    success_url=f"{SITE_URL}/?paid=1",
                    cancel_url=f"{SITE_URL}/?cancel=1",
                )
                send_receipt_email()
                st.markdown(f"""
                <script src="https://js.stripe.com/v3/"></script>
                <script>
                    const stripe = Stripe('{STRIPE_PK}');
                    stripe.redirectToCheckout({{sessionId: '{session.id}'}});
                </script>
                """, unsafe_allow_html=True)

            else:  # PayPal
                send_receipt_email()
                st.markdown(f"""
                <div id="paypal-button-container"></div>
                <script src="https://www.paypal.com/sdk/js?client-id={PAYPAL_CLIENT_ID}&currency=EUR"></script>
                <script>
                    paypal.Buttons({{
                        createOrder: (data, actions) => actions.order.create({{
                            purchase_units: [{{amount: {{value: '{total:.2f}'}}}}]
                        }}),
                        onApprove: () => window.location.href = "{SITE_URL}/?paid=1"
                    }}).render('#paypal-button-container');
                </script>
                """, unsafe_allow_html=True)
        st.markdown("---")

    # Products
    products = [
        {"name": "TNF CORE TEE [BLACK]", "price": 35.00, "type": "merch"},
        {"name": "HKR HOODIE", "price": 65.00, "type": "merch"},
        {"name": "SLIPMATS (PAIR)", "price": 20.00, "type": "merch"},
        {"name": "VOLTAGE CONTROL EP (WAV)", "price": 8.00, "type": "digital", "url": "https://yourdomain.com/dl/voltage_control.zip"},
        {"name": "SYSTEM FAILURE (Single WAV)", "price": 2.50, "type": "digital", "url": "https://yourdomain.com/dl/system_failure.wav"},
    ]

    cols = st.columns(3)
    for i, p in enumerate(products):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="product-card">
                <div style="height:180px;background:#000;display:flex;align-items:center;justify-content:center;font-size:3rem;color:{COLOR_CYAN if p['type']=='digital' else COLOR_ACCENT};">
                    {'WAV' if p['type']=='digital' else 'TNF'}
                </div>
                <h3>{p['name']}</h3>
                <p><strong>€{p['price']:.2f}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("ADD TO CART", key=p["name"]):
                item = {"name": p["name"], "price": p["price"]}
                if "url" in p:
                    item["download_url"] = p["url"]
                st.session_state.cart.append(item)
                st.rerun()

# -----------------------------
# 9. PAYMENT SUCCESS + DOWNLOADS + EMAIL
# -----------------------------
if st.query_params.get("paid") == "1":
    st.success("Payment Successful! Thank you for your order.")
    st.balloons()

    digital_items = [i for i in st.session_state.cart if "download_url" in i]
    if digital_items:
        st.markdown("### Your Downloads")
        for item in digital_items:
            st.markdown(f"**{item['name']}** → [DOWNLOAD NOW]({item['download_url']})", unsafe_allow_html=True)

    st.session_state.cart = []
    st.query_params.clear()

# -----------------------------
# 10. OTHER PAGES
# -----------------------------
elif selected == "EVENTS":
    st.markdown("## UPCOMING SHOWS")
    for show in ["NOV 04 – AMSTERDAM – SHELTER", "NOV 11 – LONDON – FOLD", "DEC 02 – PARIS – REX CLUB"]:
        st.markdown(f"<div style='background:#0f0f0f;padding:20px;border-left:5px solid {COLOR_CYAN};margin:15px 0;font-family:Space Mono;'>{show}</div>", unsafe_allow_html=True)

elif selected == "ABOUT":
    st.markdown("## ABOUT")
    st.write("Hardware-only techno project. Founded in Melbourne. Based in Berlin. No laptops. No mercy.")
    st.markdown("**mgmt@tuesdaynightfreak.com**")
