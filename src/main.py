import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup

import streamlit as st
from streamlit_folium import st_folium
import folium, requests, re

class DadosClimaticos():
    def __init__(self, local):
        self.local = local

        self.read_metadados()
        self.read_dados()

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

    def get_metadados(self):
        return self.metadados
    

    def read_dados(self):
        if 'A' in self.metadados['Codigo Estacao']:
            self.colunas_bd = []
        else:
            self.colunas_bd = ['Data Medicao', 'Evaporaçãodo Piche', 'Insolação Total', 'Precipitação Total', 'Temp. Máx.', 'Temp. Méd. Comp.', 'Temp. Mín.', 'Umidade relativa dor ar', 'Velocidade med. vento']
        
        self.df = pd.read_csv(self.local,encoding='latin1', sep = ';', decimal = ',',skiprows=13)
        self.df = self.df.drop(self.df.columns[-1], axis=1) #Remove a ultima linha que fica em branco
        self.df.columns = self.colunas_bd #Nomea as colunas

        for col in self.colunas_bd[1:]:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

    def get_dados(self):
        return self.df
    
    def get_current_temp(self, cidade):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
        tag = 'span'
        clss = '-bold -gray-dark-2 -font-55 _margin-l-20 _center'


        cidade = cidade.lower().replace(' ', '')
        response = requests.get('https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/170/' + cidade, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        return soup.find(tag, class_=re.compile(clss)).text.strip()

class Dashboard():
    def __init__(self, local):
        self.dados_c = DadosClimaticos(local)
        st.set_page_config(layout="wide")




    def generate_map(self, meta_d):
        m = folium.Map(location=[float(meta_d['Latitude']), float(meta_d['Longitude'])], zoom_start=12)
        folium.Marker([meta_d['Latitude'], meta_d['Longitude']], popup=f"Código Estação: {meta_d['Codigo Estacao']}<br>Altitude: {meta_d['Altitude']}",
            tooltip=meta_d['Nome']).add_to(m)
        st_folium(m, width=1500, height=300)


    def execute(self):
        col1, col2 = st.columns([1, 4], vertical_alignment='center')
        meta_d = self.dados_c.get_metadados()
        with col1:
            
            st.header('Temperatura atual:')
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                st.header(self.dados_c.get_current_temp(meta_d['Nome']) + 'C')

            st.caption("fonte: https://www.climatempo.com.br")


        with col2:
            self.generate_map(meta_d)
     



if __name__ == "__main__":
    file_path = Path(__file__).parent.parent / "docs" / "BELOHORIZONTE.csv"
    app = Dashboard(file_path)
    app.execute()


