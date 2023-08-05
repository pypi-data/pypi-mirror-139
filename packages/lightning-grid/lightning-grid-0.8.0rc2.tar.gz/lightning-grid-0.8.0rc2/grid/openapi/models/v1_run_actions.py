# coding: utf-8

"""
    external/v1/external_session_service.proto

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: version not set
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git

    NOTE
    ----
    standard swagger-codegen-cli for this python client has been modified
    by custom templates. The purpose of these templates is to include
    typing information in the API and Model code. Please refer to the
    main grid repository for more info
"""


import pprint
import re  # noqa: F401
from typing import TYPE_CHECKING

import six

from grid.openapi.configuration import Configuration

if TYPE_CHECKING:
    from datetime import datetime
    from grid.openapi.models import *

class V1RunActions(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'on_build': 'list[str]',
        'on_build_end': 'list[str]',
        'on_build_start': 'list[str]',
        'on_experiment_end': 'list[str]',
        'on_experiment_start': 'list[str]'
    }

    attribute_map = {
        'on_build': 'onBuild',
        'on_build_end': 'onBuildEnd',
        'on_build_start': 'onBuildStart',
        'on_experiment_end': 'onExperimentEnd',
        'on_experiment_start': 'onExperimentStart'
    }

    def __init__(self, on_build: 'list[str]' = None, on_build_end: 'list[str]' = None, on_build_start: 'list[str]' = None, on_experiment_end: 'list[str]' = None, on_experiment_start: 'list[str]' = None, _configuration=None):  # noqa: E501
        """V1RunActions - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._on_build = None
        self._on_build_end = None
        self._on_build_start = None
        self._on_experiment_end = None
        self._on_experiment_start = None
        self.discriminator = None

        if on_build is not None:
            self.on_build = on_build
        if on_build_end is not None:
            self.on_build_end = on_build_end
        if on_build_start is not None:
            self.on_build_start = on_build_start
        if on_experiment_end is not None:
            self.on_experiment_end = on_experiment_end
        if on_experiment_start is not None:
            self.on_experiment_start = on_experiment_start

    @property
    def on_build(self) -> 'list[str]':
        """Gets the on_build of this V1RunActions.  # noqa: E501


        :return: The on_build of this V1RunActions.  # noqa: E501
        :rtype: list[str]
        """
        return self._on_build

    @on_build.setter
    def on_build(self, on_build: 'list[str]'):
        """Sets the on_build of this V1RunActions.


        :param on_build: The on_build of this V1RunActions.  # noqa: E501
        :type: list[str]
        """

        self._on_build = on_build

    @property
    def on_build_end(self) -> 'list[str]':
        """Gets the on_build_end of this V1RunActions.  # noqa: E501

        commands passed to the image builder which are interpreted as RUN commands in a Dockerfile. Executes after installing dependencies from package manager.  # noqa: E501

        :return: The on_build_end of this V1RunActions.  # noqa: E501
        :rtype: list[str]
        """
        return self._on_build_end

    @on_build_end.setter
    def on_build_end(self, on_build_end: 'list[str]'):
        """Sets the on_build_end of this V1RunActions.

        commands passed to the image builder which are interpreted as RUN commands in a Dockerfile. Executes after installing dependencies from package manager.  # noqa: E501

        :param on_build_end: The on_build_end of this V1RunActions.  # noqa: E501
        :type: list[str]
        """

        self._on_build_end = on_build_end

    @property
    def on_build_start(self) -> 'list[str]':
        """Gets the on_build_start of this V1RunActions.  # noqa: E501

        commands passed to the image builder which are interpreted as RUN commands in a Dockerfile. Executes before installing dependencies from package manager.  # noqa: E501

        :return: The on_build_start of this V1RunActions.  # noqa: E501
        :rtype: list[str]
        """
        return self._on_build_start

    @on_build_start.setter
    def on_build_start(self, on_build_start: 'list[str]'):
        """Sets the on_build_start of this V1RunActions.

        commands passed to the image builder which are interpreted as RUN commands in a Dockerfile. Executes before installing dependencies from package manager.  # noqa: E501

        :param on_build_start: The on_build_start of this V1RunActions.  # noqa: E501
        :type: list[str]
        """

        self._on_build_start = on_build_start

    @property
    def on_experiment_end(self) -> 'list[str]':
        """Gets the on_experiment_end of this V1RunActions.  # noqa: E501

        on_experiment_end allows users to specify commands that need to be executed sequentially after the main experiment process ends. This command will be executed on every experiment that the run creates.  # noqa: E501

        :return: The on_experiment_end of this V1RunActions.  # noqa: E501
        :rtype: list[str]
        """
        return self._on_experiment_end

    @on_experiment_end.setter
    def on_experiment_end(self, on_experiment_end: 'list[str]'):
        """Sets the on_experiment_end of this V1RunActions.

        on_experiment_end allows users to specify commands that need to be executed sequentially after the main experiment process ends. This command will be executed on every experiment that the run creates.  # noqa: E501

        :param on_experiment_end: The on_experiment_end of this V1RunActions.  # noqa: E501
        :type: list[str]
        """

        self._on_experiment_end = on_experiment_end

    @property
    def on_experiment_start(self) -> 'list[str]':
        """Gets the on_experiment_start of this V1RunActions.  # noqa: E501

        on_experiment_start allows users to specify commands that need to be executed sequentially before the main experiment process starts. This command will be executed on every experiment that the run creates.  # noqa: E501

        :return: The on_experiment_start of this V1RunActions.  # noqa: E501
        :rtype: list[str]
        """
        return self._on_experiment_start

    @on_experiment_start.setter
    def on_experiment_start(self, on_experiment_start: 'list[str]'):
        """Sets the on_experiment_start of this V1RunActions.

        on_experiment_start allows users to specify commands that need to be executed sequentially before the main experiment process starts. This command will be executed on every experiment that the run creates.  # noqa: E501

        :param on_experiment_start: The on_experiment_start of this V1RunActions.  # noqa: E501
        :type: list[str]
        """

        self._on_experiment_start = on_experiment_start

    def to_dict(self) -> dict:
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(V1RunActions, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1RunActions') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1RunActions):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other: 'V1RunActions') -> bool:
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1RunActions):
            return True

        return self.to_dict() != other.to_dict()
