from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.benchling_app_config_option import BenchlingAppConfigOption
from ..types import UNSET, Unset

T = TypeVar("T", bound="BenchlingAppConfigurationPaginatedList")


@attr.s(auto_attribs=True, repr=False)
class BenchlingAppConfigurationPaginatedList:
    """  """

    _configuration: Union[Unset, List[BenchlingAppConfigOption]] = UNSET
    _next_token: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("configuration={}".format(repr(self._configuration)))
        fields.append("next_token={}".format(repr(self._next_token)))
        return "BenchlingAppConfigurationPaginatedList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        configuration: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._configuration, Unset):
            configuration = []
            for configuration_item_data in self._configuration:
                configuration_item = configuration_item_data.to_dict()

                configuration.append(configuration_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if configuration is not UNSET:
            field_dict["configuration"] = configuration
        if next_token is not UNSET:
            field_dict["nextToken"] = next_token

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

        def get_next_token() -> Union[Unset, str]:
            next_token = d.pop("nextToken")
            return next_token

        next_token = get_next_token() if "nextToken" in d else cast(Union[Unset, str], UNSET)

        benchling_app_configuration_paginated_list = cls(
            configuration=configuration,
            next_token=next_token,
        )

        return benchling_app_configuration_paginated_list

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
    def next_token(self) -> str:
        if isinstance(self._next_token, Unset):
            raise NotPresentError(self, "next_token")
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value

    @next_token.deleter
    def next_token(self) -> None:
        self._next_token = UNSET
