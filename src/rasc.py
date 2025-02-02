import pandas as pd
from pathlib import Path
import streamlit as st
import folium, requests, re
from streamlit_folium import st_folium
from bs4 import BeautifulSoup

class TratamentoDados():
    def __init__(self, local):
        self.local = local
        self.colunas = ['Data Medicao', 'Evaporaçãodo Piche', 'Insolação Total', 'Precipitação Total', 'Temp. Máx.', 'Temp. Méd. Comp.', 'Temp. Mín.', 'Umidade relativa dor ar', 'Velocidade med. vento']
        
        self.read_data()
        self.read_metadados()


    def read_metadados(self):
        self.metadados = dict()
        with open(self.local, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                # Adiciona linhas aos metadados até encontrar "Data Medicao", que inicia os dados reais
                if linha.startswith("Data Medicao"):
                    break
                linha = linha.strip().split(':')
                if len(linha) == 2:
                    self.metadados[linha[0]] = linha[1].strip()
                  
    def get_meta(self):
        '''self.metadados = pd.DataFrame([self.metadados])

        self.metadados['Latitude'] = pd.to_numeric(self.metadados['Latitude'])
        self.metadados['Longitude'] = pd.to_numeric(self.metadados['Longitude'])
        self.metadados['Altitude'] = pd.to_numeric(self.metadados['Altitude'])
        self.metadados = self.metadados.to_string(index=False)'''
        
        return self.metadados

    def read_data(self):
        self.df = pd.read_csv(self.local,encoding='latin1', sep = ';', decimal = ',',skiprows=13)
        self.df = self.df.drop(self.df.columns[-1], axis=1) #Remove a ultima linha que fica em branco
        self.df.columns = self.colunas #Nomea as colunas

        for col in self.colunas[1:]:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
    def get_dados(self):
        return self.df

    def get_filt(self, cols):
        self.df = self.df.dropna(subset=cols)
        return self.df[cols].copy

    def get_clima_atual(self, cidade):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
        tag = 'span'
        clss = '-bold -gray-dark-2 -font-55 _margin-l-20 _center'


        cidade = cidade.lower().replace(' ', '')
        response = requests.get('https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/170/' + cidade, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        return soup.find(tag, class_=re.compile(clss)).text.strip()


file_path = Path(__file__).parent.parent / "docs" / "BELOHORIZONTE.csv"
tratamento = TratamentoDados(file_path)
dados= tratamento.get_dados()
coord = tratamento.get_meta()
        

st.set_page_config(layout="wide")

with st.container():
    col1, col2 = st.columns([1, 4], vertical_alignment='center')
    with col1:
        st.header('Temperatura atual:')
        col_a, col_b, col_c = st.columns([1, 2, 1])
        with col_b:
            st.header(tratamento.get_clima_atual(coord['Nome']) + 'C')

        st.caption("fonte: https://www.climatempo.com.br")

    with col2:
        
        m = folium.Map(location=[float(coord['Latitude']), float(coord['Longitude'])], zoom_start=12)
        folium.Marker([coord['Latitude'], coord['Longitude']], popup=f"Código Estação: {coord['Codigo Estacao']}<br>Altitude: {coord['Altitude']}",
            tooltip=coord['Nome']).add_to(m)
        st_folium(m, width=1500, height=300)
