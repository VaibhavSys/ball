import time
import psycopg2


def _warn_is_valid(
    cursor: psycopg2.extensions.cursor,
    warn_id: int
):
    """
    Check for checking if the warn ID is valid.
    """
    cursor.execute(f"SELECT * FROM warns WHERE warn_id = {warn_id}")
    warn = cursor.fetchone()
    if not warn:
        return "InvalidWarn"


def _guild_match(
    cursor: psycopg2.extensions.cursor,
    warn_id: int,
    guild_id_invoker: int
):
    """
    Check to see if the guild ID of the command invoker and the guild ID
    of the warn being accessed are the same.
    """
    cursor.execute(f"SELECT * FROM warns WHERE warn_id = {warn_id}")
    warn = cursor.fetchone()
    if warn[3] != guild_id_invoker:
        return "GuildNoMatch"


def _warn_count(
    cursor: psycopg2.extensions.cursor,
    user_id: int,
    guild_id_invoker: int
):
    """
    Get the warn count for a member in a guild.
    """
    cursor.execute(f"""SELECT * FROM warns WHERE user_id = {user_id}
        AND guild_id = {guild_id_invoker};""")
    warns_count = cursor.fetchall()
    warns = 0
    for warn in warns_count:
        warns += 1
    return warns


def add_warn(
    cursor: psycopg2.extensions.cursor,
    user_id: int,
    moderator_id: int,
    guild_id: int,
    time: float,
    reason: str = None
):
    """
    Add warn to a member.
    """
    sql = f"""INSERT INTO warns(user_id, moderator_id, guild_id, time, reason)
    VALUES ({user_id}, {moderator_id}, {guild_id}, {time}, '{reason}');"""
    cursor.execute(sql)
    cursor.execute("SELECT warn_id FROM warns ORDER BY warn_id DESC LIMIT 1;")
    return cursor.fetchone()[0]


def remove_warn(
    cursor: psycopg2.extensions.cursor,
    warn_id: int,
    guild_id_invoker: int
):
    """
    Remove warn from a member.
    """
    valid_warn = _warn_is_valid(cursor, warn_id)
    if valid_warn == "InvalidWarn":
        return valid_warn
    guild_match = _guild_match(cursor, warn_id, guild_id_invoker)
    if guild_match == "GuildNoMatch":
        return guild_match

    cursor.execute(f"SELECT guild_id FROM warns WHERE warn_id = {warn_id};")
    guild_id = cursor.fetchone()[0]
    cursor.execute(f"DELETE FROM warns WHERE warn_id = {warn_id};")


def list_warns(
    cursor: psycopg2.extensions.cursor,
    user_id: int,
    guild_id_invoker: int
):
    """
    List all warns of a member in the guild.
    Returns a list of dictionaries.
    """
    cursor.execute(f"""SELECT * FROM warns WHERE user_id = {user_id}
    AND guild_id = {guild_id_invoker};""")
    user_warns = cursor.fetchall()
    warns = []
    for warn in user_warns:
        user_warns_dict = {
            "warn_id": warn[0],
            "user_id": warn[1],
            "moderator_id": warn[2],
            "guild_id": warn[3],
            "time": warn[4],
            "reason": warn[5]
        }
        warns.append(user_warns_dict)

    return warns


def warn_info(
    cursor: psycopg2.extensions.cursor,
    warn_id: int,
    guild_id_invoker: int
):
    """
    Get information about a warning.
    """
    valid_warn = _warn_is_valid(cursor, warn_id)
    if valid_warn == "InvalidWarn":
        return valid_warn
    guild_match = _guild_match(cursor, warn_id, guild_id_invoker)
    if guild_match == "GuildNoMatch":
        return guild_match

    cursor.execute(f"SELECT * FROM warns WHERE warn_id = {warn_id}")
    warn = cursor.fetchone()
    warn_dict = {
        "warn_id": warn[0],
        "user_id": warn[1],
        "moderator_id": warn[2],
        "guild_id": warn[3],
        "time": warn[4],
        "reason": warn[5]
    }
    return warn_dict


if __name__ == "__main__":
    pass
