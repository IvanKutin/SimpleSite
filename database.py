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

    def register(self, login, hash, admn):
        self.cur.execute("INSERT INTO site_user (login,hash,admn) VALUES (%s, %s, %s)",
                         (login, hash, admn))
        self.con.commit()

    def all(self):
        self.cur.execute("SELECT login,hash,admn FROM site_user")
        return self.cur.fetchall()

    def update(self, login, hash):
        self.cur.execute("UPDATE site_user SET hash = %s WHERE login = %s", (hash, login))
        self.con.commit()

    def all_purchase(self):
        self.cur.execute("SELECT name,price,info,small_info,category,id FROM purchase")
        return self.cur.fetchall()

    def add_purchase(self, name, cat, price, small_info, info, id):
        self.cur.execute(
            "INSERT INTO purchase (name,price,info,small_info,category,id) VALUES (%s, %s, %s, %s, %s, %s)",
            (name, price, info, small_info, cat, id))
        self.con.commit()

    def delete(self, id):
        self.cur.execute(
            "DELETE FROM purchase where id = %s", [id])
        self.con.commit()


class User():
    def __init__(self, login, hash, admn):
        self.login = login
        self.hash = hash
        self.admn = admn
