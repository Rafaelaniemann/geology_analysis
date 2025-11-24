# geology_analysis

Um pacote modular para análise comparativa de dados geológicos de campo, métodos de processamento e planos estruturais. Este repositório fornece código reutilizável, exemplos e infraestrutura para executar a análise de forma reprodutível em diferentes máquinas e áreas de estudo.

## Objetivos
- Fornecer uma pipeline end-to-end para carregar medições de campo, comparar com resultados de métodos e gerar estatísticas e visualizações.
- Facilitar a reutilização em outras áreas com parâmetros configuráveis e formato de dados documentado.
- Possibilitar execução local, em containers Docker e integração contínua (CI).

## Conteúdo do repositório
- src/geology_analysis — código-fonte modular (I/O, estatística, viz, export).
- run_analysis.py — script de entrada (CLI).
- data_examples/ — exemplos mínimos de datasets (CSV e GeoJSON).
- requirements.txt — dependências pip.
- tests/ — testes pytest básicos.
- Dockerfile — imagem para execução reprodutível.
- README.md — este arquivo.

## Formas de executar

### 1) Ambiente Python (recomendado)
Usando venv:
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Rodando a análise com dados de exemplo:
```bash
python run_analysis.py --campo data_examples/posse_campo_sample.csv --shape data_examples/planos_exemplo.geojson --out resultados
```

### 2) Usando Conda (recomendado para geoespacial)
Se preferir conda (evita problemas com dependências geoespaciais):
- Crie environment via environment.yml (se disponível):
```bash
conda env create -f environment.yml
conda activate geologia-env
pip install -r requirements.txt   # caso queira pacotes pip extras
```

### 3) Com Docker
Build da imagem:
```bash
docker build -t geologia-analise:latest .
```
Execução (montando volume para resultados):
```bash
docker run --rm -v $(pwd)/resultados:/work/resultados geologia-analise:latest \
  python run_analysis.py --campo data_examples/posse_campo_sample.csv --shape data_examples/planos_exemplo.geojson --out resultados
```

## Entrada esperada (formato dos dados)
- Arquivo de campo (CSV ou XLSX) com colunas mínimas:
  - VAR: identificador de configuração / amostra
  - Dip_dir: direção de mergulho (graus)
  - dip: mergulho (graus)
  - plano: identificador do plano (pode ser numérico ou letra A/B/C/D)
- Shapefile / GeoJSON opcional com geometrias dos planos. Se não houver coluna "plano", a rotina tentará mapear ou atribuir valores fictícios para visualização.

Exemplo mínimo (CSV):
```
VAR,Dip_dir,dip,plano
ConfigA,120,30,1
ConfigB,300,45,2
```

## Saídas
- results/analise_comparativa.xlsx — tabela com métricas por configuração, plano e método.
- results/resumo_estatistico.csv — agregados estatísticos (média, desvio, min, max).
- PNGs de visualização gerados no diretório de execução:
  - boxplot_erros_dip.png
  - boxplot_erros_dipdir.png
  - stereonet_comparativa.png
  - mapa_planos_medicoes.png (se shapefile/geojson fornecido)

## Configuração e extensão
- O comportamento pode ser adaptado alterando:
  - src/geology_analysis/io.py — validação e leitura dos dados.
  - src/geology_analysis/stats.py — testes estatísticos e regras.
  - src/geology_analysis/viz.py — parâmetros de plotagem e export.
- Para reutilizar em outra área, adapte o mapeamento de colunas e os thresholds estatísticos, ou forneça um arquivo de configuração (YAML/JSON) que mapeie nomes de colunas e parâmetros.

## Desenvolvimento
- Testes:
```bash
pytest -q
```
- Lint: configure e rode black/flake8 conforme preferir.
- Estruture mudanças em branches e abra PRs para revisão.

## Continuous Integration
- Há um workflow de exemplo (.github/workflows/ci.yml) que instala dependências e roda os testes em pushes/PRs. Ajuste conforme a política do projeto.

## Licença
- MIT (ver arquivo LICENSE). Sinta-se livre para adaptar e usar em trabalhos acadêmicos ou aplicações industriais — cite conforme apropriado.

## Como citar / publicar
Para garantir reprodutibilidade em publicações:
- Crie um release no GitHub e archive-o no Zenodo para obter um DOI.
- Inclua versão do pacote (src/geology_analysis/__init__.py -> __version__) no seu artigo.

## Contribuindo
- Abra issues para bugs e feature requests.
- Envie PRs pequenas e ative os testes locais.
- Veja CONTRIBUTING.md (se existir) para padrões de commit e revisão.

## Ajuda rápida / Troubleshooting
- Se geopandas ou fiona falharem na instalação, use o ambiente conda/conda-forge:
  conda install -c conda-forge geopandas fiona
- Para problemas de backend do matplotlib (ex.: em servidores sem X), ajuste o backend ou gere imagens sem mostrar interativamente:
  export MPLBACKEND="Agg"
