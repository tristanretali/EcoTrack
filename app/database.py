import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


def normalize_data(df_dechet, df_flux_CO2):

    # Partie du traitement du dataset contenant les déchets par région
    df_normalize_dechet = df_dechet.drop(columns=["C_REGION", "L_REGION"])
    df_normalize_dechet = df_normalize_dechet[df_normalize_dechet["ANNEE"] == 2021]
    df_normalize_dechet["TONNAGE_T"] = (
        df_normalize_dechet["TONNAGE_T"].str.replace(",", ".").astype(float)
    )
    df_grouped_dechet_per_department = (
        df_normalize_dechet.groupby(["C_DEPT", "N_DEPT"])["TONNAGE_T"]
        .sum()
        .reset_index()
    )

    df_grouped_dechet_per_department = df_grouped_dechet_per_department.rename(
        columns={
            "C_DEPT": "departement",
            "N_DEPT": "nom_departement",
            "TONNAGE_T": "tonnage_t",
        }
    )

    # Partie du traitement du dataset contenant les flux de CO2 par villes
    df_normalize_flux_CO2 = df_flux_CO2[["departement", "flux_tCO2e_an-1"]]
    df_grouped_CO2_per_department = (
        df_normalize_flux_CO2.groupby("departement")["flux_tCO2e_an-1"]
        .sum()
        .reset_index()
    )

    # Partie de fusion des dataset
    df_combined = pd.merge(
        df_grouped_dechet_per_department,
        df_grouped_CO2_per_department,
        on="departement",
        how="inner",
    )

    print(df_combined)

    return df_normalize_dechet, df_normalize_flux_CO2


def get_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "..", "data", "eco_track.db")
    DF_DECHET_PATH = os.path.join(BASE_DIR, "..", "data", "dechets_region.csv")
    DF_FLUX_CO2_PATH = os.path.join(BASE_DIR, "..", "data", "flux_CO2.csv")

    engine = create_engine(f"sqlite:///{DB_PATH}")
    df_dechet = pd.read_csv(DF_DECHET_PATH)
    df_flux_CO2 = pd.read_csv(DF_FLUX_CO2_PATH)
    df_dechet, df_flux_CO2 = normalize_data(df_dechet, df_flux_CO2)


get_db()
