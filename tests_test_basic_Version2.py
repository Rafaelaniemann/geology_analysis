import pandas as pd
from geology_analysis.io import carregar_dados
from geology_analysis.stats import analise_estatistica

def test_analise_fluxo_minimo(tmp_path):
    # criar um CSV mínimo
    csv = tmp_path / "posse_campo.csv"
    csv.write_text("VAR,Dip_dir,dip,plano\nA,120,30,1\nA,125,28,1\nB,200,60,4\n")
    campo, df_metodos, planos = carregar_dados(str(csv))
    df_comp = analise_estatistica(campo, df_metodos)
    assert "Erro_Dip" in df_comp.columns
    assert df_comp.shape[0] > 0