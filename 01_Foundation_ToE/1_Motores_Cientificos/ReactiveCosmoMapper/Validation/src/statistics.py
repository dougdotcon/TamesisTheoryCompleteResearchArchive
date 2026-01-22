from astropy.cosmology import Planck15
from astropy.coordinates import SkyCoord
from astropy import units as u
import numpy as np
from scipy.spatial import cKDTree
import matplotlib.pyplot as plt

class CosmicStatistician:
    def __init__(self, data_df):
        """
        data_df: DataFrame com colunas 'x', 'y', 'z' (Mpc) 
                 E 'ra', 'dec', 'redshift' para geometria.
        """
        self.data_df = data_df
        # Extract numpy arrays for computation
        self.data_pos = data_df[['x', 'y', 'z']].values
        self.n_galaxies = len(data_df)
        print(f"📉 CosmicStatistician V2 (Geometry-Aware) inicializado com {self.n_galaxies} galáxias.")
        
    def generate_randoms_geometry_aware(self, multiplier=2):
        """
        Gera randômicos respeitando os limites de RA, Dec e Redshift dos dados reais.
        Isso reproduz a geometria de cone/fatia do SDSS, corrigindo a densidade RR.
        """
        print(f"🎲 Gerando {self.n_galaxies * multiplier} pontos randômicos (Geometria Corrigida)...")
        
        # 1. Determinar limites da pesquisa (Bounding Box Angular)
        ra_min, ra_max = self.data_df['ra'].min(), self.data_df['ra'].max()
        dec_min, dec_max = self.data_df['dec'].min(), self.data_df['dec'].max()
        z_min, z_max = self.data_df['redshift'].min(), self.data_df['redshift'].max()

        # 2. Gerar uniformemente no espaço angular e redshift
        # Nota: Idealmente, randoms de z devem seguir a "Selection Function" N(z) suavizada.
        # Aqui, usamos uniforme em z como aproximação de primeira ordem solicitada.
        rand_ra = np.random.uniform(ra_min, ra_max, self.n_galaxies * multiplier)
        rand_dec = np.random.uniform(dec_min, dec_max, self.n_galaxies * multiplier)
        rand_z = np.random.uniform(z_min, z_max, self.n_galaxies * multiplier)

        # 3. Converter para Cartesiano (Usando a mesma cosmologia)
        # Requer astropy (importado acima)
        # O processamento em vetor é rápido.
        
        # Calcular distâncias comoveis
        distances = Planck15.comoving_distance(rand_z)
        
        c = SkyCoord(
            ra=rand_ra * u.degree, 
            dec=rand_dec * u.degree, 
            distance=distances
        )
        
        cartesian = c.cartesian
        randoms_xyz = np.column_stack([
            cartesian.x.value,
            cartesian.y.value,
            cartesian.z.value
        ])
        
        return randoms_xyz

    def compute_two_point_correlation(self, r_bins=20, r_max=200):
        """
        Calcula xi(r) usando o estimador de Landy-Szalay.
        """
        print("🧮 Calculando Função de Correlação V2 (Geometry-Aware)...")
        
        # Gerar Randoms com geometria correta
        randoms = self.generate_randoms_geometry_aware()
        
        # Árvores KD para busca rápida
        print("   - Construindo KD-Trees...")
        tree_data = cKDTree(self.data_pos)
        tree_random = cKDTree(randoms)
        
        # Definir bins logarítmicos
        bins = np.logspace(np.log10(5), np.log10(r_max), r_bins + 1)
        centers = (bins[:-1] + bins[1:]) / 2
        
        # Normalização
        nD = len(self.data_pos)
        nR = len(randoms)
        norm_DD = 2.0 / (nD * (nD - 1))
        norm_RR = 2.0 / (nR * (nR - 1))
        norm_DR = 1.0 / (nD * nR)
        
        def count_pairs(tree1, tree2, r_bins):
            return np.diff(tree1.count_neighbors(tree2, r_bins))

        print("   - Contando pares DD...")
        DD = count_pairs(tree_data, tree_data, bins) * norm_DD
        
        print("   - Contando pares RR...")
        RR = count_pairs(tree_random, tree_random, bins) * norm_RR
        
        print("   - Contando pares DR...")
        DR = count_pairs(tree_data, tree_random, bins) * norm_DR
        
        # Estimador Landy-Szalay
        valid_mask = RR > 0
        xi = np.zeros_like(DD)
        xi[valid_mask] = (DD[valid_mask] - 2*DR[valid_mask] + RR[valid_mask]) / RR[valid_mask]
        
        return centers, xi

    def plot_correlation(self, r, xi):
        plt.figure(figsize=(10, 6))
        
        # Lei de Potência Teórica (Lambda-CDM aprox.)
        # xi(r) = (r / r0)^(-gamma), r0~5 Mpc, gamma~1.8
        # Filtrar r onde r > 0 para evitar erro no log
        r_safe = r[r > 0]
        xi_theory = (r_safe / 5.0)**(-1.77) # Gamma ~ 1.77 é o valor clássico do SDSS
        
        # Plot apenas onde xi > 0 para loglog (clustering positivo)
        # Pontos negativos indicam anti-clustering (voids), comuns em r grande
        mask = xi > 0
        
        plt.loglog(r[mask], xi[mask], 'o-', label='Reactive Universe (SDSS Data)', color='orange', alpha=0.8)
        plt.loglog(r_safe, xi_theory, 'k--', label='Standard Model Prediction (Power Law)', alpha=0.5)
        
        plt.xlabel('Separação r (Mpc)')
        plt.ylabel(r'$\xi(r)$ (Probabilidade de Clustering)')
        plt.title('Teste de Turing Cosmológico: Entropia vs Matéria Escura')
        plt.legend()
        plt.grid(True, which="both", ls="-", alpha=0.2)
        
        output_file = "correlation_function_analysis.png"
        plt.savefig(output_file)
        print(f"✅ Gráfico salvo: {output_file}")
