import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import calendar
from datetime import datetime

# Konfigurasi Dashboard
st.set_page_config(
    page_title="Dashboard Final Project",
    page_icon="📊",
    layout="wide"
)

# Sidebar
st.sidebar.header("Dashboard Final Project")
st.sidebar.text("by Hanif Ismail")
st.sidebar.image("dicoding.png", use_container_width=True)

# Mendapatkan tanggal saat ini
today = datetime.today()
current_year = today.year
current_month = today.month
current_day = today.day

# Menampilkan kalender
st.sidebar.subheader("Today's date")
cal = calendar.HTMLCalendar(calendar.SUNDAY)
html_calendar = cal.formatmonth(current_year, current_month)

# Menyoroti tanggal saat ini dengan latar belakang kuning dan teks hitam
html_calendar = html_calendar.replace(f'>{current_day}<', f' bgcolor="yellow" style="color:black"><b>{current_day}</b><')
st.sidebar.markdown(html_calendar, unsafe_allow_html=True)

# Load data untuk Tab1 dan Tab2
@st.cache_data
def load_data():
    df = pd.read_csv("day.csv")
    return df

df = load_data()

# Filter by season
seasons = ['All Season', 'Spring', 'Summer', 'Fall', 'Winter']
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
df['season_label'] = df['season'].map(season_map)

def filter_data_by_season(df, selected_season):
    if selected_season == 'All Season':
        return df
    else:
        return df[df['season_label'] == selected_season]

# Tab for Pertanyaan 1
tab1, tab2, tab3 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Analisis Lanjutan"])

with tab1:
    st.header("Bagaimana distribusi rata-rata pengguna kasual dan terdaftar pada hari libur nasional berdasarkan musim?")

    # Membuat dua kolom untuk visualisasi dan insight
    col1, col2 = st.columns([2, 1])  # Membuat kolom dengan proporsi 2:1

    with col2:
        # Dropdown untuk filtering berdasarkan musim
        selected_season = st.selectbox("**Filter by**:", seasons, key="tab1_season_select")
        filtered_df = filter_data_by_season(df, selected_season)

    with col1:
        # Memetakan nama musim
        filtered_df['season_label'] = filtered_df['season'].map(season_map)

        # Filter data hari libur nasional
        holiday_df = filtered_df[filtered_df['holiday'] == 1]

        # Kelompokkan rata-rata pengguna berdasarkan musim
        casual_by_season = holiday_df.groupby('season_label')['casual'].mean()
        registered_by_season = holiday_df.groupby('season_label')['registered'].mean()

        # Bar width
        bar_width = 0.35

        # Positions of the bars on the x-axis
        r1 = np.arange(len(casual_by_season))
        r2 = [x + bar_width for x in r1]

        # Plotting
        fig, ax = plt.subplots(figsize=(6, 4))  # Mengubah ukuran figure

        # Membuat chart bar
        ax.bar(r1, casual_by_season, color='skyblue', width=bar_width, edgecolor='grey', label='Casual Users')
        ax.bar(r2, registered_by_season, color='orange', width=bar_width, edgecolor='grey', label='Registered Users')

        # Menambahkan keterangan grafik
        ax.set_title('Rata-rata Pengguna Kasual dan Terdaftar pada Hari Libur Nasional', fontsize=12, fontweight='bold')
        ax.set_xlabel('Musim', fontweight='bold', fontsize=10)
        ax.set_ylabel('Rata-rata Jumlah Pengguna', fontweight='bold', fontsize=10)

        # Memindahkan legenda
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

        # Menata layout
        plt.xticks(r1 + bar_width / 2, casual_by_season.index)
        plt.tight_layout()

        # Menampilkan plot di Streamlit
        st.pyplot(fig)

    with col2:
        # Menambahkan tabel
        st.write("**Detail Rata-rata Pengguna Kasual dan Terdaftar pada Hari Libur Nasional Berdasarkan Musim:**")
        data = {
            'Season': casual_by_season.index.tolist(),
            'Casual Users': casual_by_season.tolist(),
            'Registered Users': registered_by_season.tolist()
        }
        df_table = pd.DataFrame(data)

        # Mengatur gaya tabel
        styled_table = df_table.style.set_properties(**{
            'text-align': 'left'  # Pengaturan untuk semua kolom
        }).set_properties(subset=['Casual Users', 'Registered Users'], **{
            'text-align': 'center'  # Pengaturan khusus untuk kolom tertentu
        })

        # Menampilkan tabel dengan gaya di Streamlit
        st.write(styled_table)  # Menggunakan st.write() untuk menampilkan tabel bergaya

        # Menerapkan style pada sel baris pertama
        styled_table = styled_table.applymap(lambda x: 'text-align: center;', subset=pd.IndexSlice[0, :])

        # Menambahkan insight dengan dropdown
        with st.expander("**Insight:**"):
            st.write("""
            - Berdasarkan visualisasi, terlihat bahwa pada hari libur nasional, pengguna terdaftar (registered users) cenderung lebih dominan dibandingkan pengguna kasual (casual users) di semua musim.
            - Musim Spring menunjukkan penurunan drastis dalam jumlah pengguna baik terdaftar maupun kasual dibandingkan dengan musim lainnya. Hal ini dapat menunjukkan bahwa kegiatan pada musim Spring mungkin kurang menarik bagi mereka, atau faktor cuaca dan kondisi lain pada musim ini kurang mendukung aktivitas bersepeda bagi mereka.
            """)

