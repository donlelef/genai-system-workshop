from core.models import ColumnInfo, TableInfo, TableSchema


def get_table_list() -> list[TableInfo]:
    return [
        TableInfo(
            name="customers",
            description="Registered customers with contact info and city of residence.",
        ),
        TableInfo(
            name="products",
            description="Product catalog with categories, prices, and stock levels.",
        ),
        TableInfo(
            name="orders",
            description=(
                "Customer orders linking a customer to a product with quantity and date. "
                "Foreign keys: customer_id -> customers.id, product_id -> products.id."
            ),
        ),
    ]


def get_schema(table_name: str) -> TableSchema:
    schemas: dict[str, TableSchema] = {
        "customers": TableSchema(
            table_name="customers",
            columns=[
                ColumnInfo(
                    name="id",
                    data_type="SERIAL PRIMARY KEY",
                    description="Unique customer identifier",
                ),
                ColumnInfo(
                    name="name", data_type="VARCHAR(100)", description="Full name"
                ),
                ColumnInfo(
                    name="email",
                    data_type="VARCHAR(150)",
                    description="Email address (unique)",
                ),
                ColumnInfo(
                    name="city",
                    data_type="VARCHAR(100)",
                    description="City of residence",
                ),
                ColumnInfo(
                    name="signup_date",
                    data_type="DATE",
                    description="Registration date",
                ),
            ],
            sample_values={
                "id": ["1", "2", "3"],
                "name": ["Alice Johnson", "Bob Smith", "Carol Williams"],
                "email": ["alice@example.com", "bob@example.com", "carol@example.com"],
                "city": ["New York", "Chicago", "San Francisco"],
                "signup_date": ["2024-01-15", "2024-02-20", "2024-03-10"],
            },
        ),
        "products": TableSchema(
            table_name="products",
            columns=[
                ColumnInfo(
                    name="id",
                    data_type="SERIAL PRIMARY KEY",
                    description="Unique product identifier",
                ),
                ColumnInfo(
                    name="name", data_type="VARCHAR(200)", description="Product name"
                ),
                ColumnInfo(
                    name="category",
                    data_type="VARCHAR(50)",
                    description="Product category",
                ),
                ColumnInfo(
                    name="price",
                    data_type="NUMERIC(10,2)",
                    description="Unit price in USD",
                ),
                ColumnInfo(
                    name="stock",
                    data_type="INTEGER",
                    description="Items currently in stock",
                ),
            ],
            sample_values={
                "id": ["1", "2", "3"],
                "name": ["Wireless Mouse", "Mechanical Keyboard", "USB-C Hub"],
                "category": ["Electronics", "Stationery", "Home Office"],
                "price": ["29.99", "89.99", "49.99"],
                "stock": ["150", "75", "200"],
            },
        ),
        "orders": TableSchema(
            table_name="orders",
            columns=[
                ColumnInfo(
                    name="id",
                    data_type="SERIAL PRIMARY KEY",
                    description="Unique order identifier",
                ),
                ColumnInfo(
                    name="customer_id",
                    data_type="INTEGER",
                    description="FK to customers.id",
                ),
                ColumnInfo(
                    name="product_id",
                    data_type="INTEGER",
                    description="FK to products.id",
                ),
                ColumnInfo(
                    name="quantity",
                    data_type="INTEGER",
                    description="Number of items ordered",
                ),
                ColumnInfo(
                    name="order_date",
                    data_type="DATE",
                    description="Date the order was placed",
                ),
            ],
            sample_values={
                "id": ["1", "2", "3"],
                "customer_id": ["1", "1", "2"],
                "product_id": ["1", "3", "2"],
                "quantity": ["2", "1", "1"],
                "order_date": ["2024-09-01", "2024-09-01", "2024-09-05"],
            },
        ),
    }
    schema = schemas.get(table_name)
    if schema is None:
        raise ValueError(f"Unknown table: {table_name}")
    return schema
