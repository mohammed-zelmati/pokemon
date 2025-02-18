import pandas as pd
import pyexcel_ods

# Lire le fichier .ods
data = pyexcel_ods.get_data("pokemonExcel.ods")

# Convertir les données en DataFrame
sheet_name = list(data.keys())[0]  # Supposons que vous voulez la première feuille
df = pd.DataFrame(data[sheet_name][1:], columns=data[sheet_name][0])

# Supprimer les lignes contenant des valeurs nulles
df.dropna(inplace=True)

# Enregistrer au format JSON, encapsulé dans une liste avec des virgules
with open("ggg.json", "w", encoding="utf-8") as f:
    f.write("[\n")
    df.to_json(f, orient="records", lines=True)
    f.write("\n]")

# Ajouter des virgules entre les objets JSON
with open("ggg.json", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Enlever la dernière virgule
lines = [line.rstrip() for line in lines]
lines = ',\n'.join(lines).replace(',\n]', '\n]')

with open("ggg.json", "w", encoding="utf-8") as f:
    f.write(lines)



