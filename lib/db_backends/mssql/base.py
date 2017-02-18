# coding=utf-8

from django.db.backends import *
from django.db.backends.creation import BaseDatabaseCreation
import pymssql


class CursorWrapper(object):
    
    def __init__(self, cursor):
        self.cursor = cursor

    def execute(self, query, args=None):
        query = query.encode('utf-8')

        if args is None:
            return self.cursor.execute(query)
        elif type(args) == dict:
            return self.cursor.execute(query, args)
        else:
            # Перекодируем параметры unicode
            for i in xrange(len(args)):
                var = args[i]
                if type(var) == unicode:
                    args[i] = var.encode('utf-8')

            return self.cursor.execute(query, tuple(args))

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return self.__dict__[attr]
        else:
            return getattr(self.cursor, attr)

    def __iter__(self):
        return iter(self.cursor)


class DatabaseError(Exception):
    pass


class IntegrityError(DatabaseError):
    pass


class DatabaseOperations(BaseDatabaseOperations):
    # quote_name = complain
    pass


class DatabaseClient(BaseDatabaseClient):
    # runshell = complain
    pass


class DatabaseFeatures(BaseDatabaseFeatures):
    empty_fetchmany_value = ()
    update_can_self_select = False
    allows_group_by_pk = True
    related_fields_match_type = True
    allow_sliced_subqueries = False
    has_bulk_insert = True
    has_select_for_update = True
    has_select_for_update_nowait = False
    supports_forward_references = False
    supports_long_model_names = False
    supports_microsecond_precision = False
    supports_regex_backreferencing = False
    supports_date_lookup_using_string = False
    supports_timezones = False
    requires_explicit_null_ordering_when_grouping = True
    allows_primary_key_0 = False
    uses_savepoints = True
    atomic_transactions = False
    can_introspect_foreign_keys = False
    has_zoneinfo_database = False
    supports_transactions = True


class DatabaseCreation(BaseDatabaseCreation):
    # create_test_db = ignore
    # destroy_test_db = ignore
    pass


class DatabaseIntrospection(BaseDatabaseIntrospection):
    # get_table_list = complain
    # get_table_description = complain
    # get_relations = complain
    # get_indexes = complain
    # get_key_columns = complain
    pass

Database = pymssql

class DatabaseWrapper(BaseDatabaseWrapper):
    operators = {}
    Database = Database

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)

        self.features = DatabaseFeatures(self)
        self.ops = DatabaseOperations(self)
        self.client = DatabaseClient(self)
        self.creation = DatabaseCreation(self)
        self.introspection = DatabaseIntrospection(self)
        self.validation = BaseDatabaseValidation(self)

    def is_usable(self):
        try:
            self.connection.cursor().execute("SELECT 1")
        except DatabaseError:
            return False
        else:
            return True

    def _set_autocommit(self, autocommit):
        self.autocommit = autocommit

    def init_connection_state(self):
        cursor = self.connection.cursor()
        cursor.execute('use %s' % self.settings_dict['NAME'])
        cursor.close()

    def get_connection_params(self):
        return {'host': self.settings_dict['HOST'],
                'user': self.settings_dict['USER'],
                'password': self.settings_dict['PASSWORD'],
                'database': self.settings_dict['NAME'],
                'charset': "UTF-8"}

    def create_cursor(self):
        cursor = self.connection.cursor()
        return CursorWrapper(cursor)

    def get_new_connection(self, conn_params):
        return Database.connect(**conn_params)
        
