import seaborn as sb
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np

df=pd.read_excel("clean_BE_df.xlsx")

st.set_page_config(
    page_title="Analiza Lego",
    layout="wide",  
    initial_sidebar_state="expanded")

st.title("Analiza eksploracyjna zestawów lego star wars")
st.markdown("---")



col1, col2 = st.columns([0.20 , 0.80])

with col1:
    st.header("Filtry")
    st.subheader("Dostosuj ponizsze parametry do potrzeb Twojej analizy")

    #wiek
    max_age=int(df["Years"].max())
    min_age=int(df["Years"].min())
    age_range=st.slider("Wybierz wiek zestawów (-1 oznacza jeszcze nie wydane zestawy)",min_value=min_age,max_value=max_age,value=(min_age,max_age),step=1)
    
    

    #liczba klocków
    max_pieces=int(df["Pieces"].max())
    min_pieces=int(df["Pieces"].min())
    number_of_pices=st.slider("Wybierz liczbę elementów",min_value=min_pieces,max_value=max_pieces,value=(min_pieces,max_pieces),step=1)

    #liczba minifigurek
    max_Minifigs=int(df["Minifigs"].max())
    min_Minifigs=int(df["Minifigs"].min())
    number_of_mini_fig=st.slider("Wybierz liczbę minifigurek w zestawie",min_value=min_Minifigs,max_value=max_Minifigs,value=(min_Minifigs,max_Minifigs),step=1)

    #przedział wartosci zestawu
    max_Value=int(df["Value"].max())
    min_Value=int(df["Value"].min())
    value_range=st.slider("Wybierz wartość zestawów",min_value=min_Value,max_value=max_Value,value=(min_Value,max_Value),step=1)

    #dostepnosc w sklepach
    columns_names=df.columns.to_list()
    choice_shop_unique=columns_names[5:10]
    choice_shop=choice_shop_unique+["Wszystkie"]
    chosed_shop=st.selectbox("Wybierz sklepy",options=choice_shop,index=5)

   

    

   
    #aplikacja filtrów

    df_filtered = df.copy()


    df_filtered = df_filtered[
    (df_filtered["Years"] >= age_range[0]) & (df_filtered["Years"] <= age_range[1]) &
    (df_filtered["Pieces"] >= number_of_pices[0]) & (df_filtered["Pieces"] <= number_of_pices[1]) &
    (df_filtered["Minifigs"] >= number_of_mini_fig[0]) & (df_filtered["Minifigs"] <= number_of_mini_fig[1]) &
    (df_filtered["Value"] >= value_range[0]) & (df_filtered["Value"] <= value_range[1])
    ]


    if chosed_shop != "Wszystkie":
        df_filtered = df_filtered[df_filtered[chosed_shop] > 0]


  
    

with col2:
    st.header("Analiza")

    st.subheader("Mean Retail and current market value in years since release.")

    temp = df_filtered.groupby(['Years']).mean(numeric_only=True)[['Value', 'Retail']]
    fig_1,ax=plt.subplots(figsize=(15,6))
    
    ax.scatter(x = temp.index, y = 'Value', data = temp,color="green")
    ax.plot('Value', data=temp,color="green")
    ax.scatter(x = temp.index, y = 'Retail', data = temp,color="purple")
    ax.plot('Retail', data=temp,color="purple")
    ax.legend(loc = 'upper left')
    ax.set_xlabel('Years on market')
    ax.set_ylabel('Mean value in dolars')
    #ax.set_title('Mean Retail and current market value in years since release.')
    ax.set_xticks(temp.index)
    ax.grid(visible=True)
    st.pyplot(fig_1)

    st.subheader("Number of Lego set's Minifigs")

    fig_2, ax = plt.subplots(figsize=(15, 6))
    sns.countplot(data=df_filtered, x='Minifigs', ax=ax,palette='viridis')
    #ax.set_title("Number of Lego set's Minifigs")
    ax.set_ylabel('Counts')
    ax.set_xlabel('Minifigs')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig_2)

    st.subheader("Sets per years since release")

    fig_3, ax = plt.subplots(figsize=(15, 6))
    sns.countplot(data=df_filtered, x='Years', ax=ax, palette='viridis')
    #ax.set_title("Sets per years since release")
    ax.set_ylabel('Counts')
    ax.set_xlabel('Years')
    st.pyplot(fig_3)

    st.subheader("Number of stores where you can buy the set")

    store_cols = ['LEGO', 'Amazon', 'Bricklink', 'StockX', 'eBay']
    available_store_cols = [col for col in store_cols if col in df_filtered.columns]
    counts = (df_filtered[available_store_cols] > 0).sum()
    fig_4, ax = plt.subplots(figsize=(15, 6))
    sns.barplot(x=counts.index, y=counts.values, ax=ax, palette='viridis')
    ax.set_xlabel('Market and set type')
    ax.set_ylabel('Counts')
    #ax.set_title('Number of stores where you can buy the set')

    
    st.pyplot(fig_4)



    
   