import pandas as pd

# Carregar o arquivo CSV
file_path = "output.csv"
data = pd.read_csv(file_path)

# Renomear colunas para facilitar o trabalho
data.columns = ['ID', 'Day', 'Time', 'Product', 'Quantity', 'UnitPrice', 'TotalPrice']

# Total de compras (IDs únicos)
total_purchases = data['ID'].nunique()

# Contar em quantos IDs cada item aparece
item_purchases = data.groupby('Product')['ID'].nunique()

# Calcular o percentual para cada item
item_percentages = (item_purchases / total_purchases * 100).round(2)

# Ordenar por percentual (decrescente) para facilitar a visualização
item_percentages = item_percentages.sort_values(ascending=False)

# Mostrar os resultados
print("Percentual de compras que incluíram cada item:")
print(item_percentages.astype(str) + '%')