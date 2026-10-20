# Correção — 2026-10-20 (BRT)
A 1ª execução registrou TESTE_FALHOU, mas o motivo foi infraestrutura: o sandbox trocava HOME e o
pytest (instalado em ~/.local) não era encontrado (`No module named pytest`). Nenhum teste rodou.
Reexecução do mesmo `test_step.py`, sem alteração, com PYTHONPATH do site do usuário e rede isolada: 10 passed.
O script foi corrigido (PYTHONPATH no sandbox; erros de módulo/pytest agora contam como ERRO e não são publicados).
Continua sendo só uma checagem de sanidade (não prova; C(γ) ABERTO; exploratório; DISC-DEC-153 mantido).
