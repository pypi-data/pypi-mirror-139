"""
BigQuery Data Warehouse classes
"""

import logging
import os
from typing import List, Union

import json
import pandas as pd

from rasgoql.data.base import DataWarehouse, DWCredentials
from rasgoql.errors import (
    DWCredentialsWarning, DWConnectionError, DWQueryError,
    ParameterException, PackageDependencyWarning,
    SQLWarning, TableAccessError, TableConflictException
)
from rasgoql.imports import bq, gcp_exc, gcp_flow, gcp_svc
from rasgoql.primitives.enums import (
    check_bq_creds_type, check_response_type,
    check_table_type, check_write_method
)
from rasgoql.utils.creds import load_env, save_env
from rasgoql.utils.df import cleanse_sql_dataframe
from rasgoql.utils.messaging import verbose_message
from rasgoql.utils.sql import (
    is_scary_sql, magic_fqtn_handler,
    parse_fqtn, parse_namespace,
    validate_namespace
)

logging.basicConfig()
logger = logging.getLogger('BigQuery DataWarehouse')
logger.setLevel(logging.INFO)


class BigQueryCredentials(DWCredentials):
    """
    BigQuery Credentials
    """
    dw_type = 'bigquery'

    def __init__(
            self,
            secret_type: str,
            secret_filepath: str,
            project: str = None,
            dataset: str = None
        ):
        self.secret_type = check_bq_creds_type(secret_type)
        self.secret_filepath = secret_filepath
        self.project = project
        self.dataset = dataset

    def __repr__(self) -> str:
        return json.dumps(
            {
                "secret_type": self.secret_type,
                "secret_filepath": self.secret_filepath,
                "project": self.project,
                "dataset": self.dataset
            }
        )

    @classmethod
    def from_env(
            cls,
            filepath: str = None
        ) -> 'BigQueryCredentials':
        """
        Creates an instance of this Class from a .env file on your machine
        """
        load_env(filepath)
        if not all([
                os.getenv('bigquery_secret_type'),
                os.getenv('bigquery_secret_filepath'),
                os.getenv('bigquery_project'),
                os.getenv('bigquery_dataset')
        ]):
            raise DWCredentialsWarning(
                'Your env file is missing expected credentials. Consider running '
                'BigQueryCredentials(*args).to_env() to repair this.'
            )
        return cls(
            os.getenv('bigquery_secret_type'),
            os.getenv('bigquery_secret_filepath'),
            os.getenv('bigquery_project'),
            os.getenv('bigquery_dataset')
        )

    def to_dict(self) -> dict:
        """
        Returns a dict of the credentials
        """
        return {
            "secret_type": self.secret_type,
            "secret_filepath": self.secret_filepath,
            "project": self.project,
            "dataset": self.dataset
        }

    def to_env(
            self,
            filepath: str = None,
            overwrite: bool = False
        ):
        """
        Saves credentials to a .env file on your machine
        """
        creds = {
            "bigquery_secret_type": self.secret_type,
            "bigquery_secret_filepath": self.secret_filepath,
            "bigquery_project": self.project,
            "bigquery_dataset": self.dataset,
        }
        return save_env(creds, filepath, overwrite)


