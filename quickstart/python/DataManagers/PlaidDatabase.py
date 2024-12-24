ITEMS_TABLE = """
    CREATE TABLE IF NOT EXISTS Plaid_Item (
        item_id TEXT PRIMARY KEY,
        user_id BIGINT NOT NULL REFERENCES Users(user_id),
        access_token TEXT NOT NULL,
        transaction_cursor TEXT,
        bank_name TEXT,
        is_active INTEGER NOT NULL DEFAULT 1
    )
    """
    
ACCOUNTS_TABLE = """
    CREATE TABLE IF NOT EXISTS Plaid_Account (
        account_id TEXT PRIMARY KEY,
        item_id TEXT NOT NULL REFERENCES Plaid_Item(item_id),
        account_name TEXT
    )
    """