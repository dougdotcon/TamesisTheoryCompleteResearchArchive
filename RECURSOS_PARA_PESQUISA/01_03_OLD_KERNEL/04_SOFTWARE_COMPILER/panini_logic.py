
import matplotlib.pyplot as plt

def panini_simulation_visual():
    print("--- SIMULAÇÃO: O ALGORITMO DE COMPRESSÃO DE PÂNINI (COM VISUALIZAÇÃO) ---")

    shiva_sutras = [
        "a i u N", "r lx K", "e o G", "ai au C", "h y v r T", "l N",
        "n m ng n n M", "jh bh Y", "gh dh dh S", "j b g d d S",
        "kh ph ch th th c t t V", "k p Y", "s s s R", "h L"
    ]

    def expand_pratyahara(code):
        if len(code) < 2: return []
        start_char, end_marker = code[0], code[-1]
        result_set = []
        capturing = False
        
        for line in shiva_sutras:
            tokens = line.split()
            marker = tokens[-1]
            content = tokens[:-1]
            
            if not capturing:
                if start_char in content:
                    capturing = True
                    start_index = content.index(start_char)
                    chunk = content[start_index:]
                    result_set.extend(chunk)
                    if marker == end_marker: break
            else:
                result_set.extend(content)
                if marker == end_marker: break
        return result_set

    # Test Cases
    tests = ["aC", "hL", "aL", "yR", "jS"]
    results = {}
    
    print("Calculando Taxas de Compressão...")
    for t in tests:
        expanded = expand_pratyahara(t)
        results[t] = len(expanded)
        print(f"  > Code '{t}' expanded to {len(expanded)} phonemes.")

    # Visualization
    codes = list(results.keys())
    counts = list(results.values())
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Bar Chart: Code Length (2) vs Expanded Length
    bar_width = 0.35
    indices = range(len(codes))
    
    ax.bar(indices, [2]*len(codes), bar_width, label='Code Length (Bytes)', color='gray')
    ax.bar([i + bar_width for i in indices], counts, bar_width, label='Expanded Phonemes (Data)', color='purple')
    
    ax.set_xlabel('Pratyahara Code (Pânini Compression)')
    ax.set_ylabel('Information Density (Phoneme Count)')
    ax.set_title('Ashtadhyayi Compression Algorithm Efficiency')
    ax.set_xticks([i + bar_width/2 for i in indices])
    ax.set_xticklabels(codes)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add text labels
    for i, v in enumerate(counts):
        ax.text(i + bar_width, v + 0.5, str(v), color='black', ha='center')

    output_path = r"d:\TamesisTheoryCompleteResearchArchive\RECURSOS_PARA_PESQUISA\01_03_OLD_KERNEL\imagens\panini_compression_efficiency.png"
    plt.savefig(output_path)
    print(f"Gráfico de Insights salvo em: {output_path}")

if __name__ == "__main__":
    panini_simulation_visual()
