import streamlit as st

# ==============================================================================
# 1. ANTARMUKA INSTAN & GLOBAL ZOOM 80% (Paling Atas)
# ==============================================================================
st.set_page_config(
    page_title="Pabrik PKS",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
    /* Mengunci zoom seluruh aplikasi Streamlit di skala 80% secara instan */
    html, body, [data-testid="stAppViewContainer"] {
        zoom: 0.9;
        -moz-transform: scale(0.9); /* Dukungan untuk Firefox */
        -moz-transform-origin: top center;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    h1 {
        text-align: center;
        font-family: 'Arial', sans-serif;
        margin-bottom: 15px;
    }
    .custom-tab-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background-color: #ffffff;
        color: #31333F;
        border: 1px solid rgba(49, 51, 63, 0.2);
        padding: 0.4rem 1rem;
        border-radius: 0.5rem;
        font-weight: 500;
        font-size: 1.5rem;
        text-decoration: none;
        cursor: pointer;
        transition: background-color 0.16s ease-in-out;
        width: 100%;
        height: 42px;
    }
    .custom-tab-btn:hover {
        border-color: #ff4b4b;
        color: #ff4b4b;
        background-color: rgba(255, 75, 75, 0.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

import plotly.express as px
from PIL import Image
import time

# Navigation Bar
URL_PORTAL_FORIO = "https://forio.com/app/bustamiizhari/inl"
col_nav, _ = st.columns([2, 5])
with col_nav:
    st.markdown(
        f'<a href="{URL_PORTAL_FORIO}" target="_blank" class="custom-tab-btn">🏠 Kembali ke Menu Utama</a>', 
        unsafe_allow_html=True
    )

st.markdown("<h1>Pabrik PKS</h1>", unsafe_allow_html=True)

# ==============================================================================
# 2. MEMUAT BACKGROUND IMAGE PKS
# ==============================================================================
try:
    img = Image.open("pks.png")
    img_width, img_height = img.size
except FileNotFoundError:
    st.error("File 'pks.png' tidak ditemukan. Pastikan file gambar ada di root repository GitHub Anda.")
    st.stop()

# ==============================================================================
# 3. KOORDINAT BARU BERDASARKAN DIAGRAM ALIR PABRIK PKS (Skala Estimasi Gambar)
# ==============================================================================
# Format koordinat Plotly imshow: [x0, y0, x1, y1] dari pojok kiri atas
flow_path = [
    # --- JALUR A: KEBUN SENDIRI ---
    {
        'step_id': 'tbs_sendiri',
        'x': int(img_width * 0.18), 'y': int(img_height * 0.22),
        'label': 'Laju Penerimaan TBS (Kebun Sendiri)',
        'tank_area': [int(img_width * 0.15), int(img_height * 0.20), int(img_width * 0.22), int(img_height * 0.24)]
    },
    {
        'step_id': 'stock_pks_sendiri',
        'x': int(img_width * 0.35), 'y': int(img_height * 0.24),
        'label': 'Stock PKS Kebun Sendiri',
        'tank_area': [int(img_width * 0.32), int(img_height * 0.16), int(img_width * 0.39), int(img_height * 0.24)]
    },
    {
        'step_id': 'cpo_sendiri',
        'x': int(img_width * 0.44), 'y': int(img_height * 0.11),
        'label': 'Proses Olah & Stock CPO Sendiri',
        'tank_area': [int(img_width * 0.49), int(img_height * 0.08), int(img_width * 0.56), int(img_height * 0.13)]
    },
    {
        'step_id': 'kernel_sendiri',
        'x': int(img_width * 0.44), 'y': int(img_height * 0.22),
        'label': 'Proses Olah & Stock Palm Kernel Sendiri',
        'tank_area': [int(img_width * 0.49), int(img_height * 0.18), int(img_width * 0.58), int(img_height * 0.24)]
    },
    
    # --- JALUR B: KEBUN MITRA ---
    {
        'step_id': 'tbs_mitra',
        'x': int(img_width * 0.20), 'y': int(img_height * 0.77),
        'label': 'Laju Penerimaan TBS Mitra',
        'tank_area': [int(img_width * 0.17), int(img_height * 0.75), int(img_width * 0.24), int(img_height * 0.79)]
    },
    {
        'step_id': 'stock_pks_mitra',
        'x': int(img_width * 0.35), 'y': int(img_height * 0.77),
        'label': 'Stock PKS Mitra',
        'tank_area': [int(img_width * 0.32), int(img_height * 0.72), int(img_width * 0.38), int(img_height * 0.81)]
    },
    {
        'step_id': 'cpo_mitra',
        'x': int(img_width * 0.43), 'y': int(img_height * 0.69),
        'label': 'Laju Olah & Stock CPO Mitra',
        'tank_area': [int(img_width * 0.48), int(img_height * 0.68), int(img_width * 0.55), int(img_height * 0.73)]
    },
    {
        'step_id': 'kernel_mitra',
        'x': int(img_width * 0.43), 'y': int(img_height * 0.78),
        'label': 'Laju Olah & Stock Palm Kernel Mitra',
        'tank_area': [int(img_width * 0.48), int(img_height * 0.77), int(img_width * 0.56), int(img_height * 0.83)]
    },

    # --- JALUR OUTPUT TOTAL TRANSMISI ---
    {
        'step_id': 'total_cpo',
        'x': int(img_width * 0.75), 'y': int(img_height * 0.35),
        'label': 'Total CPO Yang Dihasilkan',
        'tank_area': [int(img_width * 0.77), int(img_height * 0.30), int(img_width * 0.85), int(img_height * 0.52)]
    },
    {
        'step_id': 'total_kernel',
        'x': int(img_width * 0.75), 'y': int(img_height * 0.70),
        'label': 'Total Palm Kernel Yang Dihasilkan',
        'tank_area': [int(img_width * 0.77), int(img_height * 0.65), int(img_width * 0.85), int(img_height * 0.85)]
    }
]

# ==============================================================================
# 4. LOOPING ANIMASI BERJALAN SECARA PARALEL/BERURUTAN
# ==============================================================================
placeholder = st.empty()
render_count = 0

while True:
    for step in range(len(flow_path)):
        current = flow_path[step]
        fig = px.imshow(img)
        
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        
        # 1. GAMBAR KOTAK HIJAU TRANSPARAN PADA PROSES YANG AKTIF
        area = current['tank_area']
        fig.add_shape(
            type="rect", 
            x0=area[0], y0=area[1], x1=area[2], y1=area[3],
            fillcolor="rgba(0, 255, 0, 0.35)",
            line=dict(color="LimeGreen", width=3),
        )
        
        # 2. SEGI TIGA PENANDA GERAKAN KUNING
        fig.add_scatter(
            x=[current['x']], y=[current['y']], mode="markers+text",
            marker=dict(size=30, color="yellow", symbol="triangle-right", line=dict(width=2, color="orange")),
            text=[current['label']], textposition="top center",
            textfont=dict(size=18, color="darkred", family="Arial Black")
        )
        
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=650)
        
        with placeholder.container():
            st.plotly_chart(
                fig, 
                use_container_width=True, 
                config={'displayModeBar': False}, 
                key=f"pks_render_{render_count}"
            )
        
        render_count += 1
        time.sleep(1.5)  # Kecepatan transisi alur per langkah
