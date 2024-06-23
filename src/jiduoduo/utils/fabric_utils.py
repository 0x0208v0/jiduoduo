import io
from typing import Callable

from fabric2 import Connection
from invoke import UnexpectedExit


def has_command(conn: Connection, command: str) -> bool:
    try:
        conn.run(command)
        return True
    except UnexpectedExit as e:
        return False


def has_curl(conn: Connection) -> bool:
    return has_command(conn=conn, command='curl')


def has_wget(conn: Connection) -> bool:
    return has_command(conn=conn, command='wget')


def has_sudo(conn: Connection) -> bool:
    return has_command(conn=conn, command='sudo')


class StreamFlusher:
    def __init__(self, flush_callback: Callable[[str], None]):
        self.flush_callback = flush_callback
        self.buffer = io.StringIO()

    def write(self, message):
        self.buffer.write(message)

    def flush(self):
        self.flush_callback(self.buffer.getvalue())
