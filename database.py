import psycopg2


class Database():
    def __init__(self):
        self.con = psycopg2.connect(
            database="flask_sem",
            user="postgres",
            password="8453",
            host="localhost",
            port=1111
        )
        self.cur = self.con.cursor()

    def register(self, login, hash):
        self.cur.execute("INSERT INTO site_user (login,hash) VALUES (%s, %s)",
                         (login, hash))
        self.con.commit()

    def all(self):
        self.cur.execute("SELECT login,hash FROM site_user")
        return self.cur.fetchall()

    def update(self, login, hash):
        self.cur.execute("UPDATE site_user SET hash = %s WHERE login = %s", (hash, login))
        self.con.commit()

    def all_purchase(self):
        self.cur.execute("SELECT name,price,info,small_info,category,id FROM purchase")
        return self.cur.fetchall()


class User():
    def __init__(self, login, hash):
        self.login = login
        self.hash = hash
