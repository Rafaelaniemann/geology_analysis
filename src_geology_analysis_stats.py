"""
Funções para análise estatística comparativa.
"""
import logging
from typing import Tuple
import pandas as pd
import numpy as np
from scipy import stats

logger = logging.getLogger(__name__)


def analise_estatistica(campo: pd.DataFrame, df_metodos: pd.DataFrame) -> pd.DataFrame:
    """
    Produz um DataFrame comparativo entre medições de campo e resultados de métodos.
    Realiza testes de normalidade e testes apropriados (t pareado ou Wilcoxon) por plano.
    """
    if campo.empty or df_metodos.empty:
        raise ValueError("Dados de entrada vazios")

    resultados = []
    for config in campo["VAR"].unique():
        campo_config = campo[campo["VAR"] == config]
        metodos_config = df_metodos[df_metodos["Config"] == str(config).lower()]

        for metodo in metodos_config["Metodo"].unique():
            metodo_data = metodos_config[metodos_config["Metodo"] == metodo]
            for plano in [1, 2, 3, 4]:
                campo_plano = campo_config[campo_config["plano"] == plano]
                if len(campo_plano) > 0:
                    resultados.append(
                        {
                            "Config": config,
                            "Plano": plano,
                            "Metodo": metodo,
                            "Dip_Campo": campo_plano["dip"].mean(),
                            "DipDir_Campo": campo_plano["Dip_dir"].mean(),
                            "Dip_Metodo": metodo_data["ErroMedio_Dip"].mean(),
                            "DipDir_Metodo": metodo_data["ErroMedio_DipDir"].mean(),
                            "N_Medicoes": len(campo_plano),
                        }
                    )

    if not resultados:
        raise ValueError("Nenhum dado encontrado para comparação")

    df_comparacao = pd.DataFrame(resultados)
    df_comparacao["Erro_Dip"] = (df_comparacao["Dip_Campo"] - df_comparacao["Dip_Metodo"]).abs()
    df_comparacao["Erro_DipDir"] = (df_comparacao["DipDir_Campo"] - df_comparacao["DipDir_Metodo"]).abs()

    # imprimir sumário rápido com testes por plano/metodo
    logger.info("=== RESUMO ESTATÍSTICO (por plano/metodo) ===")
    for plano in df_comparacao["Plano"].unique():
        plano_data = df_comparacao[df_comparacao["Plano"] == plano]
        logger.info(f"Plano {plano}: {len(plano_data)} entradas")
        for metodo in plano_data["Metodo"].unique():
            md = plano_data[plano_data["Metodo"] == metodo]
            if len(md) < 3:
                logger.info(f"  {metodo}: n={len(md)} (insuficiente para testes robustos)")
                continue
            dif = md["Dip_Campo"] - md["Dip_Metodo"]
            # teste de normalidade
            try:
                _, p_norm = stats.shapiro(dif)
            except Exception:
                p_norm = 0.0
            if p_norm > 0.05:
                stat, p_val = stats.ttest_rel(md["Dip_Campo"], md["Dip_Metodo"])
                test_name = "t pareado"
            else:
                try:
                    stat, p_val = stats.wilcoxon(md["Dip_Campo"], md["Dip_Metodo"])
                    test_name = "Wilcoxon"
                except Exception:
                    stat, p_val = (np.nan, np.nan)
                    test_name = "Wilcoxon (falha)"
            logger.info(f"  {metodo}: {test_name}, p={p_val:.4f} (n={len(md)})")

    return df_comparacao