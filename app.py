import streamlit as st
import plotly.express as px
from PIL import Image
import time

# ==============================================================================
# 1. KONFIGURASI HALAMAN UTAMA (Wajib Paling Atas)
# ==============================================================================
st.set_page_config(
    page_title="Pabrik PKS - Mode Live",
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

# ==============================================================================
# 2. STRATEGI TURUNKAN LAYOUT 
# ==============================================================================
st.markdown("<br><br>", unsafe_allow_html=True)

# ==============================================================================
# 3. NAVIGASI & JUDUL SEBARIS (Balanced Design Button & Title)
# ==============================================================================
st.markdown(
    """
    <style>
    /* 1. Mengatur Ukuran & Corak Kotak Tombol Navigasi */
    .stLinkButton > a {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%) !important; /* Gradasi biru premium */
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important; 
        padding: 8px 20px !important; 
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25) !important;
        transition: all 0.3s ease-in-out !important;
        text-decoration: none !important;
        
        /* KUNCI KESEIMBANGAN: Lebar otomatis dan tidak melar penuh */
        display: inline-flex !important;
        width: auto !important;
        max-width: 320px !important; 
    }

    /* 2. Menyesuaikan Ukuran Font di Dalam Tombol */
    .stLinkButton > a p {
        font-size: 16px !important; 
        font-weight: bold !important;
        color: #FFFFFF !important;
        letter-spacing: 0.5px !important;
    }

    /* 3. Efek Hover Interaktif */
    .stLinkButton > a:hover {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%) !important;
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4) !important;
        transform: translateY(-1px) !important;
    }

    /* 4. Mengatur Teks Judul Diagram Agar Selaras Sebaris */
    .custom-title {
        font-size: 20px !important; 
        font-weight: 500 !important;
        color: #1E293B;
        margin-top: 8px; 
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Pembagian kolom rasio agar seimbang dan sejajar lurus secara vertikal
col_btn, col_title = st.columns([1.2, 2.8])

with col_btn:
    st.link_button("🏠 ke Menu Simulasi", "https://forio.com/app/bustamiizhari/research-day", use_container_width=False)

with col_title:
    st.markdown('<p class="custom-title">Produksi PKS</p>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 4. MEMUAT BACKGROUND IMAGE PKS
# ==============================================================================
try:
    img = Image.open("pks.png")
except FileNotFoundError:
    st.error("File 'pks.png' tidak ditemukan. Pastikan file gambar ada di root repository GitHub Anda.")
    st.stop()

# ==============================================================================
# 5. DATA KOORDINAT XY MURNI (Hasil Kalibrasi Pas)
#    Format tank_area: [X_Mulai, Y_Mulai, X_Akhir, Y_Akhir]
# ==============================================================================
process_phases = [
    # --- FASE 1: PENERIMAAN TBS BARENGAN ---
    [
        {
            'label': '',
            'tank_area': [177, 121, 313, 210]
        },
        {
            'label': '',
            'tank_area': [192, 485, 332, 610]
        }
    ],
    
    # --- FASE 2: STOCK PKS BARENGAN ---
    [
        {
            'label': '',
            'tank_area': [326, 110, 470, 200]
        },
        {
            'label': '',
            'tank_area': [338, 483, 451, 584]
        }
    ],
    
    # --- FASE 3: PROSES MASUK KE TANGKI CPO BARENGAN ---
    [
        {
            'label': '',
            'tank_area': [620, 40, 749, 108]
        },
        {
            'label': '',
            'tank_area': [605, 405, 745, 490]
        }
    ],
    
    # --- FASE 4: PROSES MASUK KE STORAGE KERNEL BARENGAN ---
    [
        {
            'label': '',
            'tank_area': [625, 125, 763, 200]
        },
        {
            'label': '',
            'tank_area': [615, 495, 755, 583]
        }
    ],

    # --- FASE 5: OUTPUT TRANSMISI TOTAL BARENGAN (UBAH JADI CIRCLE) ---
    [
        {
            'label': '',
            'shape_type': 'circle',  # Mengubah total CPO menjadi Lingkaran
            'tank_area': [1106,157,1245,290]
        },
        {
            'label': '',
            'shape_type': 'circle',  # Mengubah total Palm Kernel menjadi Lingkaran
            'tank_area': [1116,467,1253,598]
        }
    ]
]

# ==============================================================================
# 6. LOOPING RENDERING (MODE NORMAL - GRID OFF)
# ==============================================================================
placeholder = st.empty()
render_count = 0

while True:
    for phase in process_phases:
        fig = px.imshow(img)
        
        # --- MODE NORMAL: Menonaktifkan Grid dan Sumbu Koordinat ---
        fig.update_xaxes(visible=False, showgrid=False)
        fig.update_yaxes(visible=False, showgrid=False)
        
        for component in phase:
            area = component['tank_area']
            # Mengambil nilai shape_type, default-nya ke 'rect' (kotak) jika tidak ditulis
            shape = component.get('shape_type', 'rect')
            
            # 1. Menggambar Bentuk Berdasarkan Tipe Dinamik (Kotak/Lingkaran)
            fig.add_shape(
                type=shape, 
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
            margin=dict(l=0, r=0, t=15, b=0), 
            height=500,
            autosize=True,
            showlegend=False
        )
        
        with placeholder.container():
            st.plotly_chart(
                fig, 
                use_container_width=True, 
                config={
                    'displayModeBar': False, 
                    'responsive': True
                }, 
                key=f"pks_live_mode_{render_count}"
            )
        
        render_count += 1
        time.sleep(3.0)
