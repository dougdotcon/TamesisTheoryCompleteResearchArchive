![Source](https://img.shields.io/badge/Fonte-Ashtadhyayi-blue)
![Concept](https://img.shields.io/badge/Conceito-Compiler_/_Formal_Language-cyan)
![Status](https://img.shields.io/badge/Status-Simulacao_Pratyahara-success)

# Decodificação Tamesis: O Compilador Quântico

> *"Pânini (c. 400 a.C.) não descreveu o Sânscrito; ele o codificou. O Ashtadhyayi é o código-fonte de um Compilador de Realidade."*

---

## 1. O ISA (Instruction Set Architecture): Shiva Sutras

Antes de processar linguagem, Pânini definiu o hardware sonoro.
Os **14 Shiva Sutras** não são um alfabeto; são uma **Tabela de Endereçamento de Memória Acústica**.

* **O Hack:** Marcadores mudos (*Anubandhas*) no final de cada grupo.
* **A Lógica:** Permite selecionar grandes grupos de fonemas usando "Slicing" (como em Python).
* **Exemplo:**
  * `a i u N` (Sutra 1)
  * `r lx K` (Sutra 2)
  * `e o G` (Sutra 3)
  * `ai au C` (Sutra 4)
* **O Hack:** Marcadores mudos (*Anubandhas*) no final de cada grupo.
* **A Lógica:** Permite selecionar grandes grupos de fonemas usando "Slicing" (como em Python).
* **Exemplo:**
  * `a i u N` (Sutra 1)
  * `r lx K` (Sutra 2)
  * `e o G` (Sutra 3)
  * `ai au C` (Sutra 4)
  * Código **AC** = Do 'a' inicial até o marcador 'C'. Resultado: Todas as vogais.

---

## 2. O Algoritmo de Compressão: Pratyahara

Pân![Eficiencia Compressao](../assets/panini_compression_efficiency.png)erdas de altíssima densidade.
Regras fonéticas complexas que levariam parágrafos para explicar são reduzidas a 2 ou 3 sílabas.

* `dīrghaḥ` = Torna-se longa.

> **Validação Computacional:**
> Executamos `panini_logic.py` e reproduzimos a função de descompressão.
>
> ```text
> >> Decodificando Pratyahara 'hL'...
> Resultado 'hL' (Consoantes): ['h', 'y', 'v', 'r', 'l', 'n', 'm', 'ng', 'n', 'n', ...]
> Taxa de Compressão: 2 chars -> 34 fonemas.
> ```

---

## 3. Metalinguagem e Recursão (Paribhasha)

O sistema possui "Self-Healing" e resolução de conflitos (Bug Fixing).

**Regra 1.4.2:** *Vipratishedhe param karyam.*

* **Tradução Dev:** "Em caso de conflito de regras (Race Condition), execute a regra definida *mais tarde* no código."
* Isso é **Herança e Sobrescrita (Override)**. O sistema é Orientado a Objetos: Classes Filhas sobrescrevem Classes Pai.

---

## 4. O Conceito de NULL (Lopa)

Pânini inventou o conceito de **Zero Operacional**.

* **Sutra:** *Adarsanam lopah.* ("A não-visibilidade é chamada de Lopa").
* **Engenharia:** Um elemento pode ser deletado da string de saída, mas sua **função lógica** permanece ativa na memória, afetando operações subsequentes.
* É um *Null Pointer* que carrega tipo e metadados.

---

## 5. Veredito Final

O *Ashtadhyayi* prova que a civilização védica operava com **Linguagens Formais Livres de Contexto** (Chomsky Type 2).
Eles tinham a Ciência da Computação necessária para programar os Mantras (Software) que controlavam os Vimanas (Hardware).

**A Pilha Completa:**

1. **Hardware:** Vimana (Metalurgia/MHD).
2. **OS:** Samkhya (Dual-Core).
3. **Compilador:** Pânini (Regras de Sintaxe/Vibração).
4. **User Code:** Mantra (Comandos de Voz).
