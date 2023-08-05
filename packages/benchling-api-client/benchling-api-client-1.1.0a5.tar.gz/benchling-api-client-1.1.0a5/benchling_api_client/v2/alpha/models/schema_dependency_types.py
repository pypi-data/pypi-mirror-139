from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class SchemaDependencyTypes(Enums.KnownString):
    ENTITY_SCHEMA = "entity-schema"
    CONTAINER_SCHEMA = "container-schema"
    PLATE_SCHEMA = "plate-schema"
    LOCATION_SCHEMA = "location-schema"
    BOX_SCHEMA = "box-schema"
    ASSAY_RUN_SCHEMA = "assay-run-schema"
    ASSAY_RESULT_SCHEMA = "assay-result-schema"
    REQUEST_SCHEMA = "request-schema"
    ENTRY_SCHEMA = "entry-schema"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "SchemaDependencyTypes":
        if not isinstance(val, str):
            raise ValueError(f"Value of SchemaDependencyTypes must be a string (encountered: {val})")
        newcls = Enum("SchemaDependencyTypes", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(SchemaDependencyTypes, getattr(newcls, "_UNKNOWN"))
