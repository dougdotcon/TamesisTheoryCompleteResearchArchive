Perfeito — e isso é **normal**.
O Google Patents **não foi feito para pensar**, foi feito para **consultar**. A marcação, curadoria e inteligência **precisam ser externas**.

Vou te dar um **workflow mínimo, prático, sem frescura**, que resolve exatamente isso.

---

## 1️⃣ Aceite a limitação da plataforma (e use contra ela)

No Google Patents você só faz 3 coisas:

* ler
* baixar
* copiar URL

👉 **É tudo o que você precisa.**
A “marcação como referência” **não acontece lá**.

---

## 2️⃣ Sistema de marcação fora do Google (ultra simples)

### Opção A — CSV (mais rápido possível)

Crie um arquivo:

```
patent_log.csv
```

Colunas mínimas:

```
id, title, year, assignee, class, motivo, status
```

Exemplo real para a Calnetix:

```
US6897587B1,Energy storage flywheel,2003,Calnetix,ENERGY_STORAGE,"Morreu por custo + controle; voltou com materiais modernos","REFERENCIA"
```

Isso já é um **banco de ativos latentes**.

---

## 3️⃣ Taxonomia que realmente importa (não complique)

Use **tags conceituais**, não técnicas.

Sugestão fixa (não invente moda):

* MORREU_CUSTO
* MORREU_CONTROLE
* MORREU_REGULATORIO
* CEDEU_ECOSISTEMA
* REFERENCIA
* TES E_CENTRAL

Uma patente pode ter **mais de uma**.

---

## 4️⃣ Captura mínima de informação (5 minutos por patente)

Quando abrir uma patente boa, capture só isso:

1. **ID** (ex: US6897587B1)
2. **Ano de prioridade**
3. **Por que morreu** (1 frase)
4. **O que mudou desde então** (1 frase)
5. **Por que vale hoje** (1 frase)

Nada além disso.

Se você escreve parágrafo, você está perdendo tempo.

---

## 5️⃣ Se quiser automatizar (mas sem exagero)

Depois que tiver 20–30 linhas no CSV:

* use Python para:

  * agrupar por “morreu por”
  * contar recorrência
  * detectar padrões

Mas **não comece** pelo script.
Comece pelo olho humano.

---

## 6️⃣ Como usar o próprio Google Patents como “bookmark”

Hack simples:

* Copie o **link da patente**
* Cole junto da linha no CSV
* Opcional: salve o PDF local com nome padronizado:

```
2003_Calnetix_Flywheel_MORREU_CUSTO.pdf
```

Pronto. Melhor que qualquer botão de “favoritar”.

---

## 7️⃣ O que a Calnetix representa no seu mapa mental

Ela não é:

* produto
* startup
* oportunidade direta

Ela é:

* **âncora histórica**
* prova de padrão
* ponto de comparação

Toda vez que você encontrar:

* storage mecânico
* sistemas rotativos
* controle magnético

Você pergunta:

> isso é melhor ou pior que Calnetix 2003?

Se for melhor → potencial
Se for igual → redundante
Se for pior → lixo

---

## 8️⃣ Resumo seco

* Google Patents ≠ ferramenta de pensamento
* Marcação é externa
* CSV simples > qualquer software
* Patente boa vira **referência conceitual**, não “favorito”

Você agora está fazendo **curadoria**, não busca.

---

### Próximas perguntas (continuação natural)

**Q1:** Que outros “ativos âncora” além de flywheel eu deveria capturar primeiro?
**Q2:** Como saber quando uma patente vira tese central vs só referência?
**Q3:** Em que momento vale transformar esse CSV em algo vendável?
