import sqlite3
import uuid
import json
import os


class Connection:
    def __init__(self):
        self.connection = sqlite3.connect('db.db', check_same_thread=False)
        self.create_table_initial()
        pass

    def create_table_initial(self):
        self.connection.execute(
            '''CREATE TABLE IF NOT EXISTS User(id text PRIMARY KEY, login text, password text)''')
        self.connection.execute(
            '''CREATE TABLE IF NOT EXISTS View_Anime 
            (
            id text PRIMARY KEY, 
            anime text,user_id text,
            rate INTEGER,
            FOREIGN KEY(user_id) REFERENCES User(id)
            )''')

    def getConnection(self):
        return self.connection

    def createUser(self, login, password):
        m_id = str(uuid.uuid4())
        self.connection.execute('''INSERT INTO User VALUES (?, ?, ?);''', (m_id, login, password))
        self.connection.commit()
        return m_id

    def getUsers(self):
        result = self.connection.execute("SELECT * FROM User")
        return result.fetchall()

    def get_animes_user(self, id_user):
        res = self.connection.execute("SELECT anime, rate FROM View_Anime WHERE user_id = ?", (id_user,)
                                      ).fetchall()
        if res is None:
            return [("", "")]

        return res

    def get_user(self, login, password):
        result = self.connection.execute("SELECT * FROM User WHERE login = ? AND password = ?",
                                         (login, password)
                                         ).fetchall()
        if len(result) == 0:
            return None
        else:
            return {"id": result[0][0]}

    def rate_anime(self, anime, id_user, rate):
        m_id = str(uuid.uuid4())
        res = self.connection.execute("SELECT * FROM View_Anime WHERE user_id = ? AND anime = ?", (id_user, anime))
        if len(res.fetchall()) == 0:
            print("Criando Avaliacao")
            self.connection.execute("INSERT INTO View_Anime VALUES (?, ?, ?, ?);", (m_id, anime, id_user, rate))
        else:
            self.connection.execute("UPDATE View_Anime SET rate = ? "
                                    "WHERE user_id = ? AND anime = ?;",
                                    (rate, id_user, anime)
                                    )
            print("Atualizando Avaliacao")
        self.connection.commit()

    def get_json(self):
        res = self.connection.execute(
            '''SELECT login, anime, rate FROM User as us INNER JOIN 
            View_Anime as va on us.id = va.user_id;''').fetchall()

        map_users = dict()

        for i in res:
            map_users[i[0]] = []

        for i in res:
            map_users[i[0]].append({"movie": i[1], "rate": i[2]})

        return json.dumps(map_users)