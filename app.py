import streamlit as st
from streamlit_option_menu import option_menu
import requests
import stripe

# Session state
for k in ["page_index", "expanded_gallery"]:
    if k not in st.session_state: st.session_state[k] = 0 if k == "page_index" else None

# Config + SEO
st.set_page_config(page_title="Tuesday Night Freak | Hardware Techno", page_icon="⚫", layout="wide")

st.markdown("""
<meta name="description" content="Melbourne hardware techno. Analog error. No laptops. Bookings, merch, releases on Bandcamp, SoundCloud, Spotify.">
<meta property="og:title" content="TNF | Underground Analog Techno">
<meta property="og:description" content="Raw machine rhythms from Melbourne. Join the freakout.">
<meta property="og:image" content="https://images.unsplash.com/photo-1571266028243-371695063ad6?w=1200">
<meta property="og:url" content="https://tuesdaynightfreak.streamlit.app">
""", unsafe_allow_html=True)

# CSS: Black nav fix + small logo + glitch BG + Spotify class
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Space+Mono&display=swap');
.stApp { background: #080808; color: #f0f0f0; font-family: 'Inter', sans-serif; }
.block-container { padding: 1rem !important; max-width: 100% !important; }
@media (min-width: 768px) { .block-container { padding: 2rem !important; } }
h1,h2,h3 { font-weight: 900; text-transform: uppercase; letter-spacing: -1px; color: #00f7ff; }
.stButton>button { background: #00f7ff; color: #000; border-radius: 0; font-weight: 900; width: 100%; margin: 0.5rem 0; }
.stButton>button:hover { background: #ff0033; color: white; }
/* BLACK NAV OVERRIDE */
div[data-testid="stHorizontalBlock"] { background: #000 !important; }
div[data-testid="stHorizontalBlock"] button { background: #000 !important; color: #fff !important; border: none !important; font-weight: bold; text-transform: uppercase; }
div[data-testid="stHorizontalBlock"] button:hover { background: #000 !important; color: #00f7ff !important; border-bottom: 2px solid #00f7ff !important; }
/* SMALL LOGO */
.logo { width: 220px; height: 70px; margin: 0 auto; display: block; }
/* GLITCH BG */
@keyframes glitch { 0%,100%{transform:translate(0);}20%{transform:translate(-2px,2px);}40%{transform:translate(-2px,-2px);}60%{transform:translate(2px,2px);}80%{transform:translate(2px,-2px);} }
body::before { content:''; position:fixed; top:0; left:0; width:100vw; height:100vh; background:linear-gradient(45deg,#00f7ff,#ff0033,#080808); opacity:0.1; z-index:-1; animation:glitch 2s infinite; }
.overlay { position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(8,8,8,0.92); z-index:-1; }
iframe,audio { width:100% !important; border:none; border-radius:0; }
.soundcloud { height:465px; }
.spotify { height:380px; }
</style>
<div class="overlay"></div>
""", unsafe_allow_html=True)

# Smaller Logo
st.markdown("""
<div class="logo">
<svg viewBox="0 0 300 90" xmlns="http://www.w3.org/2000/svg">
<text x="4" y="65" font-family="Arial Black" font-size="68" fill="#00f7ff" opacity="0.6" letter-spacing="-4">TNF</text>
<text x="-2" y="65" font-family="Arial Black" font-size="68" fill="#ff0033" opacity="0.8" letter-spacing="-4">TNF</text>
<text x="0" y="65" font-family="Arial Black" font-size="68" fill="#f0f0f0" letter-spacing="-4">TNF</text>
</svg>
</div>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center; margin-top:-10px'>TUESDAY NIGHT FREAK</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:#00f7ff'>HARDWARE ONLY • ANALOG ERROR</h4>", unsafe_allow_html=True)

# Spotify Embed (Home page)
st.markdown("### STREAM ON SPOTIFY")
st.markdown("""
<iframe class="spotify" src="https://open.spotify.com/embed/artist/5F8sL2i5QeP5i5QeP5i5Qe?utm_source=generator" width="100%" height="380" frameborder="0" allowfullscreen allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
""", unsafe_allow_html=True)  # Replace artist ID

# Navigation (Black, Fixed)
options = ["HOME", "MUSIC", "EVENTS", "BOOKING", "STORE", "GALLERY", "ABOUT"]
icons = ["house","disc","calendar3","envelope","bag","images","info-circle"]
selected = option_menu(None, options, icons=icons, default_index=st.session_state.page_index, orientation="horizontal",
                       styles={"container": {"background-color": "#000 !important", "padding": "0.5rem !important"}, 
                               "nav-link": {"font-weight": "bold", "text-transform": "uppercase", "color": "#fff !important"},
                               "nav-link-selected": {"color": "#00f7ff !important", "border-bottom": "3px solid #00f7ff !important"}})

if options.index(selected) != st.session_state.page_index:
    st.session_state.page_index = options.index(selected)
    st.session_state.expanded_gallery = None

# Pages
if selected == "HOME":
    # Bandcamp
    st.markdown("### LATEST: VOLTAGE CONTROL EP")
    st.markdown('<iframe style="border:0;width:100%;height:472px;" src="https://bandcamp.com/EmbeddedPlayer/album=4240000000/size=large/bgcol=080808/linkcol=00f7ff/transparent=true/" seamless></iframe>', unsafe_allow_html=True)
    # SoundCloud
    st.markdown("### LATEST MIX")
    st.markdown('<iframe class="soundcloud" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/1798583209&color=%23ff0033&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>', unsafe_allow_html=True)
    # TikTok Grid
    st.markdown("### @tuesdaynightfreak")
    cols = st.columns(3)
    imgs = ["https://images.unsplash.com/photo-1571266028243-371695063ad6?w=300&h=400&fit=crop", "https://images.unsplash.com/photo-1619967657960-983b6329c370?w=300&h=400&fit=crop", "https://images.unsplash.com/photo-1550291652-6ea9114a47b1?w=300&h=400&fit=crop"]
    for col, img in zip(cols, imgs):
        with col: st.image(img, use_column_width=True); st.caption("Synth live • Gear closeup • Analog chaos")
    # Mailchimp
    st.markdown("#### JOIN THE FAMILY")
    with st.form("nl"):
        email = st.text_input("Email")
        consent = st.checkbox("GDPR: I agree to updates")
        if st.form_submit_button("SIGN UP") and email and consent:
            try:
                mc = st.secrets["mailchimp"]
                url = f"https://{mc['api_key'].split('-')[1]}.api.mailchimp.com/3.0/lists/{mc['audience_id']}/members/"
                data = {"email_address": email, "status_if_new": "pending"}
                auth = ("user", mc['api_key'].split('-')[0])
                r = requests.post(url, auth=auth, json=data)
                st.success("Signed up! Confirm in inbox.") if r.status_code == 200 else st.error("Try again.")
            except: st.error("Add Mailchimp secrets.")

elif selected == "MUSIC":
    st.title("DISCOGRAPHY")
    st.markdown("### VOLTAGE CONTROL EP")
    st.markdown('<iframe style="border:0;width:100%;height:472px;" src="https://bandcamp.com/EmbeddedPlayer/album=4240000000/size=large/bgcol=080808/linkcol=00f7ff/transparent=true/" seamless></iframe>', unsafe_allow_html=True)
    st.markdown("### ON SPOTIFY")
    st.markdown("""
<iframe class="spotify" src="https://open.spotify.com/embed/artist/5F8sL2i5QeP5i5QeP5i5Qe?utm_source=generator" width="100%" height="380" frameborder="0" allowfullscreen allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
    """, unsafe_allow_html=True)

elif selected == "EVENTS":
    st.title("UPCOMING SHOWS")
    try:
        ra_id = st.secrets["ra"]["artist_id"]
        r = requests.get(f"https://ra.co/api/events?artist={ra_id}&per_page=5")
        events = r.json().get("events", [])
        for e in events[:3]:
            st.markdown(f"**{e['datetime'][:10]}** — {e['venue']['city']} — {e['venue']['name']}")
            st.divider()
    except: st.info("No events yet. Powered by RA API.")

elif selected == "BOOKING":
    st.title("BOOKING")
    with st.form("book"):
        st.text_input("Name/Promoter")
        email = st.text_input("Email *")
        st.text_input("Venue")
        st.text_input("City")
        st.date_input("Date", min_value=st.date.today())
        st.selectbox("Capacity", ["<500", "500-1000", "1000-3000", ">3000"])
        st.text_area("Rider/Message")
        if st.form_submit_button("SEND") and email: st.success("Sent! Reply in 48h."); st.balloons()
        else: st.warning("Email required.")

elif selected == "STORE":
    st.title("MERCH")
    try: stripe.api_key = st.secrets["stripe"]["secret_key"]
    except: pass
    items = [("TNF Tee", 35, "https://images.unsplash.com/photo-1612872087729-bb3898a6e1e7?q=80"), ("HKR Hoodie", 65, "https://images.unsplash.com/photo-1556821840-3a63f95609a7?q=80"), ("Slipmats", 20, "https://images.unsplash.com/photo-1603048588665-791ca8aea617?q=80")]
    cols = st.columns(3)
    for col, (name, price, img) in zip(cols, items):
        with col:
            st.image(img + "&w=600", use_column_width=True)
            st.markdown(f"**{name}** €{price}")
            if st.button("BUY NOW", key=name):
                if 'stripe' in globals() and stripe.api_key:
                    session = stripe.checkout.Session.create(payment_method_types=['card'], line_items=[{'price_data': {'currency': 'eur', 'product_data': {'name': name}, 'unit_amount': price*100}, 'quantity': 1}], mode='payment', success_url=st.secrets.get("site_url", "https://tuesdaynightfreak.streamlit.app") + "?success=1", cancel_url=st.secrets.get("site_url", "https://tuesdaynightfreak.streamlit.app") + "?cancel=1")
                    st.markdown(f'<meta http-equiv="refresh" content="0;url={session.url}">', unsafe_allow_html=True)
                else: st.info("Add Stripe secrets for checkout.")

elif selected == "GALLERY":
    st.title("VISUAL ARCHIVE")
    images = ["https://images.unsplash.com/photo-1571266028243-371695063ad6", "https://images.unsplash.com/photo-1619967657960-983b6329c370", "https://images.unsplash.com/photo-1550291652-6ea9114a47b1", "https://images.unsplash.com/photo-1599841180182-5f3a4e2d9b7a"]
    caps = ["EURORACK", "LIVE RIG", "303 ACID", "MODULAR"]
    if st.session_state.expanded_gallery is not None:
        i = st.session_state.expanded_gallery
        st.image(images[i] + "?w=1600", caption=caps[i], use_column_width=True)
        if st.button("← BACK"): st.session_state.expanded_gallery = None
    else:
        cols = st.columns(2)
        for i, (img, cap) in enumerate(zip(images, caps)):
            with cols[i%2]:
                st.image(img + "?w=800", caption=cap, use_column_width=True)
                if st.button("EXPAND", key=f"exp{i}"): st.session_state.expanded_gallery = i

elif selected == "ABOUT":
    st.title("ABOUT")
    st.markdown("""
    **Tuesday Night Freak**: Melbourne hardware techno.  
    No laptops. Pure analog glitch.  
    Berlin warehouses • Detroit soul • Eurorack chaos.  
    From basements to Berghain — the machine lives.  
    """)
    st.code("tuesdaynightfreak@gmail.com")
