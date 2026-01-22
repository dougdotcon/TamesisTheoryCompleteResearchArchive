from data_ingestor import DataIngestor
import os
import sys

# Adiciona o diretório atual ao path para garantir que imports funcionem
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    # Define o diretório de dados relativo à raiz do projeto
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(project_root, "data")
    
    ingestor = DataIngestor(data_dir=data_dir)

    # 1. Dados para Curvas de Rotação (Validação Local)
    print("\n--- Obtendo Dados SPARC ---")
    sparc_df = ingestor.get_sparc_data()

    # 2. Dados para Mapeamento 3D (Validação Cosmológica)
    print("\n--- Obtendo Dados SDSS (Big Data Mode) ---")
    # Usando método paralelo como solicitado
    sdss_df = ingestor.get_sdss_sample_parallel(limit=50000, batch_size=5000, max_workers=5)

    if sparc_df is not None:
        print("\nExemplo de dados SPARC (Massa vs Velocidade):")
        # Colunas úteis: 'Mstar' (Massa Estelar), 'Mgas' (Massa Gás), 'Vflat' (Velocidade Plana)
        try:
            print(sparc_df[['Galaxy', 'Mstar', 'Mgas', 'Vflat']].head())
        except KeyError:
            print("Colunas esperadas não encontradas no SPARC. Colunas disponíveis:", sparc_df.columns)

    if sdss_df is not None:
        print("\nExemplo de dados SDSS:")
        print(sdss_df.head())

if __name__ == "__main__":
    main()
