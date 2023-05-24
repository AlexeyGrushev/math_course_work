import sqlite3 as sq


class DBHelper:
    def __init__(self) -> None:
        self.db_name = "data/database.sqlite3"
        self.connect = sq.connect(self.db_name)
        self.cursor = self.connect.cursor()
        pass

    def setup_table(self) -> None:
        self.connect.execute(
            """
            CREATE TABLE IF NOT EXISTS "accounts" (
            "Id"	INTEGER NOT NULL UNIQUE,
            "Login"	TEXT NOT NULL UNIQUE,
            "Password"	TEXT NOT NULL,
            PRIMARY KEY("Id" AUTOINCREMENT)
            );
            """
        )

        self.connect.execute(
            """
            CREATE TABLE IF NOT EXISTS "stats" (
            "Id"	INTEGER NOT NULL UNIQUE,
            "eqTrue"	INTEGER NOT NULL,
            "eqFalse"	INTEGER NOT NULL,
            "eqSkip"	INTEGER NOT NULL,
            "graps"	INTEGER NOT NULL,
            PRIMARY KEY("Id" AUTOINCREMENT)
            );
            """
        )

        self.connect.execute(
            """
            CREATE TABLE IF NOT EXISTS "students" (
            "Id"	INTEGER NOT NULL,
            "FirstName"	TEXT NOT NULL,
            "LastName"	TEXT NOT NULL,
            "Class2"	TEXT NOT NULL,
            PRIMARY KEY("Id" AUTOINCREMENT)
            );
            """
        )

    def user_registration(self, data: list) -> None:
        self.cursor.execute(
            """
            INSERT INTO accounts
            (Login, Password)
            VALUES (?, ?);
            """,
            (data[0], data[1])
        )

        self.cursor.execute(
            """
            INSERT INTO students
            (FirstName, LastName, Class2)
            VALUES (?, ?, ?);
            """,
            (data[2], data[3], data[4])
        )

        self.cursor.execute(
            """
            INSERT INTO stats
            (eqTrue,eqFalse,eqSkip,graps)
            VALUES (0,0,0,0);
            """
        )
        self.connect.commit()

    def user_authentication(self, data: list) -> list:
        return self.cursor.execute(
            f"""
            SELECT Id, Login, Password
            FROM accounts WHERE
            Login == "{data[0]}"
            AND Password == "{data[1]}";
            """
        ).fetchall()

    def user_profile_load(self, data: str) -> list:
        return self.cursor.execute(
            """
            SELECT Login
            FROM accounts
            WHERE Id == (?);
            """,
            (data)
        ).fetchall()

    def user_profile_info_load(self, data: str) -> list:
        return self.cursor.execute(
            """
            SELECT FirstName, LastName, Class2
            FROM students WHERE Id == (?);
            """,
            (data)
        ).fetchall()

    def user_correct_eq_update(self, data: str) -> None:
        self.cursor.execute(
            """
            UPDATE stats
            SET eqTrue = (eqTrue + 1)
            WHERE Id == (?);
            """, (data)
        )
        self.connect.commit()

    def user_incorrect_eq_update(self, data: str) -> None:
        self.cursor.execute(
            """
            UPDATE stats
            SET eqFalse = (eqFalse + 1)
            WHERE Id == (?);
            """, (data)
        )
        self.connect.commit()

    def user_skip_eq_update(self, data: str) -> None:
        self.cursor.execute(
            """
            UPDATE stats
            SET eqSkip = (eqSkip + 1)
            WHERE Id == (?);
            """, (data)
        )
        self.connect.commit()

    def user_eqTrue_stat_load(self, data: str) -> int:
        return self.cursor.execute(
            """
            SELECT eqTrue
            FROM stats
            WHERE Id == (?);
            """, (data)
        ).fetchall()[0][0]
    
    def user_statistics_load(self, data: str) -> list:
        return self.cursor.execute(
            """
            SELECT eqTrue, eqFalse, eqSkip, graps
            FROM stats WHERE Id == (?) 
            """, (data)
        ).fetchall()
    
    def user_graphic_update(self, data: str) -> None:
        self.cursor.execute(
            """
            UPDATE stats
            SET graps = (graps + 1)
            WHERE Id == (?);
            """, (data)
        ), (data)
        self.connect.commit()
