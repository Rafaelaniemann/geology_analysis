```markdown
# geology_analysis (refactor/package)

Pacote refatorado da análise geológica. Objetivo: fornecer um pacote modular, testável e reusável.

Como rodar (local):
1. criar venv e instalar dependências:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. rodar com dados de exemplo:
   python run_analysis.py --campo data_examples/posse_campo_sample.csv --shape data_examples/planos_exemplo.geojson --out resultados

Estrutura:
- src/geology_analysis: módulo principal
- run_analysis.py: script de entrada
- requirements.txt
- data_examples/: exemplos mínimos
- tests/: testes pytest

Licença: MIT
```