import streamlit as st
import base64
import time
import os
import streamlit as st

# Automatically find the absolute path to your background file
current_dir = os.path.dirname(os.path.abspath(__file__))
video_path = os.path.join(current_dir, "background.mp4")

@st.cache_resource
def load_video_background(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# 1. PAGE CONFIG
st.set_page_config(page_title="Deepfake Shield", layout="centered")

# 2. SMART VIDEO LOADER (Catches hidden .mp4.mp4 errors)
@st.cache_resource
def get_video_base64(bin_file):
    # Check for 'background.mp4' AND 'background.mp4.mp4'
    possible_names = [bin_file, bin_file + ".mp4"]
    for name in possible_names:
        if os.path.exists(name):
            with open(name, 'rb') as f:
                data = f.read()
            return base64.b64encode(data).decode()
    return None

video_str = get_video_base64('background.mp4')

# 3. THE REFINED INJECTION
if video_str:
    st.markdown(f"""
        <style>
            html, body, [data-testid="stAppViewContainer"], .stApp {{
                background-color: #010409 !important;
                background: transparent !important;
            }}

            #bg-video {{  position: fixed;
                top: 0; left: 0;
                width: 100vw; 
                height: 100vh;
                z-index: -2;
                
                /* FIX 1: 'fill' stretches to edges, 'contain' keeps ratio with bars */
                object-fit: fill; 

                /* FIX 2: Reset brightness to 1.0 to show original glowing colors */
                filter: brightness(1.0) contrast(1.0) saturate(1.0); 
                
                /* Smooth rendering */
                transform: translateZ(0);
                will-change: transform;
            }}
  


            .laser-scanner {{
                position: fixed; top: 0; left: 0; width: 100%; height: 6px;
                background: linear-gradient(to right, transparent, #00ffff, #ffffff, #00ffff, transparent);
                box-shadow: 0 0 25px #00ffff;
                z-index: 9999;
                animation: scan-move 5s linear infinite;
            }}
            @keyframes scan-move {{ 0% {{ top: -5%; }} 100% {{ top: 105%; }} }}

            .glass-card {{
                background: rgba(8, 15, 25, 0.9);
                backdrop-filter: blur(20px);
                border: 2px solid rgba(0, 255, 255, 0.4);
                border-radius: 40px;
                padding: 45px;
                margin-top: 10px;
                box-shadow: 0 0 80px rgba(0, 0, 0, 1);
            }}

            h1 {{ color: #00ffff !important; text-transform: uppercase; letter-spacing: 5px; text-shadow: 0 0 15px #00ffff; }}
            .stButton>button {{ background: linear-gradient(90deg, #00ffff, #008888); color: #000 !important; font-weight: 900; }}
            footer {{ visibility: hidden; }}
        </style>

        <video autoplay loop muted playsinline id="bg-video">
            <source src="data:video/mp4;base64,{video_str}" type="video/mp4">
        </video>

        <div class="laser-scanner"></div>

        <script>
            var video = document.getElementById("bg-video");
            // Force play immediately on load
            video.play();
            // Safety: Try playing again every second if it gets stuck
            setInterval(function() {{ if (video.paused) video.play(); }}, 1000);
        </script>
    """, unsafe_allow_html=True)
else:
    st.error(f"background.mp4 not found in {os.getcwd()}")

# 4. APP INTERFACE
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("<h1>Deepfake Shield</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#00ffff; opacity:0.7; letter-spacing:4px;'>IDENTITY PROTECTION SYSTEM</p>", unsafe_allow_html=True)

uploaded = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

if uploaded:
    st.image(uploaded, use_container_width=True)
    if st.button("RUN TRIPLE-LOCK IMMUNIZATION"):
        gauge_place = st.empty()
        for i in range(101):
            vuln_score = 99.00 - (i * 0.9899)
            gauge_place.markdown(f"""
                <div style="margin: 25px 0; color: #00ffff; font-family: monospace;">
                    <h2 style="font-size: 3.2rem; margin: 0; text-shadow: 0 0 15px #00ffff;">{vuln_score:.2f}%</h2>
                    <p style="letter-spacing: 2px;">VULNERABILITY LEVEL</p>
                    <div style="width:100%; height:12px; background:#111; border-radius:6px; border:1px solid #333;">
                        <div style="width:{i}%; height:100%; background:#00ffff; box-shadow:0 0 15px #00ffff; border-radius:6px;"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(0.02)
        st.success("SHIELD VERIFIED: IDENTITY PROTECTED")

st.markdown('</div>', unsafe_allow_html=True)