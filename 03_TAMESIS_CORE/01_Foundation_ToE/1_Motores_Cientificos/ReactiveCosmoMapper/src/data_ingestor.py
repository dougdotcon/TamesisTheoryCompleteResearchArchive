import os
import pandas as pd
from astroquery.sdss import SDSS
from astropy import coordinates as coords
import astropy.units as u

class DataIngestor:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        print("📡 Iniciando Protocolo de Ingestão de Dados Bariônicos...")

    def get_sparc_data(self):
        """
        Baixa o catálogo mestre do SPARC diretamente.
        Essencial para validar a relação Bariônica Tully-Fisher (BTFR).
        """
        url = "http://astroweb.cwru.edu/SPARC/SPARC_Master_New.csv"
        output_path = os.path.join(self.data_dir, "sparc_master.csv")
        
        if os.path.exists(output_path):
            print(f"ℹ️ Arquivo SPARC já existe em: {output_path}")
            return pd.read_csv(output_path)

        try:
            print(f"⬇️ Baixando SPARC de {url}...")
            df = pd.read_csv(url)
            df.to_csv(output_path, index=False)
            print(f"✅ SPARC carregado e salvo: {len(df)} galáxias prontas para análise entrópica.")
            return df
        except Exception as e:
            print(f"❌ Erro ao baixar SPARC: {e}")
            return None

    def get_sdss_sample_parallel(self, limit=50000, batch_size=5000, max_workers=5):
        """
        Baixa dados do SDSS em paralelo dividindo o céu em faixas de RA (Ascensão Reta).
        Isso evita o uso de OFFSET (lento) e erros de sintaxe.
        """
        output_path = os.path.join(self.data_dir, "sdss_sample.csv")
        
        # Simples verificação de existência
        if os.path.exists(output_path):
             existing_df = pd.read_csv(output_path)
             if len(existing_df) >= limit:
                 print(f"ℹ️ Arquivo SDSS já existe com {len(existing_df)} registros.")
                 return existing_df
        
        from concurrent.futures import ThreadPoolExecutor, as_completed
        import time

        print(f"🚀 Iniciando ingestão paralela via Particionamento de RA...")
        
        # Dividir os 360 graus de RA em N partições
        # Se queremos 50.000 total, e usamos 10 workers (exemplo), cada um busca 5.000.
        # Mas a densidade não é uniforme. Vamos dividir em mais fatias para garantir.
        
        slices = max_workers 
        ra_step = 360.0 / slices
        limit_per_slice = int(limit / slices) + 1000 # Buffer extra

        def fetch_ra_slice(slice_idx):
            ra_min = slice_idx * ra_step
            ra_max = (slice_idx + 1) * ra_step
            
            query = f"""
            SELECT TOP {limit_per_slice} 
                p.objid, p.ra, p.dec, s.z as redshift, 
                p.petroMag_r as mag_r
            FROM PhotoObj AS p
            JOIN SpecObj AS s ON s.bestobjid = p.objid
            WHERE 
                p.type = 3 -- Galáxias
                AND s.z > 0.01 
                AND s.zWarning = 0
                AND p.ra >= {ra_min} AND p.ra < {ra_max}
            """
            try:
                # print(f"  ⬇️ Slice RA {ra_min:.1f}-{ra_max:.1f}...")
                res = SDSS.query_sql(query)
                return res.to_pandas() if res else None
            except Exception as e:
                print(f"  ❌ Erro slice {slice_idx}: {e}")
                return None

        all_dfs = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_slice = {executor.submit(fetch_ra_slice, i): i for i in range(slices)}
            
            for future in as_completed(future_to_slice):
                i = future_to_slice[future]
                try:
                    df_batch = future.result()
                    if df_batch is not None:
                        all_dfs.append(df_batch)
                        print(f"  ✅ Slice {i} (RA {i*ra_step:.0f}-{(i+1)*ra_step:.0f}) processado: {len(df_batch)} galáxias.")
                    else:
                        print(f"  ⚠️ Slice {i} retornou vazio.")
                except Exception as exc:
                    print(f"  ❌ Exceção Slice {i}: {exc}")

        if not all_dfs:
            print("❌ Falha crítica na ingestão.")
            return None

        final_df = pd.concat(all_dfs, ignore_index=True)
        final_df.drop_duplicates(subset=['objid'], inplace=True)
        
        # Truncar para o limite solicitado
        if len(final_df) > limit:
            final_df = final_df.head(limit)
            
        print(f"✅ Ingestão Completa! Total consolidado: {len(final_df)} galáxias.")
        final_df.to_csv(output_path, index=False)
        return final_df
