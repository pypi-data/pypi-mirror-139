from pydoc import doc
import sqlite3
import time
import json
import random
import string
from typing import Iterable, List
from uuid import uuid4, UUID
from docdb.exceptions import *
from sqlite3 import IntegrityError

class Collection:
    """ the collection object """
    def __init__(self, database_name: str, collection_name: str, pk: str = None):
        self.conn = sqlite3.connect(database_name)
        self.name = collection_name
        self.pk = pk

    def _index_pk(self, cur, value, id):
        """ writes the pk to the meta table for the collection """
        now = time.time()
        if type(value) == int or self._isint(value):
            typ = "int"
        elif type(value) == float or self._isfloat(value):
            typ = "real"
        else:
            typ = "str"
        sql = f"INSERT INTO {self.name}_meta(uuid,is_pk,key,type,value_{typ},composite,date_created,date_updated) VALUES (?,?,?,?,?,?,?,?)"
        cur.execute(sql, (id, '1', self.pk, typ, value, f'{self.pk}:{value}', now, now))
    
    def _index_prop(self, cur, key, value, id):
        """ writes the prop to the meta table for the collection """
        now = time.time()
        if type(value) == int or self._isint(value):
            typ = "int"
        elif type(value) == float or self._isfloat(value):
            typ = "real"
        else:
            typ = "str"
        sql = f"INSERT INTO {self.name}_meta(uuid,is_pk,key,type,value_{typ},composite,date_created,date_updated) VALUES (?,?,?,?,?,?,?,?)"
        cur.execute(sql, (id, '0', key, typ, value, f'{self.pk}:{value}:{id}', now, now))
    
    def _delete_pk(self, cur, id):
        """ removes all pk fields associated with a given id """
        sql = f"DELETE FROM {self.name}_meta WHERE uuid = ? AND is_pk = '1'"
        cur.execute(sql, (id,))

    def _delete_props(self, cur, id):
        """ removes all prop fields associated with a given id """
        sql = f"DELETE FROM {self.name}_meta WHERE uuid = ? AND is_pk = '0'"
        cur.execute(sql, (id,))

    def _isfloat(self, x):
        try:
            a = float(x)
        except (TypeError, ValueError):
            return False
        else:
            return True

    def _isint(self, x):
        try:
            a = float(x)
            b = int(a)
        except (TypeError, ValueError):
            return False
        else:
            return a == b
    
    def _is_valid_uuid(self, uuid_to_test):
        try:
            uuid_obj = UUID(uuid_to_test, version=4)
        except ValueError:
            return False
        return str(uuid_obj) == uuid_to_test

    def _statement_to_sql(self, l, key, op, val) -> str:
        """ constructs the sql statement for a query """
        valid_ops = ['lt', 'gt', 'lte', 'gte', 'eq', 'sw', 'ew', 'in', '!sw', '!ew', '!eq', '!in', 'bt', '!bt']
        statement = None
        if type(val) == int or self._isint(val):
            typ = "int"
        elif type(val) == float or self._isfloat(val):
            typ = "real"
        else:
            typ = "str"
        if op not in valid_ops:
            raise InvalidOperator(f"'{op}' is not a valid operator")
        if op == 'lt':
            statement = f"{l}.key = '{key}' AND {l}.value_{typ} < '{val}'"
        elif op == 'gt':
            statement = f"{l}.key = '{key}' AND {l}.value_{typ} > '{val}'"
        elif op == 'lte':
            statement = f"{l}.key = '{key}' AND {l}.value_{typ} <= '{val}'"
        elif op == 'gte':
            statement = f"{l}.key = '{key}' AND {l}.value_{typ} >= '{val}'"
        elif op == 'eq':
            statement = f"{l}.key = '{key}' AND {l}.value_{typ} = '{val}'"
        elif op == '!eq':
            statement = f"{l}.key = '{key}' AND {l}.value_{typ} != '{val}'"
        elif op == 'sw':
            statement = f"{l}.key = '{key}' AND {l}.value_{typ} LIKE '{val}%'"
        elif op == 'ew':
            statement = f"{l}.key = '{key}' AND {l}.value_{typ} LIKE '%{val}'"
        elif op == 'in':
            statement = f"{l}.key = '{key}' AND {l}.value_{typ} LIKE '%{val}%'"
        elif op == '!sw':
            statement = f"{l}.key = '{key}' AND {l}.value_{typ} NOT LIKE '{val}%'"
        elif op == '!ew':
            statement = f"{l}.key = '{key}' AND {l}.value_{typ} NOT LIKE '%{val}'"
        elif op == '!in':
            statement = f"{l}.key = '{key}' AND {l}.value_{typ} NOT LIKE '%{val}%'"
        elif op == 'bt':
            s, e = val.split(',')
            if type(s) == int or self._isint(s):
                typ = "int"
            elif type(s) == float or self._isfloat(s):
                typ = "real"
            else:
                typ = "str"
            statement = f"{l}.key = '{key}' AND {l}.value_{typ} BETWEEN '{s}' AND '{e}'"
        elif op == '!bt':
            s, e = val.split(',')
            if type(s) == int or self._isint(s):
                typ = "int"
            elif type(s) == float or self._isfloat(s):
                typ = "real"
            else:
                typ = "str"
            statement = f"{l}.key = '{key}' AND {l}.value_{typ} NOT BETWEEN '{s.strip()}' AND '{e.strip()}'"
        return statement
    
    def _random_string(self, len: int = 5) -> str:
        """ returns a random string """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(len))

    @property
    def documents(self) -> Iterable[dict]:
        """ iterate over all documents in a collection """
        # TODO: figure out how to improve this for really 
        # large collections.
        cur = self.conn.cursor()
        sql = f"SELECT body FROM {self.name};"
        cur.execute(sql)
        rows = cur.fetchall()
        if len(rows) > 0:
            return [json.loads(x[0]) for x in rows]
        return []

    def get(self, uuid) -> dict:
        """ return a document given its uuid or raise a not found exception """
        cur = self.conn.cursor()
        sql = f""" SELECT body FROM {self.name} WHERE uuid = ?;"""
        cur.execute(sql, (uuid,))
        document = cur.fetchone()
        if document is None:
            raise DocumentNotFound(f"could not find a document with _id '{uuid}'")
        return json.loads(document[0])
    
    def bulk_get(self, uuids: List[str]) -> List[dict]:
        if type(uuids) == list:
            cur = self.conn.cursor()
            id_group = ','.join(f'"{i}"' for i in uuids)
            sql = f"SELECT body FROM {self.name} WHERE uuid IN ({id_group})"
            cur.execute(sql)
            rows = cur.fetchall()
            if len(rows) == 0:
                raise NoDocumentsFound
            return [ json.loads(x[0]) for x in rows ]
        raise NonIterable("you must pass a list of valid UUIDs to bulk_get")
    
    def lookup(self, value) -> dict:
        """ lookup allows fetching a document by its pk """
        cur = self.conn.cursor()
        if type(value) == int or self._isint(value):
            typ = "value_int"
        elif type(value) == float or self._isfloat(value):
            typ = "value_real"
        else:
            typ = "value_str"
        sql = f"SELECT uuid FROM {self.name}_meta WHERE is_pk = '1' AND key = ? AND {typ} = ?;"
        cur.execute(sql, (self.pk, value,))
        id = cur.fetchone()
        if id is None:
            raise DocumentNotFound
        return self.get(id[0])

    def bulk_lookup(self, values: List[any]):
        """ bulk_lookup allows fetching a list of documents by their pk's """
        docs = []
        for value in values:
            docs.append(self.lookup(value))
        return docs

    def insert(self, document: dict, props: List[str] = []) -> dict:
        """ insert a single document into the collection """
        try:
            cur = self.conn.cursor()
            now = time.time()
            if '_id' in document.keys():
                id = document.get('_id')
                if not self._is_valid_uuid(id):
                    raise InvalidDocumentID
            else:
                id = str(uuid4())
                document['_id'] = id
                sql = f"INSERT INTO {self.name} (uuid,body,date_created,date_updated) VALUES (?,?,?,?)"
                cur.execute(sql, (id, json.dumps(document), now, now,))
                self.conn.commit()

            # Handle indexing our PK if it exist
            if self.pk is not None:
                value = document.get(self.pk, None)
                if value is None:
                    raise PKNotInDocument
                cur = self.conn.cursor()
                self._index_pk(cur, value, id)
                self.conn.commit()
            
            # Handle indexing any props if they exist
            if len(props) > 0:
                cur = self.conn.cursor()
                for prop in props:
                    value = document.get(prop, None)
                    if value is not None:
                        self._index_prop(cur, prop, value, id)
                self.conn.commit()

            return {"_id": id}
        except IntegrityError as e:
            if "UNIQUE constraint failed:" in str(e):
                raise DocumentAlreadyExist

    def bulk_insert(self, documents: List[dict], props: List[str] = []) -> dict:
        if type(documents) == list:
            try:
                count = 0
                cur = self.conn.cursor()
                for document in documents:
                    now = time.time()
                    if '_id' in document.keys():
                        id = document.get('_id')
                        if not self._is_valid_uuid(id):
                            raise InvalidDocumentID
                    else:
                        id = str(uuid4())
                        document['_id'] = id
                        sql = f"INSERT INTO {self.name} (uuid,body,date_created,date_updated) VALUES (?,?,?,?)"
                        count += cur.execute(sql, (id, json.dumps(document), now, now,)).rowcount

                    if self.pk is not None:
                        value = document.get(self.pk, None)
                        if value is None:
                            raise PKNotInDocument
                        self._index_pk(cur, value, id)

                    if len(props) > 0:
                        for prop in props:
                            value = document.get(prop, None)
                            if value is not None:
                                self._index_prop(cur, prop, value, id)
                self.conn.commit()
                return {"documents_inserted_count": count}
            except IntegrityError as e:
                if "UNIQUE constraint failed:" in str(e):
                    raise DocumentAlreadyExist
        raise NonIterable("you must provide a list of dictionaries to bulk_insert")

    def update(self, document: dict, props: List[str] = []) -> dict:
        id = document.get('_id', None)
        if id is None:
            raise InvalidDocumentID("the provided document has no _id field")
        cur = self.conn.cursor()
        now = time.time()
        sql = f""" UPDATE {self.name} SET body = ?, date_updated = ? WHERE uuid = ?;"""
        doc = json.dumps(document)
        count = cur.execute(sql, (doc, now, id,)).rowcount
        if self.pk is not None:
            if self.pk not in document.keys():
                raise PKNotInDocument(f"the pk was not found in the document (pk = '{self.pk}')")
            else:
                c = self.conn.cursor()
                self._delete_pk(c, id)
                self.conn.commit()

                val = document.get(self.pk)
                self._index_pk(cur, val, id)

        if len(props) > 0:
            c = self.conn.cursor()
            self._delete_props(cur, id)
            self.conn.commit()
            for prop in props:
                value = document.get(prop, None)
                if value is not None:
                    self._index_prop(cur, prop, value, id)
        self.conn.commit()        
        return {"documents_updated_count": count}

    def bulk_update(self, documents: List[dict], props: List[str] = []) -> dict:
        count = 0
        cur = self.conn.cursor()
        for document in documents:
            id = document.get('_id', None)
            if not id:
                raise InvalidDocumentID(f"the provided document has no _id field: {json.dumps(document)}")
            now = time.time()
            sql = f""" UPDATE {self.name} SET body = ?, date_updated = ? WHERE uuid = ?;"""
            count += cur.execute(sql, (json.dumps(document), now, id,)).rowcount
            if self.pk is not None:
                if self.pk not in document.keys():
                    raise PKNotInDocument(f"the pk was not found in the document (pk = '{self.pk}')")
                else:
                    c = self.conn.cursor()
                    self._delete_pk(c, id)
                    self.conn.commit()

                    val = document.get(self.pk)
                    self._index_pk(cur, val, id)
            
            if len(props) > 0:
                c = self.conn.cursor()
                self._delete_props(cur, id)
                self.conn.commit()
                for prop in props:
                    value = document.get(prop, None)
                    if value is not None:
                        self._index_prop(cur, prop, value, id)

        self.conn.commit()
        return {"documents_updated_count": count}

    def delete(self, id: str) -> dict:
        cur = self.conn.cursor()
        s1 = f"DELETE FROM {self.name} WHERE uuid = ?;"
        s2 = f"DELETE FROM {self.name}_meta WHERE uuid = ?;"
        count = cur.execute(s1, (id,)).rowcount
        cur.execute(s2, (id,))
        self.conn.commit()
        return {"documents_deleted_count": count}

    def bulk_delete(self, uuids: List[str]) -> dict:
        cur = self.conn.cursor()
        args = ','.join(f'"{i}"' for i in uuids)
        count = cur.execute(f"DELETE FROM {self.name} WHERE uuid IN ({args})").rowcount
        cur.execute(f"DELETE FROM {self.name}_meta WHERE uuid IN ({args})")
        self.conn.commit()
        return {"documents_deleted_count": count}
    
    def query(self, exprs: List[str]) -> dict:
        """ a lightweight query interface """
        i = 0
        cur = self.conn.cursor()
        s1 = f"select a.uuid from {self.name}_meta as a"
        s2 = ""
        for expr in exprs:

            if expr != '&' and expr != '|':
                i += 1
                k, o, v = expr.split(':')
                l1 = string.ascii_letters[i]
                l2 = string.ascii_letters[i - 1]
                s1 += f" inner join {self.name}_meta as {l1} on a.uuid = {l1}.uuid"
                s2 += self._statement_to_sql(l2, k, o, v)
            elif expr == '&':
                s2 += " AND "
            elif expr == '|':
                s2 += " OR "

        statement = f"{s1} where {s2}"
        return [json.loads(doc[0]) for doc in cur.execute(f"SELECT body FROM {self.name} WHERE uuid IN ({statement});")]