import os
import sqlite3

class Bootstrap:
    """
    Rebuild application from scratch with the following command:
    python -m lib.bootstrap
    """
    def rebuildDB(self):
        path = os.path.join(os.path.dirname(__file__), '../schema.sql')
        schema = open(path).read()
        if os.path.exists('tmp.db'):
            os.unlink('tmp.db')
        conn = sqlite3.connect('tmp.db')
        c = conn.cursor()
        c.executescript(schema)
        conn.commit()
        conn.close()
        
if __name__ == '__main__':
    b = Bootstrap()
    b.rebuildDB()