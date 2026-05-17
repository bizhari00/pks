import streamlit as st

# ==============================================================================
# 1. KONFIGURASI HALAMAN UTAMA (Wajib Paling Atas)
# ==============================================================================
st.set_page_config(
    page_title="Pabrik PKS - Grid Kelipatan 25",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Pengaturan padding halaman utama (Sudah Teruji Aman di Forio 80%)
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2.0rem !important; 
        padding-bottom: 1.5rem !important;
        padding-left: 2.0rem !important;
        padding-right: 2.0rem !important;
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
# 2. STRATEGI TURUNKAN LAYOUT 
# ==============================================================================
st.markdown("<br><br>", unsafe_allow_html=True)

# ==============================================================================
# 3. NAVIGASI & JUDUL SEBARIS
# ==============================================================================
col_btn, col_title = st.columns([1.2, 2.8])

with col_btn:
    st.link_button("🏠 Kembali ke Menu Utama", "https://forio.com/app/bustamiizhari/inl", use_container_width=True)

with col_title:
    st.subheader("Mode Kalibrasi Akurat (Grid Kerapatan 25 px)")

st.divider()

# ==============================================================================
# 4. MEMUAT BACKGROUND IMAGE PKS
# ==============================================================================
try:
    img = Image.open("pks.png")
    img_width, img_height = img.size
except FileNotFoundError:
    st.error("File 'pks.png' tidak ditemukan. Pastikan file gambar ada di root repository GitHub Anda.")
    st.stop()

# ==============================================================================
# 5. STRUKTUR FASE PROSES PARALEL
# ==============================================================================
process_phases = [
    # --- FASE 1: PENERIMAAN TBS BARENGAN ---
    [
        {
            'x': int(img_width * 0.25), 'y': int(img_height * 0.41),
            'label': 'Laju Penerimaan TBS',
            'tank_area': [int(img_width * 0.22), int(img_height * 0.38), int(img_width * 0.29), int(img_height * 0.44)]
        },
        {
            'x': int(img_width * 0.29), 'y': int(img_height * 0.81),
            'label': 'Laju Penerimaan TBS Mitra',
            'tank_area': [int(img_width * 0.25), int(img_height * 0.78), int(img_width * 0.32), int(img_height * 0.84)]
        }
    ],
    
    # --- FASE 2: STOCK PKS BARENGAN ---
    [
        {
            'x': int(img_width * 0.35), 'y': int(img_height * 0.41),
            'label': 'Stock PKS Kebun Sendiri',
            'tank_area': [int(img_width * 0.31), int(img_height * 0.38), int(img_width * 0.39), int(img_height * 0.44)]
        },
        {
            'x': int(img_width * 0.35), 'y': int(img_height * 0.81),
            'label': 'Stock PKS Mitra',
            'tank_area': [int(img_width * 0.31), int(img_height * 0.78), int(img_width * 0.39), int(img_height * 0.84)]
        }
    ],
    
    # --- FASE 3: PROSES MASUK KE TANGKI CPO BARENGAN ---
    [
        {
            'x': int(img_width * 0.54), 'y': int(img_height * 0.31),
            'label': 'Stock CPO Kebun Sendiri',
            'tank_area': [int(img_width * 0.50), int(img_height * 0.28), int(img_width * 0.58), int(img_height * 0.34)]
        },
        {
            'x': int(img_width * 0.54), 'y': int(img_height * 0.71),
            'label': 'Stock CPO Mitra',
            'tank_area': [int(img_width * 0.50), int(img_height * 0.68), int(img_width * 0.58), int(img_height * 0.74)]
        }
    ],
    
    # --- FASE 4: PROSES MASUK KE STORAGE KERNEL BARENGAN ---
    [
        {
            'x': int(img_width * 0.54), 'y': int(img_height * 0.41),
            'label': 'Stock Palm Kernel Kebun Sendiri',
            'tank_area': [int(img_width * 0.50), int(img_height * 0.38), int(img_width * 0.58), int(img_height * 0.44)]
        },
        {
            'x': int(img_width * 0.54), 'y': int(img_height * 0.81),
            'label': 'Stock Palm Kernel Mitra',
            'tank_area': [int(img_width * 0.50), int(img_height * 0.78), int(img_width * 0.58), int(img_height * 0.84)]
        }
    ],

    # --- FASE 5: OUTPUT TRANSMISI TOTAL BARENGAN ---
    [
        {
            'x': int(img_width * 0.81), 'y': int(img_height * 0.45),
            'label': 'Total CPO Yang Dihasilkan',
            'tank_area': [int(img_width * 0.76), int(img_height * 0.38), int(img_width * 0.86), int(img_height * 0.52)]
        },
        {
            'x': int(img_width * 0.81), 'y': int(img_height * 0.76),
            'label': 'Total Palm Kernel Yang Dihasilkan',
            'tank_area': [int(img_width * 0.76), int(img_height * 0.69), int(img_width * 0.86), int(img_height * 0.83)]
        }
    ]
]

# ==============================================================================
# 6. LOOPING SIMULASI (GRID RESOLUSI TINGGI / INCREMENT 25)
# ==============================================================================
placeholder = st.empty()
render_count = 0

while True:
    for phase in process_phases:
        fig = px.imshow(img)
        
        # --- AKTIFKAN GRID RAPAT KELIPATAN 25 ---
        fig.update_xaxes(
            visible=True, 
            showgrid=True, 
            gridwidth=1, 
            gridcolor='rgba(255, 0, 0, 0.25)', # Warna merah tipis agar tidak terlalu silau
            dtick=25 # Garis grid muncul setiap 25 piksel
        )
        fig.update_yaxes(
            visible=True, 
            showgrid=True, 
            gridwidth=1, 
            gridcolor='rgba(255, 0, 0, 0.25)', 
            dtick=25
        )
        
        for component in phase:
            # 1. Gambar Kotak Hijau Transparan
            area = component['tank_area']
            fig.add_shape(
                type="rect", 
                x0=area[0], y0=area[1], x1=area[2], y1=area[3],
                fillcolor="rgba(0, 255, 0, 0.4)",
                line=dict(color="LimeGreen", width=3),
            )
            
            # 2. Gambar Segitiga Indikator Kuning & Label Teks
            fig.add_scatter(
                x=[component['x']], y=[component['y']], mode="markers+text",
                marker=dict(size=24, color="yellow", symbol="triangle-right", line=dict(width=2, color="orange")),
                text=[component['label']], textposition="bottom center",
                textfont=dict(size=12, color="darkred", family="Arial Black")
            )
        
        # Penyesuaian layout agar koordinat sumbu X dan Y terbaca nyaman
        fig.update_layout(
            margin=dict(l=40, r=40, t=15, b=25),
            height=510,
            autosize=True
        )
        
        with placeholder.container():
            st.plotly_chart(
                fig, 
                use_container_width=True, 
                config={
                    'displayModeBar': True,
                    'responsive': True
                }, 
                key=f"pks_grid_25_{render_count}"
            )
        
        render_count += 1
        time.sleep(3.0) # Waktu tunggu dinaikkan ke 3 detik agar lebih leluasa membaca grid 25
