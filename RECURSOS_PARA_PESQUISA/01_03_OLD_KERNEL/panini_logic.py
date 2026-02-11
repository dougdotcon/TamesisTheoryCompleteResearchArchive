
def panini_simulation():
    print("--- SIMULAÇÃO: O ALGORITMO DE COMPRESSÃO DE PÂNINI (SHIVA SUTRAS) ---")

    # 1. OS DADOS (Shiva Sutras - O 'Hardware' Sonoro)
    # Lista de strings onde os caracteres representam fonemas.
    # A última letra de cada string é um 'Anubandha' (Marcador Mudo/Terminador).
    # Eles não fazem parte do conjunto fonético real, servem apenas para lógica de slicing.
    shiva_sutras = [
        "a i u N",      # 1. Vogais simples
        "r lx K",       # 2. Vogais líquidas (lx = lring)
        "e o G",        # 3. Ditongos curtos
        "ai au C",      # 4. Ditongos longos
        "h y v r T",    # 5. Semivogais
        "l N",          # 6. Semivogal lateral
        "n m ng n n M", # 7. Nasais (ñ, m, ṅ, ṇ, n)
        "jh bh Y",      # 8. Aspiradas sonoras
        "gh dh dh S",   # 9. Aspiradas sonoras
        "j b g d d S",  # 10. Não-aspiradas sonoras
        "kh ph ch th th c t t V", # 11. Aspiradas surdas
        "k p Y",        # 12. Não-aspiradas surdas
        "s s s R",      # 13. Sibilantes
        "h L"           # 14. Aspirada final
    ]

    print(f"Dataset Carregado: {len(shiva_sutras)} Sutras (Linhas de Código).")

    # 2. A LÓGICA DO KERNEL (Função de Descompressão: Pratyahara)
    def expand_pratyahara(code):
        """
        Decodifica um Pratyahara (ex: 'aC', 'haL') na lista completa de fonemas.
        Lógica:
        1. Encontre a letra inicial no dataset.
        2. Comece a capturar.
        3. Ignore os marcadores finais de cada sutra intermediário.
        4. Pare quando encontrar o marcador final do código.
        """
        if len(code) < 2:
            return []
            
        start_char = code[0] # Letra de início (ex: 'a')
        end_marker = code[-1] # Marcador de fim (ex: 'C')
        
        result_set = []
        capturing = False
        
        print(f"\n>> Decodificando Pratyahara '{code}'...")
        
        found_start = False
        found_end = False
        
        for line in shiva_sutras:
            tokens = line.split()
            marker = tokens[-1]       # O último char é o Anubandha
            content = tokens[:-1]     # O conteúdo são os anteriores
            
            # Se ainda não estamos capturando, procure o início
            if not capturing:
                if start_char in content:
                    capturing = True
                    found_start = True
                    # Começa a capturar a partir do char inicial
                    start_index = content.index(start_char)
                    chunk = content[start_index:]
                    result_set.extend(chunk)
                    
                    # Checagem edge case: se o marcador final está NESTA MESMA linha
                    if marker == end_marker:
                        found_end = True
                        break
            
            # Se já estamos capturando
            else:
                result_set.extend(content)
                # Se encontramos o marcador final nesta linha, PARE.
                if marker == end_marker:
                    found_end = True
                    break
        
        if not found_start:
            print(f"ERRO: Caracter inicial '{start_char}' não encontrado.")
        if not found_end and capturing:
            print(f"ERRO: Marcador final '{end_marker}' não encontrado após o início.")
            
        return result_set

    # 3. TESTES DE COMPRESSÃO (Pratyaharas)
    
    # Teste 1: 'aC' (Todas as Vogais)
    # Deve pegar de 'a' (Sutra 1) até 'C' (Sutra 4)
    # Sutras: 1(a i u N), 2(r lx K), 3(e o G), 4(ai au C)
    # Esperado: a, i, u, r, lx, e, o, ai, au (Marcadores N, K, G, C são ignorados)
    ac_pratyahara = expand_pratyahara("aC")
    print(f"Resultado 'aC' (Vogais): {ac_pratyahara}")
    print(f"Taxa de Compressão: 2 chars -> {len(ac_pratyahara)} fonemas.")

    # Teste 2: 'haL' (Todas as Consoantes)
    # De 'h' (Sutra 5) até 'L' (Sutra 14)
    hal_pratyahara = expand_pratyahara("hL")
    print(f"Resultado 'hL' (Consoantes): {hal_pratyahara}")
    print(f"Taxa de Compressão: 2 chars -> {len(hal_pratyahara)} fonemas.")
    
    # Teste 3: 'aL' (Alfabeto Completo)
    # De 'a' (Sutra 1) até 'L' (Sutra 14)
    al_pratyahara = expand_pratyahara("aL")
    print(f"Resultado 'aL' (Universo): {len(al_pratyahara)} fonemas.")

if __name__ == "__main__":
    panini_simulation()
