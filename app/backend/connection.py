import sqlite3
import uuid
import json
import os


class Connection:
    def __init__(self):
        self.connection = sqlite3.connect('db.db', check_same_thread=False)
        self.create_table_initial()
        # self.populate_animes()


    def create_table_initial(self):
        self.connection.execute(
            '''CREATE TABLE IF NOT EXISTS User(id text PRIMARY KEY, login text, password text)''')
        
        self.connection.execute(
            '''
            CREATE TABLE IF NOT EXISTS Anime(
                id text PRIMARY KEY,
                name text,
                drama INTEGER DEFAULT 0,
                romance INTEGER DEFAULT 0,
                school INTEGER DEFAULT 0,
                supernatural INTEGER DEFAULT 0,
                action INTEGER DEFAULT 0,
                adventure INTEGER DEFAULT 0,
                fantasy INTEGER DEFAULT 0,
                magic INTEGER DEFAULT 0,
                military INTEGER DEFAULT 0,
                shounen INTEGER DEFAULT 0,
                comedy INTEGER DEFAULT 0,
                historical INTEGER DEFAULT 0,
                parody INTEGER DEFAULT 0,
                samurai INTEGER DEFAULT 0,
                sci_Fi INTEGER DEFAULT 0,
                thriller INTEGER DEFAULT 0,
                sports INTEGER DEFAULT 0,
                super Power INTEGER DEFAULT 0,
                space INTEGER DEFAULT 0,
                slice_of_life INTEGER DEFAULT 0,
                mecha INTEGER DEFAULT 0,
                music INTEGER DEFAULT 0,
                mystery INTEGER DEFAULT 0,
                seinen INTEGER DEFAULT 0,
                martial_rts INTEGER DEFAULT 0,
                vampire INTEGER DEFAULT 0,
                shoujo INTEGER DEFAULT 0,
                horror INTEGER DEFAULT 0,
                police INTEGER DEFAULT 0,
                psychological INTEGER DEFAULT 0,
                demons INTEGER DEFAULT 0,
                ecchi INTEGER DEFAULT 0,
                josei INTEGER DEFAULT 0,
                shounen_ai INTEGER DEFAULT 0,
                game INTEGER DEFAULT 0,
                dementia INTEGER DEFAULT 0,
                harem INTEGER DEFAULT 0,
                cars INTEGER DEFAULT 0,
                kids INTEGER DEFAULT 0,
                shoujo_ai INTEGER DEFAULT 0,
                genre INTEGER DEFAULT 0,
                hentai INTEGER DEFAULT 0,
                yaoi INTEGER DEFAULT 0,
                yuri INTEGER DEFAULT 0
            )
            '''
        )
        
        self.connection.execute(
            '''CREATE TABLE IF NOT EXISTS View_Anime 
            (
            id text PRIMARY KEY, 
            anime_id text,
            user_id text,
            rate INTEGER,
            FOREIGN KEY(user_id) REFERENCES User(id),
            FOREIGN KEY(anime_id) REFERENCES Anime(id)
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
        res = self.connection.execute("SELECT anime_id, rate FROM View_Anime WHERE user_id = ?", (id_user,)
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
    
    def get_all_animes(self):
        result = self.connection.execute("SELECT * FROM Anime")
        return result.fetchall()

    def get_n_animes(self, n=10):
        result = self.connection.execute(f"SELECT * FROM Anime LIMIT {n}")
        return result.fetchall()
    
    def populate_animes(self):
        animes = self.get_all_animes()
        if len(animes) <= 0:
            path = os.path.join('app', 'backend')
            fullpath = os.path.join(path, 'animes.json')
            with open(fullpath) as json_file:
                data = json.load(json_file)
                for key,value in data.items():
                    m_id = str(uuid.uuid4())
                    v = list(value.values())
                    v.insert(0, key)
                    v.insert(0, m_id)
                    print(f"##=Values={tuple(v)}")
                    self.connection.execute('''INSERT INTO Anime VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''', v)
                self.connection.commit()

    def rate_anime(self, anime, id_user, rate):
        m_id = str(uuid.uuid4())
        res = self.connection.execute("SELECT * FROM View_Anime WHERE user_id = ? AND anime_id = ?", (id_user, anime))
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
            '''SELECT login, anime_id, rate FROM User as us INNER JOIN 
            View_Anime as va on us.id = va.user_id;''').fetchall()

        map_users = dict()

        for i in res:
            map_users[i[0]] = []

        for i in res:
            map_users[i[0]].append({"movie": i[1], "rate": i[2]})

        return json.dumps(map_users)