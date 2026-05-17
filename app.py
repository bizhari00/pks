import streamlit as st

# ==============================================================================
# 1. KONFIGURASI HALAMAN UTAMA (Wajib Paling Atas)
# ==============================================================================
st.set_page_config(
    page_title="Pabrik PKS",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Pembersihan CSS: Struktur grid murni tanpa overflow:hidden kustom agar tidak memotong kontainer luar
st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        zoom: 1.0;
        overflow-y: auto !important;
    }
    
    .block-container {
        padding-top: 1.5rem !important; 
        padding-bottom: 1rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

import plotly.express as px
from PIL import Image
import time

# ==============================================================================
# 2. NAVIGASI & JUDUL SEBARIS (Struktur Grid Murni Streamlit & HTML Inline)
# ==============================================================================
# Membagi halaman menjadi 2 kolom: Kolom kiri untuk tombol, Kolom kanan untuk judul
col_btn, col_title = st.columns([3, 7])

with col_btn:
    st.link_button("🏠 Kembali ke Menu Utama", "https://forio.com/app/bustamiizhari/inl", use_container_width=True)

with col_title:
    # Menggunakan tag paragraf dengan padding atas agar sejajar horizontal dengan tombol di sampingnya
    st.markdown(
        "<p style='margin: 0px; padding-top: 8px; font-size: 1.35rem; font-weight: bold; font-family: sans-serif; color: #31333F;'>Pabrik PKS (Simulasi Aliran)</p>", 
        unsafe_allow_html=True
    )

st.divider()

# ==============================================================================
# 3. MEMUAT BACKGROUND IMAGE PKS
# ==============================================================================
try:
    img = Image.open("pks.png")
    img_width, img_height = img.size
except FileNotFoundError:
    st.error("File 'pks.png' tidak ditemukan. Pastikan file gambar ada di root repository GitHub Anda.")
    st.stop()

# ==============================================================================
# 4. KOORDINAT DIAGRAM ALIR PABRIK PKS (Skala Rasio Gambar)
# ==============================================================================
flow_path = [
    # --- JALUR A: KEBUN SENDIRI ---
    {
        'step_id': 'tbs_sendiri',
        'x': int(img_width * 0.25), 'y': int(img_height * 0.41),
        'label': 'Laju Penerimaan TBS',
        'tank_area': [int(img_width * 0.22), int(img_height * 0.38), int(img_width * 0.29), int(img_height * 0.44)]
    },
    {
        'step_id': 'stock_pks_sendiri',
        'x': int(img_width * 0.35), 'y': int(img_height * 0.41),
        'label': 'Stock PKS Kebun Sendiri',
        'tank_area': [int(img_width * 0.31), int(img_height * 0.38), int(img_width * 0.39), int(img_height * 0.44)]
    },
    {
        'step_id': 'cpo_sendiri',
        'x': int(img_width * 0.54), 'y': int(img_height * 0.31),
        'label': 'Stock CPO Kebun Sendiri',
        'tank_area': [int(img_width * 0.50), int(img_height * 0.28), int(img_width * 0.58), int(img_height * 0.34)]
    },
    {
        'step_id': 'kernel_sendiri',
        'x': int(img_width * 0.54), 'y': int(img_height * 0.41),
        'label': 'Stock Palm Kernel Kebun Sendiri',
        'tank_area': [int(img_width * 0.50), int(img_height * 0.38), int(img_width * 0.58), int(img_height * 0.44)]
    },
     
    # --- JALUR B: KEBUN MITRA ---
    {
        'step_id': 'tbs_mitra',
        'x': int(img_width * 0.29), 'y': int(img_height * 0.81),
        'label': 'Laju Penerimaan TBS Mitra',
        'tank_area': [int(img_width * 0.25), int(img_height * 0.78), int(img_width * 0.32), int(img_height * 0.84)]
    },
    {
        'step_id': 'stock_pks_mitra',
        'x': int(img_width * 0.35), 'y': int(img_height * 0.81),
        'label': 'Stock PKS Mitra',
        'tank_area': [int(img_width * 0.31), int(img_height * 0.78), int(img_width * 0.39), int(img_height * 0.84)]
    },
    {
        'step_id': 'cpo_mitra',
        'x': int(img_width * 0.54), 'y': int(img_height * 0.71),
        'label': 'Stock CPO Mitra',
        'tank_area': [int(img_width * 0.50), int(img_height * 0.68), int(img_width * 0.58), int(img_height * 0.74)]
    },
    {
        'step_id': 'kernel_mitra',
        'x': int(img_width * 0.54), 'y': int(img_height * 0.81),
        'label': 'Stock Palm Kernel Mitra',
        'tank_area': [int(img_width * 0.50), int(img_height * 0.78), int(img_width * 0.58), int(img_height * 0.84)]
    },

    # --- JALUR OUTPUT TOTAL TRANSMISI ---
    {
        'step_id': 'total_cpo',
        'x': int(img_width * 0.81), 'y': int(img_height * 0.45),
        'label': 'Total CPO Yang Dihasilkan',
        'tank_area': [int(img_width * 0.76), int(img_height * 0.38), int(img_width * 0.86), int(img_height * 0.52)]
    },
    {
        'step_id': 'total_kernel',
        'x': int(img_width * 0.81), 'y': int(img_height * 0.76),
        'label': 'Total Palm Kernel Yang Dihasilkan',
        'tank_area': [int(img_width * 0.76), int(img_height * 0.69), int(img_width * 0.86), int(img_height * 0.83)]
    }
]

# ==============================================================================
# 5. LOOPING SIMULASI (PENGUNCIAN SKALA TINGGI DIAGRAM)
# ==============================================================================
placeholder = st.empty()
render_count = 0

while True:
    for step in range(len(flow_path)):
        current = flow_path[step]
        fig = px.imshow(img)
        
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        
        # 1. Kotak Hijau Transparan di Atas Komponen Diagram
        area = current['tank_area']
        fig.add_shape(
            type="rect", 
            x0=area[0], y0=area[1], x1=area[2], y1=area[3],
            fillcolor="rgba(0, 255, 0, 0.4)",
            line=dict(color="LimeGreen", width=3),
        )
        
        # 2. Segitiga Gerak Kuning & Label Teks
        fig.add_scatter(
            x=[current['x']], y=[current['y']], mode="markers+text",
            marker=dict(size=24, color="yellow", symbol="triangle-right", line=dict(width=2, color="orange")),
            text=[current['label']], textposition="bottom center",
            textfont=dict(size=12, color="darkred", family="Arial Black")
        )
        
        # Tinggi dikunci ke 500px agar proporsional dan muat satu monitor utuh
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=500,
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
