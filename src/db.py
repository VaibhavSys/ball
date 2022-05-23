import psycopg2

connect = psycopg2.connect

def add_warn(
    cursor: psycopg2.extensions.cursor,
    user_id: int,
    moderator_id: int,
    reason: str = None
    ):
    sql = f"INSERT INTO warns(user_id, moderator_id, reason) VALUES ({user_id}, {moderator_id}, '{reason}');"
    cursor.execute(sql)


def delete_warn(
    cursor: psycopg2.extensions.cursor,
    warn_id: int
    ):
    sql = f"DELETE FROM warns WHERE warn_id = {warn_id};"
    cursor.execute(sql)


if __name__ == "__main__":
    connection = connect(host="127.0.0.1", database="postgres", user="postgres", password="password")
    cursor = connection.cursor()
    delete_warn(cursor, 3)
    cursor.close()
    connection.commit()
