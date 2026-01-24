import numpy as np

class SolidUniverseExporter:
    def __init__(self, output_filename="reactive_universe_solid.obj"):
        self.filename = output_filename
        self.vertices = []
        self.lines = []
        
    def load_from_existing_obj(self, input_filename="reactive_universe.obj"):
        """Lê o arquivo de vértices/linhas original"""
        print(f"📂 Lendo dados de {input_filename}...")
        try:
            with open(input_filename, 'r') as f:
                for line in f:
                    parts = line.split()
                    if not parts: continue
                    if parts[0] == 'v':
                        self.vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
                    elif parts[0] == 'l':
                        # Ajustando índices (OBJ começa em 1, Python em 0)
                        self.lines.append([int(parts[1])-1, int(parts[2])-1])
            print(f"✅ Carregados {len(self.vertices)} galáxias e {len(self.lines)} filamentos.")
            return True
        except FileNotFoundError:
            print("❌ Arquivo original não encontrado.")
            return False

    def export_solid(self, galaxy_size=5.0):
        """
        Reescreve o OBJ transformando cada PONTO em um CUBO visível.
        """
        print(f"🔨 Solidificando o Universo em {self.filename}...")
        
        with open(self.filename, 'w') as f:
            f.write(f"# Reactive Universe Solidified Output\n")
            f.write(f"o ReactiveUniverse\n")
            
            # --- 1. Escrever as Galáxias como Cubos ---
            # Um cubo precisa de 8 vértices e 6 faces
            vertex_count = 1
            
            # Offsets para criar um cubo centrado no ponto original
            d = galaxy_size 
            offsets = [
                (-d, -d, -d), (d, -d, -d), (d, d, -d), (-d, d, -d), # Base
                (-d, -d, d), (d, -d, d), (d, d, d), (-d, d, d)      # Topo
            ]
            
            for i, (x, y, z) in enumerate(self.vertices):
                # Escrever os 8 vértices do cubo ao redor da galáxia
                for ox, oy, oz in offsets:
                    f.write(f"v {x+ox:.4f} {y+oy:.4f} {z+oz:.4f}\n")
                
                # Definir as faces do cubo (conectando os 8 vértices)
                base = vertex_count
                # Faces (f v1 v2 v3 v4)
                f.write(f"f {base} {base+1} {base+2} {base+3}\n") # Baixo
                f.write(f"f {base+4} {base+5} {base+6} {base+7}\n") # Cima
                f.write(f"f {base} {base+1} {base+5} {base+4}\n") # Frente
                f.write(f"f {base+1} {base+2} {base+6} {base+5}\n") # Direita
                f.write(f"f {base+2} {base+3} {base+7} {base+6}\n") # Trás
                f.write(f"f {base+3} {base} {base+4} {base+7}\n") # Esquerda
                
                vertex_count += 8

            # --- 2. (Opcional) Filamentos ---
            # O Visualizador do Windows ainda pode ignorar linhas 'l'.
            # Para garantir visualização, escrevemos como linhas, mas dependendo
            # do zoom podem ficar finas. Cubos são a prioridade.
            for v_idx1, v_idx2 in self.lines:
                 # Índices originais não funcionam mais direto pois inflamos os vértices
                 # Vamos conectar os centros dos cubos (aproximadamente)
                 # O centro do cubo 'i' é aproximadamente o vértice base + offset
                 # Mas OBJ 'l' conecta vértices. Vamos conectar o primeiro vértice de cada cubo.
                 
                 idx1_mapped = (v_idx1 * 8) + 1
                 idx2_mapped = (v_idx2 * 8) + 1
                 f.write(f"l {idx1_mapped} {idx2_mapped}\n")

        print(f"🚀 Exportação concluída! Abra '{self.filename}' no Visualizador 3D.")

# --- Execução ---
if __name__ == "__main__":
    converter = SolidUniverseExporter()
    if converter.load_from_existing_obj("reactive_universe.obj"):
        # Tamanho 10.0 garante que sejam visíveis na escala de Megaparsecs
        converter.export_solid(galaxy_size=15.0)
