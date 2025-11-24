"""
Funções para exportar resultados (Excel/CSV).
"""
import os
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def exportar_resultados(df_comparacao: pd.DataFrame, out_dir: str = "resultados"):
    os.makedirs(out_dir, exist_ok=True)
    excel_path = os.path.join(out_dir, "analise_comparativa.xlsx")
    csv_path = os.path.join(out_dir, "resumo_estatistico.csv")
    df_comparacao.to_excel(excel_path, index=False)
    resumo = df_comparacao.groupby(["Plano", "Metodo"]).agg({
        "Erro_Dip": ["mean", "std", "min", "max"],
        "Erro_DipDir": ["mean", "std", "min", "max"],
        "N_Medicoes": "sum"
    })
    resumo.to_csv(csv_path)
    logger.info(f"Exportados: {excel_path}, {csv_path}")