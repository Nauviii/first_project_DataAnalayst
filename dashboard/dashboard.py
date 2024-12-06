import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("https://raw.githubusercontent.com/Nauviii/first_project_DataAnalyst/main/dashboard/cleaned_bike_day_data.csv")

data = load_data()

# Streamlit Layout
st.title("📊 Dashboard: Analisis Bike Sharing")
st.markdown("""
**Deskripsi**: Dashboard ini berisi visualisasi data dan insight untuk menjawab pertanyaan bisnis terkait layanan penyewaan sepeda.
""")

# Pertanyaan Bisnis
st.header("💡 Pertanyaan Bisnis")
st.markdown("""
1. Bagaimana pengaruh musim terhadap jumlah pelanggan?
2. Bagaimana pengaruh cuaca terhadap jumlah pelanggan?
3. Apakah jumlah pelanggan lebih tinggi pada hari kerja dibandingkan akhir pekan?
""")

# Visualisasi 1: Total penyewaan berdasarkan musim
st.subheader("1️⃣ Total Penyewaan Berdasarkan Musim")
fig1, ax1 = plt.subplots(figsize=(8, 4))
season_data = data.groupby("season")["cnt"].sum().sort_values(ascending=False)
sns.barplot(x=season_data.index, y=season_data.values, ax=ax1, palette="viridis")
ax1.set_title("Total Penyewaan Berdasarkan Musim")
ax1.set_xlabel("Musim")
ax1.set_ylabel("Total Penyewaan")
st.pyplot(fig1)

# Visualisasi 2: Pengaruh cuaca terhadap jumlah pelanggan
st.subheader("2️⃣ Pengaruh Cuaca Terhadap Jumlah Pelanggan")
fig2, ax2 = plt.subplots(figsize=(8, 4))
weather_data = data.groupby("weathersit")["cnt"].mean().sort_values(ascending=False)
sns.barplot(x=weather_data.index, y=weather_data.values, ax=ax2, palette="coolwarm")
ax2.set_title("Rata-rata Penyewaan Berdasarkan Cuaca")
ax2.set_xlabel("Kondisi Cuaca")
ax2.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig2)

# Visualisasi 3: Penyewaan pada musim dan kondisi cuaca
st.subheader("3️⃣ Rata-rata penyewaan sepeda berdasarkan musim dan kondisi cuaca")

# Membuat pivot table untuk rata-rata jumlah penyewaan berdasarkan musim dan kondisi cuaca
pivot_table = data.pivot_table(values="cnt", index="season", columns="weathersit", aggfunc="mean")

# Mengubah pivot table ke dalam format long (melting) untuk mempermudah plotting
melted_data = pivot_table.reset_index().melt(id_vars="season", value_name="avg_rentals", var_name="weathersit")

# Membuat clustered bar chart
fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.barplot(data=melted_data, x="season", y="avg_rentals", hue="weathersit", palette=["#f0e594", "#57b884", "#ffab8d"], ax=ax3)
ax3.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Musim dan Kondisi Cuaca", fontsize=16, fontweight="bold")
ax3.set_xlabel("Musim", fontsize=14)
ax3.set_ylabel("Jumlah Penyewaan (Rata-rata)", fontsize=14)
ax3.legend(title="Kondisi Cuaca", loc="upper right", fontsize=12)
ax3.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig3)

# Visualisasi 4: Proporsi Penyewaan Selama Weekday dan Weekend
st.subheader("4️⃣ Proporsi Penyewaan Selama Weekday dan Weekend")
weekday_sales = data.groupby("day_type").cnt.sum().sort_values(ascending=False).reset_index()
labels = ["Workday", "Weekend"]

# Fungsi untuk menampilkan nilai dan persentase
def values(pct, all_values):
    absolute = int(round(pct / 100. * sum(all_values)))
    return f"{absolute:,}\n({pct:.1f}%)"

colors = ["#f0e594", "#57b884"]

# Membuat pie chart
fig4, ax4 = plt.subplots(figsize=(8, 8))
ax4.pie(
    weekday_sales["cnt"],
    labels=weekday_sales["day_type"],
    autopct=lambda pct: values(pct, weekday_sales["cnt"]),
    startangle=90,
    colors=colors,
    wedgeprops={"edgecolor": "black"}
)

ax4.set_title("Proporsi Penyewaan Sepeda Selama Weekday", fontsize=16)
ax4.legend(labels, loc='best', fontsize=12)
plt.text(0.3, -1.2, f'Total = {weekday_sales["cnt"].sum():,}', fontsize=12, ha='right')
st.pyplot(fig4)

# Visualisasi 5: Rata-rata Penyewaan Berdasarkan Musim, Kondisi Cuaca, dan Tipe Hari
st.subheader("5️⃣ Rata-rata Penyewaan Berdasarkan Musim, Kondisi Cuaca, dan Tipe Hari")

# Menghitung rata-rata jumlah penyewaan berdasarkan kombinasi musim, cuaca, dan hari kerja
summary = data.groupby(["season", "weathersit", "day_type"])["cnt"].mean().reset_index()

# Membuat FacetGrid berdasarkan day_type
plot = sns.FacetGrid(
    summary,
    col="day_type",
    height=6,
    aspect=1.2,
    sharey=True,  # Sumbu y sama untuk memudahkan perbandingan
    palette="coolwarm"
)

# Membuat clustered bar chart pada setiap FacetGrid
plot.map_dataframe(
    sns.barplot,
    x="season",
    y="cnt",
    hue="weathersit",
    ci=None
)

plot.set_axis_labels("Musim", "Jumlah Penyewaan (Rata-rata)")
plot.set_titles("{col_name}")
plot.add_legend(title="Kondisi Cuaca")

# Menambahkan judul global
plt.subplots_adjust(top=0.85)
plot.fig.suptitle(
    "Rata-rata Penyewaan Sepeda Berdasarkan Musim, Kondisi Cuaca, dan Tipe Hari",
    fontsize=16,
    fontweight="bold"
)

st.pyplot(plot.fig)



# Insight
st.header("🔍 Insight")
st.markdown("""
- **Musim Fall** memiliki jumlah penyewaan tertinggi, sedangkan musim Spring memiliki jumlah terendah.
- Cuaca yang cerah (Clear, Few clouds, Partly cloudy) mendorong lebih banyak pelanggan dibandingkan cuaca buruk.
- Hari kerja menunjukkan jumlah penyewaan yang lebih tinggi dibandingkan akhir pekan, menunjukkan penggunaan sepeda untuk aktivitas rutin seperti bekerja.
- Cuaca, Musim, dan Hari kerja sangat berpengaruh terhadap jumlah banyaknya penyewaan
""")

