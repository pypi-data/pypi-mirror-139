#!/usr/bin/env python

"""
This module contains the MDB extension to :class:`Table <agate.table.Table>`.
"""

import datetime
from collections import OrderedDict

import agate
import io
import os
import re
import subprocess


MDB_TO_AGATE_TYPE = {
    # See:
    # - https://github.com/mdbtools/mdbtools/blob/master/src/libmdb/backend.c
    # - https://support.microsoft.com/en-us/office/data-types-for-access-desktop-databases-df2b83ba-cef6-436d-b679-3418f622e482
    'Boolean': agate.Boolean(), # MDB_BOOL
    'Byte': agate.Number(), # MDB_BYTE
    'Integer': agate.Number(), # MDB_INT
    'Long Integer': agate.Number(), # MDB_LONGINT
    'Currency': agate.Number(), # MDB_MONEY
    'Single': agate.Number(), # MDB_FLOAT
    'Double': agate.Number(), # MDB_DOUBLE
    'DateTime': agate.DateTime(), # MDB_DATETIME
# Not every version of agate ships a Blob type, so for now we keep it deactivated
#TODO    'Binary': agate.Blob(), # MDB_BINARY
    'Text': agate.Text(), # MDB_TEXT aka Short Text
#TODO    'OLE': agate.Blob(), # MDB_OLE
    'Memo/Hyperlink': agate.Text(), # MDB_MEMO aka Long Text
    'Replication ID': agate.Number(), # MDB_REPID
    'Numeric': agate.Number(), # MDB_NUMERIC
}


def from_mdb(cls, path, table_name=None, skip_lines=0, header=True, encoding_override=None,
             row_limit=None, column_names=None, column_types=None, **kwargs):
    """
    Parse a Microsoft Access database file.

    :param path:
        Path to a Microsoft Access database file to load.
    :param table_name:
        The names of the tables to load. If not specified
        then it is assumed that the database contains only one table.
    :param skip_lines:
        The number of rows to skip from the top of the table.
    :param encoding_overrides:
        From Access 2000 onwards, database files are UTF-8 encoded and this parameter should not be used.
        It is only useful to define the charset of a JET3 (Access 97) file if different from the default CP1252.
    :param row_limit:
        Limit how many rows of data will be read
    """
    if not isinstance(skip_lines, int):
        raise ValueError('skip_lines argument must be an int')

    if encoding_override is None:
        env = {**os.environ}
    else:
        env = {**os.environ, 'MDB_JET3_CHARSET': encoding_override}


    def get_table_names(f):
        mdb_tables = subprocess.run(
            ['mdb-tables', '-1', f],
            env=env, capture_output=True, text=True,
        )
        mdb_tables.check_returncode()
        tables = mdb_tables.stdout.splitlines()

        return tables

    TABLE_DEF_RE = re.compile(r'CREATE TABLE \[?([^\n]+)\]?\s*\n\s*\((.*?)\);', re.MULTILINE | re.DOTALL)
    COLUMN_DEF_RE = re.compile(r'\s*\[?([^\t]+)\]?\s*(.*?),?\s*')
    TYPE_DEF_RE = re.compile(r'\W+')

    def get_column_types(f, table_name):
        mdb_schema = subprocess.run(
            ['mdb-schema', '-T', table_name, f],
            env=env, capture_output=True, text=True,
        )
        mdb_schema.check_returncode()
        schema_ddl = '\n'.join(l for l in mdb_schema.stdout.splitlines() if l and not l.startswith('-'))

        table_defs = dict(TABLE_DEF_RE.findall(schema_ddl))
        assert len(table_defs) == 1, f"No table definition found for {table_name}"

        column_defs = [
            COLUMN_DEF_RE.fullmatch(column_def)
                for column_def in table_defs[table_name].splitlines()
        ]
        column_defs = {
            match.group(1): tuple(word for word in TYPE_DEF_RE.split(match.group(2)) if word)
                for match in column_defs if match
        }
        agate_column_types = dict()
        for column_name, column_def in column_defs.items():
            mdb_column_type = column_def[0]
            agate_column_types[column_name] = determine_agate_type(mdb_column_type)

        return agate_column_types


    def get_data(f, table_name, **kwargs):
        mdb_export = subprocess.run(
            ['mdb-export', '-D', '%F', '-T', '%F %T', f, table_name],
            env=env, capture_output=True, text=True,
        )
        try:
            mdb_export.check_returncode()
        except subprocess.CalledProcessError:
            # The installed version of mdb-export probably doesn't support -T,
            # so we'll try again without it
            mdb_export = subprocess.run(
                ['mdb-export', '-D', '%F %T', f, table_name],
                env=env, capture_output=True, text=True,
            )
            mdb_export.check_returncode()

        csv_data = mdb_export.stdout
        column_types_detected = get_column_types(f, table_name)
        column_names_detected = list(column_types_detected.keys())

        if column_names is None:
            table_column_names = column_names_detected
        else:
            table_column_names = column_names

        if column_types is None:
            table_column_types = column_types_detected
        elif isinstance(column_types, dict):
            table_column_types = {**column_types_detected, **column_types}
        elif isinstance(column_types, agate.TypeTester):
            table_column_types = agate.TypeTester(
                force={**column_types_detected, **column_types._force},
                limit=column_types._limit,
                types=column_types._possible_types,
            )
        else:
            table_column_types = column_types

        return agate.Table.from_csv(
            io.StringIO(csv_data),
            column_names=table_column_names,
            column_types=table_column_types,
            skip_lines=skip_lines,
            row_limit=row_limit,
            **kwargs,
        )

    available_table_names = get_table_names(path)

    if table_name is None:
        if len(available_table_names) != 1:
            raise KeyError(f"Too many tables found, please specify a table name among {available_table_names}")
        table_name = available_table_names[0]

    multiple = agate.utils.issequence(table_name)
    if multiple:
        table_names = table_name
    else:
        table_names = [table_name]

    tables = OrderedDict()
    for table_name in table_names:
        if table_name not in available_table_names:
            raise KeyError(f"Table '{table_name}' not found")
        tables[table_name] = get_data(path, table_name, **kwargs)

    if multiple:
        return agate.MappedSequence(tables.values(), tables.keys())
    else:
        return tables.popitem()[1]


def determine_agate_type(mdb_type):
    try:
        return MDB_TO_AGATE_TYPE[mdb_type]
    except KeyError:
#TODO        return agate.Blob()
        raise agate.exceptions.DataTypeError(f"Unknown MDB data type: {mdb_column_type}")


agate.Table.from_mdb = classmethod(from_mdb)
