#!/usr/bin/env python3
"""
Script de Automação: Executa Todas as Simulações do Projeto
Física do Big Bang - Nova Hipótese de Bounce Gravitacional
"""

import os
import sys
import subprocess
import json
from datetime import datetime
import argparse

def executar_simulacao(script_path, descricao, *args):
    """
    Executa uma simulação específica
    """
    print(f"\n{'='*60}")
    print(f"🚀 Executando: {descricao}")
    print('='*60)

    try:
        # Construir comando
        cmd = [sys.executable, script_path] + list(args)

        # Executar
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())

        if result.returncode == 0:
            print(f"✅ {descricao} - Sucesso!")
            print(result.stdout[-500:])  # Últimas 500 linhas
        else:
            print(f"❌ {descricao} - Falhou!")
            print("Erro:", result.stderr[-1000:])

        return result.returncode == 0

    except Exception as e:
        print(f"💥 Erro ao executar {descricao}: {e}")
        return False

def verificar_dependencias():
    """
    Verifica se as dependências estão instaladas
    """
    print("🔍 Verificando dependências...")

    dependencias = [
        'numpy', 'scipy', 'matplotlib', 'json', 'os'
    ]

    dependencias_opcionais = [
        'sklearn', 'pandas', 'plotly'
    ]

    faltando = []
    opcionais_faltando = []

    for dep in dependencias:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            faltando.append(dep)
            print(f"❌ {dep}")

    for dep in dependencias_opcionais:
        try:
            __import__(dep)
            print(f"✅ {dep} (opcional)")
        except ImportError:
            opcionais_faltando.append(dep)
            print(f"⚠️  {dep} (opcional - não encontrado)")

    if faltando:
        print(f"\n💥 Dependências faltando: {', '.join(faltando)}")
        print("Instale com: pip install -r requirements.txt")
        return False

    if opcionais_faltando:
        print(f"\n⚠️  Dependências opcionais faltando: {', '.join(opcionais_faltando)}")
        print("Algumas funcionalidades podem não funcionar.")

    return True

def criar_relatorio_execucao(resultados, tempo_inicio):
    """
    Cria relatório da execução
    """
    tempo_fim = datetime.now()
    duracao = tempo_fim - tempo_inicio

    relatorio = {
        'timestamp_inicio': tempo_inicio.isoformat(),
        'timestamp_fim': tempo_fim.isoformat(),
        'duracao_segundos': duracao.total_seconds(),
        'resultados': resultados,
        'resumo': {
            'total_simulacoes': len(resultados),
            'sucessos': sum(1 for r in resultados.values() if r['sucesso']),
            'falhas': sum(1 for r in resultados.values() if not r['sucesso'])
        }
    }

    # Salvar relatório
    os.makedirs('resultados/relatorios', exist_ok=True)
    timestamp = tempo_inicio.strftime("%Y%m%d_%H%M%S")
    filename = f'resultados/relatorios/relatorio_execucao_{timestamp}.json'

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)

    print(f"\n📋 Relatório salvo em: {filename}")
    return relatorio

def main():
    """
    Função principal
    """
    parser = argparse.ArgumentParser(description='Executar todas as simulações do projeto')
    parser.add_argument('--skip-verificacao', action='store_true',
                       help='Pular verificação de dependências')
    parser.add_argument('--simulacao', choices=['teste', 'completa', 'hipoteses', 'todas'],
                       default='todas', help='Qual simulação executar')

    args = parser.parse_args()

    print("🚀 Física do Big Bang - Executor Automático de Simulações")
    print("=" * 70)
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Diretório: {os.getcwd()}")
    print()

    # Verificar dependências
    if not args.skip_verificacao:
        if not verificar_dependencias():
            print("\n💥 Abortando devido a dependências faltando.")
            sys.exit(1)
    else:
        print("⏭️  Pulando verificação de dependências")

    # Criar diretórios necessários
    os.makedirs('resultados', exist_ok=True)
    os.makedirs('resultados/simulacoes_multiplas', exist_ok=True)
    os.makedirs('resultados/relatorios', exist_ok=True)

    tempo_inicio = datetime.now()
    resultados = {}

    # Definir simulações a executar
    simulacoes = []

    if args.simulacao in ['teste', 'todas']:
        simulacoes.append({
            'script': 'simulacoes/teste_bounce_simples.py',
            'descricao': 'Teste Simples de Bounce',
            'args': []
        })

    if args.simulacao in ['completa', 'todas']:
        simulacoes.append({
            'script': 'simulacoes/simulacao_campo_escalar_bounce.py',
            'descricao': 'Simulação Completa Campo Escalar',
            'args': []
        })

    if args.simulacao in ['hipoteses', 'todas']:
        simulacoes.append({
            'script': 'simulacoes/hipoteses_alternativas.py',
            'descricao': 'Comparação de Hipóteses Alternativas',
            'args': []
        })

    # Executar simulações
    for sim in simulacoes:
        if os.path.exists(sim['script']):
            sucesso = executar_simulacao(
                sim['script'],
                sim['descricao'],
                *sim['args']
            )
            resultados[sim['descricao']] = {
                'sucesso': sucesso,
                'script': sim['script'],
                'timestamp': datetime.now().isoformat()
            }
        else:
            print(f"⚠️  Script não encontrado: {sim['script']}")
            resultados[sim['descricao']] = {
                'sucesso': False,
                'erro': 'Script não encontrado',
                'script': sim['script'],
                'timestamp': datetime.now().isoformat()
            }

    # Criar relatório
    relatorio = criar_relatorio_execucao(resultados, tempo_inicio)

    # Resumo final
    print("\n" + "="*70)
    print("📊 RESUMO DA EXECUÇÃO")
    print("="*70)
    print(f"Total de simulações: {len(resultados)}")
    print(f"Sucessos: {relatorio['resumo']['sucessos']}")
    print(f"Falhas: {relatorio['resumo']['falhas']}")
    print(f"Duração: {relatorio['duracao_segundos']:.1f} segundos")

    if relatorio['resumo']['sucessos'] == len(resultados):
        print("🎉 Todas as simulações executadas com sucesso!")
        status_code = 0
    else:
        print("⚠️  Algumas simulações falharam. Verifique o relatório.")
        status_code = 1

    print("\n💡 Próximos passos:")
    print("   1. Verifique os gráficos gerados na pasta 'resultados/'")
    print("   2. Analise os arquivos JSON para dados detalhados")
    print("   3. Execute 'python scripts/analisar_resultados.py' para análise avançada")
    print("   4. Gere relatório com 'python scripts/gerar_relatorio.py'")

    sys.exit(status_code)

if __name__ == "__main__":
    main()
