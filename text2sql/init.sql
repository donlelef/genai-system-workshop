CREATE TABLE customers (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    city  VARCHAR(100) NOT NULL,
    signup_date DATE NOT NULL
);

CREATE TABLE products (
    id       SERIAL PRIMARY KEY,
    name     VARCHAR(200) NOT NULL,
    category VARCHAR(50)  NOT NULL,
    price    NUMERIC(10, 2) NOT NULL,
    stock    INTEGER NOT NULL
);

CREATE TABLE orders (
    id          SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers (id),
    product_id  INTEGER NOT NULL REFERENCES products (id),
    quantity    INTEGER NOT NULL,
    order_date  DATE    NOT NULL
);

-- Customers
INSERT INTO customers (name, email, city, signup_date) VALUES
    ('Alice Johnson',   'alice@example.com',   'New York',     '2024-01-15'),
    ('Bob Smith',       'bob@example.com',     'Chicago',      '2024-02-20'),
    ('Carol Williams',  'carol@example.com',   'San Francisco','2024-03-10'),
    ('David Brown',     'david@example.com',   'New York',     '2024-04-05'),
    ('Eve Davis',       'eve@example.com',     'Chicago',      '2024-05-12'),
    ('Frank Miller',    'frank@example.com',   'Los Angeles',  '2024-06-18'),
    ('Grace Wilson',    'grace@example.com',   'San Francisco','2024-07-22'),
    ('Hank Moore',      'hank@example.com',    'New York',     '2024-08-30');

-- Products
INSERT INTO products (name, category, price, stock) VALUES
    ('Wireless Mouse',       'Electronics', 29.99,  150),
    ('Mechanical Keyboard',  'Electronics', 89.99,   75),
    ('USB-C Hub',            'Electronics', 49.99,  200),
    ('Notebook A5',          'Stationery',   5.99,  500),
    ('Ballpoint Pen Pack',   'Stationery',   3.49,  800),
    ('Desk Lamp',            'Home Office', 39.99,  120),
    ('Monitor Stand',        'Home Office', 59.99,   60),
    ('Webcam HD',            'Electronics', 74.99,   90),
    ('Ergonomic Chair',      'Home Office',249.99,   30),
    ('Sticky Notes Bundle',  'Stationery',   7.99,  400);

-- Orders
INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES
    (1, 1, 2, '2024-09-01'),
    (1, 3, 1, '2024-09-01'),
    (2, 2, 1, '2024-09-05'),
    (2, 6, 1, '2024-09-05'),
    (3, 4, 10,'2024-09-10'),
    (3, 5, 5, '2024-09-10'),
    (4, 7, 1, '2024-09-15'),
    (4, 9, 1, '2024-09-15'),
    (5, 1, 1, '2024-10-01'),
    (5, 8, 1, '2024-10-01'),
    (6, 2, 2, '2024-10-10'),
    (6, 3, 3, '2024-10-10'),
    (1, 6, 1, '2024-10-20'),
    (7, 4, 20,'2024-10-25'),
    (7, 10,10,'2024-10-25'),
    (8, 9, 1, '2024-11-01'),
    (2, 1, 1, '2024-11-10'),
    (3, 7, 2, '2024-11-15'),
    (5, 5, 3, '2024-11-20'),
    (4, 8, 1, '2024-12-01');
