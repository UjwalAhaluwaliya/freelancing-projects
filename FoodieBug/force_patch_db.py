import pymysql
try:
    conn = pymysql.connect(host='localhost', user='root', password='2202', db='foodiebug')
    cur = conn.cursor()
    cur.execute("DESCRIBE orders;")
    columns = [row[0] for row in cur.fetchall()]
    print("CURRENT COLUMNS in 'orders' table:", columns)
    
    if 'delivery_partner_id' not in columns:
        print("Column missing! I will aggressively add it using PyMySQL directly.")
        cur.execute("ALTER TABLE orders ADD COLUMN delivery_partner_id INT DEFAULT NULL;")
        cur.execute("ALTER TABLE orders ADD CONSTRAINT fk_orders_delivery_partner FOREIGN KEY (delivery_partner_id) REFERENCES users(id);")
        conn.commit()
        print("Added successfully!")
    else:
        print("Column ALREADY exists. The issue is caching via the running Flask server.")
    conn.close()
except Exception as e:
    print("Exception:", e)