# """**Bagian 3: Tab2 - Pertanyaan 2**"""

# Filter by season
seasons = ['All Season', 'Spring', 'Summer', 'Fall', 'Winter']
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
df['season_label'] = df['season'].map(season_map)

def filter_data_by_season(df, selected_season):
    if selected_season == 'All Season':
        return df
    else:
        return df[df['season_label'] == selected_season]

with tab2:
    st.header("Bagaimana perbedaan rata-rata suhu, kelembapan, kecepatan angin, dan penyewaan sepeda pada akhir pekan dan hari kerja selama periode 2011 hingga 2012?")

    # Membuat dua kolom untuk visualisasi dan insight
    col1, col2 = st.columns([2, 1])  # Membuat kolom dengan proporsi 2:1

    with col2:
        # Dropdown untuk filtering berdasarkan musim
        selected_season = st.selectbox("**Filter by**:", seasons, key="tab2_season_select")
        filtered_df = filter_data_by_season(df, selected_season)

    with col1:
        # Menambahkan kolom tipe hari (Weekday/Weekend)
        filtered_df['day_type'] = filtered_df['weekday'].apply(lambda x: 'Weekend' if x in [0, 6] else 'Weekday')

        # Kelompokkan rata-rata data berdasarkan tipe hari
        weather_analysis = filtered_df.groupby('day_type')[['temp', 'hum', 'windspeed', 'cnt']].mean()

        # Plotting
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('Rata-rata Faktor Cuaca dan Penyewaan Sepeda\nBerdasarkan Tipe Hari', fontsize=16, fontweight='bold')

        # Subplot 1: Rata-rata Suhu
        axes[0, 0].bar(weather_analysis.index, weather_analysis['temp'], color='salmon')
        axes[0, 0].set_title('Rata-rata Suhu', fontsize=12, fontweight='bold')
        axes[0, 0].set_ylabel('Suhu (Skala Normalisasi)', fontsize=10, fontweight='bold')

        for i, v in enumerate(weather_analysis['temp']):
            axes[0, 0].text(i, v / 2, f'{v:.3f}', ha='center', va='center', color='white', fontsize=10)

        # Menambahkan garis horizontal untuk setiap tipe hari (Weekday dan Weekend)
        axes[0, 0].axhline(y=weather_analysis.loc['Weekday', 'temp'], color='red', linestyle='--', label='Weekday Avg')
        axes[0, 0].axhline(y=weather_analysis.loc['Weekend', 'temp'], color='blue', linestyle='--', label='Weekend Avg')

        # Subplot 2: Rata-rata Kelembapan
        axes[0, 1].bar(weather_analysis.index, weather_analysis['hum'], color='teal')
        axes[0, 1].set_title('Rata-rata Kelembapan', fontsize=12, fontweight='bold')
        axes[0, 1].set_ylabel('Kelembapan (Skala Normalisasi)', fontsize=10, fontweight='bold')

        for i, v in enumerate(weather_analysis['hum']):
            axes[0, 1].text(i, v / 2, f'{v:.3f}', ha='center', va='center', color='white', fontsize=10)

        # Menambahkan garis horizontal untuk setiap tipe hari (Weekday dan Weekend)
        axes[0, 1].axhline(y=weather_analysis.loc['Weekday', 'hum'], color='red', linestyle='--', label='Weekday Avg')
        axes[0, 1].axhline(y=weather_analysis.loc['Weekend', 'hum'], color='blue', linestyle='--', label='Weekend Avg')

        # Subplot 3: Rata-rata Kecepatan Angin
        axes[1, 0].bar(weather_analysis.index, weather_analysis['windspeed'], color='purple')
        axes[1, 0].set_title('Rata-rata Kecepatan Angin', fontsize=12, fontweight='bold')
        axes[1, 0].set_ylabel('Kecepatan Angin (Skala Normalisasi)', fontsize=10, fontweight='bold')

        for i, v in enumerate(weather_analysis['windspeed']):
            axes[1, 0].text(i, v / 2, f'{v:.3f}', ha='center', va='center', color='white', fontsize=10)

        # Menambahkan garis horizontal untuk setiap tipe hari (Weekday dan Weekend)
        axes[1, 0].axhline(y=weather_analysis.loc['Weekday', 'windspeed'], color='red', linestyle='--', label='Weekday Avg')
        axes[1, 0].axhline(y=weather_analysis.loc['Weekend', 'windspeed'], color='blue', linestyle='--', label='Weekend Avg')

        # Subplot 4: Rata-rata Jumlah Penyewaan
        axes[1, 1].bar(weather_analysis.index, weather_analysis['cnt'], color='gold')
        axes[1, 1].set_title('Rata-rata Penyewaan Sepeda', fontsize=12, fontweight='bold')
        axes[1, 1].set_ylabel('Jumlah Penyewaan Sepeda (Unit)', fontsize=10, fontweight='bold')
        for i, v in enumerate(weather_analysis['cnt']):
            axes[1, 1].text(i, v / 2, f'{v:.0f}', ha='center', va='center', color='white', fontsize=10)

        # Menambahkan garis horizontal untuk setiap tipe hari (Weekday dan Weekend)
        axes[1, 1].axhline(y=weather_analysis.loc['Weekday', 'cnt'], color='red', linestyle='--', label='Weekday Avg')
        axes[1, 1].axhline(y=weather_analysis.loc['Weekend', 'cnt'], color='blue', linestyle='--', label='Weekend Avg')

        # Menambahkan legenda untuk garis rata-rata sekali saja
        handles, labels = axes[0, 0].get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper right', fontsize=12, frameon=True, fancybox=True)

        # Menata layout
        for ax in axes.flat:
            ax.set_xlabel('Tipe Hari', fontsize=10, fontweight='bold')
            ax.grid(axis='y', linestyle='--', alpha=0.7)

        plt.tight_layout(rect=[0, 0, 1, 0.95])

        # Menampilkan plot di Streamlit
        st.pyplot(fig)

    with col2:
        # Menambahkan tabel dengan detail angka yang sudah difilter berdasarkan musim
        st.write("**Detail Rata-rata Faktor Cuaca dan Penyewaan Sepeda Berdasarkan Tipe Hari:**")
        data = {
            'Tipe Hari': ['Weekday', 'Weekend'],
            'Rata-rata Suhu': weather_analysis['temp'].tolist(),
            'Rata-rata Kelembapan': weather_analysis['hum'].tolist(),
            'Rata-rata Kecepatan Angin': weather_analysis['windspeed'].tolist(),
            'Rata-rata Penyewaan Sepeda': weather_analysis['cnt'].tolist()
        }
        df_table = pd.DataFrame(data)
        st.table(df_table.style.hide(axis='index'))

        # Menambahkan insight dengan dropdown
        with st.expander("**Insight:**"):
            st.write("""
            - Rata-rata suhu pada hari kerja cenderung sedikit lebih tinggi dibandingkan dengan akhir pekan, meskipun perbedaannya tidak signifikan.
            - Kelembapan rata-rata lebih rendah pada akhir pekan, yang dapat sedikit meningkatkan kenyamanan untuk aktivitas luar ruang.
            - Kecepatan angin rata-rata lebih tinggi pada akhir pekan dibandingkan dengan hari kerja, yang mungkin mempengaruhi keputusan untuk melakukan aktivitas luar ruang.
            - Jumlah penyewaan sepeda lebih tinggi pada hari kerja, yang kemungkinan mencerminkan penggunaan sepeda sebagai alat transportasi utama untuk bekerja atau sekolah.
            """)


