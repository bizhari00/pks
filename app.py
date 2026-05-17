import streamlit as st

# ==============================================================================
# 1. ANTARMUKA RESPONSIF & DOCKING TOMBOL NAVIGASI (Wajib Paling Atas)
# ==============================================================================
st.set_page_config(
    page_title="Pabrik PKS",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
    /* Mengunci halaman agar tidak memiliki scrollbar vertikal ganda */
    html, body, [data-testid="stAppViewContainer"] {
        zoom: 1.0;
        overflow: hidden;
    }
    
    /* Memaksimalkan container tanpa margin kosong di sisi kanan-kiri */
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0rem;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
    
    h1 {
        text-align: center;
        font-family: 'Arial', sans-serif;
        margin-top: 5px;
        margin-bottom: 5px;
        font-size: 1.8rem;
        color: #31333F;
    }
    
    /* Desain tombol kustom agar kokoh dan tidak tergeser */
    .custom-tab-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background-color: #ffffff;
        color: #31333F;
        border: 1px solid rgba(49, 51, 63, 0.2);
        padding: 0.3rem 1rem;
        border-radius: 0.5rem;
        font-weight: 500;
        font-size: 1.1rem;
        text-decoration: none;
        cursor: pointer;
        transition: all 0.16s ease-in-out;
        width: 100%;
        height: 38px;
        box-shadow: 0px 1px 3px rgba(0,0,0,0.05);
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

# Navigation Bar - Menggunakan kolom proporsional agar hemat ruang
col_nav, _ = st.columns([2.5, 7.5])
with col_nav:
    st.markdown(
        f'<a href="https://forio.com/app/bustamiizhari/inl" target="_blank" class="custom-tab-btn">🏠 Kembali ke Menu Utama</a>', 
        unsafe_allow_html=True
    )

st.markdown("<h1>Pabrik PKS (Simulasi Aliran)</h1>", unsafe_allow_html=True)

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
# 3. KOORDINAT BERDASARKAN DIAGRAM ALIR PABRIK PKS (Skala Rasio Gambar)
# ==============================================================================
flow_path = [
    # --- JALUR A: KEBUN SENDIRI ---
    {
        'step_id': 'tbs_sendiri',
        'x': int(img_width * 0.17), 'y': int(img_height * 0.42),
        'label': 'Laju Penerimaan TBS (Kebun Sendiri)',
        'tank_area': [int(img_width * 0.14), int(img_height * 0.38), int(img_width * 0.20), int(img_height * 0.45)]
    },
    {
        'step_id': 'stock_pks_sendiri',
        'x': int(img_width * 0.30), 'y': int(img_height * 0.41),
        'label': 'Stock PKS Kebun Sendiri',
        'tank_area': [int(img_width * 0.25), int(img_height * 0.37), int(img_width * 0.35), int(img_height * 0.45)]
    },
    {
        'step_id': 'cpo_sendiri',
        'x': int(img_width * 0.54), 'y': int(img_height * 0.33),
        'label': 'Stock CPO Kebun Sendiri',
        'tank_area': [int(img_width * 0.49), int(img_height * 0.29), int(img_width * 0.59), int(img_height * 0.36)]
    },
    {
        'step_id': 'kernel_sendiri',
        'x': int(img_width * 0.54), 'y': int(img_height * 0.41),
        'label': 'Stock Palm Kernel Kebun Sendiri',
        'tank_area': [int(img_width * 0.49), int(img_height * 0.38), int(img_width * 0.59), int(img_height * 0.45)]
    },
     
    # --- JALUR B: KEBUN MITRA ---
    {
        'step_id': 'tbs_mitra',
        'x': int(img_width * 0.26), 'y': int(img_height * 0.81),
        'label': 'Laju Penerimaan TBS Mitra',
        'tank_area': [int(img_width * 0.23), int(img_height * 0.77), int(img_width * 0.29), int(img_height * 0.84)]
    },
    {
        'step_id': 'stock_pks_mitra',
        'x': int(img_width * 0.37), 'y': int(img_height * 0.90),
        'label': 'Stock PKS Mitra',
        'tank_area': [int(img_width * 0.33), int(img_height * 0.86), int(img_width * 0.41), int(img_height * 0.93)]
    },
    {
        'step_id': 'cpo_mitra',
        'x': int(img_width * 0.54), 'y': int(img_height * 0.77),
        'label': 'Stock CPO Mitra',
        'tank_area': [int(img_width * 0.49), int(img_height * 0.73), int(img_width * 0.59), int(img_height * 0.80)]
    },
    {
        'step_id': 'kernel_mitra',
        'x': int(img_width * 0.54), 'y': int(img_height * 0.85),
        'label': 'Stock Palm Kernel Mitra',
        'tank_area': [int(img_width * 0.49), int(img_height * 0.82), int(img_width * 0.59), int(img_height * 0.89)]
    },

    # --- JALUR OUTPUT TOTAL TRANSMISI ---
    {
        'step_id': 'total_cpo',
        'x': int(img_width * 0.85), 'y': int(img_height * 0.45),
        'label': 'Total CPO Yang Dihasilkan',
        'tank_area': [int(img_width * 0.79), int(img_height * 0.36), int(img_width * 0.91), int(img_height * 0.55)]
    },
    {
        'step_id': 'total_kernel',
        'x': int(img_width * 0.85), 'y': int(img_height * 0.76),
        'label': 'Total Palm Kernel Yang Dihasilkan',
        'tank_area': [int(img_width * 0.79), int(img_height * 0.67), int(img_width * 0.91), int(img_height * 0.86)]
    }
]

# ==============================================================================
# 4. LOOPING ANIMASI DENGAN TINGGI TERKALIBRASI (ANTI-MELUBER)
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
            textfont=dict(size=16, color="darkred", family="Arial Black")
        )
        
        # DIKALIBRASI: Mengunci height di angka 540 agar pks.png muat sempurna di sisa vertical space monitor
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0), 
            height=540,
            autosize=True
        )
        
        with placeholder.container():
            st.plotly_chart(
                fig, 
                use_container_width=True, 
                config={
                    'displayModeBar': False,
                    'responsive': True
                }, 
                key=f"pks_render_{render_count}"
            )
        
        render_count += 1
        time.sleep(1.6)
