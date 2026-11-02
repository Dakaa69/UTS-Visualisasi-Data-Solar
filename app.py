from pathlib import Path
from textwrap import dedent

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# =========================================================
# KONFIGURASI HALAMAN
# =========================================================
st.set_page_config(
    page_title="Solar Power Generation Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Identitas mahasiswa
NAMA = "Raka Ramadhan"
NIM = "241051016"
PROGRAM_STUDI = "Sistem Informasi"
MATA_KULIAH = "Visualisasi Data"

DATA_PATH = (
    Path(__file__).resolve().parent
    / "dataset"
    / "solar_cleaned.csv"
)


# =========================================================
# TEMA DAN CSS
# =========================================================
st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(
                circle at 85% 5%,
                rgba(25,120,76,.13),
                transparent 28%
            ),
            linear-gradient(
                135deg,
                #07100d,
                #08120e 55%,
                #07100d
            );
        color: #f2f7f3;
    }

    [data-testid="stSidebar"] {
        background: #0b1711;
        border-right: 1px solid rgba(39,230,138,.23);
    }

    .main .block-container {
        padding-top: 2.1rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    h1, h2, h3 {
        color: #f2f7f3 !important;
    }

    .hero-title {
        font-size: clamp(2rem, 4vw, 3.2rem);
        font-weight: 850;
        line-height: 1.1;
        margin-bottom: .35rem;
        animation: fadeUp .7s ease both;
    }

    .hero-title span,
    .section-kicker {
        color: #27e68a;
    }

    .hero-subtitle,
    .section-description {
        color: #a8b9ae;
        line-height: 1.7;
    }

    .identity-card {
        background: linear-gradient(
            120deg,
            rgba(19,43,30,.95),
            rgba(13,27,20,.95)
        );
        border: 1px solid rgba(39,230,138,.23);
        border-radius: 16px;
        padding: 18px 22px;
        margin: 1.3rem 0 1.8rem;
        animation: fadeUp .8s ease both;
    }

    .identity-name {
        font-size: 1.12rem;
        font-weight: 750;
        margin-bottom: 5px;
    }

    .identity-detail {
        color: #a8b9ae;
        font-size: .82rem;
    }

    .section-kicker {
        font-size: .76rem;
        font-weight: 800;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        margin-bottom: .25rem;
    }

    .section-description {
        font-size: .88rem;
        margin-top: -.45rem;
        margin-bottom: 1rem;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(
            145deg,
            #122219,
            #0c1912
        );
        border: 1px solid rgba(39,230,138,.23);
        border-radius: 16px;
        padding: 18px;
        min-height: 118px;
        transition: .25s;
        animation: fadeUp .65s ease both;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        border-color: rgba(39,230,138,.65);
        box-shadow: 0 10px 28px rgba(0,210,120,.1);
    }

    div[data-testid="stMetricLabel"] {
        color: #a8b9ae !important;
    }

    div[data-testid="stMetricValue"] {
    color: #27e68a !important;
    font-weight: 850;
    font-size: clamp(1.1rem, 1.6vw, 1.55rem) !important;
    white-space: nowrap;
    }

    .explain-card {
        background: rgba(17,32,23,.88);
        border: 1px solid rgba(39,230,138,.12);
        border-left: 3px solid #27e68a;
        border-radius: 0 12px 12px 0;
        padding: 13px 16px;
        margin: .3rem 0 1.8rem;
        color: #bdcfc3;
        font-size: .82rem;
        line-height: 1.7;
    }

    .insight-card {
        background: linear-gradient(
            145deg,
            #12271b,
            #0b1811
        );
        border: 1px solid rgba(39,230,138,.23);
        border-radius: 14px;
        padding: 16px 18px;
        min-height: 112px;
        margin-bottom: .4rem;
    }

    .insight-label {
        color: #a8b9ae;
        font-size: .68rem;
        font-weight: 800;
        letter-spacing: .8px;
        text-transform: uppercase;
    }

    .insight-value {
        color: #27e68a;
        font-size: 1.25rem;
        font-weight: 850;
        margin: 7px 0 4px;
    }

    .insight-note {
        color: #bdcfc3;
        font-size: .78rem;
        line-height: 1.5;
    }

    .footer-note {
        color: #8fa398;
        font-size: .76rem;
        line-height: 1.6;
        border-top: 1px solid rgba(39,230,138,.23);
        padding-top: 1rem;
        margin-top: 2rem;
    }

    div[data-testid="stPlotlyChart"] {
        animation: fadeIn .8s ease both;
    }

    @keyframes fadeUp {
        from {
            opacity: 0;
            transform: translateY(13px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @media(max-width:768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .identity-card {
            padding: 15px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# FUNGSI BANTU
# =========================================================
@st.cache_data(show_spinner="Memuat dataset...")
def load_data(path):
    data = pd.read_csv(path)

    required = {
        "DATE_TIME",
        "PLANT_NAME",
        "INVERTER_KEY",
        "AC_POWER",
        "IRRADIATION",
    }

    missing = required.difference(data.columns)

    if missing:
        raise ValueError(
            "Kolom tidak ditemukan: "
            + ", ".join(sorted(missing))
        )

    data["DATE_TIME"] = pd.to_datetime(
        data["DATE_TIME"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["DATE_TIME"]
    ).copy()

    numeric_columns = [
        "DC_POWER",
        "AC_POWER",
        "IRRADIATION",
        "AMBIENT_TEMPERATURE",
        "MODULE_TEMPERATURE",
    ]

    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column],
                errors="coerce"
            )

    data["DATE"] = data["DATE_TIME"].dt.date
    data["HOUR"] = data["DATE_TIME"].dt.hour

    return data


@st.cache_data(show_spinner=False)
def calculate_daily_energy(data):
    """
    Mengestimasi energi menggunakan metode trapesium.

    Perhitungan hanya menggunakan pasangan observasi
    berurutan dengan interval tepat 15 menit.

    Asumsi: AC_POWER menggunakan satuan kW.
    """

    ordered = data.sort_values(
        ["PLANT_NAME", "INVERTER_KEY", "DATE_TIME"]
    ).copy()

    groups = ordered.groupby(
        ["PLANT_NAME", "INVERTER_KEY"],
        sort=False
    )

    ordered["NEXT_TIME"] = groups[
        "DATE_TIME"
    ].shift(-1)

    ordered["NEXT_AC_POWER"] = groups[
        "AC_POWER"
    ].shift(-1)

    ordered["INTERVAL_MINUTES"] = (
        ordered["NEXT_TIME"] - ordered["DATE_TIME"]
    ).dt.total_seconds() / 60

    valid = ordered.loc[
        ordered["INTERVAL_MINUTES"].eq(15)
        & ordered["AC_POWER"].notna()
        & ordered["NEXT_AC_POWER"].notna()
    ].copy()

    valid["ENERGY_KWH"] = (
        (valid["AC_POWER"] + valid["NEXT_AC_POWER"]) / 2
    ) * 0.25

    valid["DATE"] = valid["DATE_TIME"].dt.date

    daily_energy = (
        valid.groupby(
            ["DATE", "PLANT_NAME"],
            as_index=False
        )
        .agg(
            TOTAL_ENERGY_KWH=("ENERGY_KWH", "sum"),
            VALID_INTERVALS=("ENERGY_KWH", "count"),
        )
    )

    return daily_energy


def compact(value):
    """Memformat angka besar agar tidak terpotong pada KPI."""

    if pd.isna(value):
        return "N/A"

    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"

    if abs(value) >= 1_000:
        return f"{value / 1_000:.2f}K"

    return f"{value:,.2f}"


def chart_theme(fig, height=390):
    """Menyeragamkan tema grafik."""

    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Arial",
            color="#dce9e0",
            size=11
        ),
        margin=dict(
            l=20,
            r=25,
            t=45,
            b=25
        ),
        legend=dict(
            title="Pembangkit",
            y=1,
            x=1.01
        ),
        hoverlabel=dict(
            bgcolor="#14251b",
            bordercolor="#27e68a",
            font_color="white"
        )
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False
    )

    fig.update_yaxes(
        gridcolor="rgba(160,190,170,.16)",
        zerolinecolor="rgba(160,190,170,.22)"
    )

    return fig


def explain(reading, interpretation):
    st.markdown(
        f"""
        <div class="explain-card">
            <b>Cara membaca grafik:</b>
            {reading}
            <br><br>
            <b>Interpretasi:</b>
            {interpretation}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# MEMUAT DATASET
# =========================================================
if not DATA_PATH.exists():
    st.error(
        "Dataset tidak ditemukan. Pastikan file berada "
        "di folder dataset/solar_cleaned.csv."
    )
    st.stop()

try:
    df = load_data(str(DATA_PATH))

except Exception as error:
    st.error(f"Gagal membaca dataset: {error}")
    st.stop()

if df.empty:
    st.error(
        "Dataset tidak memiliki data yang dapat dianalisis."
    )
    st.stop()

energy_all = calculate_daily_energy(df)


# =========================================================
# SIDEBAR DAN FILTER
# =========================================================
plants = sorted(
    df["PLANT_NAME"].dropna().unique().tolist()
)

min_date = df["DATE_TIME"].min().date()
max_date = df["DATE_TIME"].max().date()

with st.sidebar:

    st.markdown(
        """
        <h2 style="
            color:#27e68a;
            font-size:1.35rem;
            margin-bottom:0
        ">
            CONTROL PANEL
        </h2>

        <p style="
            color:#a8b9ae;
            font-size:.78rem
        ">
            Atur tampilan data dashboard
        </p>
        """,
        unsafe_allow_html=True
    )

    if "plants_filter" not in st.session_state:
        st.session_state.plants_filter = plants.copy()

    if "date_filter" not in st.session_state:
        st.session_state.date_filter = (
            min_date,
            max_date
        )

    def reset_filters():
        st.session_state.plants_filter = plants.copy()
        st.session_state.date_filter = (
            min_date,
            max_date
        )

    st.button(
        "Reset Filter",
        use_container_width=True,
        on_click=reset_filters,
        type="primary"
    )

    st.markdown("**Pilih Pembangkit**")

    selected_plants = st.multiselect(
        "Pembangkit",
        plants,
        key="plants_filter",
        label_visibility="collapsed"
    )

    st.markdown("**Rentang Tanggal**")

    selected_dates = st.date_input(
        "Rentang tanggal",
        min_value=min_date,
        max_value=max_date,
        key="date_filter",
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown(
        """
        <div style="
            color:#9eb0a4;
            font-size:.8rem;
            line-height:2.1
        ">
            <b>Dataset:</b> Solar Power Generation Data
            <br>
            <b>Sumber:</b> Kaggle, Ani Kannal
            <br>
            <b>Periode:</b> 15 Mei sampai 17 Juni 2020
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# MENERAPKAN FILTER
# =========================================================
if not selected_plants:
    st.warning(
        "Pilih minimal satu pembangkit pada Control Panel."
    )
    st.stop()

if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
else:
    start_date = selected_dates
    end_date = selected_dates

if start_date > end_date:
    st.warning(
        "Tanggal awal tidak boleh melebihi tanggal akhir."
    )
    st.stop()

filtered = df[
    df["PLANT_NAME"].isin(selected_plants)
    & df["DATE_TIME"].dt.date.between(
        start_date,
        end_date
    )
].copy()

energy = energy_all[
    energy_all["PLANT_NAME"].isin(selected_plants)
    & energy_all["DATE"].between(
        start_date,
        end_date
    )
].copy()

if filtered.empty:
    st.warning(
        "Tidak ada data pada kombinasi filter yang dipilih."
    )
    st.stop()


# =========================================================
# HEADER DAN IDENTITAS
# =========================================================
st.markdown(
    """
    <div class="hero-title">
        SOLAR POWER <span>GENERATION</span>
    </div>

    <div class="hero-subtitle">
        Interactive Data Analytics Dashboard
        <br>
        Analisis performa pembangkit listrik tenaga surya
        berdasarkan data produksi dan kondisi lingkungan.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    dedent(f"""
    <div class="identity-card">
        <div class="identity-name">{NAMA}</div>
        <div class="identity-detail">
            NIM: {NIM}
            &nbsp; | &nbsp;
            Program Studi: {PROGRAM_STUDI}
            &nbsp; | &nbsp;
            Mata Kuliah: {MATA_KULIAH}
        </div>
    """),
    unsafe_allow_html=True
)


# =========================================================
# KPI
# =========================================================
st.markdown(
    '<div class="section-kicker">Ringkasan</div>',
    unsafe_allow_html=True
)

st.header("Overview Performa")

st.markdown(
    """
    <div class="section-description">
        Ringkasan indikator utama berdasarkan filter aktif.
    </div>
    """,
    unsafe_allow_html=True
)

total_energy = energy["TOTAL_ENERGY_KWH"].sum()
avg_ac = filtered["AC_POWER"].mean()
avg_irr = filtered["IRRADIATION"].mean()

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Estimated Energy",
    f"{compact(total_energy)} kWh",
    help=(
        "Estimasi energi dari pasangan observasi berurutan "
        "dengan interval tepat 15 menit. "
        "Mengasumsikan AC_POWER dalam kW."
    )
)

k2.metric(
    "Average AC Power",
    f"{avg_ac:,.2f}" if pd.notna(avg_ac) else "N/A",
    help="Rata-rata AC_POWER pada observasi yang masuk filter."
)

k3.metric(
    "Average Irradiation",
    f"{avg_irr:.3f}" if pd.notna(avg_irr) else "N/A",
    help="Rata-rata irradiation pada observasi yang masuk filter."
)

k4.metric(
    "Total Records",
    f"{len(filtered):,}",
    help="Jumlah baris setelah filter diterapkan."
)

st.caption(
    "Catatan: Estimasi energi menggunakan pasangan data berurutan "
    "dengan interval tepat 15 menit. Perhitungan mengasumsikan "
    "AC_POWER dalam satuan kW. Verifikasi satuan pada dokumentasi "
    "dataset sebelum menganggap hasil sebagai pengukuran energi resmi."
)


# =========================================================
# GRAFIK 1: TREN PRODUKSI ENERGI HARIAN
# =========================================================
st.divider()

st.markdown(
    '<div class="section-kicker">01 / Analisis temporal</div>',
    unsafe_allow_html=True
)

st.subheader("Tren Produksi Energi Harian")

st.markdown(
    """
    <div class="section-description">
        Perubahan estimasi energi dari hari ke hari
        pada setiap pembangkit.
    </div>
    """,
    unsafe_allow_html=True
)

if energy.empty:

    st.info(
        "Tidak tersedia pasangan interval valid "
        "untuk menghitung estimasi energi."
    )

else:

    fig = px.line(
        energy.sort_values("DATE"),
        x="DATE",
        y="TOTAL_ENERGY_KWH",
        color="PLANT_NAME",
        markers=True,
        labels={
            "DATE": "Tanggal",
            "TOTAL_ENERGY_KWH": "Estimasi Energi (kWh)",
            "PLANT_NAME": "Pembangkit"
        },
        color_discrete_sequence=[
            "#27e68a",
            "#55a7ff"
        ]
    )

    fig.update_traces(
        line=dict(width=2.8),
        marker=dict(size=5),
        hovertemplate=(
            "Tanggal: %{x}<br>"
            "Estimasi energi: %{y:,.2f} kWh"
            "<extra>%{fullData.name}</extra>"
        )
    )

    fig = chart_theme(fig)
    fig.update_layout(hovermode="x unified")

    st.plotly_chart(
        fig,
        use_container_width=True
    )

explain(
    "Sumbu horizontal menunjukkan tanggal pengamatan. "
    "Sumbu vertikal menunjukkan estimasi energi harian dalam kWh. "
    "Setiap garis mewakili satu pembangkit.",
    "Bandingkan perubahan antarhari. Perubahan dapat berkaitan "
    "dengan radiasi matahari, ketersediaan data, dan kondisi "
    "operasional. Estimasi hanya menggunakan interval berurutan "
    "yang valid."
)


# =========================================================
# GRAFIK 2: POLA PRODUKSI BERDASARKAN JAM
# =========================================================
st.markdown(
    '<div class="section-kicker">02 / Pola intrahari</div>',
    unsafe_allow_html=True
)

st.subheader("Pola Produksi Berdasarkan Jam")

st.markdown(
    """
    <div class="section-description">
        Mengidentifikasi waktu dengan rata-rata output AC tertinggi.
    </div>
    """,
    unsafe_allow_html=True
)

hourly = (
    filtered.groupby(
        ["HOUR", "PLANT_NAME"],
        as_index=False
    )
    .agg(
        AVERAGE_AC_POWER=("AC_POWER", "mean")
    )
)

fig = px.line(
    hourly,
    x="HOUR",
    y="AVERAGE_AC_POWER",
    color="PLANT_NAME",
    markers=True,
    labels={
        "HOUR": "Jam",
        "AVERAGE_AC_POWER": "Rata-rata AC Power",
        "PLANT_NAME": "Pembangkit"
    },
    color_discrete_sequence=[
        "#27e68a",
        "#55a7ff"
    ]
)

fig.update_traces(
    line=dict(width=2.8),
    marker=dict(size=6)
)

fig.update_xaxes(
    tickmode="linear",
    dtick=2,
    range=[0, 23]
)

fig = chart_theme(fig)

st.plotly_chart(
    fig,
    use_container_width=True
)

hour_avg = filtered.groupby("HOUR")["AC_POWER"].mean()

peak_hour = int(hour_avg.idxmax())
peak_value = float(hour_avg.max())

explain(
    "Sumbu horizontal menunjukkan jam pengamatan. "
    "Sumbu vertikal menunjukkan rata-rata AC Power pada jam tersebut. "
    "Area berwarna mewakili masing-masing pembangkit.",
    f"Jam {peak_hour:02d}:00 memiliki rata-rata AC Power gabungan "
    f"tertinggi sebesar {peak_value:,.2f}. Grafik menunjukkan pola "
    "rata-rata, bukan produksi setiap inverter secara individual."
)


# =========================================================
# GRAFIK 3: HUBUNGAN IRRADIATION DAN AC POWER
# =========================================================
st.markdown(
    '<div class="section-kicker">03 / Hubungan antarvariabel</div>',
    unsafe_allow_html=True
)

st.subheader("Hubungan Radiasi Matahari dan Output")

st.markdown(
    """
    <div class="section-description">
        Melihat hubungan antara irradiation dan AC Power.
    </div>
    """,
    unsafe_allow_html=True
)

scatter = filtered.dropna(
    subset=["IRRADIATION", "AC_POWER"]
)

fig = px.scatter(
    scatter,
    x="IRRADIATION",
    y="AC_POWER",
    color="PLANT_NAME",
    opacity=.55,
    render_mode="webgl",
    labels={
        "IRRADIATION": "Irradiation",
        "AC_POWER": "AC Power",
        "PLANT_NAME": "Pembangkit"
    },
    color_discrete_sequence=[
        "#27e68a",
        "#55a7ff"
    ],
    hover_data={
        "DATE_TIME": True,
        "INVERTER_KEY": True,
        "IRRADIATION": ":.3f",
        "AC_POWER": ":.2f"
    }
)

fig.update_traces(
    marker=dict(size=5)
)

fig = chart_theme(fig, 420)

st.plotly_chart(
    fig,
    use_container_width=True
)

corr = (
    scatter["IRRADIATION"].corr(scatter["AC_POWER"])
    if len(scatter) > 1
    else np.nan
)

explain(
    "Setiap titik mewakili satu observasi. Sumbu horizontal "
    "menunjukkan irradiation, sedangkan sumbu vertikal menunjukkan "
    "AC Power. Titik yang bergerak ke kanan atas menunjukkan "
    "irradiation dan output AC yang lebih tinggi.",
    "Sebaran titik menunjukkan arah dan kekuatan hubungan. "
    "Korelasi tidak membuktikan sebab-akibat. Faktor lain, "
    "seperti kondisi inverter dan kualitas data, juga dapat "
    "memengaruhi output."
)


# =========================================================
# GRAFIK 4: TOP 10 INVERTER
# =========================================================
st.markdown(
    '<div class="section-kicker">04 / Perbandingan unit</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Top 10 Inverter Berdasarkan Rata-rata Output"
)

st.markdown(
    """
    <div class="section-description">
        Menampilkan sepuluh inverter dengan rata-rata AC Power
        tertinggi pada filter aktif.
    </div>
    """,
    unsafe_allow_html=True
)

inverter = (
    filtered.groupby(
        ["PLANT_NAME", "INVERTER_KEY"],
        as_index=False
    )
    .agg(
        AVERAGE_AC_POWER=("AC_POWER", "mean"),
        OBSERVATIONS=("AC_POWER", "count")
    )
    .dropna(
        subset=["AVERAGE_AC_POWER"]
    )
)

top10 = inverter.nlargest(
    10,
    "AVERAGE_AC_POWER"
).copy()

top10["INVERTER_LABEL"] = (
    top10["PLANT_NAME"]
    + " | "
    + top10["INVERTER_KEY"].astype(str)
)

top10 = top10.sort_values(
    "AVERAGE_AC_POWER",
    ascending=True
)

fig = px.bar(
    top10,
    x="AVERAGE_AC_POWER",
    y="INVERTER_LABEL",
    color="PLANT_NAME",
    orientation="h",
    text="AVERAGE_AC_POWER",
    labels={
        "AVERAGE_AC_POWER": "Rata-rata AC Power",
        "INVERTER_LABEL": "Inverter",
        "PLANT_NAME": "Pembangkit"
    },
    color_discrete_sequence=[
        "#27e68a",
        "#55a7ff"
    ],
    hover_data={
        "OBSERVATIONS": True
    }
)

fig.update_traces(
    texttemplate="%{text:.1f}",
    textposition="outside",
    cliponaxis=False
)

fig = chart_theme(fig, 450)

fig.update_layout(
    yaxis=dict(
        title="Inverter",
        automargin=True,
        tickfont=dict(size=10)
    ),
    xaxis=dict(
        title="Rata-rata AC Power"
    ),
    margin=dict(
        l=25,
        r=70,
        t=35,
        b=35
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

explain(
    "Setiap batang menunjukkan satu inverter. Panjang batang "
    "menunjukkan rata-rata AC Power selama periode yang dipilih. "
    "Warna membedakan pembangkit.",
    "Grafik hanya menampilkan sepuluh inverter dengan rata-rata "
    "tertinggi agar label mudah dibaca. Perbandingan bersifat "
    "deskriptif. Perbedaan skala DC_POWER dan AC_POWER antarplant "
    "perlu diperhatikan sebelum menarik kesimpulan tentang efisiensi."
)


# =========================================================
# TEMUAN UTAMA
# =========================================================
st.divider()

st.markdown(
    '<div class="section-kicker">05 / Ringkasan analisis</div>',
    unsafe_allow_html=True
)

st.subheader("Temuan Utama")

st.markdown(
    """
    <div class="section-description">
        Ringkasan otomatis berdasarkan data yang telah difilter.
    </div>
    """,
    unsafe_allow_html=True
)

if not energy.empty:

    plant_energy = (
        energy.groupby("PLANT_NAME")["TOTAL_ENERGY_KWH"]
        .sum()
        .sort_values(ascending=False)
    )

    best_plant = plant_energy.index[0]
    best_energy = plant_energy.iloc[0]

else:

    best_plant = "Tidak tersedia"
    best_energy = np.nan

corr_text = (
    f"{corr:.3f}"
    if pd.notna(corr)
    else "Tidak tersedia"
)

a, b = st.columns(2)

with a:
    st.markdown(
        dedent(f"""
        <div class="insight-card">
            <div class="insight-label">
                Pembangkit dengan estimasi energi tertinggi
            </div>
            <div class="insight-value">
                {best_plant}
            </div>
            <div class="insight-note">
                Estimasi energi sebesar {compact(best_energy)} kWh
                pada periode filter yang dipilih.
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )

with b:
    st.markdown(
        dedent(f"""
        <div class="insight-card">
            <div class="insight-label">
                Jam dengan rata-rata AC Power tertinggi
            </div>
            <div class="insight-value">
                {peak_hour:02d}:00
            </div>
            <div class="insight-note">
                Rata-rata AC Power gabungan mencapai
                {peak_value:,.2f} pada jam tersebut.
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )

st.markdown(
    dedent(f"""
    <div class="insight-card" style="margin-top:.4rem">
        <div class="insight-label">
            Korelasi Irradiation dan AC Power
        </div>
        <div class="insight-value">
            {corr_text}
        </div>
        <div class="insight-note">
            Nilai korelasi menunjukkan arah dan kekuatan hubungan
            linear pada data yang difilter. Korelasi bukan bukti
            hubungan sebab-akibat.
        </div>
    </div>
    """),
    unsafe_allow_html=True
)

# =========================================================
# INFORMASI DATASET DAN METODOLOGI
# =========================================================
st.divider()

st.markdown(
    '<div class="section-kicker">06 / Transparansi data</div>',
    unsafe_allow_html=True
)

st.subheader("Informasi Dataset")

with st.expander(
    "Lihat informasi dan metodologi pengolahan data"
):

    st.markdown(
        """
        **Sumber data:** Solar Power Generation Data,
        Kaggle, oleh Ani Kannal.

        **Periode pengamatan:** 15 Mei sampai 17 Juni 2020.

        **Jumlah observasi setelah penggabungan:**
        136.476 baris sebelum filter.

        **Metode penggabungan:** Data generation dan weather
        digabung menggunakan `DATE_TIME` dan `PLANT_ID`.
        `SOURCE_KEY` tidak digunakan sebagai kunci karena
        mewakili perangkat yang berbeda.

        **Penanganan data cuaca kosong:** Nilai tanpa pasangan
        data cuaca dipertahankan sebagai `NaN`, bukan diubah
        menjadi nol.

        **Estimasi energi:** Metode trapesium pada pasangan
        observasi berurutan dengan interval tepat 15 menit.
        Pasangan dengan interval lain tidak dimasukkan.

        **Asumsi satuan:** Perhitungan kWh mengasumsikan
        `AC_POWER` dalam kW. Satuan perlu diverifikasi melalui
        dokumentasi dataset.

        **Batasan interpretasi:** Dataset mencakup sekitar
        34 hari. Hasil analisis tidak dapat digunakan untuk
        menyimpulkan tren tahunan atau performa jangka panjang.

        **Catatan perbandingan pembangkit:** Perbedaan skala
        `DC_POWER` dan `AC_POWER` antarplant perlu diperhatikan.
        Rata-rata output tidak otomatis menunjukkan efisiensi
        yang lebih baik.
        """
    )


# =========================================================
# FOOTER
# =========================================================
st.markdown(
    f"""
    <div class="footer-note">
        <b>{NAMA}</b> | {NIM} | {PROGRAM_STUDI}
        <br>
        Dashboard Ujian Tengah Semester - {MATA_KULIAH}
        <br>
        Dataset: Solar Power Generation Data, Kaggle.
        Periode: 15 Mei - 17 Juni 2020.
    </div>
    """,
    unsafe_allow_html=True
)