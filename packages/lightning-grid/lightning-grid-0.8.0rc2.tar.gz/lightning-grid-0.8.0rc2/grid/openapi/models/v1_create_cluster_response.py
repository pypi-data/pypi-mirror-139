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

class V1CreateClusterResponse(object):
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
        'id': 'str',
        'name': 'str',
        'spec': 'V1ClusterSpec',
        'status': 'V1ClusterStatus'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'spec': 'spec',
        'status': 'status'
    }

    def __init__(self, id: 'str' = None, name: 'str' = None, spec: 'V1ClusterSpec' = None, status: 'V1ClusterStatus' = None, _configuration=None):  # noqa: E501
        """V1CreateClusterResponse - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._id = None
        self._name = None
        self._spec = None
        self._status = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if spec is not None:
            self.spec = spec
        if status is not None:
            self.status = status

    @property
    def id(self) -> 'str':
        """Gets the id of this V1CreateClusterResponse.  # noqa: E501


        :return: The id of this V1CreateClusterResponse.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: 'str'):
        """Sets the id of this V1CreateClusterResponse.


        :param id: The id of this V1CreateClusterResponse.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self) -> 'str':
        """Gets the name of this V1CreateClusterResponse.  # noqa: E501


        :return: The name of this V1CreateClusterResponse.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: 'str'):
        """Sets the name of this V1CreateClusterResponse.


        :param name: The name of this V1CreateClusterResponse.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def spec(self) -> 'V1ClusterSpec':
        """Gets the spec of this V1CreateClusterResponse.  # noqa: E501


        :return: The spec of this V1CreateClusterResponse.  # noqa: E501
        :rtype: V1ClusterSpec
        """
        return self._spec

    @spec.setter
    def spec(self, spec: 'V1ClusterSpec'):
        """Sets the spec of this V1CreateClusterResponse.


        :param spec: The spec of this V1CreateClusterResponse.  # noqa: E501
        :type: V1ClusterSpec
        """

        self._spec = spec

    @property
    def status(self) -> 'V1ClusterStatus':
        """Gets the status of this V1CreateClusterResponse.  # noqa: E501


        :return: The status of this V1CreateClusterResponse.  # noqa: E501
        :rtype: V1ClusterStatus
        """
        return self._status

    @status.setter
    def status(self, status: 'V1ClusterStatus'):
        """Sets the status of this V1CreateClusterResponse.


        :param status: The status of this V1CreateClusterResponse.  # noqa: E501
        :type: V1ClusterStatus
        """

        self._status = status

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
        if issubclass(V1CreateClusterResponse, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1CreateClusterResponse') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1CreateClusterResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other: 'V1CreateClusterResponse') -> bool:
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1CreateClusterResponse):
            return True

        return self.to_dict() != other.to_dict()
