from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass(frozen=True)  # immutable
class SnowflakeTable:
    created_on: datetime
    name: str
    database_name: str
    schema_name: str
    kind: str
    comment: str
    cluster_by: str
    rows: int
    bytes: int
    owner: str
    rentention_time: str # days
    automatic_clustering: str
    search_optimization: str
    is_external: str

    def qualified_name(self):
        return f'{self.database_name}.{self.schema_name}.{self.name}'


@dataclass(frozen=True)
class SnowflakeColumn:
    table_name: str
    schema_name: str
    name: str
    data_type: Dict
    nullable: str  # aka "null?"
    default: str
    kind: str
    expression: str
    comment: str
    database_name: str
    autoincrement: str
