import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(filepath):
    """Carrega os dados de um arquivo CSV."""
    try:
        df = pd.read_csv(filepath)
        print(f"Dados carregador com sucesso de : {filepath}")
        return df
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {filepath}")
        return None

def clean_data(df):
    """Limpeza básica nos dados"""
    if df is None:
        return None
    print("Iniciando limpeza de dados")
    #renomeando colunas para letras minusculas e snake_case
    df.columns = df.columns.str.lower().str.replace(' ','_')

    #converter 'order_date' para datetime
    df['order_date'] = pd.to_datetime(df['order_date'])

    # Exemplo: remover linhas com nulos
    df.dropna(inplace=True)

    # Remover duplicatas (se aplicável)
    df.drop_duplicates(inplace=True)

    print("Limpeza de dados concluída.")
    return df

def perform_analysis(df):
    """Realização das análises"""
    if df is None:
        return None

    print("\nRealizando análises")

    #1. Total de vendas e quantidad vendida
    df['total_price'] = df['price'] * df['quantity']
    total_sales = df['total_price'].sum()
    total_quantity = df['quantity'].sum()
    print(f"Total de Vendas: R${total_sales:,.2f}")
    print(f"Total de Produtos Vendidos: {total_quantity}")

    #2. Vendas por categoria
    sales_by_category = df.groupby('category')['total_price'].sum().sort_values(ascending=False)
    print("\nVendas por Categoria:")
    print(sales_by_category)

    #3. Produtos mais vendidos em quantidade
    top_products_quantity = df.groupby('category')['quantity'].sum().sort_values(ascending=False).head(5)
    print("\nTop 5 Produtos Mais Vendidos(por quantidade)")
    print(top_products_quantity)

    #4. Vendas por Região
    sales_by_region = df.groupby('region')['total_price'].sum().sort_values(ascending=False)
    print("\nVendas por região")
    print(sales_by_region)

    #5. Vendas ao Longo do Tempo(por mês)#
    df['month'] = df['order_date'].dt.strftime('%Y-%d-%m')


    sales_by_month = df.groupby('month')['total_price'].sum().sort_index()
    print("\nVendas Mensais:")
    print(sales_by_month)

    #Visualizações com matplotlib e seaborn
    #vendas por categoria
    plt.figure(figsize=(10,6))
    sns.barplot(x=sales_by_category.index,y=sales_by_category.values)
    plt.title('Vendas Totais por categoria de produto')
    plt.xlabel('Categoria')
    plt.ylabel('Total de vendas(R$)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('monthly_sales_category.png')
    plt.show()


    #vendas mensais
    plt.figure(figsize=(10, 6))
    sales_by_month.plot(kind='line',marker='o', color='skyblue')
    plt.title('Tendência de Vendas Mensais')
    plt.xlabel('Mês')
    plt.ylabel('Total de vendas(R$)')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('monthly_sales_trend.png')
    plt.show()





if __name__ == "__main__":
    data_filepath = 'data/sales_data.csv'
    df_raw = load_data(data_filepath)

    if df_raw is not None:
        df_cleaned = clean_data(df_raw.copy())

    perform_analysis(df_cleaned)




