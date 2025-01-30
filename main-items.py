import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Carregar o arquivo CSV
file_path = "output.csv"
data = pd.read_csv(file_path)

# Renomear colunas para facilitar o trabalho
data.columns = ['ID', 'Day', 'Time', 'Product', 'Quantity', 'UnitPrice', 'TotalPrice']

# Criar a tabela de transações (cesta de compras)
basket = data.groupby(['ID', 'Product'])['Quantity'].sum().unstack().fillna(0)
basket = basket > 0

# Gerar padrões frequentes e regras de associação
frequent_itemsets = apriori(basket, min_support=0.01, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1, num_itemsets=len(frequent_itemsets))

# 1. Filtrar as regras onde o "Cookie Gotas de Chocolate" é o consequente
cookie_rules = rules[rules['consequents'].apply(lambda x: 'COOKIE GOTAS DE CHOCOLATE' in x)]

# 2. Verificar cestas onde o cookie está presente com outros itens
cookie_carts = data[data['Product'] == 'COOKIE GOTAS DE CHOCOLATE']['ID'].unique()
multi_item_carts = data[data['ID'].isin(cookie_carts)].groupby('ID').filter(lambda x: len(x['Product'].unique()) > 1)

# 3. Contar proporção de cestas com cookie como único item
cookie_only_carts = data[data['ID'].isin(cookie_carts)].groupby('ID').filter(lambda x: len(x['Product'].unique()) == 1)
cookie_only_count = cookie_only_carts['ID'].nunique()
multi_item_count = multi_item_carts['ID'].nunique()

# Mostrar os resultados
print("Regras onde o Cookie é o consequente:")
print(cookie_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

print(f"\nTotal de cestas com cookie como único item: {cookie_only_count}")
print(f"Total de cestas com cookie e outros itens: {multi_item_count}")