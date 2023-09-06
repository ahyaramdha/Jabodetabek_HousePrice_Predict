import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import streamlit as st

# white background (?)
st.markdown(
    """
    <style>
    body {
        background-color: #f2f7ff; /* Ganti dengan kode warna yang Anda inginkan */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Loaddata
df = pd.read_csv('HargaRumahJabodetabek_clean.csv')
df2 = df

# Sidebar
st.sidebar.title('Menu Page')
page = st.sidebar.selectbox('Select Page', ['Home', 'Dashboard Harga Rumah', 'Prediksi Harga Rumah'])

# Home page
if page == 'Home':
    st.title('Selamat Datang di Website Sederhana Saya!')
    st.header('Analisis Harga Rumah di Jabodetabek')
    st.subheader('Free Prediksi Harga Rumah!')
    st.text('By Ahya Ramdhanitasari')
    st.markdown('<small>Silakan buka menu disamping! (atau klik tanda [>] di kiri atas) </small>', unsafe_allow_html=True)
    st.markdown('<small>Sumber: Kaggle dan rumah123.com (2022)</small>', unsafe_allow_html=True)

    # Sidebar navigation to other pages
    #if st.sidebar.button('Analisis Harga Rumah'):
        #page = 'House Price Analysis'
    #if st.sidebar.button('Peta Interaktif'):
        #page = 'Interactive Map'
    #if st.sidebar.button('Prediksi Harga Rumah'):
        #page = 'Price Prediction'

elif page == 'Dashboard Harga Rumah':
    st.title('Dashboard Harga Rumah di Jabodetabek')
    # Interactive Map
    #st.subheader('Sebaran Harga Rumah')
    df.rename(columns={'Kecamatan': 'Wilayah'}, inplace= True)

    df2 = df[df['Harga'] <= 300000000000]
    total = df2['Harga'].max()
    #total2 = df2['Harga'].min()

    #handling outlier
    def outlier (x):
        sorted(x)
        q1, q3 = x.quantile([0.25, 0.75])
        IQR = q3 - q1
        lwr_bound = q1 - (1.5*IQR)
        upr_bound = q3 + (1.5*IQR)
        return lwr_bound, upr_bound
    
    # apply the algorithm    
    low, high = outlier(df['Harga'])
    low2, high2 = outlier(df['K. Tidur'])
    low3, high3 = outlier(df['K. Mandi'])
    low4, high4 = outlier(df['Luas Bangunan'])
    low5, high5 = outlier(df['Luas Tanah'])
    
    #replacing outlier with upper bound and lower bound value
    df['Harga'] = np.where(df['Harga']>high, high, df['Harga'])
    df['Harga'] = np.where(df['Harga']<low, low, df['Harga'])
        
    df['K. Tidur'] = np.where(df['K. Tidur']>high2, high2, df['K. Tidur'])
    df['K. Tidur'] = np.where(df['K. Tidur']<low2, low2, df['K. Tidur'])
        
    df['K. Mandi'] = np.where(df['K. Mandi']>high3, high3, df['K. Mandi'])
    df['K. Mandi'] = np.where(df['K. Mandi']<low3, low3, df['K. Mandi'])
        
    df['Luas Bangunan'] = np.where(df['Luas Bangunan']>high4, high4, df['Luas Bangunan'])
    df['Luas Bangunan'] = np.where(df['Luas Bangunan']<low4, low4, df['Luas Bangunan'])
        
    df['Luas Tanah'] = np.where(df['Luas Tanah']>high5, high5, df['Luas Tanah'])
    df['Luas Tanah'] = np.where(df['Luas Tanah']<low5, low5, df['Luas Tanah'])
        
    df = df.rename(columns={'long':'lon'})
    #st.dataframe(df)
    df['Ukuran'] = 1

    # Create scatterplot map using Plotly Express
    fig = px.scatter_mapbox(df, lat=df['lat'], lon=df['lon'], center={'lat': -6.21462, 'lon': 106.84513}, zoom=9, color='Harga', labels={'Harga': 'Harga'},size = df['Ukuran'], size_max = 10, color_continuous_scale=px.colors.sequential.Rainbow, width=720, height=500, hover_name="Kota", custom_data=['Wilayah', 'Harga'])
    hovertemplate = '<b>%{customdata[0]}</b><br>Harga: %{customdata[1]:,.2f}'
    fig.update_traces(hovertemplate=hovertemplate)

    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(margin={'r': 0, 't': 50, 'l': 0, 'b': 0})

    # Show the map with color bar if the checkbox is selected
    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3= st.columns(3)
    with col1:
        metric_title = 'Total Data'
        totale = df['title'].count()
        st.metric(metric_title, '{:,}'.format(totale))
    with col2:
        metric_title = 'Median Harga'
        median = df2['Harga'].median()
        total_display = f'{median/1e9:.2f} M'
        st.metric(metric_title, total_display)
    with col3:
        metric_title = 'Max Harga'
        #total = df2['Harga'].max()
        total_display = f'{total/1e9:} M'
        st.metric(metric_title, total_display)

    #st.subheader('Grafik')
    col1, col2 = st.columns(2)
    with col1:
        # Display Distribution of Price using Plotly
        Harga = df2['Harga']
        fig_hist = px.histogram(df2, x='Harga', nbins=500, color_discrete_sequence=['aqua'])
        fig_hist.update_layout( title='Distribusi Harga Rumah di Jabodetabek', xaxis_title='Harga', yaxis_title='Jumlah rumah', xaxis=dict(range=[100000, 75000000000], tickvals=[i*10e9 for i in range(1, 76)], ticktext=[f'{i*10} M' for i in range(1, 76)]))# xaxis_tickformat=',.0f')
        st.plotly_chart(fig_hist, use_container_width=True)
    with col2:
        # Display lagi
        plt.clf()
        df_grouped = df2.groupby('Kota')['Harga'].mean().sort_values(ascending=False)
        fig = px.bar(df_grouped, x=df_grouped.index, y='Harga', title='Rata-rata Harga Rumah per-Kota\ndi Jabodetabek', color_discrete_sequence=['aqua'])
        fig.update_layout(
            xaxis_title='Kota',
            yaxis_title='Harga',
            xaxis=dict(tickangle=30),
            yaxis=dict(
                tickvals=[i*5e9 for i in range(1, 20)], 
                ticktext=[f'{i*5} M' for i in range(1, 20)],
                tickformat=',.0f'))
        st.plotly_chart(fig, use_container_width=True)

    # Display the new table
    st.subheader('Gambaran Data')
    st.text('Berikut ini adalah gambaran data yang dipakai:')
    df.rename(columns={'Kecamatan': 'Wilayah'}, inplace= True)
    st.dataframe(df2[['Kota', 'Wilayah', 'K. Tidur', 'K. Mandi', 'K. Tidur Pembantu', 'K. Mandi Pembantu', 'Lantai', 'Luas Tanah', 'Luas Bangunan', 'Carport', 'furnishing', 'TahunRumah', 'Harga']])

    # hasil analisis
    st.subheader('Hasil Analisis')
    st.text('1. Kota Administratif Jakarta Pusat memiliki rata-rata harga rumah tertinggi di Jabodetabek.')
    st.text('2. Depok merupakan kota dengan rata-rata harga rumah terendah di Jabodetabek')
    st.text('3. Umumnya harga rumah di Jabodetabek dibawah 5 miliar.')

    st.text(' ')
    st.text(' ')
    st.text('Keterangan:')
    st.text('* Satuan Harga pada bar warna (legenda) adalah miliar rupiah. Jadi\njika ditampilkan angka 7B, maka angka tersebut menunjukkan\nharga 7 Miliar Rupiah.')
    st.text('* Dilakukan penanganan pada outlier sebelum dilakukan plot karena nilai\noutlier yang terlalu tinggi, sehingga dapat mengganggu penggambaran\ndan interpretasi data.')
    st.text('* Data yang dipakai pada peta interaktif adalah data yang sudah diatur nilai ekstremnya (outlier), sedangkan data yang dipakai pada grafik menggunakan data asli.')
    st.text('* Banyak data dengan harga yang sangat tinggi melebihi ratusan miliar.\nSetelah melihat ke sumber data (website), itu adalah mansion mewahh\natau apartemen.')
    st.markdown('<small>+ Jika ada tulisan yang terpotong, geser ke kiri. (Pengguna HP)</small>', unsafe_allow_html=True)

elif page == 'Prediksi Harga Rumah':
    st.title('Prediksi Harga Rumah')
    st.write('Author hanya menyediakan prediksi harga rumah pada Kota/wilayah tertentu, berdasarkan kepentingan dan hasil diskusi dari author. Prediksi dilakukan dengan model regresi linear atau regresi ridge tergantung dari jumlah fitur yang harus diprediksi (banyaknya wilayah/distrik).')

    if st.button('Jakarta Timur', key='jaktim'):
        st.write('Click here!: [link](https://jaktimhousepricepredict.streamlit.app/)')
    if st.button('Jakarta Selatan', key='jaksel'):
        st.write('Click here!: [link](https://jakselhousepricepredict.streamlit.app/)')
    if st.button('Bekasi', key='bekasi'):
        st.write('Click here!: [link](https://bekasihousepricepredict.streamlit.app/)')
    if st.button('Depok', key='depok'):
        st.write('Click here!: [link](https://depokhousepricepredict.streamlit.app/)')

    st.text('Terimakasih telah berkunjung ke website ini!')
    st.text('Terbuka untuk pertanyaan dan kerjasama.')
    st.markdown('<small>e-mail: ahyaramdha02@gmail.com</small>', unsafe_allow_html=True)
