from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ResourceDependencyTypes(Enums.KnownString):
    AA_SEQUENCE = "aa-sequence"
    ASSAY_RESULT = "assay-result"
    ASSAY_RUN = "assay-run"
    AUTOMATION_INPUT_GENERATOR = "automation-input-generator"
    AUTOMATION_OUTPUT_PROCESSOR = "automation-output-processor"
    BLOB = "blob"
    BOX = "box"
    CONTAINER = "container"
    CUSTOM_ENTITY = "custom-entity"
    DNA_ALIGNMENT = "dna-alignment"
    DNA_OLIGO = "dna-oligo"
    DNA_SEQUENCE = "dna-sequence"
    ENTRY = "entry"
    FOLDER = "folder"
    LABEL_PRINTER = "label-printer"
    LABEL_TEMPLATE = "label-template"
    LOCATION = "location"
    PLATE = "plate"
    PROJECT = "project"
    REGISTRY = "registry"
    REQUEST = "request"
    WORKFLOW_TASK_GROUP = "workflow task group"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ResourceDependencyTypes":
        if not isinstance(val, str):
            raise ValueError(f"Value of ResourceDependencyTypes must be a string (encountered: {val})")
        newcls = Enum("ResourceDependencyTypes", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ResourceDependencyTypes, getattr(newcls, "_UNKNOWN"))
