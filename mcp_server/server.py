import os
from fastmcp import FastMCP
import psycopg
from psycopg.rows import dict_row

mcp = FastMCP("travel-notes")

@mcp.tool()
def list_travel_notes(limit: int = 20) -> list[dict]:
    """Read recent travel notes; never changes database data."""
    with psycopg.connect(os.environ["DATABASE_URL"], row_factory=dict_row) as conn, conn.cursor() as cur:
        cur.execute("SELECT id, name, message, created_at FROM simple_multi_llm.notes ORDER BY id DESC LIMIT %s", (min(max(limit, 1), 50),))
        return [dict(row) for row in cur.fetchall()]

if __name__ == "__main__":
    mcp.run()
