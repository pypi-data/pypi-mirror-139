from typing import Any

from .base import BIT, MySQLDialect, MySQLExecutionContext

class _oursqlBIT(BIT):
    def result_processor(self, dialect, coltype) -> None: ...

class MySQLExecutionContext_oursql(MySQLExecutionContext):
    @property
    def plain_query(self): ...

class MySQLDialect_oursql(MySQLDialect):
    driver: str
    supports_statement_cache: bool
    supports_unicode_binds: bool
    supports_unicode_statements: bool
    supports_native_decimal: bool
    supports_sane_rowcount: bool
    supports_sane_multi_rowcount: bool
    colspecs: Any
    @classmethod
    def dbapi(cls): ...
    def do_execute(self, cursor, statement, parameters, context: Any | None = ...) -> None: ...
    def do_begin(self, connection) -> None: ...
    def do_begin_twophase(self, connection, xid) -> None: ...
    def do_prepare_twophase(self, connection, xid) -> None: ...
    def do_rollback_twophase(self, connection, xid, is_prepared: bool = ..., recover: bool = ...) -> None: ...
    def do_commit_twophase(self, connection, xid, is_prepared: bool = ..., recover: bool = ...) -> None: ...
    def has_table(self, connection, table_name, schema: Any | None = ...): ...  # type: ignore[override]
    def get_table_options(self, connection, table_name, schema: Any | None = ..., **kw): ...
    def get_columns(self, connection, table_name, schema: Any | None = ..., **kw): ...
    def get_view_names(self, connection, schema: Any | None = ..., **kw): ...
    def get_table_names(self, connection, schema: Any | None = ..., **kw): ...
    def get_schema_names(self, connection, **kw): ...
    def initialize(self, connection): ...
    def is_disconnect(self, e, connection, cursor): ...
    def create_connect_args(self, url): ...

dialect = MySQLDialect_oursql
