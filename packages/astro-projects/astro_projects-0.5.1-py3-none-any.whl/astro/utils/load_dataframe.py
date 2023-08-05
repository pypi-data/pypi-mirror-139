"""
Copyright Astronomer, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from typing import Optional, Union

from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from pandas import DataFrame
from pandas.io.sql import SQLDatabase
from snowflake.connector import pandas_tools

from astro.sql.operators.temp_hooks import TempSnowflakeHook
from astro.utils.schema_util import set_schema_query


def move_dataframe_to_sql(
    output_table_name,
    conn_id,
    database,
    schema,
    warehouse,
    conn_type,
    df: DataFrame,
    user,
    chunksize,
):
    # Select database Hook based on `conn` type
    hook: Union[PostgresHook, TempSnowflakeHook] = {  # type: ignore
        "postgresql": PostgresHook(postgres_conn_id=conn_id, schema=database),
        "postgres": PostgresHook(postgres_conn_id=conn_id, schema=database),
        "snowflake": TempSnowflakeHook(
            snowflake_conn_id=conn_id,
            database=database,
            schema=schema,
            warehouse=warehouse,
        ),
        "bigquery": BigQueryHook(use_legacy_sql=False, gcp_conn_id=conn_id),
    }.get(conn_type, None)
    if not hook:
        raise ValueError("conn id needs to either snowflake or postgres")
    if database:
        hook.database = database

    schema_query = set_schema_query(
        conn_type=conn_type, hook=hook, schema_id=schema, user=user
    )
    hook.run(schema_query)
    if conn_type == "snowflake":

        db = SQLDatabase(engine=hook.get_sqlalchemy_engine())
        # make columns uppercase to prevent weird errors in snowflake
        df.columns = df.columns.str.upper()
        db.prep_table(
            df,
            output_table_name.lower(),
            schema=schema,
            if_exists="replace",
            index=False,
        )
        pandas_tools.write_pandas(
            hook.get_conn(),
            df,
            output_table_name,
            chunk_size=chunksize,
            quote_identifiers=False,
        )
    elif conn_type == "bigquery":
        df.to_gbq(
            f"{schema}.{output_table_name}",
            if_exists="replace",
            chunksize=chunksize,
            project_id=hook.project_id,
        )
    else:
        df.to_sql(
            output_table_name,
            con=hook.get_sqlalchemy_engine(),
            schema=schema,
            if_exists="replace",
            chunksize=chunksize,
            method="multi",
            index=False,
        )
