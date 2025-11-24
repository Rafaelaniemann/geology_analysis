"""
Visualizações: mapa, boxplots e stereonet.
As funções tentam executar apenas quando as bibliotecas necessárias estão presentes.
"""
import logging
from typing import Optional
import pandas as pd

logger = logging.getLogger(__name__)


def gerar_visualizacoes(campo: pd.DataFrame, df_comparacao: pd.DataFrame, planos: Optional[object]):
    """
    Gera mapas e gráficos e salva arquivos PNG na pasta atual.
    A função é resiliente: se alguma biblioteca/fonts/CRT não estiverem disponíveis,
    ela loga e continua.
    """
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np
        import geopandas as gpd
        import mplstereonet  # may fail in some envs
        from shapely.geometry import Point
    except Exception as e:
        logger.warning(f"Bibliotecas de plot não disponíveis: {e}. Pulando visualizações.")
        return

    sns.set_style("whitegrid")
    sns.set_palette("husl")

    # Boxplots
    try:
        plt.figure(figsize=(12, 6))
        sns.boxplot(x="Plano", y="Erro_Dip", hue="Metodo", data=df_comparacao, showfliers=False)
        plt.title("Distribuição de Erros de Mergulho por Plano e Método")
        plt.savefig("boxplot_erros_dip.png", dpi=300)
        plt.close()

        plt.figure(figsize=(12, 6))
        sns.boxplot(x="Plano", y="Erro_DipDir", hue="Metodo", data=df_comparacao, showfliers=False)
        plt.title("Distribuição de Erros de Direção por Plano e Método")
        plt.savefig("boxplot_erros_dipdir.png", dpi=300)
        plt.close()
        logger.info("Boxplots salvos")
    except Exception as e:
        logger.error(f"Erro ao gerar boxplots: {e}")

    # Stereonet comparativa (se mplstereonet disponível)
    try:
        fig = plt.figure(figsize=(14, 10))
        for i, plano in enumerate([1, 2, 3, 4], start=1):
            ax = fig.add_subplot(2, 2, i, projection="stereonet")
            campo_plano = campo[campo["plano"] == plano]
            if not campo_plano.empty:
                ax.line(campo_plano["Dip_dir"], campo_plano["dip"], "ro", markersize=6, label="Campo")
            for metodo, marker in zip(["DSE_Antes", "DSE_Depois", "RANSAC"], ["s", "^", "d"]):
                md = df_comparacao[(df_comparacao["Plano"] == plano) & (df_comparacao["Metodo"] == metodo)]
                if not md.empty:
                    ax.line(md["DipDir_Metodo"], md["Dip_Metodo"], marker=marker, markersize=6, linestyle="", label=metodo)
            ax.set_title(f"Plano {plano}")
            ax.grid(True)
        fig.legend(loc="upper right")
        plt.tight_layout()
        plt.savefig("stereonet_comparativa.png", dpi=300)
        plt.close()
        logger.info("Stereonet salva")
    except Exception as e:
        logger.warning(f"Stereonet falhou: {e}")

    # Mapa geoespacial se planos fornecidos
    if planos is not None:
        try:
            ax = planos.plot(column="plano", cmap="viridis", alpha=0.6, legend=True)
            # gerar pontos aleatórios dentro dos bounds apenas para representação
            xmin, ymin, xmax, ymax = planos.total_bounds
            import numpy as np
            xs = np.random.uniform(xmin, xmax, len(campo))
            ys = np.random.uniform(ymin, ymax, len(campo))
            import geopandas as gpd
            from shapely.geometry import Point
            campo_gdf = gpd.GeoDataFrame(campo.copy(), geometry=[Point(x, y) for x, y in zip(xs, ys)], crs=planos.crs)
            campo_gdf.plot(ax=ax, column="plano", markersize=50, alpha=0.7)
            ax.figure.savefig("mapa_planos_medicoes.png", dpi=300)
            logger.info("Mapa salvo")
        except Exception as e:
            logger.warning(f"Falha ao gerar mapa: {e}")