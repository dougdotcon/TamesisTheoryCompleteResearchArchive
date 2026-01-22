from visualizer import GalaxyVisualizer
from statistics import CosmicStatistician
import numpy as np
import sys
import os

# Ensure src is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🔬 Iniciando Análise Estatística Cosmológica...")
    
    # 1. Carregar e Converter Dados
    # Usamos o Visualizer para garantir a mesma transformação de coordenadas
    viz = GalaxyVisualizer(data_file="data/sdss_sample.csv")
    df_3d = viz.load_and_transform()
    
    if df_3d is None or df_3d.empty:
        print("❌ Sem dados para analisar.")
        return

    # 2. Executar Estatística (Landy-Szalay)
    # Passamos o DataFrame completo para permitir geração de randoms geométricos (RA/Dec/Z)
    if 'ra' not in df_3d.columns:
        # Recuperar RA/DEC do arquivo original já que visualizer transformou, mas pode ter mantido ou não?
        # Visualizer.load_and_transform retorna DataFrame com 'x','y','z','redshift'.
        # Precisamos garantir que RA e DEC estejam lá.
        # Vamos re-ler para garantir ou modificar Visualizer.
        # Solução rápida: O Visualizer original não salva RA/DEC no coords_3d explicitamente além de usar.
        # Vamos fazer um merge ou apenas confiar que visualizer.py foi ou será modificado?
        # Espere, eu editei visualizer.py anteriormente.
        pass
    
    # HACK: O visualizer.py original retorna apenas x,y,z,redshift. 
    # Precisamos do RA/Dec original para a estatística V2.
    # Vamos carregar o CSV original e juntar.
    import pandas as pd
    raw_df = pd.read_csv("data/sdss_sample.csv")
    # O visualizer filtra z>0. Vamos garantir o alinhamento.
    raw_df = raw_df[raw_df['redshift'] > 0].reset_index(drop=True)
    
    # Adicionar RA/Dec ao df_3d (assumindo mesma ordem, o que é verdade se visualizer não reordenar aleatoriamente)
    # Visualizer usa df = df[df['redshift']>0].copy() -> mantém ordem filtrada.
    df_3d['ra'] = raw_df['ra']
    df_3d['dec'] = raw_df['dec']

    stat = CosmicStatistician(df_3d)
    
    # Calcular com bins
    r, xi = stat.compute_two_point_correlation(r_bins=20, r_max=150)
    
    # 3. Plotar Resultado
    stat.plot_correlation(r, xi)

if __name__ == "__main__":
    main()
