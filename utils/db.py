import os
import sys

import psycopg2


class SingletonDB(object):
    _cursor = None
    _conn = None
    _is_transaction = False

    @property
    def is_transaction(self):
        return self._is_transaction

    @property
    def conn(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, cursor):
        self._cursor = cursor

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonDB, cls).__new__(cls)
        return cls.instance

    def run_query(self, query):
        if not self.is_transaction:
            self.open_connection()
        try:
            if not self.cursor:
                self._cursor = self.conn.cursor()
            if 'SELECT' in query:
                records = []
                self._cursor.execute(query)
                result = self._cursor.fetchall()
                for row in result:
                    records.append(row)
                if not self.is_transaction:
                    self.cursor.close()
                    self.cursor = None
                return records
            self.cursor.execute(query)
            return self.cursor.rowcount
        except psycopg2.Error as e:
            print('psycopg2.Error', e)
            self.rollback()
            self.cursor.close()
            self.cursor = None
            self._is_transaction = False
            return False

    def open_connection(self):
        try:
            if self.conn is None or self.conn.closed:
                if self.conn is None:
                    self._conn = psycopg2.connect(
                        user=os.environ.get("DB_USER", "admin"),
                        password=os.environ.get("DB_PASSWORD", "1234"),
                        host=os.environ.get("DB_HOST", "localhost"),
                        port=os.environ.get("DB_PORT", "5432"),
                        database=os.environ.get("DB_DATABASE", "CodeChallenges"),
                    )
                    self._cursor = self.conn.cursor()
                elif self.conn.closed:
                    print('reconnecting with db...')
            else:
                print('connecting is already open')
        except psycopg2.Error as error:
            print(error)
            sys.exit()

        finally:
            print('Connection opened successfully.')

    def close_connection(self):
        self._is_transaction = False
        if self.conn:
            if self.cursor:
                self._cursor.close()
            if not self.conn.closed:
                self.conn.close()
            self._conn = None
            print('Database connection closed.')

    def begin_transaction(self):
        self.open_connection()
        self._cursor = self.conn.cursor()
        self._is_transaction = True
        print('Transaction has begin')

    def rollback(self):
        try:
            self.conn.rollback()
            print('rollback has begin made')
        except AttributeError as error:
            print(error)
        finally:
            self._is_transaction = False

    def commit(self):
        self.cursor.close()
        self._cursor = None
        self.conn.commit()
        self._is_transaction = False
        print('commit has begin made')


db = SingletonDB()
