"""
I/O utilities: carregamento e validação de dados.
"""
from typing import Optional, Tuple
import os
import logging
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point

logger = logging.getLogger(__name__)


def _ensure_columns(df: pd.DataFrame, required):
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Colunas obrigatórias faltando: {missing}")


def carregar_dados(caminho_campo: str, caminho_shape: Optional[str] = None
                   ) -> Tuple[pd.DataFrame, pd.DataFrame, Optional[gpd.GeoDataFrame]]:
    """
    Carrega arquivo de campo (CSV ou Excel), constrói um DataFrame de 'métodos' (fake
    se não informado) e carrega shapefile/geojson opcionalmente.
    Retorna: campo, df_metodos, planos (ou None)
    """
    # 1. Carregar dados de campo
    if not os.path.exists(caminho_campo):
        raise FileNotFoundError(f"Arquivo de campo '{caminho_campo}' não encontrado!")

    logger.info("Carregando dados de campo...")
    suffix = os.path.splitext(caminho_campo)[1].lower()
    if suffix in [".csv"]:
        campo = pd.read_csv(caminho_campo)
    else:
        campo = pd.read_excel(caminho_campo)

    # validar colunas mínimas
    required = ["VAR", "Dip_dir", "dip", "plano"]
    _ensure_columns(campo, required)

    # normalizar tipos
    campo = campo.copy()
    # mapear planos opcionais que possam vir como letras
    if campo["plano"].dtype == object:
        campo["plano"] = campo["plano"].replace({"A": 1, "B": 2, "C": 3, "D": 4})
    campo["plano"] = pd.to_numeric(campo["plano"], errors="coerce").fillna(0).astype("int8")

    # 2. Construir df_metodos (placeholder se não houver)
    logger.info("Preparando dados de métodos (simulados)...")
    configs = campo["VAR"].astype(str).str.lower().unique()
    metodos = ["DSE_Antes", "DSE_Depois", "RANSAC"]
    dados = {
        "Config": np.repeat(configs, len(metodos)),
        "Metodo": np.tile(metodos, len(configs)),
        "ErroMedio_Dip": np.random.uniform(5, 30, len(configs) * len(metodos)),
        "ErroMedio_DipDir": np.random.uniform(0, 150, len(configs) * len(metodos)),
        "Erro_Combinado": np.random.uniform(10, 100, len(configs) * len(metodos)),
    }
    df_metodos = pd.DataFrame(dados)

    # 3. Carregar shapefile/geojson se fornecido
    planos = None
    if caminho_shape:
        if not os.path.exists(caminho_shape):
            logger.warning(f"Shape/GeoJSON especificado ('{caminho_shape}') não encontrado. Ignorando.")
        else:
            try:
                planos = gpd.read_file(caminho_shape)
                # lidar com geometrias 3D simplificando para 2D se necessário
                if any(getattr(g, "has_z", False) for g in planos.geometry):
                    planos = planos.assign(geometry=planos.geometry.apply(lambda g: Point(g.coords[0][:2]) if g.geom_type == "Point" else g))
                    logger.warning("Geometrias 3D convertidas para 2D")
                # tentar mapear coluna de plano em várias línguas
                plano_col = next((c for c in planos.columns if c.lower() in ("plano", "plane", "layer", "tipo")), None)
                if plano_col:
                    planos["plano"] = planos[plano_col].replace({"A": 1, "B": 2, "C": 3, "D": 4}).fillna(0).astype("int8")
                else:
                    planos["plano"] = np.random.randint(1, 5, size=len(planos)).astype("int8")
            except Exception as e:
                logger.error(f"Erro ao carregar shapefile/geojson: {e}")
                planos = None

    return campo, df_metodos, planos