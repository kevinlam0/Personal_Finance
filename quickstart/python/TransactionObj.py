PLAID_CONFIDENCE_LEVELS = {"VERY HIGH", "HIGH", "MEDIUM", "LOW", "UNKNOWN"}

class Transaction:
    t_id: str = None
    user_id: int = None
    account_id: str = None
    category: str = None
    date: str = None
    authorized_date: str = None
    pending_transaction_id: str = None
    
    def __init__(self, t_id: str, user_id: int, account_id: str, category: str, date: str, authorized_date: str, pending_id: str):
        self.t_id = t_id
        self.user_id = user_id
        self.account_id = account_id
        self.category = category
        self.date = date
        self.authorized_date = authorized_date
        self.pending_transaction_id = pending_id