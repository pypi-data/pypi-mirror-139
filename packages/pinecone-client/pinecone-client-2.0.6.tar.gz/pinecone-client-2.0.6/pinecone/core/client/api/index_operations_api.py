#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

"""
    Pinecone API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: version not set
    Contact: support@pinecone.io
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from pinecone.core.client.api_client import ApiClient, Endpoint as _Endpoint
from pinecone.core.client.model_utils import (  # noqa: F401
    check_allowed_values,
    check_validations,
    date,
    datetime,
    file_type,
    none_type,
    validate_and_convert_types
)
from pinecone.core.client.model.create_request import CreateRequest
from pinecone.core.client.model.index_meta import IndexMeta
from pinecone.core.client.model.patch_request import PatchRequest


class IndexOperationsApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

        def __create_index(
            self,
            **kwargs
        ):
            """create_index  # noqa: E501

            This operation creates a Pinecone index. You can use it to specify the measure of similarity, the dimension of vectors to be stored in the index, the numbers of shards and replicas to use, and more.  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.create_index(async_req=True)
            >>> result = thread.get()


            Keyword Args:
                create_request (CreateRequest): [optional]
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (int/float/tuple): timeout setting for this request. If
                    one number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                str
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            return self.call_with_http_info(**kwargs)

        self.create_index = _Endpoint(
            settings={
                'response_type': (str,),
                'auth': [
                    'ApiKeyAuth'
                ],
                'endpoint_path': '/databases',
                'operation_id': 'create_index',
                'http_method': 'POST',
                'servers': [
                    {
                        'url': "https://controller.{environment}.pinecone.io",
                        'description': "No description provided",
                        'variables': {
                            'environment': {
                                'description': "No description provided",
                                'default_value': "unknown",
                                }
                            }
                    },
                ]
            },
            params_map={
                'all': [
                    'create_request',
                ],
                'required': [],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'create_request':
                        (CreateRequest,),
                },
                'attribute_map': {
                },
                'location_map': {
                    'create_request': 'body',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'text/plain'
                ],
                'content_type': [
                    'application/json'
                ]
            },
            api_client=api_client,
            callable=__create_index
        )

        def __delete_index(
            self,
            index_name,
            **kwargs
        ):
            """delete_index  # noqa: E501

            This operation deletes an existing index.  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.delete_index(index_name, async_req=True)
            >>> result = thread.get()

            Args:
                index_name (str): The name of the index

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (int/float/tuple): timeout setting for this request. If
                    one number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                str
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['index_name'] = \
                index_name
            return self.call_with_http_info(**kwargs)

        self.delete_index = _Endpoint(
            settings={
                'response_type': (str,),
                'auth': [
                    'ApiKeyAuth'
                ],
                'endpoint_path': '/databases/{indexName}',
                'operation_id': 'delete_index',
                'http_method': 'DELETE',
                'servers': [
                    {
                        'url': "https://controller.{environment}.pinecone.io",
                        'description': "No description provided",
                        'variables': {
                            'environment': {
                                'description': "No description provided",
                                'default_value': "unknown",
                                }
                            }
                    },
                ]
            },
            params_map={
                'all': [
                    'index_name',
                ],
                'required': [
                    'index_name',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'index_name':
                        (str,),
                },
                'attribute_map': {
                    'index_name': 'indexName',
                },
                'location_map': {
                    'index_name': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'text/plain'
                ],
                'content_type': [],
            },
            api_client=api_client,
            callable=__delete_index
        )

        def __describe_index(
            self,
            index_name,
            **kwargs
        ):
            """describe_index  # noqa: E501

            Get a description of an index.  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.describe_index(index_name, async_req=True)
            >>> result = thread.get()

            Args:
                index_name (str): The name of the index

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (int/float/tuple): timeout setting for this request. If
                    one number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                IndexMeta
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['index_name'] = \
                index_name
            return self.call_with_http_info(**kwargs)

        self.describe_index = _Endpoint(
            settings={
                'response_type': (IndexMeta,),
                'auth': [
                    'ApiKeyAuth'
                ],
                'endpoint_path': '/databases/{indexName}',
                'operation_id': 'describe_index',
                'http_method': 'GET',
                'servers': [
                    {
                        'url': "https://controller.{environment}.pinecone.io",
                        'description': "No description provided",
                        'variables': {
                            'environment': {
                                'description': "No description provided",
                                'default_value': "unknown",
                                }
                            }
                    },
                ]
            },
            params_map={
                'all': [
                    'index_name',
                ],
                'required': [
                    'index_name',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'index_name':
                        (str,),
                },
                'attribute_map': {
                    'index_name': 'indexName',
                },
                'location_map': {
                    'index_name': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client,
            callable=__describe_index
        )

        def __list_indexes(
            self,
            **kwargs
        ):
            """list_indexes  # noqa: E501

            This operation returns a list of your Pinecone indexes.  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.list_indexes(async_req=True)
            >>> result = thread.get()


            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (int/float/tuple): timeout setting for this request. If
                    one number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                [str]
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            return self.call_with_http_info(**kwargs)

        self.list_indexes = _Endpoint(
            settings={
                'response_type': ([str],),
                'auth': [
                    'ApiKeyAuth'
                ],
                'endpoint_path': '/databases',
                'operation_id': 'list_indexes',
                'http_method': 'GET',
                'servers': [
                    {
                        'url': "https://controller.{environment}.pinecone.io",
                        'description': "No description provided",
                        'variables': {
                            'environment': {
                                'description': "No description provided",
                                'default_value': "unknown",
                                }
                            }
                    },
                ]
            },
            params_map={
                'all': [
                ],
                'required': [],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                },
                'attribute_map': {
                },
                'location_map': {
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json; charset=utf-8'
                ],
                'content_type': [],
            },
            api_client=api_client,
            callable=__list_indexes
        )

        def __scale_index(
            self,
            index_name,
            **kwargs
        ):
            """scale_index  # noqa: E501

            This operation increases or decreases the number of replicas in an index.  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.scale_index(index_name, async_req=True)
            >>> result = thread.get()

            Args:
                index_name (str): The name of the index

            Keyword Args:
                patch_request (PatchRequest): The number of replicas. [optional]
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (int/float/tuple): timeout setting for this request. If
                    one number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                str
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['index_name'] = \
                index_name
            return self.call_with_http_info(**kwargs)

        self.scale_index = _Endpoint(
            settings={
                'response_type': (str,),
                'auth': [
                    'ApiKeyAuth'
                ],
                'endpoint_path': '/databases/{indexName}',
                'operation_id': 'scale_index',
                'http_method': 'PATCH',
                'servers': [
                    {
                        'url': "https://controller.{environment}.pinecone.io",
                        'description': "No description provided",
                        'variables': {
                            'environment': {
                                'description': "No description provided",
                                'default_value': "unknown",
                                }
                            }
                    },
                ]
            },
            params_map={
                'all': [
                    'index_name',
                    'patch_request',
                ],
                'required': [
                    'index_name',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'index_name':
                        (str,),
                    'patch_request':
                        (PatchRequest,),
                },
                'attribute_map': {
                    'index_name': 'indexName',
                },
                'location_map': {
                    'index_name': 'path',
                    'patch_request': 'body',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'text/plain'
                ],
                'content_type': [
                    'application/json'
                ]
            },
            api_client=api_client,
            callable=__scale_index
        )
