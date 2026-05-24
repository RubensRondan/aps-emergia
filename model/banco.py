import sqlite3


class BancoDados:

    def __init__(self):

        self.conexao = sqlite3.connect(
            "database/emergia.db"
        )

        self.cursor = self.conexao.cursor()

        self.criar_tabela()

    def criar_tabela(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS calculos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recurso TEXT,
                energia REAL,
                transformidade REAL,
                emergia REAL
            )
        """)

        self.conexao.commit()

    def salvar_calculo(
        self,
        recurso,
        energia,
        transformidade,
        emergia
    ):

        self.cursor.execute("""
            INSERT INTO calculos (
                recurso,
                energia,
                transformidade,
                emergia
            )
            VALUES (?, ?, ?, ?)
        """, (
            recurso,
            energia,
            transformidade,
            emergia
        ))

        self.conexao.commit()