import psycopg2 as db
import csv


class Config:
    def __init__(self):
        self.config = {
            "postgres": {
                "user": "postgres",
                "password": "1234",
                "host": "127.0.0.1",
                "port": "5432",
                "database": "pydb"
            }
        }


class Connection(Config):
    def __init__(self):
        super().__init__()
        try:
            self.conn = db.connect(**self.config["postgres"])
            self.cur = self.conn.cursor()
        except Exception as e:
            print("Erro na conexão", e)
            exit(1)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()  # Fix: Use self.conn.commit() instead of self.commit()
        self.conn.close()   # Fix: Use self.conn.close() instead of self.connection.close()

    @property
    def connection(self):
        return self.conn

    @property
    def cursor(self):
        return self.cur

    def commit(self):
        self.conn.commit()

    def fetchall(self):
        return self.cur.fetchall()

    def execute(self, sql, params=None):
        self.cur.execute(sql, params or ())

    def query(self, sql, params=None):
        self.cur.execute(sql, params or ())
        return self.fetchall()


class Pessoa(Connection):
    def __init__(self):
        super().__init__()

    def insert(self, *args):
        try:
            sql = "INSERT INTO pessoa (nome) VALUES (%s)"
            self.execute(sql, args)
            self.conn.commit()  # Commit after insertion
        except Exception as e:
            print("Erro ao inserir", e)

    def insert_csv(self, filename):
        try:
            data = csv.DictReader(open(filename, encoding="utf-8"))
            for row in data:
                self.insert(row["nome"])
                print("Registro Inserido")
            self.conn.commit()  # Commit after all insertions
        except Exception as e:
            print("Erro ao inserir csv", e)

    def delete(self, id):
        try:
            sql_s = f"SELECT * FROM pessoa WHERE id = {id}"
            if not self.query(sql_s):
                return "Registro não encontrado para deletar"
            sql_d = f"DELETE FROM pessoa WHERE id = {id}"
            self.execute(sql_d)
            self.conn.commit()  # Commit after deletion
            return "Registro deletado"
        except Exception as e:
            print("Erro ao deletar", e)

    def update(self, id, *args):
        try:
            sql = f"UPDATE pessoa SET nome = %s WHERE id = {id}"
            self.execute(sql, args)
            self.conn.commit()  # Commit after update
            print("Registro atualizado")
        except Exception as e:
            print("Erro ao atualizar", e)


if __name__ == "__main__":
    pessoa = Pessoa()

    # Inserir 6 novos registros do arquivo CSV
    pessoa.insert_csv("data.csv")

    # Atualizar o nome de "Maria" para "Maria Antônio"
    pessoa.update(14, "Maria Antônio")

    # Deletar o registro de "Miguel"
    pessoa.delete(15)
