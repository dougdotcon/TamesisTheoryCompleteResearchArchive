# Papéis, cegamento e governança

- **Operador:** executa a bancada e registra desvios.
- **Custodiante:** guarda setpoints, rótulos e originais.
- **Analista de calibração:** desenvolve o modelo permitido.
- **Analista cego:** prediz sem temperatura verdadeira.
- **Coordenador:** mantém protocolo, proveniência, hashes e decisões.

Testar leakage em nomes, diretórios, timestamps, metadata, ordem, tamanho de
arquivo, logs, imagens e comentários. O analista cego não recebe caderno do
operador nem pode consultar o custodiante por sample ID. Sobreposição de papéis
é registrada como limitação.

Todo desvio recebe ID, data, autor, motivo, dados afetados e decisão de validade.

