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

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("day.csv")
    return df

df = load_data()

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

# Main dashboard content
st.title("Proyek Analisis Data: Bike Sharing Dataset")

# Add Tabs
tab1, tab2, tab3 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Analisis Lanjutan"])

# Tab for Pertanyaan 1
with tab1:
    st.header("Bagaimana distribusi rata-rata pengguna kasual dan terdaftar pada hari libur nasional berdasarkan musim?")

    # Membuat dua kolom untuk visualisasi dan insight
    col1, col2 = st.columns([2, 1])  # Membuat kolom dengan proporsi 2:1

    with col1:
        # Memetakan nama musim
        season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
        df['season_label'] = df['season'].map(season_map)

        # Filter data hari libur nasional
        holiday_df = df[df['holiday'] == 1]

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
            'Season': ['Fall', 'Spring', 'Summer', 'Winter'],
            'Casual Users': [2207, 306, 1487, 907],
            'Registered Users': [3501, 1381, 3423, 3119]
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

# Tab for Pertanyaan 2
with tab2:
    st.header("Bagaimana perbedaan rata-rata suhu, kelembapan, kecepatan angin, dan penyewaan sepeda pada akhir pekan dan hari kerja selama periode 2011 hingga 2012?")

    # Membuat dua kolom untuk visualisasi dan insight
    col1, col2 = st.columns([2, 1])  # Membuat kolom dengan proporsi 2:1

    with col1:
        # Menambahkan kolom tipe hari (Weekday/Weekend)
        df['day_type'] = df['weekday'].apply(lambda x: 'Weekend' if x in [0, 6] else 'Weekday')

        # Kelompokkan rata-rata data berdasarkan tipe hari
        weather_analysis = df.groupby('day_type')[['temp', 'hum', 'windspeed', 'cnt']].mean()

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

        # Menambahkan tabel dengan detail angka
        st.write("**Detail Rata-rata Faktor Cuaca dan Penyewaan Sepeda Berdasarkan Tipe Hari:**")
        data = {
            'Tipe Hari': ['Weekday', 'Weekend'],
            'Rata-rata Suhu': [0.500, 0.483],
            'Rata-rata Kelembapan': [0.630, 0.624],
            'Rata-rata Kecepatan Angin': [0.190, 0.193],
            'Rata-rata Penyewaan Sepeda': [4551, 4390]
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

# Tab for Analisis Lanjutan
with tab3:
    st.header("Analisis Lanjutan: Clustering Berdasarkan Musim dan Tipe Hari")

    # Membuat dua kolom untuk visualisasi dan insight
    col1, col2 = st.columns([2, 1])  # Membuat kolom dengan proporsi 2:1

    with col1:
        # Tahap 1: Membuat dataset berdasarkan data yang diberikan
        season_data = {
            "season_label": ["Fall", "Spring", "Summer", "Winter"],
            "casual_avg": [2207.0, 306.43, 1486.5, 906.67],
            "registered_avg": [3500.75, 1381.43, 3422.75, 3118.67],
        }

        day_type_data = {
            "day_type": ["Weekday", "Weekend"],
            "temp_avg": [0.500444, 0.482833],
            "hum_avg": [0.629621, 0.623610],
            "windspeed_avg": [0.189651, 0.192559],
            "cnt_avg": [4550.566219, 4389.685714],
        }

        season_df = pd.DataFrame(season_data)
        day_type_df = pd.DataFrame(day_type_data)

        # Tahap 2: Melakukan clustering manual berdasarkan rata-rata pengguna kasual dan terdaftar
        def classify_season(row):
            if row['casual_avg'] > 1500 and row['registered_avg'] > 3000:
                return 'High Usage'
            else:
                return 'Low Usage'

        season_df['usage_cluster'] = season_df.apply(classify_season, axis=1)

        def classify_day_type(row):
            if row['cnt_avg'] > 4500:
                return 'High Usage'
            else:
                return 'Low Usage'

        day_type_df['usage_cluster'] = day_type_df.apply(classify_day_type, axis=1)

        # Tahap 3: Visualisasi clustering berdasarkan musim
        fig1, ax1 = plt.subplots(figsize=(12, 8))
        bar_width = 0.35  # Lebar bar
        index = range(len(season_df['season_label']))  # Index bar untuk kategori musim

        # Bar chart untuk casual_avg
        ax1.bar(index, season_df['casual_avg'], bar_width, label='Casual Average', color='steelblue')

        # Bar chart untuk registered_avg
        ax1.bar([i + bar_width for i in index], season_df['registered_avg'], bar_width, label='Registered Average', color='darkorange')

        # Menambahkan garis horizontal untuk memisahkan clustering
        threshold_registered = 3000  # Threshold untuk registered_avg
        threshold_casual = 1500  # Threshold untuk casual_avg

        ax1.axhline(y=threshold_registered, color='red', linestyle='--', label='Threshold Registered Avg')
        ax1.axhline(y=threshold_casual, color='green', linestyle='--', label='Threshold Casual Avg')

        # Menambahkan label, judul, dan legenda
        ax1.set_xticks([i + bar_width / 2 for i in index])
        ax1.set_xticklabels(season_df['season_label'])
        ax1.set_title('Clustering Musim Berdasarkan Rata-rata Pengguna', fontsize=14)
        ax1.set_xlabel('Musim', fontsize=12)
        ax1.set_ylabel('Rata-rata Pengguna', fontsize=12)
        ax1.legend(loc='upper left')

        # Menampilkan plot di Streamlit
        st.pyplot(fig1)

        # Tahap 4: Visualisasi clustering berdasarkan tipe hari
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.barplot(x='day_type', y='cnt_avg', hue='usage_cluster', data=day_type_df, palette='coolwarm', ax=ax2)

        # Menambahkan garis horizontal untuk memisahkan clustering
        threshold = 4500  # Threshold untuk clustering
        ax2.axhline(y=threshold, color='red', linestyle='--', label='Threshold High Usage')

        # Menambahkan label, judul, dan legenda
        ax2.set_title('Clustering Tipe Hari Berdasarkan Rata-rata Penyewaan Sepeda', fontsize=14)
        ax2.set_xlabel('Tipe Hari', fontsize=12)
        ax2.set_ylabel('Rata-rata Penyewaan Sepeda', fontsize=12)
        ax2.legend(loc='upper right')

        # Menampilkan plot di Streamlit
        st.pyplot(fig2)

    with col2:

        # Menambahkan tabel dengan detail angka
        st.write("**Detail Clustering Berdasarkan Musim:**")
        season_table = {
            'Musim': season_df['season_label'],
            'Casual Users Avg': season_df['casual_avg'].astype(int),
            'Registered Users Avg': season_df['registered_avg'].astype(int),
            'Usage Cluster': season_df['usage_cluster']
        }
        season_df_table = pd.DataFrame(season_table)
        st.table(season_df_table.style.hide(axis='index'))

        st.write("**Detail Clustering Berdasarkan Tipe Hari:**")
        day_type_table = {
            'Tipe Hari': day_type_df['day_type'],
            'Rata-rata Suhu': day_type_df['temp_avg'].round(3),
            'Rata-rata Kelembapan': day_type_df['hum_avg'].round(3),
            'Rata-rata Kecepatan Angin': day_type_df['windspeed_avg'].round(3),
            'Rata-rata Penyewaan Sepeda': day_type_df['cnt_avg'].astype(int),
            'Usage Cluster': day_type_df['usage_cluster']
        }
        day_type_df_table = pd.DataFrame(day_type_table)
        st.table(day_type_df_table.style.hide(axis='index'))

        # Menambahkan insight dengan dropdown
        with st.expander("**Insight:**"):
            st.write("""
        - Clustering berdasarkan musim menunjukkan bahwa Fall dan Summer termasuk dalam kategori 'High Usage' karena memiliki rata-rata pengguna kasual dan terdaftar yang tinggi.
        - Musim Spring dan Winter masuk dalam kategori 'Low Usage' dengan rata-rata pengguna kasual dan terdaftar yang lebih rendah.
        - Pembagian cluster untuk pengguna terdaftar (registered) ditentukan pada batas 3000, sedangkan untuk pengguna kasual (casual) ditentukan pada batas 1500.
        - Clustering berdasarkan tipe hari menunjukkan bahwa hari kerja (Weekday) memiliki rata-rata penyewaan sepeda yang lebih tinggi dibandingkan akhir pekan (Weekend), mencerminkan penggunaan sepeda sebagai alat transportasi utama.
        - Akhir pekan memiliki rata-rata kecepatan angin yang sedikit lebih tinggi dibandingkan hari kerja, yang dapat mempengaruhi keputusan untuk melakukan aktivitas luar ruang.
        - Pembagian cluster untuk penyewaan sepeda ditentukan pada batas 4500.
        """)
