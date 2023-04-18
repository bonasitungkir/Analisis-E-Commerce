#Import Library
import streamlit as st 
import numpy as np
import pandas  as pd
import matplotlib.pyplot as plt
import seaborn as sns
#Tampilan awal dan judul
st.markdown("<h1 style='text-align: center;'>Dashboard E-Commerce</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>By Bonatua Harianto Situngkir</h2>", unsafe_allow_html=True)
# Menambahkan latar belakang
st.write('Sebagai perusahaan E-commerce, kita perlu mengevaluasi performa penjualan. Selain itu, kita juga perlu lebih memahami tingkat kepuasan costomer serta persebaran pelanggan kita sehingga kita dapat membuat sebuah strategi pemasaran yang lebih efektif.')

# Menambahkan pertanyaan analisis
st.header('Pertanyaan Analisis:')
st.write('1. Bagaimana performa penjualan di platform e-commerce saya selama periode waktu tertentu? Apakah ada tren penjualan yang menunjukkan kenaikan atau penurunan?')
st.write('2. Apakah ada korelasi antara rating produk dan jumlah penjualan? Apakah produk dengan rating yang lebih tinggi cenderung memiliki penjualan yang lebih banyak?')
st.write('3. Bagaimana persebaran pelanggan di seluruh wilayah? Apakah ada daerah yang menjadi target pasar utama?')
#masukkan dataset
customers_df=pd.read_csv("customers_dataset.csv")
# 10 negara dengan pembeli terbanyak
customer_by_state = customers_df.groupby('customer_city')['customer_unique_id'].nunique()
top_states = customer_by_state.sort_values(ascending=False)[:10]

# Membuat barchart dengan mathplotlib
fig, ax = plt.subplots()
ax.bar(top_states.index, top_states.values)
ax.set_xticklabels(top_states.index, rotation=45)
ax.set_xlabel('State')
ax.set_ylabel('Number of Customers')
ax.set_title('Top 10 States by Customer Count')
# Menampilkan dalam streamlit
st.pyplot(fig)

#data set untuk visualisasi ke -2
order_items_df = pd.read_csv("order_items_dataset.csv")
#permbersihan missing value
order_items_df.drop(order_items_df[order_items_df['freight_value'] == 0].index, inplace=True)
#Visualisasi korelasi antara harga dengan biaya kargo
fig, ax = plt.subplots()
ax.scatter(order_items_df["price"], order_items_df["freight_value"])
ax.set_title("Price vs Freight Value")
ax.set_xlabel("Price")
ax.set_ylabel("Freight Value")
st.pyplot(fig)
#visualisasi ke-3
order_items_df['month_year'] = pd.to_datetime(order_items_df['shipping_limit_date']).dt.to_period('Y')
monthly_data = order_items_df.groupby('month_year').agg({'price' : 'mean'})
monthly_data.index = monthly_data.index.strftime('%Y')
fig, ax = plt.subplots()
ax.plot(monthly_data.index, monthly_data['price'], label='Average Price')
ax.set_xlabel('Year')
ax.set_ylabel('Value')
ax.set_title('Yearly Trend of Price')
ax.legend()
st.pyplot(fig)
#Visualisasi ke-4
fig, ax = plt.subplots()
sns.heatmap(order_items_df.corr(), annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Correlation Matrix")
st.pyplot(fig)
#Visualisasi ke-5
order_payments_df = pd.read_csv("order_payments_dataset.csv")
order_payments_df.drop(order_payments_df[order_payments_df['payment_installments'] == 0].index, inplace=True)
order_payments_df.drop(order_payments_df[order_payments_df['payment_value'] == 0].index, inplace=True)
payment_counts = order_payments_df['payment_type'].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=payment_counts.index, y=payment_counts.values, ax=ax)
ax.set_xlabel('Payment Type')
ax.set_ylabel('Frequency')
ax.set_title('Frequency of Payment Types')
st.pyplot(fig)
#Visualisasi ke-6
order_reviews_df = pd.read_csv("order_reviews_dataset.csv")
score_counts = order_reviews_df['review_score'].value_counts()
labels = ['Positive', 'Negative']
sizes = [score_counts[4] + score_counts[5], score_counts[1] + score_counts[2] + score_counts[3]]
colors = ['lightgreen', 'salmon']
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
ax.set_title('Proportion of Positive and Negative Reviews')
st.pyplot(fig)
#Visualisasi ke-7

