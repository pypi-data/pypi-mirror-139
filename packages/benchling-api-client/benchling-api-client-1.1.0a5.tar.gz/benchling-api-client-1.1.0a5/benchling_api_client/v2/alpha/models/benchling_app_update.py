from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.benchling_app_config_option import BenchlingAppConfigOption
from ..types import UNSET, Unset

T = TypeVar("T", bound="BenchlingAppUpdate")


@attr.s(auto_attribs=True, repr=False)
class BenchlingAppUpdate:
    """  """

    _configuration: Union[Unset, List[BenchlingAppConfigOption]] = UNSET
    _description: Union[Unset, str] = UNSET
    _name: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("configuration={}".format(repr(self._configuration)))
        fields.append("description={}".format(repr(self._description)))
        fields.append("name={}".format(repr(self._name)))
        return "BenchlingAppUpdate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        configuration: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._configuration, Unset):
            configuration = []
            for configuration_item_data in self._configuration:
                configuration_item = configuration_item_data.to_dict()

                configuration.append(configuration_item)

        description = self._description
        name = self._name

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if configuration is not UNSET:
            field_dict["configuration"] = configuration
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def get_configuration() -> Union[Unset, List[BenchlingAppConfigOption]]:
            configuration = []
            _configuration = d.pop("configuration")
            for configuration_item_data in _configuration or []:
                configuration_item = BenchlingAppConfigOption.from_dict(configuration_item_data)

                configuration.append(configuration_item)

            return configuration

        configuration = (
            get_configuration()
            if "configuration" in d
            else cast(Union[Unset, List[BenchlingAppConfigOption]], UNSET)
        )

        def get_description() -> Union[Unset, str]:
            description = d.pop("description")
            return description

        description = get_description() if "description" in d else cast(Union[Unset, str], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        name = get_name() if "name" in d else cast(Union[Unset, str], UNSET)

        benchling_app_update = cls(
            configuration=configuration,
            description=description,
            name=name,
        )

        return benchling_app_update

    @property
    def configuration(self) -> List[BenchlingAppConfigOption]:
        if isinstance(self._configuration, Unset):
            raise NotPresentError(self, "configuration")
        return self._configuration

    @configuration.setter
    def configuration(self, value: List[BenchlingAppConfigOption]) -> None:
        self._configuration = value

    @configuration.deleter
    def configuration(self) -> None:
        self._configuration = UNSET

    @property
    def description(self) -> str:
        if isinstance(self._description, Unset):
            raise NotPresentError(self, "description")
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @description.deleter
    def description(self) -> None:
        self._description = UNSET

    @property
    def name(self) -> str:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = UNSET
