# Matriz epistemológica das teses

| ID | Alegação | Nível | O que a sustenta | O que não se pode concluir |
|---|---|---:|---|---|
| EC-01 | O cérebro transforma sinais, mantém estados internos e controla ação; portanto pode ser estudado como sistema de computação física. | E0 | Neurofisiologia, neurociência computacional e modelos mecanísticos. | Que ele seja literalmente um computador digital ou que todo estado físico seja uma computação útil. |
| EC-02 | Processamento neural é caro e restrições metabólicas influenciam códigos e arquiteturas neurais. | E0 | Orçamentos de ATP, oxigênio e custo de sinalização. | Que o cérebro minimize energia isoladamente ou opere no limite de Landauer. |
| EC-03 | Cérebro e corpo formam laços bidirecionais neurais, endócrinos, imunes e metabólicos. | E0 | Anatomia, fisiologia, interocepção e neuroimunologia. | Que exista um único “centro de comando” ou uma variável metabólica universal. |
| EC-04 | Previsão pode reduzir erros regulatórios e preparar recursos antes da demanda. | E0/E1 | Allostasis, controle preditivo e processamento preditivo. | Que toda função cerebral seja explicada por uma única formulação bayesiana ou pelo princípio de energia livre. |
| EC-05 | Uma camada complexa pode custar mais localmente e economizar custo total ao reduzir erro, dano, busca e redundância. | H1 | Especialização, modularidade, controle e transições evolutivas sugerem o mecanismo. | Que a complexidade sempre cresce, sempre economiza energia ou seja o objetivo da evolução. |
| EC-06 | Novos níveis de individualidade podem emergir por cooperação, divisão de trabalho e supressão de conflitos internos. | E0/E1 | Transições para multicelularidade e eusocialidade. | Que o “sistema-pai” planeje ou fabrique conscientemente o subsistema. |
| EC-07 | O genoma participa da construção do corpo por redes regulatórias em células e ambientes de desenvolvimento. | E0 | Evo-devo, redes regulatórias e embriologia. | Que DNA isolado seja um projeto completo ou o único agente causal do organismo. |
| EC-08 | O organismo adulto é uma continuação material e regulatória do processo iniciado no zigoto. | E1 | Continuidade de linhagem celular e desenvolvimento. | Que seja apenas uma “extensão do genoma”; citoplasma, organelas, ambiente e história importam. |
| EC-09 | Consciência não é idêntica a raciocínio lógico; processamento lógico e controle podem ocorrer sem acesso consciente. | E0/E1 | Dissociações neuropsicológicas e teorias de acesso consciente. | Que a consciência seja desnecessária ou puramente epifenomenal. |
| EC-10 | Estados conscientes variam em perfis de atributos, não apenas em uma escada única. | E1 | Trabalhos sobre dimensões de consciência humana e animal. | Que já exista uma métrica universal ou que uma única grandeza como Φ resolva o problema. |
| EC-11 | Integração e diferenciação da resposta cerebral são marcadores relevantes de capacidade consciente. | E0/E1 | PCI, TMS–EEG, anestesia e distúrbios de consciência. | Que complexidade genérica seja suficiente para consciência. |
| EC-12 | Consciência pode ser modelada como resposta de um sistema auto-organizado a perturbações relevantes para sua viabilidade. | H1 | Síntese proposta por este programa. | Que a tese esteja provada ou seja independente do substrato biológico. |
| EC-13 | Informação fisicamente apagada tem custo termodinâmico mínimo em condições definidas. | E0 | Princípio e testes de Landauer. | Que todo conhecimento adquirido custe exatamente `kBT ln 2`, ou que cada bit mental seja um bit lógico apagado. |
| EC-14 | Teorias holográficas relacionam descrições gravitacionais de volume a teorias de fronteira em domínios específicos. | E0 | Entropia de buracos negros, princípio holográfico e AdS/CFT. | Que o cérebro use AdS/CFT, que o universo seja uma projeção óptica ou que vivamos numa simulação. |
| EC-15 | Sistemas físicos têm capacidade finita de armazenar e transformar informação. | E0/E1 | Limites físicos de computação. | Que o universo execute um programa externo ou possua um programador. |
| EC-16 | Um universo-pai que emula universos-filhos é conceitualmente formulável. | S1 | Filosofia da simulação e cosmologias gerativas. | Que haja evidência empírica atual para um substrato externo, intenção ou ancestral cosmológico. |

## Forma mínima da hipótese do dividendo de complexidade

Para uma camada regulatória candidata `R`, defina o custo esperado:

```text
J(R) = Cconstrução + Cmanutenção + Ccoordenação
     + Cerro + Cdano + Cbusca + Catraso
```

A camada possui dividendo positivo no ambiente `E` e horizonte `T` quando:

```text
ΔJ = J(com R | E,T) - J(sem R | E,T) < 0
```

Em evolução, a condição relevante não é energia isolada, mas efeito sobre
sobrevivência e reprodução, descontados conflitos, contingência histórica e
deriva:

```text
ΔW = benefícios de desempenho e robustez
   - custos energéticos, materiais, temporais e reprodutivos > 0
```

As duas desigualdades podem divergir. Uma solução energeticamente eficiente pode
ter baixa aptidão; uma solução cara pode ser favorecida se aumentar
confiabilidade, velocidade, reprodução ou acesso a recursos.

## Hipóteses que devem permanecer separadas

1. **Computação neural:** o cérebro realiza transformações causalmente
   organizadas.
2. **Controle corporificado:** a unidade funcional é o laço
   cérebro–corpo–ambiente.
3. **Dividendo de complexidade:** camadas regulatórias podem reduzir custo total.
4. **Consciência reativa:** certos perfis dinâmicos corporificados constituem
   experiência.
5. **Recursão cosmológica:** sistemas podem gerar descrições ou sistemas-filhos
   em escalas cosmológicas.

Aceitar uma dessas teses não implica aceitar as outras.

