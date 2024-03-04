import streamlit as st
import pandas as pd
import io



#Title
st.title('Dicoding Task')
st.title('Bike Sharing Dataset')
st.caption("Dalam tugas Dicoding kali ini, kami mempelajari dunia data bike-sharing untuk melakukan langkah-langkah penting dalam ilmu data"
        " - pembersihan data, penggabungan data, dan analisis dasar. Kumpulan data yang berisi informasi tentang penyewaan sepeda, "
        "memberikan kesempatan menarik untuk mengungkap pola, tren, dan wawasan yang bisa sangat berharga untuk mengoptimalkan layanan berbagi sepeda..")
#import the dataset
st.subheader('Import the dataset')
code = '''import pandas as pd

df=pd.read_csv("yourdata.csv")'''
st.code(code, language='python')
df_bike = pd.read_csv("data\\day.csv") #import dataset
st.caption('example output from code above :')  
st.write(df_bike) #showing the dataset

#DataCleansing
st.subheader('Delete or remove unused attribute')
code = '''df = df_day.drop('instant', axis=1)'''
st.code(code, language='python')
st.caption('We can see that we have removed the "instant" attribute: ')
df_bike = df_bike.drop('instant', axis=1)
st.write(df_bike)

#Checking the missing values
st.subheader('Check for missing values of each attribute')
code = '''df.isnull().sum()'''
st.code(code, language='python')
df = df_bike.isnull().sum()
st.write(df)

#Check the datatype
st.subheader('Check the datatype of each attribute')
code = '''df.info()'''
st.code(code, language='python')
buffer = io.StringIO()
df_bike.info(buf=buffer)
s = buffer.getvalue()
st.text(s)
st.markdown("Note: Tipe data :blue[`dteday`] ini adalah objek, yang biasanya mengindikasikan bahwa data ini "
            "berisi informasi tanggal atau stempel waktu. Anda mungkin ingin"
            " mempertimbangkan untuk mengonversinya ke tipe data datetime"
            " untuk memudahkan penanganan operasi terkait tanggal.")

df_bike = pd.read_csv("data\\day.csv")

# Changing the datetime datatype
df_bike['datetime'] = pd.to_datetime(df_bike['dteday'])
df_bike['month'] = df_bike['datetime'].dt.strftime('%B')
df_bike['year'] = df_bike['datetime'].dt.year
df_bike['month_num'] = df_bike['datetime'].dt.month
df_bike['number of day'] = df_bike['datetime'].dt.dayofweek
df_bike['day of week'] = df_bike['datetime'].dt.strftime('%A')


# Displaying the DataFrame
st.subheader('DataFrame after changing datetime datatype')
st.write(df_bike.head())
st.markdown("Berikut adalah syntax untuk membagi dteday attribute menjadi attribut-attribut baru: ")
code_for_split = '''df_bike['datetime'] = pd.to_datetime(df_bike['dteday'])
df_bike['month'] = df_bike['datetime'].dt.strftime('%B')
df_bike['year'] = df_bike['datetime'].dt.year
df_bike['month_num'] = df_bike['datetime'].dt.month
df_bike['number of day'] = df_bike['datetime'].dt.dayofweek
df_bike['day of week'] = df_bike['datetime'].dt.strftime('%A')'''
st.code(code_for_split, language='python')

# Displaying additional information
st.subheader('DataFrame Info')
buffer = io.StringIO()
df_bike.info(buf=buffer)
s = buffer.getvalue()
st.text(s)

#Mengdeklarasikan attribut season menjadi string values
st.subheader('Declaring season attribut from int into string values')
code_split_season = '''mapping_seasons = {1 : 'springer',
                   2 : 'summer',
                   3 : 'fall',
                   4 : 'winter'}
df['season'] = df['season'].map(mapping_seasons)
df.tail(20)'''
st.code(code_split_season, language='python')
mapping_seasons = {1 : 'springer',
                   2 : 'summer',
                   3 : 'fall',
                   4 : 'winter'}
df_bike['season'] = df_bike['season'].map(mapping_seasons)
st.write(df_bike.tail(20))


#Percentage of registered and casual users
st.subheader("Showing the percentage of total registered users and casual users")
code_for_averageRegistered = '''df['registered'].sum() / df['cnt'].sum() * 100'''
code_for_averageCasual = '''df_bike['casual'].sum()/df_bike['cnt'].sum()*100'''
st.code(code_for_averageRegistered, language='python')
st.code(code_for_averageCasual, language='python')

# Calculate and display the result
percentage_registered = df_bike['registered'].sum() / df_bike['cnt'].sum() * 100
st.write("Percentage of registered users:", percentage_registered)
percentage_casual = df_bike['casual'].sum()/df_bike['cnt'].sum()*100
st.write("Percentage of casual users:", percentage_casual)

#Visualize weather cond
st.subheader("Visualize of weather conditions affecting the number of bicycle users")
df_bike['weathersit'] = df_bike['weathersit'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})
df_bike['weathersit'] = df_bike['weathersit'].astype('category')
chart_data = df_bike.groupby('weathersit')['cnt'].mean().reset_index()
st.bar_chart(chart_data.set_index('weathersit'))
st.markdown("Note: Kita dapat melihat bahwa cuaca cukup mempengaruhi minat pengguna sepeda, karna pada cuaca cerah peningkatan sewa sepeda cukup tinggi")

#Visualize Season vs Rent
seasonal_usage = df_bike.groupby('season')[['registered', 'casual']].sum().reset_index()
fig, ax = plt.subplots()
ax.bar(seasonal_usage['season'], seasonal_usage['registered'], label='Registered', color='tab:blue')
ax.bar(seasonal_usage['season'], seasonal_usage['casual'], label='Casual', color='tab:orange')
ax.set_xlabel('Season')
ax.set_ylabel('Count')
ax.set_title('Season vs Rent')
ax.legend()
st.pyplot(fig)
st.markdown("Note: Kita dapat melihat bahwa musim mempengaruhi minat pengguna sepeda, karna pada musim gugur peningkatan sewa sepeda cukup tinggi, baik dari registered ataupun casual")



#Count bike that rented in differet year
monthly_counts = df_bike.groupby(by=["month", "year"]).agg({"cnt": "sum"}).reset_index()
fig, ax = plt.subplots(figsize=(10, 10))
sns.lineplot(
    data=monthly_counts,
    x="month",
    y="cnt",
    hue="year",
    palette="rocket",
    marker="o",
    ax=ax,
    sort=False,  # Disable sorting of categorical variable
    hue_order=df_bike['year'].unique(),  # Ensure the order of the years is maintained
    units="year"
)
ax.set_title("Total number of bicycles rented by Month and year")
ax.set_xlabel("Month")
ax.set_ylabel("Total")
ax.legend(title="Year", loc="upper right")
plt.tight_layout()
st.pyplot(fig)
st.markdown('Dari visualisasi menggunakan lineplot, dapat disimpulkan bahwa pada tahun 2012 (yang diwakili oleh angka 1), terjadi peningkatan yang signifikan dalam penyewaan sepeda dari bulan Januari hingga Desember. Puncak penyewaan terjadi pada bulan September, sementara bulan dengan jumlah penyewaan terendah adalah Januari. Sebaliknya, pada tahun 2011, puncak penyewaan sepeda terjadi pada bulan Juni, dengan bulan Januari sebagai bulan dengan penyewaan terendah.')
