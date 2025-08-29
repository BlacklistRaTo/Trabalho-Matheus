import pandas as pd
import matplotlib.pyplot as plt

# --- IMPORTAR DADOS ---
df = pd.read_csv("tabela_mortes.csv")

# --- BUSCA CIDADE COM MAIS E MENOS CASOS ---
cidade_max = df.loc[df["Total_de_mortes"].idxmax()]
cidade_min = df.loc[df["Total_de_mortes"].idxmin()]

# Salvar resumo em TXT
with open("resumo_cidades.txt", "w", encoding="utf-8") as f:
    f.write("📊 Cidade com MAIS mortes:\n")
    f.write(f"- Estado: {cidade_max['Estado']}\n")
    f.write(f"- Cidade: {cidade_max['Cidade']}\n")
    f.write(f"- Total de mortes: {cidade_max['Total_de_mortes']}\n")
    f.write(f"- População inicial: {cidade_max['Populacao_inicial']}\n")
    f.write(f"- População final: {cidade_max['Populacao_final']}\n\n")

    f.write("📉 Cidade com MENOS mortes:\n")
    f.write(f"- Estado: {cidade_min['Estado']}\n")
    f.write(f"- Cidade: {cidade_min['Cidade']}\n")
    f.write(f"- Total de mortes: {cidade_min['Total_de_mortes']}\n")
    f.write(f"- População inicial: {cidade_min['Populacao_inicial']}\n")
    f.write(f"- População final: {cidade_min['Populacao_final']}\n")

print("✅ Resumo salvo em 'resumo_cidades.txt'")

# --- PEGAR TOP 10 CIDADES PARA OS GRÁFICOS ---
top10_cidades = df.sort_values(by="Total_de_mortes", ascending=False).head(10)

# --- GRÁFICO 1: Top 10 cidades com mais mortes ---
plt.figure(figsize=(10,6))
bars = plt.bar(top10_cidades["Cidade"], top10_cidades["Total_de_mortes"], color='red')
plt.title("Top 10 cidades com mais mortes")
plt.ylabel("Total de mortes")
plt.xticks(rotation=45)

# Adicionar valores em cima das barras
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + (yval*0.01),
             f"{int(yval):,}".replace(",", "."), ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig("top10_mortes.png", dpi=300)
plt.close()

print("✅ Gráfico 'top10_mortes.png' salvo com sucesso")

# --- GRÁFICO 2: População inicial x final ---
plt.figure(figsize=(12,6))
x = range(len(top10_cidades))
bar_width = 0.35

bars1 = plt.bar([i - bar_width/2 for i in x], top10_cidades["Populacao_inicial"], 
                width=bar_width, label="População inicial")
bars2 = plt.bar([i + bar_width/2 for i in x], top10_cidades["Populacao_final"], 
                width=bar_width, label="População final", alpha=0.7)

plt.title("População inicial x final (Top 10 cidades com mais mortes)")
plt.ylabel("População")
plt.xticks(x, top10_cidades["Cidade"], rotation=45)
plt.legend()

# Adicionar valores em cima das barras
for bar in bars1 + bars2:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + (yval*0.01),
             f"{int(yval):,}".replace(",", "."), ha='center', va='bottom', fontsize=8, rotation=90)

plt.tight_layout()
plt.savefig("populacao_inicial_final.png", dpi=300)
plt.close()

print("✅ Gráfico 'populacao_inicial_final.png' salvo com sucesso")
