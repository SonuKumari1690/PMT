import sqlite3

conn = sqlite3.connect('pmt.db')
print("Opened database successfully")


sql = '''CREATE TABLE users(
           ID INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,
           USERNAME CHAR(30) NOT NULL,
           EMAIL CHAR(30) NOT NULL,
           PASSWORD CHAR(30)  NOT NULL

        )'''
conn.execute(sql)
print("Table created successfully........")


conn.execute("INSERT INTO users (USERNAME,EMAIL,PASSWORD) VALUES ('Demo', 'demo', 'demo')")
conn.commit()
print("Records created successfully")

cursor = conn.execute("SELECT * from users")
for row in cursor:
    print("ID = ", row[0])
    print("NAME = ", row[1])
    print("EMAIL = ", row[2])
    print("PASSWORD = ", row[3]), "\n"

print("Operation done successfully")
conn.close()