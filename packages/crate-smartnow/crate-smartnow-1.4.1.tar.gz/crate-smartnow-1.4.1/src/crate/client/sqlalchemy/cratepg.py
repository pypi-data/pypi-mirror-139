from .dialect import CrateDialect, colspecs, TABLE_TYPE_MIN_VERSION, SCHEMA_MIN_VERSION, TYPES_MAP

from sqlalchemy import types as sqltypes
from sqlalchemy.engine import default, reflection
from sqlalchemy.dialects.postgresql.psycopg2 import PGDialect_psycopg2

from .compiler import (
    CrateCompiler,
    CrateTypeCompiler,
    CrateDDLCompiler
)


class CratePGDialect(PGDialect_psycopg2):
    name = 'cratepg'
    driver = 'crate-python'
    statement_compiler = CrateCompiler
    ddl_compiler = CrateDDLCompiler
    type_compiler = CrateTypeCompiler
    supports_native_boolean = True
    colspecs = colspecs
    implicit_returning = True
    client_encoding = "utf8"
    use_native_hstore=True,
    use_native_uuid=True,

    def __init__(self, *args, **kwargs):
        super(PGDialect_psycopg2, self).__init__(*args, **kwargs)
        # currently our sql parser doesn't support unquoted column names that
        # start with _. Adding it here causes sqlalchemy to quote such columns
        self.identifier_preparer.illegal_initial_characters.add('_')

    def initialize(self, connection):
        # get lowest server version
        # self.server_version_info = \
        #     self._get_server_version_info(connection)
        # get default schema name
        self.default_schema_name = \
            self._get_default_schema_name(connection)

    def do_rollback(self, connection):
        # if any exception is raised by the dbapi, sqlalchemy by default
        # attempts to do a rollback crate doesn't support rollbacks.
        # implementing this as noop seems to cause sqlalchemy to propagate the
        # original exception to the user
        pass

    # def connect(self, host=None, port=None, *args, **kwargs):
    #     server = None
    #     if host:
    #         server = '{0}:{1}'.format(host, port or '4200')
    #     if 'servers' in kwargs:
    #         server = kwargs.pop('servers')
    #     if server:
    #         return self.dbapi.connect(servers=server, **kwargs)
    #     return self.dbapi.connect(**kwargs)

    def connect(self, *cargs, **cparams):
        # inherits the docstring from interfaces.Dialect.connect
        return self.dbapi.connect(*cargs, **cparams)

    def _get_default_schema_name(self, connection):
        return 'doc'

    def _get_server_version_info(self, connection):
        return tuple(connection.connection.lowest_server_version.version)

    @classmethod
    def dbapi(cls):
        # from crate import client
        # return client
        import psycopg2Crate

        return psycopg2Crate

    @classmethod
    def _psycopg2_extensions(cls):
        from psycopg2Crate import extensions

        return extensions

    @classmethod
    def _psycopg2_extras(cls):
        from psycopg2Crate import extras

        return extras

    def has_schema(self, connection, schema):
        return schema in self.get_schema_names(connection)

    def has_table(self, connection, table_name, schema=None):
        return table_name in self.get_table_names(connection, schema=schema)

    @reflection.cache
    def get_schema_names(self, connection, **kw):
        cursor = connection.execute(
            "select schema_name "
            "from information_schema.schemata "
            "order by schema_name asc"
        )
        return [row[0] for row in cursor.fetchall()]

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        table_filter = "AND table_type = 'BASE TABLE' " \
            if self.server_version_info >= TABLE_TYPE_MIN_VERSION else ""
        cursor = connection.execute(
            "SELECT table_name FROM information_schema.tables "
            "WHERE {0} = ? {1}"
            "ORDER BY table_name ASC, {0} ASC".format(self.schema_column,
                                                      table_filter),
            [schema or self.default_schema_name]
        )
        return [row[0] for row in cursor.fetchall()]

    @reflection.cache
    def get_columns(self, connection, table_name, schema=None, **kw):
        query = "SELECT column_name, data_type " \
                "FROM information_schema.columns " \
                "WHERE table_name = ? AND {0} = ? " \
                "AND column_name !~ ?" \
            .format(self.schema_column)
        cursor = connection.execute(
            query,
            [table_name,
             schema or self.default_schema_name,
             r"(.*)\[\'(.*)\'\]"]  # regex to filter subscript
        )
        return [self._create_column_info(row) for row in cursor.fetchall()]

    @reflection.cache
    def get_pk_constraint(self, engine, table_name, schema=None, **kw):
        if self.server_version_info >= (2, 3, 0):
            query = """SELECT column_name
                    FROM information_schema.key_column_usage
                    WHERE table_name = ? AND table_catalog = ?"""

            def result_fun(result):
                rows = result.fetchall()
                return list(set(map(lambda el: el[0], rows)))
        else:
            query = """SELECT constraint_name
                   FROM information_schema.table_constraints
                   WHERE table_name = ? AND {schema_col} = ?
                   AND constraint_type='PRIMARY_KEY'
                   """.format(schema_col=self.schema_column)

            def result_fun(result):
                rows = result.fetchone()
                return set(rows[0] if rows else [])

        pk_result = engine.execute(
            query,
            [table_name, schema or self.default_schema_name]
        )
        pks = result_fun(pk_result)
        return {'constrained_columns': pks,
                'name': 'PRIMARY KEY'}

    @reflection.cache
    def get_foreign_keys(self, connection, table_name, schema=None,
                         postgresql_ignore_search_path=False, **kw):
        # Crate doesn't support Foreign Keys, so this stays empty
        return []

    @reflection.cache
    def get_indexes(self, connection, table_name, schema, **kw):
        return []

    @property
    def schema_column(self):
        return "table_schema" \
            if self.server_version_info >= SCHEMA_MIN_VERSION \
            else "schema_name"

    def _create_column_info(self, row):
        return {
            'name': row[0],
            'type': self._resolve_type(row[1]),
            # In Crate every column is nullable except PK
            # Primary Key Constraints are not nullable anyway, no matter what
            # we return here, so it's fine to return always `True`
            'nullable': True
        }

    def _resolve_type(self, type_):
        return TYPES_MAP.get(type_, sqltypes.UserDefinedType)
