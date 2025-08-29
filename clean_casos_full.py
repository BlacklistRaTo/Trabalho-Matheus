#!/usr/bin/env python3
import pandas as pd

def main(input_csv):
    # Colunas necessárias
    usecols = [
        "date", "state", "city",
        "last_available_deaths",
        "estimated_population",
        "estimated_population_2019"
    ]

    print("Lendo arquivo (pode demorar um pouco)...")
    df = pd.read_csv(input_csv, usecols=usecols, low_memory=False)

    # Garantir tipos corretos
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["last_available_deaths"] = pd.to_numeric(df["last_available_deaths"], errors="coerce").fillna(0).astype(int)
    df["estimated_population"] = pd.to_numeric(df["estimated_population"], errors="coerce").fillna(0).astype(int)
    df["estimated_population_2019"] = pd.to_numeric(df["estimated_population_2019"], errors="coerce").fillna(0).astype(int)

    # === Construindo a tabela final ===

    # 1) Total de mortes por cidade (máximo do período)
    mortes_por_cidade = (
        df.groupby(["state", "city"], as_index=False)["last_available_deaths"]
          .max()
          .rename(columns={"last_available_deaths": "Total_de_mortes"})
    )

    # 2) População inicial
    pop_inicio = (
        df.sort_values("date")
          .groupby(["state", "city"], as_index=False)
          .first()[["state", "city", "estimated_population"]]
    )

    # 3) População final
    pop_fim = (
        df.sort_values("date")
          .groupby(["state", "city"], as_index=False)
          .last()[["state", "city", "estimated_population_2019"]]
    )

    # 4) Juntar tudo (um registro por cidade)
    tabela_final = (
        mortes_por_cidade
        .merge(pop_inicio, on=["state", "city"], how="left")
        .merge(pop_fim, on=["state", "city"], how="left")
    )

    # 5) Renomear colunas finais
    tabela_final = tabela_final.rename(columns={
        "state": "Estado",
        "city": "Cidade",
        "Total_de_mortes": "Total_de_mortes",
        "estimated_population": "Populacao_inicial",
        "estimated_population_2019": "Populacao_final"
    })

    # 6) Salvar
    tabela_final.to_csv("tabela_mortes.csv", index=False, encoding="utf-8")

    print("\n✅ Arquivo gerado com sucesso:")
    print("- tabela_mortes.csv")

if __name__ == "__main__":
    main("casos_full.csv")
