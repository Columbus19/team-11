import utils.functions as funct

def tmp():
    conn = funct.get_database_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users(username, password, email) VALUES (?, ?, ?)", ("hi", "password", "email"))
    cursor.execute("INSERT INTO debt(date, location,parent_id) VALUES (?, ?,?)", ("Bob", "joshua",0))
       
    #    cursor.execute("SELECT id from debt")
    cursor.execute("SELECT *  from debt")

    data = cursor.fetchone()
    print(data, flush = True)
       # print(cursor.execute("SELECT * FROM debt-user"), flush=True)
    #    print("hi", flush = True)
tmp()