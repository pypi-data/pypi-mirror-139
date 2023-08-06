import sqlite3
from docdb.collection import Collection
from docdb.exceptions import CollectionDoesNotExist

class Engine:
    """ the lightweight document engine """

    def __init__(self, database_name: str):
        # NOTE: this will automatically create the database file if it doesn't exist.
        self.db_name = database_name
        self.conn = sqlite3.connect(database_name)

    @property
    def collections(self):
        cur = self.conn.cursor()
        return [x[0] for x in cur.execute(""" SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '%_meta';""")]

    def collection(self, collection_name: str, pk: str = None):
        """ create a new collection """
        # TODO: add validation to the collection name
        # only alphanum w/ _ or - are allowed
        cur = self.conn.cursor()
        if collection_name not in self.collections:
            cur.execute(f"""
            CREATE TABLE {collection_name} (
                uuid BLOB NOT NULL PRIMARY KEY
            , body TEXT
            , date_created INTEGER
            , date_updated INTEGER
            , size INTEGER GENERATED ALWAYS AS (length(body)) STORED
            );
            """)
            cur.execute(f"""
            CREATE TABLE {collection_name}_meta (
                uuid BLOB NOT NULL
            , is_pk INTEGER NOT NULL
            , "key" TEXT NOT NULL
            , "type" TEXT NOT NULL
            , value_str TEXT NULL
            , value_int INTEGER NULL
            , value_real REAL NULL
            , composite TEXT NOT NULL
            , date_created INTEGER NOT NULL
            , date_updated INTEGER NOT NULL
            , UNIQUE(composite)
            );
            """)
            self.conn.commit()
        return Collection(self.db_name, collection_name, pk)
    
    def delete_collection(self, collection_name: str):
        """ delete the entire collection (HARD DELETE) """
        try:
            cur = self.conn.cursor()
            cur.execute(f"DROP TABLE {collection_name};")
            cur.execute(f"DROP TABLE {collection_name}_meta;")
            return True
        except sqlite3.OperationalError as e:
            if "no such table:" in str(e):
                raise CollectionDoesNotExist