# """**Bagian 4: Tab3 - Analisis Lanjutan**"""

# Load data untuk Analisis Lanjutan
@st.cache_data
def load_hour_data():
    return pd.read_csv('hour.csv')

# Memuat data
df_hour = load_hour_data()

# Filter by season
seasons = ['All Season', 'Spring', 'Summer', 'Fall', 'Winter']
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
df_hour['season_label'] = df_hour['season'].map(season_map)

def filter_data_by_season(df, selected_season):
    if selected_season == 'All Season':
        return df
    else:
        return df[df['season_label'] == selected_season]

# Preprocessing Data
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])
df_hour['hour'] = df_hour['hr']
df_hour['month'] = df_hour['mnth']

with tab3:
    st.header("Analisis Lanjutan: Clustering Berdasarkan Jam Penggunaan Sepeda")

    # Membuat dua kolom untuk visualisasi dan insight
    col1, col2 = st.columns([2, 1])  # Membuat kolom dengan proporsi 2:1

    with col2:
        # Dropdown untuk filtering berdasarkan musim
        selected_season = st.selectbox("**Filter by**:", seasons)
        filtered_df_hour = filter_data_by_season(df_hour, selected_season)

    # Mengelompokkan rata-rata pengguna berdasarkan jam
    hour_avg = filtered_df_hour.groupby('hour')[['casual', 'registered', 'cnt']].mean().reset_index()

    # Menghitung median dan persentil ke-75 dari penggunaan sepeda
    median_usage = np.median(hour_avg['cnt'])
    percentile_75 = np.percentile(hour_avg['cnt'], 75)

    # Menggunakan threshold persentil ke-75
    def classify_hour_usage(row):
        if row['cnt'] > percentile_75:
            return 'High Usage'
        else:
            return 'Low Usage'

    hour_avg['usage_cluster'] = hour_avg.apply(classify_hour_usage, axis=1)

    with col1:
        # Visualisasi bar chart
        fig, ax = plt.subplots(figsize=(12, 8))  # Membuat objek figure dan axes
        bar_width = 0.35
        index = range(len(hour_avg.index))

        ax.bar(index, hour_avg['cnt'], bar_width, color='skyblue', label='Total Usage')
        ax.axhline(y=percentile_75, color='red', linestyle='--', label='Threshold High Usage')

        ax.set_xticks(index)
        ax.set_xticklabels(hour_avg['hour'])
        ax.set_title('Clustering Berdasarkan Jam Penggunaan Sepeda dengan Threshold Optimal\n(Penggabungan Casual dan Registered User)')
        ax.set_xlabel('Jam')
        ax.set_ylabel('Rata-rata Penggunaan (unit)')
        ax.legend(loc='upper left')

        # Menampilkan plot di Streamlit dengan objek figure
        st.pyplot(fig)

        # Menambahkan insight dengan dropdown
        with st.expander("**Insight:**"):
            st.write("""
            - Penggunaan sepeda mencapai puncaknya pada 8 pagi, 5 sore, dan 6 sore, menunjukkan bahwa sepeda banyak digunakan saat jam sibuk untuk pergi dan pulang kerja atau sekolah.
            - Sebagian besar waktu dalam sehari memiliki penggunaan sepeda yang rendah, dengan hanya beberapa jam tertentu yang menunjukkan penggunaan tinggi. Ini menunjukkan ada peluang untuk meningkatkan penggunaan sepeda pada waktu-waktu yang kurang sibuk.
            """)

    with col2:
        # Menampilkan tabel dari DataFrame
        st.write("**Detail Rata-rata Pengguna Berdasarkan Jam:**")
        st.dataframe(hour_avg)

        # Menambahkan catatan pemilihan threshold dengan dropdown
        with st.expander("Dalam analisis lanjutan, threshold persentil ke-75 (quartile 3) dipilih untuk membagi cluster penggunaan sepeda menjadi high usage dan low usage. Hal ini karena:"):
            st.write("""
            - Quartile 3 membantu mengidentifikasi jam-jam dengan penggunaan sepeda yang benar-benar tinggi, yang memberikan wawasan yang lebih baik tentang pola penggunaan sepeda.
            - Rata-rata dan median mungkin tidak cukup untuk tujuan analisis yang lebih mendalam dan dapat terpengaruh oleh outlier.
            - Menggunakan quartile 3 memberikan informasi tentang 25% teratas dari distribusi data, yang lebih berguna dalam memahami variabilitas dan pola penggunaan sepeda.
            """)
