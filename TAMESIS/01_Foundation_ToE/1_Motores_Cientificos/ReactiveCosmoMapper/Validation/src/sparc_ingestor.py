import pandas as pd
import numpy as np
from astropy.constants import G, M_sun, kpc
import astropy.units as u
import os

class SPARCIngestor:
    """
    Tradutor de dados observacionais (SPARC) para o Kernel Entrópico.
    Converte Luminosidade em Massa Bariônica Total.
    """
    
    def __init__(self, filepath='data/SPARC_Master_New.csv'):
        self.filepath = filepath
        # Relação Massa-Luminosidade estelar (Banda 3.6 microns)
        # Lelli et al (2016) sugere 0.5 para disco e 0.7 para bulbo. 
        # Usamos 0.5 como média conservadora para pop. estelar.
        self.Upsilon_disk = 0.5 
        self.Upsilon_bulge = 0.7

    def load_and_process(self):
        """
        Lê o CSV, calcula Massas e prepara o DataFrame para simulação.
        """
        if not os.path.exists(self.filepath):
            print(f"❌ Arquivo não encontrado: {self.filepath}")
            print("⚠️ Baixe manualmente de: http://astroweb.cwru.edu/SPARC/SPARC_Master_New.csv")
            return None

        try:
            raw_df = pd.read_csv(self.filepath)
        except Exception as e:
            print(f"❌ Erro ao ler arquivo SPARC: {e}")
            return None

        print(f"📡 Processando {len(raw_df)} galáxias do SPARC...")
        
        sim_data = []

        # Check required columns to avoid KeyErrors
        required_cols = ['Galaxy', 'LDisk', 'LBulge', 'MHI', 'Reff', 'Vflat', 'D']
        if not all(col in raw_df.columns for col in required_cols):
             print(f"❌ Colunas faltando no CSV. Colunas encontradas: {raw_df.columns}")
             # Fallback for the mock data which might not have all columns or different names depending on creation
             return None

        for _, row in raw_df.iterrows():
            # 1. Cálculo da Massa Estelar (M_star)
            # L_3.6 é dado em 10^9 L_sun
            L_disk = row['LDisk'] * 1e9
            L_bulge = row['LBulge'] * 1e9
            
            M_star = (L_disk * self.Upsilon_disk) + (L_bulge * self.Upsilon_bulge)
            
            # 2. Cálculo da Massa de Gás (M_gas)
            # M_HI é dado em 10^9 M_sun.
            # Multiplicamos por 1.33 para incluir Hélio e metais.
            M_HI = row['MHI'] * 1e9
            M_gas = 1.33 * M_HI
            
            # 3. Massa Bariônica Total (A 'Carga' da Gravidade Entrópica)
            M_baryon = M_star + M_gas
            
            # 4. Raio Característico (Escala)
            # Usamos o Raio Efetivo do Disco como proxy para R_scale
            R_eff = row['Reff'] # kpc
            
            # 5. Velocidade Plana Observada (Para validação)
            V_flat = row['Vflat']

            sim_data.append({
                'name': row['Galaxy'],
                'M_baryon_sol': M_baryon, # Massa solar
                'R_eff_kpc': R_eff,
                'V_flat_obs': V_flat,
                'Distance_Mpc': row['D']
            })

        return pd.DataFrame(sim_data)

    def generate_simulation_inputs(self, df_processed):
        """
        Converte o DataFrame processado em arrays numpy prontos para o ReactiveCosmoMapper.
        """
        if df_processed is None:
            return None, None, None, None

        # Filtra NaNs
        clean_df = df_processed.dropna(subset=['M_baryon_sol', 'V_flat_obs'])
        
        masses = clean_df['M_baryon_sol'].values * M_sun.value # kg
        radii = clean_df['R_eff_kpc'].values * kpc.value # metros
        v_obs = clean_df['V_flat_obs'].values * 1000 # m/s
        names = clean_df['name'].values
        
        return names, masses, radii, v_obs
