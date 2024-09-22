import datetime
import psycopg2

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
        except psycopg2.Error as e:
            print("Error reading from database: " + str(e))
        return []

    def addPost(self, title, text, is_visible=True):
        try:
            tm = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.__cur.execute("INSERT INTO posts (title, text, time, is_visible) VALUES (%s, %s, %s, %s)",
                               (title, text, tm, is_visible))
            self.__db.commit()
        except psycopg2.Error as e:
            print("Error reading from database: " + str(e))
            return False
        return True

    def getPost(self, postId):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE id = %s LIMIT 1", (postId,))
            res = self.__cur.fetchone()
            if res:
                return res
        except psycopg2.Error as e:
            print("Error reading from database: " + str(e))
        return (False, False)

    def getPostsAnonce(self):
        try:
            self.__cur.execute("SELECT id, title, text FROM posts WHERE is_visible = TRUE ORDER BY time DESC")
            res = self.__cur.fetchall()
            return [{'id': row[0], 'title': row[1], 'text': row[2]} for row in res]
        except psycopg2.Error as e:
            print("Error reading from database: " + str(e))
        return []

    def setPostVisibility(self, postId, is_visible):
        try:
            self.__cur.execute("UPDATE posts SET is_visible = %s WHERE id = %s", (is_visible, postId))
            self.__db.commit()
        except psycopg2.Error as e:
            print("Error reading from database: " + str(e))
            return False
        return True

    def getAllPosts(self):
        try:
            self.__cur.execute(f"SELECT id, title, text, is_visible FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res: return res
        except psycopg2.Error as e:
            print("Error reading from database: " + str(e))
        return []