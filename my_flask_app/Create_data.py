import pymysql

schema_name = "mydb"

# Establishing a connection to DB
conn = pymysql.connect(host='127.0.0.1', port=3306, user='user', passwd='password', db=schema_name)
conn.autocommit(True)

# Getting a cursor from Database
cursor = conn.cursor()

# Create table if it doesn't exist
create_table_statement = """
CREATE TABLE IF NOT EXISTS `registration` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(45) NOT NULL,
    `age` INT NOT NULL,
    `address` VARCHAR(255) NOT NULL,
    `postcode` VARCHAR(10) NOT NULL,
    `email` VARCHAR(100) NOT NULL
);
"""
cursor.execute(create_table_statement)

cursor.close()
conn.close()