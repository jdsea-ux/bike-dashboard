import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Pengaturan halaman (layout wide agar plot lebih jelas)
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Load data
df_jam = pd.read_csv("main_data.csv")
df_hari = pd.read_csv("day_data.csv")

# Pastikan kolom tanggal berformat datetime
df_jam['dteday'] = pd.to_datetime(df_jam['dteday'])
df_hari['dteday'] = pd.to_datetime(df_hari['dteday'])

# Menambahkan sidebar
min_date = df_hari['dteday'].min()
max_date = df_hari['dteday'].max()

with st.sidebar:
    st.title("Filters")
    st.markdown("Use the filters below to change the date range:")
    
    date_range = st.date_input(
        label='Select Date Range',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Mencegah error jika user baru memilih 1 tanggal
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = date_range[0]
    end_date = date_range[0]

# Filter data
df_jam_filtered = df_jam[(df_jam['dteday'] >= pd.to_datetime(start_date)) & (df_jam['dteday'] <= pd.to_datetime(end_date))]
df_hari_filtered = df_hari[(df_hari['dteday'] >= pd.to_datetime(start_date)) & (df_hari['dteday'] <= pd.to_datetime(end_date))]

# Proses data
# Data jam
def group_time(hr):
    if    4 <= hr < 12: return 'Morning'
    elif 12 <= hr < 18: return 'Afternoon'
    elif 18 <= hr < 21: return 'Evening'
    else: return 'Night'

df_jam_filtered['time'] = df_jam_filtered['hr'].apply(group_time)
df_jam_filtered['time'] = pd.Categorical(df_jam_filtered['time'], categories=['Morning', 'Afternoon', 'Evening', 'Night'], ordered=True)

# Buat dataframe agregasi rata-rata
waktu_sewa_df              = df_jam_filtered.groupby(['workingday', 'time'])['cnt'].mean().reset_index()
waktu_sewa_df['Tipe Hari'] = waktu_sewa_df['workingday'].map({0: 'Holiday/Weekend', 1: 'Working Day'})

# Data hari
# Binning Suhu
df_hari_filtered['temp_bin'] = pd.cut(df_hari_filtered['temp'], bins=3, labels=['Cold', 'Mild', 'Hot'])

# Agregasi Cuaca dan Suhu (Melt)
cuaca_sewa_df = df_hari_filtered.groupby('weathersit')[['casual', 'registered']].sum().reset_index()
cuaca_melt    = pd.melt(cuaca_sewa_df, id_vars=['weathersit'], value_vars=['casual', 'registered'], var_name='User Type', value_name='Total')

suhu_sewa_df = df_hari_filtered.groupby('temp_bin')[['casual', 'registered']].sum().reset_index()
suhu_melt = pd.melt(suhu_sewa_df, id_vars=['temp_bin'], value_vars=['casual', 'registered'], var_name='User Type', value_name='Total')

# Menampilkan dashboard
st.title("Bike Sharing Analytics Dashboard")
st.markdown("Analysis of demographic rental trends based on time, weather, and temperature (2011-2012).")
st.divider()

# Visualisasi 1
st.subheader("Bike Rental Patterns: Working Day vs Holiday")

fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=waktu_sewa_df, 
    x='time', 
    y='cnt', 
    hue='Tipe Hari', 
    palette=['#FF0000', '#0000FF'], # Merah: Holiday, Biru: Working Day
    ax=ax1
)
ax1.set_title("Average Bike Rentals: Working Day vs Holiday by Time Group")
ax1.set_xlabel("Time Category")
ax1.set_ylabel("Average Rentals")
st.pyplot(fig1)

with st.expander("Show Analysis"):
    st.write("""
    **Analysis:**
    * On **Working Days** (blue bars), the highest rental peak occurs during the **Evening** (commute home), followed by the **Afternoon**. This shows intensive use of bikes at the end of productive hours as a daily mobility tool.
    * On **Holidays/Weekends** (red bars), the rental peak shifts to the **Afternoon**, followed by the **Evening**. Unlike working days, there is no significant morning surge. This indicates that on holidays, bikes are primarily used for recreational and leisure activities from midday to afternoon.
    """)

st.divider()

# Visualisasi 2
st.subheader("Environmental Impact on Casual vs Registered Users")

kolom1, kolom2 = st.columns(2)

with kolom1:
    st.markdown("#### Total Rentals by Weather")
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.barplot(
        data=cuaca_melt,
        x='weathersit',
        y='Total',
        hue='User Type',
        palette=['#FFD700', '#4B0082'],
        ax=ax2
    )
    ax2.set_xlabel("Weather Condition")
    ax2.set_ylabel("Total Rentals")
    st.pyplot(fig2)

with kolom2:
    st.markdown("#### Total Rentals by Temperature")
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    sns.barplot(
        data=suhu_melt,
        x='temp_bin',
        y='Total',
        hue='User Type',
        palette=['#FFD700', '#4B0082'],
        ax=ax3
    )
    ax3.set_xlabel("Temperature Category")
    ax3.set_ylabel("Total Rentals")
    st.pyplot(fig3)

with st.expander("Show Analysis"):
    st.write("""
    **Analysis:**
    * **Weather Impact:** Rental volume reaches its highest point in **Clear** weather, the main driver of activity for both user types. However, there is a stark contrast in retention when weather deteriorates to **Light Snow**. On a macro scale, the *casual* user data visually vanishes, representing an extreme proportional drop (near zero). Conversely, *registered* users maintain a notable baseline volume, demonstrating a higher functional dependence on the service. Additionally, **Heavy Rain** is completely absent from the dataset, indicating possible service suspension during severe conditions.
    * **Temperature Impact:** There is a positive correlation between temperature and rental volume, with the **Hot** category recording the highest rentals. The **Cold** category records the lowest activity. It is evident that *casual* users strongly avoid cold temperatures, while *registered* users remain active despite a decline, demonstrating their reliance on the service as a daily utility.
    """)