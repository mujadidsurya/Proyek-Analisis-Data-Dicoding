
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


"""# Dashboard Penyewaan Sepeda"""

# Set style seaborn
sns.set(style='dark')

# Menyiapkan data bike_df
bike_df = pd.read_csv("main_data.csv")
bike_df.head()


# Menghapus kolom yang tidak diperlukan
drop_col = ['windspeed', 'hum']

for i in bike_df.columns:
  if i in drop_col:
    bike_df.drop(labels=i, axis=1, inplace=True)

# Mengubah nama judul kolom
bike_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'Tahun',
    'mnth': 'Bulan',
    'weathersit': 'Kondisi Cuaca',
    'cnt': 'Jumlah',
    'season': 'Musim'
}, inplace=True)

# Mengubah angka menjadi keterangan
bike_df['Bulan'] = bike_df['Bulan'].map({
    1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April', 5: 'Mei', 6: 'Juni',
    7: 'Juli', 8: 'Agustus', 9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
})
bike_df['Musim'] = bike_df['Musim'].map({
    1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'
})
bike_df['weekday'] = bike_df['weekday'].map({
    0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'
})


# Menyiapkan daily_rent_df
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dateday').agg({
        'Jumlah': 'sum'
    }).reset_index()
    return daily_rent_df

# Menyiapkan daily_casual_rent_df
def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

# Menyiapkan daily_registered_rent_df
def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df

# Menyiapkan season_rent_df
def create_season_rent_df(df):
    season_rent_df = df.groupby(by='Musim')[['registered', 'casual']].sum().reset_index()
    return season_rent_df

# Menyiapkan monthly_rent_df
def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='Bulan').agg({
        'Jumlah': 'sum'
    })
    ordered_months = [
        'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
        'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

# Menyiapkan weekday_rent_df
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'Jumlah': 'sum'
    }).reset_index()
    return weekday_rent_df



# Membuat komponen filter
min_date = pd.to_datetime(bike_df['dateday']).dt.date.min()
max_date = pd.to_datetime(bike_df['dateday']).dt.date.max()

with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = bike_df[(bike_df['dateday'] >= str(start_date)) &
                (bike_df['dateday'] <= str(end_date))]



# Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)



# Membuat Dashboard secara lengkap

# Membuat judul
st.header('By Mujadid Choirus Surya')

# Membuat jumlah penyewaan harian
st.subheader('Pengguna Sewa Sepeda')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_total = daily_rent_df['Jumlah'].sum()
    st.metric('Total Pengguna', value= daily_rent_total)
    

with col2:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Pengguna Casual', value= daily_rent_casual)
    
with col3:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Pengguna Terdaftar', value= daily_rent_registered)

# Membuat jumlah penyewaan bulanan
st.subheader('Penyewaan Setiap Bulan')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    monthly_rent_df.index,
    monthly_rent_df['Jumlah'],
    marker='o',
    linewidth=2,
    color='tab:blue'
)

for index, row in enumerate(monthly_rent_df['Jumlah']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)



# Membuat jumlah penyewaan berdasarkan musimnya
st.subheader('Penyewaan Setiap Musim Berdasarkan Tipe Pengguna')

fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
    x='Musim',
    y='registered',
    data=season_rent_df,
    label='Registered',
    color='tab:blue',
    ax=ax
)

sns.barplot(
    x='Musim',
    y='casual',
    data=season_rent_df,
    label='Casual',
    color='tab:orange',
    ax=ax
)


for index, row in season_rent_df.iterrows():
    ax.text(index, row['registered'], str(row['registered']), ha='center', va='bottom', fontsize=12)
    ax.text(index, row['casual'], str(row['casual']), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)


# Membuat jumlah penyewaan berdasarkan weekday
st.subheader('Penyewaan Setiap Hari')

fig, ax = plt.subplots(figsize=(15,10))

colors=["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink"]

# Berdasarkan weekday
sns.barplot(
  x='weekday',
  y='Jumlah',
  data=weekday_rent_df,
  color='tab:blue',
  ax=ax)

for index, row in enumerate(weekday_rent_df['Jumlah']):
    ax.text(index, row, str(row), ha='center', va='bottom', fontsize=12)

ax.set_title('Jumlah Penyewa Sepeda Berdasarkan Hari')
ax.set_ylabel("Jumlah Pengguna")
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig)

st.caption('Copyright (c) Mujadid Choirus Surya 2024')