class BigQueryDataWarehouse(DataWarehouse):
    """
    Google BigQuery DataWarehouse
    """
    dw_type = 'bigquery'
    credentials_class = BigQueryCredentials

    def __init__(self):
        if bq is None:
            raise PackageDependencyWarning(
                'Missing a required python package to run BigQuery. '
                'Please download the BigQuery package by running: '
                'pip install rasgoql[bigquery]')

        super().__init__()
        self.credentials: dict = None
        self.connection: bq.Client = None
        self.default_project = None
        self.default_dataset = None

    # ---------------------------
    # Core Data Warehouse methods
    # ---------------------------
    def change_namespace(
            self,
            namespace: str
        ) -> None:
        """
        Changes the default namespace of your connection

        Params:
        `namespace`: str:
            namespace (project.dataset)
        """
        namespace = self._validate_namespace(namespace)
        project, dataset = parse_namespace(namespace)
        try:
            self.execute_query(f'USE PROJECT {project}')
            self.execute_query(f'USE DATASET {dataset}')
            self.default_namespace = namespace
            self.default_project = project
            self.default_dataset = dataset
            verbose_message(
                f"Namespace reset to {self.default_namespace}",
                logger
            )
        except Exception as e:
            self._error_handler(e)

    def connect(
            self,
            credentials: Union[dict, BigQueryCredentials]
        ):
        """
        Connect to BigQuery

        Params:
        `credentials`: dict:
            dict (or DWCredentials class) holding the connection credentials
        """
        if isinstance(credentials, BigQueryCredentials):
            credentials = credentials.to_dict()

        try:
            self.default_project = credentials.get('project')
            self.default_dataset = credentials.get('dataset')
            if credentials.get('secret_type') == 'SERVICE':
                self.credentials = self._get_service_credentials(
                    credentials.get('secret_filepath')
                )
            else:
                self.credentials = self._get_appflow_credentials(
                    credentials.get('secret_filepath')
                )
            self.connection = bq.Client(
                credentials=self.credentials,
                project=self.default_project
            )
            verbose_message(
                "Connected to BigQuery",
                logger
            )
        except Exception as e:
            self._error_handler(e)

    def close_connection(self):
        """
        Close connection to BigQuery
        """
        try:
            if self.connection:
                self.connection.close()
            self.connection = None
            verbose_message(
                "Connection to BigQuery closed",
                logger
            )
        except Exception as e:
            self._error_handler(e)

    def create(
            self,
            sql: str,
            fqtn: str,
            table_type: str = 'VIEW',
            overwrite: bool = False
        ):
        """
        Create a view or table from given SQL

        Params:
        `sql`: str:
            query that returns data (i.e. can be wrapped in a CREATE TABLE statement)
        `fqtn`: str:
            Fully-qualified table name (database.schema.table)
            Name for the new table
        `table_type`: str:
            One of values: [view, table]
        `overwrite`: bool
            pass True when this table name already exists in your DataWarehouse
            and you know you want to overwrite it
            WARNING: This will completely overwrite data in the existing table
        """
        table_type = check_table_type(table_type)
        fqtn = magic_fqtn_handler(fqtn, self.default_namespace)
        if self._table_exists(fqtn) and not overwrite:
            msg = f'A table or view named {fqtn} already exists. ' \
                   'If you are sure you want to overwrite it, ' \
                   'pass in overwrite=True and run this function again'
            raise TableConflictException(msg)
        query = f'CREATE OR REPLACE {table_type} {fqtn} AS {sql}'
        self.execute_query(query, acknowledge_risk=True, response='None')
        return fqtn

    @property
    def default_namespace(self) -> str:
        """
        Returns the default project.dataset of this connection
        """
        return f'{self.default_project}.{self.default_dataset}'

    def execute_query(
            self,
            sql: str,
            response: str = 'tuple',
            acknowledge_risk: bool = False
        ):
        """
        Run a query against BigQuery and return all results

        `sql`: str:
            query text to execute
        `response`: str:
            Possible values: [dict, df, None]
        `acknowledge_risk`: bool:
            pass True when you know your SQL statement contains
            a potentially dangerous or data-altering operation
            and still want to run it against your DataWarehouse
        """
        response = check_response_type(response)
        if is_scary_sql(sql) and not acknowledge_risk:
            msg = 'It looks like your SQL statement contains a ' \
                  'potentially dangerous or data-altering operation.' \
                  'If you are positive you want to run this, ' \
                  'pass in acknowledge_risk=True and run this function again.'
            raise SQLWarning(msg)
        verbose_message(
            f"Executing query: {sql}",
            logger
        )
        if response == 'DICT':
            raise NotImplementedError("BigQuery doesn't do that")
        if response == 'DF':
            return self._query_into_pandas(sql)
        return self._execute_string(sql, ignore_results=(response == 'NONE'))

    def get_ddl(
            self,
            fqtn: str
        ) -> str:
        """
        Returns the create statement for a table or view

        `fqtn`: str:
            Fully-qualified Table Name (database.schema.table)
        """
        fqtn = magic_fqtn_handler(fqtn, self.default_namespace)
        proj, ds, tbl = parse_fqtn(fqtn)
        sql = f"SELECT DDL FROM {proj}.{ds}.INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='{tbl}'"
        query_response = self.execute_query(sql)
        return query_response[0]

    def get_object_details(
            self,
            fqtn: str
        ) -> tuple:
        """
        Return details of a table or view in BigQuery

        Params:
        `fqtn`: str:
            Fully-qualified table name (database.schema.table)

        Response:
            object exists: bool
            is rasgo object: bool
            object type: [table|view|unknown]
        """
        fqtn = magic_fqtn_handler(fqtn, self.default_namespace)
        obj_exists = False
        is_rasgo_obj = False
        obj_type = 'unknown'
        try:
            table = self.connection.get_table(fqtn)
            obj_exists = True
            obj_type = table.table_type
            if table.labels:
                for label, value in table.labels.items():
                    if value == 'rasgoql':
                        is_rasgo_obj = True
            return obj_exists, is_rasgo_obj, obj_type
        except gcp_exc.NotFound:
            return obj_exists, is_rasgo_obj, obj_type

    def get_schema(
            self,
            fqtn: str
        ) -> dict:
        """
        Return the schema of a table or view

        Params:
        `fqtn`: str:
            Fully-qualified table name (database.schema.table)
        """
        fqtn = magic_fqtn_handler(fqtn, self.default_namespace)
        try:
            table = self.connection.get_table(fqtn)
            return table.schema
        except Exception as e:
            self._error_handler(e)

    def list_tables(
            self,
            database: str = None,
            schema: str = None
        ) -> pd.DataFrame:
        """
        List all tables and views available in default namespace

        Params:
        `database`: str:
            override database
        `schema`: str:
            override schema
        """
        project = database or self.default_project
        dataset = schema or self.default_dataset
        namespace = f'{project}.{dataset}'
        try:
            tables = self.connection.list_tables(namespace)
            records = []
            columns = [
                'TABLE_NAME',
                'FQTN',
                'TABLE_TYPE',
                'ROW_COUNT',
                'CREATED',
                'LAST_ALTERED'
            ]
            for tbl in tables:
                # TODO: This may be inefficient - do we need to return all this data?
                table = self.connection.get_table(tbl)
                records.append(
                    (
                        table.table_id,
                        f'{table.project}.{table.dataset_id}.{table.table_id}',
                        table.table_type,
                        table.num_rows,
                        table.created,
                        table.modified
                    )
                )
            return pd.DataFrame(
                records,
                columns=columns
            )
        except Exception as e:
            self._error_handler(e)

    def preview(
            self,
            sql: str,
            limit: int = 10
        ) -> pd.DataFrame:
        """
        Returns 10 records into a pandas DataFrame

        Params:
        `sql`: str:
            SQL statment to run
        `limit`: int:
            Records to return
        """
        return self.execute_query(
            f'{sql} LIMIT {limit}',
            response='df',
            acknowledge_risk=True
        )

    def save_df(
            self,
            df: pd.DataFrame,
            fqtn: str,
            method: str = None
        ):
        """
        Creates a table in BigQuery from a pandas Dataframe

        Params:
        `df`: pandas DataFrame:
            DataFrame to upload
        `fqtn`: str:
            Fully-qualied table name (database.schema.table)
            Name for the new table
        `overwrite`: bool
            pass True when this table name already exists in your DataWarehouse
            and you know you want to overwrite it
            WARNING: This will completely overwrite data in the existing table
        """
        if method:
            method = check_write_method(method)
        fqtn = magic_fqtn_handler(fqtn, self.default_namespace)
        table_exists = self._table_exists(fqtn)
        if table_exists and not method:
            msg = f"A table named {fqtn} already exists. " \
                   "If you are sure you want to write over it, pass in " \
                   "method='append' or method='replace' and run this function again"
            raise TableConflictException(msg)
        try:
            cleanse_sql_dataframe(df)
            # TODO: Test write_disposition to handle overwrite vs append
            job_config = bq.LoadJobConfig(
                write_disposition='WRITE_TRUNCATE' if method == 'REPLACE' else None,
                default_dataset=self.default_namespace
            )
            job = self.connection.load_table_from_dataframe(
                df,
                fqtn,
                job_config=job_config
            )
            # Wait for the job to complete
            #job.result()
        except Exception as e:
            self._error_handler(e)


    # ---------------------------
    # Core Data Warehouse helpers
    # ---------------------------
    def _table_exists(
            self,
            fqtn: str
        ) -> bool:
        """
        Check for existence of fqtn in the Data Warehouse and return a boolean

        Params:
        `fqtn`: str:
            Fully-qualified table name (database.schema.table)
        """
        fqtn = magic_fqtn_handler(fqtn, self.default_namespace)
        try:
            self.connection.get_table(fqtn)
            return True
        except gcp_exc.NotFound:
            return False

    def _validate_namespace(
            self,
            namespace: str
        ):
        """
        Checks a namespace string for compliance with BigQuery format

        Params:
        `namespace`: str:
            namespace (project.dataset)
        """
        # Does this match a 'string.string' pattern?
        try:
            validate_namespace(namespace)
            return namespace
        except ValueError:
            raise ParameterException("Bigquery namespaces should be format: PROJECT.DATASET")

    # --------------------------
    # BigQuery specific helpers
    # --------------------------
    @property
    def _default_job_config(self) -> 'bq.QueryJobConfig':
        return bq.QueryJobConfig(
            default_dataset=self.default_namespace
            )

    def _error_handler(
            self,
            exception: Exception,
            query: str = None
        ) -> None:
        """
        Handle Snowflake exceptions that need additional info
        """
        verbose_message(
            f'Exception occurred while running query: {query}',
            logger
        )
        if exception is None:
            return
        if isinstance(exception, gcp_exc.NotFound):
            raise TableAccessError('Table does not exist')
        if isinstance(exception, gcp_exc.ServiceUnavailable):
            raise DWConnectionError('Service is not available')
        raise exception

    def _execute_string(
            self,
            query: str,
            ignore_results: bool = False
        ) -> List[tuple]:
        """
        Execute a query string against the DataWarehouse connection and fetch all results
        """
        try:
            query_job = self.connection.query(
                query,
                job_config=self._default_job_config
            )
            if ignore_results:
                return
            return list(query_job.result())
        except Exception as e:
            self._error_handler(e)

    def _get_appflow_credentials(
            self,
            filepath: str
        ):
        try:
            appflow = gcp_flow.InstalledAppFlow.from_client_secrets_file(
                filepath,
                scopes=["https://www.googleapis.com/auth/bigquery"]
            )
            appflow.run_local_server()
            #appflow.run_console()
            return appflow.credentials
        except Exception as e:
            self._error_handler(e)

    def _get_service_credentials(
            self,
            filepath: str
        ):
        try:
            credentials = gcp_svc.Credentials.from_service_account_file(
                filepath,
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            return credentials
        except Exception as e:
            self._error_handler(e)

    def _query_into_pandas(
            self,
            query: str
    ) -> pd.DataFrame:
        """
        Return results of query in a pandas DataFrame
        """
        try:
            return self.connection.query(
                query,
                job_config=self._default_job_config
                ) \
                .result() \
                .to_dataframe()
        except Exception as e:
            self._error_handler(e)
