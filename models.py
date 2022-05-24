import json

from SQL_Manage import create_connection, execute_sql

class Todos:
    def __init__(self):
        try:
            with open("todos.json", "r") as f:
                self.todos = json.load(f)
        except FileNotFoundError:
            self.todos = []

    def all(self):
        return self.todos

    def get(self, id):
        todo = [todo for todo in self.all() if todo['id'] == id]
        if todo:
            return todo[0]
        return []

    def create(self, data):
        self.todos.append(data)
        self.save_all()

    def save_all(self):
        with open("todos.json", "w") as f:
            json.dump(self.todos, f)

    def update(self, id, data):
        todo = self.get(id)
        data.pop('csrf_token')
        if todo:
            index = self.todos.index(todo)
            data['id']=index+1
            self.todos[index] = data
            self.save_all()
    
    def delete(self, id):
        todo = self.get(id)
        self.todos.remove(todo)
        self.save_all()

db_file = "todos.db"
make_table="""CREATE TABLE IF NOT EXISTS todos (
      id_ integer PRIMARY KEY,
      title VARCHAR(250) NOT NULL,
      description VARCHAR(250) NOT NULL,
      done TEXT NOT NULL
   );"""

with create_connection(db_file) as conn:
       execute_sql(conn, make_table)

class TodosSQLite:
    def con_into_lib(self, tuple_):
        out=[]
        for e in tuple_:
            out.append({"id_":e[0],"title":e[1],"description":e[2],"done":e[3]})
        if len(out)==1:
            return out[0]
        return out
    
    def con_into_tuple(self, lib):
        return (lib["id_"],lib["title"],lib["description"],lib["done"])

    def all(self):
        with create_connection(db_file) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM todos")
            return self.con_into_lib(cur.fetchall())

    def get(self, id):
        with create_connection(db_file) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM todos WHERE id_=?", (id,))
            rows = cur.fetchone()
            row = {"id_":rows[0],"title":rows[1],"description":rows[2],"done":rows[3]}
            if row:
                return row
            return []

    def create(self, data):
        data2=self.con_into_tuple(data)
        with create_connection(db_file) as conn:
            sql = '''INSERT INTO todos(id_, title, description, done)
             VALUES(?,?,?,?)'''
            cur = conn.cursor()
            cur.execute(sql, data2)
    
    def update(self, id, data):
        data.pop('csrf_token')
        parameters = [f"{k} = '{v}'" for k, v in data.items()]
        parameters = ", ".join(parameters)
        print(parameters)
        sql = f''' UPDATE todos
             SET {parameters}
             WHERE id_ = {id};'''
        with create_connection(db_file) as conn:
            cur = conn.cursor()
            cur.execute(sql)
    
    def delete(self, id):
        sql = f'DELETE FROM todos WHERE id_ = {id}'
        with create_connection(db_file) as conn:
            cur=conn.cursor()
            cur.execute(sql)

    def del_all(self):
        sql = """ DELETE FROM todos"""
        with create_connection(db_file) as conn:
            cur=conn.cursor()
            cur.execute(sql)

todos = TodosSQLite()
#todos.create({"id_": 2, "title": "Potoppp", "description": "H. Sienkiewicz", "done": "Powiesc"})
print(todos.all())