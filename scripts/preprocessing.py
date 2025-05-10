import pandas as pd
import os

def load_data(transactions_path: str, categories_path: str = None):
    """Load transaction and optional category data."""
    transactions = pd.read_csv(transactions_path)
    categories = pd.read_csv(categories_path) if categories_path else None
    return transactions, categories

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw transaction data."""
    df = df.dropna()
    df.columns = df.columns.str.strip()
    return df

def merge_with_categories(transactions: pd.DataFrame, categories: pd.DataFrame) -> pd.DataFrame:
    """Enrich transactions with merchant category info."""
    return transactions.merge(categories, on='MerchantName', how='left')

def compute_rfm(df: pd.DataFrame) -> pd.DataFrame:
    """Compute Recency, Frequency, Monetary RFM table."""
    rfm = df.groupby('CustomerID').agg({
        'CustomerLastTransactionFrom(days)': 'min',    # Recency
        'TransactionValue': 'sum',                      # Monetary
        'TransactionRank': 'count'                      # Frequency
    }).reset_index()

    rfm.rename(columns={
        'CustomerLastTransactionFrom(days)': 'Recency',
        'TransactionValue': 'Monetary',
        'TransactionRank': 'Frequency'
    }, inplace=True)

    return rfm

def save_processed_data(df: pd.DataFrame, path: str):
    """Save processed RFM data."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)

def main():
    transactions_path = 'data/raw/Transactions.csv'
    categories_path = 'data/raw/Categories.csv'
    output_path = 'data/processed/rfm_table.csv'

    transactions, categories = load_data(transactions_path, categories_path)
    transactions = clean_data(transactions)
    
    if categories is not None:
        transactions = merge_with_categories(transactions, categories)

    rfm_table = compute_rfm(transactions)
    save_processed_data(rfm_table, output_path)
    print("✅ RFM table saved to", output_path)

if __name__ == "__main__":
    main()
