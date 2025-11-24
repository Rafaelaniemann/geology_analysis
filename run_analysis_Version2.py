"""Entry-point script. Exemplo de chamada simples."""
import argparse
import logging
from geology_analysis import carregar_dados, analise_estatistica, gerar_visualizacoes, exportar_resultados

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Rodar análise geológica (pacote refatorado).")
    parser.add_argument("--campo", required=True, help="Arquivo de medições (csv ou xlsx)")
    parser.add_argument("--shape", required=False, help="Arquivo geo (shp/geojson) opcional")
    parser.add_argument("--out", default="resultados", help="Pasta de saída")
    args = parser.parse_args()

    campo, df_metodos, planos = carregar_dados(args.campo, args.shape)
    df_comparacao = analise_estatistica(campo, df_metodos)
    gerar_visualizacoes(campo, df_comparacao, planos)
    exportar_resultados(df_comparacao, args.out)
    logger.info("Execução finalizada. Verifique a pasta de resultados.")

if __name__ == "__main__":
    main()