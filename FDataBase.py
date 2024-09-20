import datetime
import sqlite3


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Error reading from database")
        return []

    def addPost(self, title, text, is_visible=True):
        try:
            tm = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.__cur.execute("INSERT INTO posts (title, text, time, is_visible) VALUES (?, ?, ?, ?)",
                               (title, text, tm, is_visible))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error adding post to database: " + str(e))
            return False
        return True

    def getPost(self, postId):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE id = {postId} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Error reading from database: " + str(e))
        return (False, False)

    def getPostsAnonce(self):
        try:
            self.__cur.execute(f"SELECT id, title, text FROM posts WHERE is_visible = TRUE ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Error reading from database: " + str(e))
        return []

    def setPostVisibility(self, postId, is_visible):
        try:
            self.__cur.execute("UPDATE posts SET is_visible = ? WHERE id = ?", (is_visible, postId))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error reading from database: " + str(e))
            return False
        return True

    def getAllPosts(self):
        try:
            self.__cur.execute(f"SELECT id, title, text, is_visible FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Error reading from database: " + str(e))
        return []