# Merge data
merged_df = pd.merge(order_reviews_df, order_items_df, on='order_id')
corr = merged_df['review_score'].corr(merged_df['price'])
fig, ax = plt.subplots()
ax.scatter(merged_df['price'], merged_df['review_score'])
ax.set_xlabel('Price')
ax.set_ylabel('Review Score')
ax.set_title(f'Correlation between Review Score and Price: {corr:.2f}')
st.pyplot(fig)


st.subheader("Trend Penjualan dan korelasi Penjualan dengan biaya angkut")

# First Column
col1, col2 = st.columns(2)

with col1:
    order_items_df['month_year'] = pd.to_datetime(order_items_df['shipping_limit_date']).dt.to_period('Y')
    monthly_data = order_items_df.groupby('month_year').agg({'price' : 'mean'})
    monthly_data.index = monthly_data.index.strftime('%Y')
    fig, ax = plt.subplots()
    ax.plot(monthly_data.index, monthly_data['price'], label='Average Price')
    ax.set_xlabel('Year')
    ax.set_ylabel('Value')
    ax.set_title('Yearly Trend of Price')
    ax.legend()
    st.pyplot(fig)

# Second Column
with col2:
    fig, ax = plt.subplots()
    sns.heatmap(order_items_df.corr(), annot=True, cmap="coolwarm", ax=ax)
    ax.set_title("Correlation Matrix")
    st.pyplot(fig)


# Menambahkan judul pada aplikasi
st.title('Hasil Analisis dan Saran')

# Menampilkan hasil analisis
st.header('Hasil Analisis:')
st.write('1. Dalam melakukan pembayaran, pelanggan biasanya melakukan pembayaran dengan Credit Card dan sangat jarang menggunakan Debit Card. Performa penjualan dari tahun 2016 – 2020 mengalami penurunan, yaitu pada tahun 2016 sampai 2017 mengalami penurunan yang sedikit, kemudian di tahun 2017 sampai 2018 cenderung stabil, namun pada tahun 2018 sampai 2020 mengalami penurunan yang sangat signifikan.')
st.write('2. Rating produk positif sebanyak 77,1 %, sementara rating produk negatif sebanyak 22,9 %. Setelah dikorelasi antara rating produk dengan harga produk ternyata hasilnya Tidak ada korelasi. Tapi terlihat dari data jika rating yang lebih tinggi memiliki penjualan yang lebih banyak.')
st.write('3. 10 wilayah Penjualan terbanyak berada di Sao Paulo, kemudian diikuti oleh Rio de Janeiro, Belo Horizonte, Brasilia, Curitiba, Campinas, Porto Alegre, Salvador, Guarulhos, dan terakhir Sao Bernando do Campo.')

# Menampilkan saran
st.header('Saran:')
st.write('1. Untuk meningkatkan penjualan, kita dapat melakukan beberapa hal seperti menawarkan promosi dan diskon pada metode pembayaran dengan debit card untuk meningkatkan pembelian dengan jenis pembayaran tersebut, dan meningkatkan kualitas layanan pelanggan.')
st.write('2. Meningkatkan kualitas produk dan kualitas layanan pelanggan agar produk kita mendapatkan rating yang baik dan ulasan positif lebih banyak sehingga penjualan semakin meningkat.')
st.write('3. Penjualan terbanyak berada di Sao Paulo, maka wilayah tersebutlah yang menjadi target pasar utama. Untuk itu perlu diberikan pelayanan yang lebih baik lagi. Selain itu, kita juga perlu memastikan produk dapat menjangkau pelanggan di setiap wilayah agar penjualan semakin meningkat.')
