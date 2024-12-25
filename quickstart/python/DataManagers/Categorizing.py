from psycopg2.extensions import connection
# Rules table which matches keyword to a category defined by the user
RULES_SQL = """
    CREATE TABLE IF NOT EXISTS Categorizing_Rule (
        rule_id INT PRIMARY KEY,
        user_id BIGINT NOT NULL REFERENCES Users(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
        keyword TEXT NOT NULL,
        category_id INT NOT NULL REFERENCES Category(category_id) ON UPDATE CASCADE ON DELETE CASCADE
    )
    """
    
# Mapping for Plaid's auto-categorization to custom category
CATEGORY_MAPPING = """
    CREATE TABLE IF NOT EXISTS Plaid_Category_Mapping (
        user_id INT NOT NULL REFERENCES Users(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
        plaid_category TEXT NOT NULL,
        customer_category_id INT NOT NULL REFERENCES Category(category_id),
        CONSTRAINT pk_userCat PRIMARY KEY (user_id, plaid_category)
    )
    """
    
def create_category(conn: connection, user_id: int, labels: list[str]):
    sql = f"""
        INSERT INTO Category (user_id, label) VALUES 
        ({user_id}, {labels[0]})
        """
    if len(labels) > 1:
        for i in range(1, len(labels)):
            sql += f", ({user_id}, {labels[i]})"
    print(sql)