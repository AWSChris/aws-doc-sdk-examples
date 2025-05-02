# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Stub functions that are used by the Amazon Bedrock Agents Runtime unit tests.

When tests are run against an actual AWS account, the stubber class does not
set up stubs and passes all calls through to the Boto3 client.
"""

from test_tools.example_stubber import ExampleStubber


class BedrockAgentRuntimeStubber(ExampleStubber):
    """
    A class that implements stub functions used by Amazon Bedrock Agents Runtime unit tests.
    """

    def __init__(self, client, use_stubs=True):
        """
        Initializes the object with a specific client and configures it for
        stubbing or AWS passthrough.

        :param client: A Boto3 Amazon Bedrock Agents Runtime client.
        :param use_stubs: When True, uses stubs to intercept requests. Otherwise,
                          passes requests through to AWS.
        """
        super().__init__(client, use_stubs)

    def stub_invoke_agent(self, expected_params, response, error_code=None):
        self._stub_bifurcator(
            "invoke_agent", expected_params, response, error_code=error_code
        )
        
    def add_invoke_agent_response(self, expected_params, response_chunks, version="1.0"):
        """
        Adds a response for the invoke_agent method that includes streaming chunks.
        
        :param expected_params: The parameters that are expected to be passed to the method.
        :param response_chunks: A list of chunks to be returned in the completion field.
        :param version: The version of the response.
        """
        response = {
            "completion": response_chunks,
            "version": version
        }
        self._stub_bifurcator(
            "invoke_agent", expected_params, response
        )
        
    def add_client_error(self, method_name, expected_params, service_error_code, service_message):
        """
        Adds a client error response for the specified method.
        
        :param method_name: The name of the method that raises the error.
        :param expected_params: The parameters that are expected to be passed to the method.
        :param service_error_code: The error code to return.
        :param service_message: The error message to return.
        """
        self.client.meta.client.exceptions.ClientError.service_error_meta = {
            'Code': service_error_code,
            'Message': service_message
        }
        self._stub_bifurcator(
            method_name,
            expected_params,
            service_error_code=service_error_code,
            service_message=service_message,
            error_code=service_error_code
        )
        
    def stub_invoke_flow(self, expected_params, response, error_code=None):
        self._stub_bifurcator(
            "invoke_flow", expected_params, response, error_code=error_code
        )