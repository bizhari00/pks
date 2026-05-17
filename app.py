import streamlit as st

# ==============================================================================
# 1. KONFIGURASI HALAMAN UTAMA (Wajib Paling Atas)
# ==============================================================================
st.set_page_config(
    page_title="Pabrik PKS - Kalibrasi Kotak",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Pengaturan padding halaman utama agar aman di Forio 80%
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
    st.subheader("Kalibrasi Posisi: Pengaturan Kotak via Koordinat XY Murni")

st.divider()

# ==============================================================================
# 4. MEMUAT BACKGROUND IMAGE PKS
# ==============================================================================
try:
    img = Image.open("pks.png")
except FileNotFoundError:
    st.error("File 'pks.png' tidur/tidak ditemukan. Pastikan file gambar ada di root repository GitHub Anda.")
    st.stop()

# ==============================================================================
# 5. INPUT KOORDINAT XY MURNI (Fokus pada tank_area saja)
#    Format tank_area: [X_Mulai, Y_Mulai, X_Akhir, Y_Akhir]
# ==============================================================================
process_phases = [
    # --- FASE 1: PENERIMAAN TBS BARENGAN ---
    [
        {
            'label': 'Laju Penerimaan TBS Kebun Sendiri',
            'tank_area': [177, 121, 313, 210]
        },
        {
            'label': 'Laju Penerimaan TBS Mitra',
            'tank_area': [192, 485, 332, 610]
        }
    ],
    
    # --- FASE 2: STOCK PKS BARENGAN ---
    [
        {
            'label': 'Stock PKS Kebun Sendiri',
            'tank_area': [322, 188, 466, 194]
        },
        {
            'label': 'Stock PKS Mitra',
            'tank_area': [338, 483, 451, 584]
        }
    ],
    
    # --- FASE 3: PROSES MASUK KE TANGKI CPO BARENGAN ---
    [
        {
            'label': 'Stock CPO Kebun Sendiri',
            'tank_area': [500, 135, 580, 165]
        },
        {
            'label': 'Stock CPO Mitra',
            'tank_area': [500, 335, 580, 365]
        }
    ],
    
    # --- FASE 4: PROSES MASUK KE STORAGE KERNEL BARENGAN ---
    [
        {
            'label': 'Stock Palm Kernel Kebun Sendiri',
            'tank_area': [500, 185, 580, 215]
        },
        {
            'label': 'Stock Palm Kernel Mitra',
            'tank_area': [500, 385, 580, 415]
        }
    ],

    # --- FASE 5: OUTPUT TRANSMISI TOTAL BARENGAN ---
    [
        {
            'label': 'Total CPO Yang Dihasilkan',
            'tank_area': [760, 185, 860, 255]
        },
        {
            'label': 'Total Palm Kernel Yang Dihasilkan',
            'tank_area': [760, 345, 860, 415]
        }
    ]
]

# ==============================================================================
# 6. LOOPING RENDERING & GRID SISTEM
# ==============================================================================
placeholder = st.empty()
render_count = 0

while True:
    for phase in process_phases:
        fig = px.imshow(img)
        
        # Grid pembantu kelipatan 50 aktif untuk melihat posisi angka kotak
        fig.update_xaxes(
            visible=True, 
            showgrid=True, 
            gridwidth=1, 
            gridcolor='rgba(255, 0, 0, 0.3)', 
            dtick=50
        )
        fig.update_yaxes(
            visible=True, 
            showgrid=True, 
            gridwidth=1, 
            gridcolor='rgba(255, 0, 0, 0.3)', 
            dtick=50
        )
        
        for component in phase:
            area = component['tank_area']
            
            # 1. Menggambar Kotak Berdasarkan Nilai XY Murni
            fig.add_shape(
                type="rect", 
                x0=area[0], y0=area[1], x1=area[2], y1=area[3],
                fillcolor="rgba(0, 255, 0, 0.4)",
                line=dict(color="LimeGreen", width=3),
            )
            
            # 2. Perhitungan Otomatis Koordinat Label di Bawah Kotak
            text_x = (area[0] + area[2]) / 2  # Titik tengah horizontal kotak
            text_y = area[3] + 20             # Menaruh teks 20 piksel di bawah batas bawah kotak
            
            # 3. Menggambar Teks Label Hasil Kalkulasi Dinamis
            fig.add_scatter(
                x=[text_x], y=[text_y], 
                mode="text",
                text=[component['label']], 
                textposition="bottom center",
                textfont=dict(size=11, color="darkred", family="Arial Black")
            )
        
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
                key=f"pks_xy_calibration_{render_count}"
            )
        
        render_count += 1
        time.sleep(3.0)
