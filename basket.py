import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Carregar o arquivo CSV
file_path = "output.csv"  
data = pd.read_csv(file_path)

# Renomear colunas para facilitar o trabalho
data.columns = ['ID', 'Day', 'Time', 'Product', 'Quantity', 'UnitPrice', 'TotalPrice']

# Criar uma tabela de transações (cesta de compras)
basket = data.groupby(['ID', 'Product'])['Quantity'].sum().unstack().fillna(0)

# Converter as quantidades em presença/ausência (0/1)
basket = basket > 0

# Gerar padrões frequentes com o algoritmo Apriori
frequent_itemsets = apriori(basket, min_support=0.01, use_colnames=True)

# Gerar as regras de associação
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1, num_itemsets=frequent_itemsets.shape[0])


# Ordenar as regras por lift (relevância) e mostrar as principais
rules = rules.sort_values(by='lift', ascending=False)

# Exibir as 10 principais regras de associação
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10))