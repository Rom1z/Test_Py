# MySQL
CREATE DATABASE inventory_db;

USE inventory_db;

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    warehouse VARCHAR(255) NOT NULL
);

-------------------------------------------
## Шаг 2: Пишем код на Python
Установите необходимые библиотеки:
*pip install mysql-connector-python*
