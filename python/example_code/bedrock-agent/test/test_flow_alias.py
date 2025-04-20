# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Unit tests for flow_alias.py.
"""

import boto3
from botocore.exceptions import ClientError
import pytest

from test.conftest import FakeFlowData as Fake

from flows import flow_alias


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_create_flow_alias(make_stubber, error_code):
    bedrock_agent_client = boto3.client("bedrock-agent")
    bedrock_agent_stubber = make_stubber(bedrock_agent_client)

    expected_params = {
        "flowIdentifier": Fake.FLOW_ID,
        "name": Fake.ALIAS_NAME,
        "description": Fake.ALIAS_DESCRIPTION,
        "routingConfiguration": Fake.ROUTING_CONFIG
    }

    response = {
        "arn": Fake.ALIAS_ARN,
        "createdAt": Fake.CREATED_AT,
        "description": Fake.ALIAS_DESCRIPTION,
        "flowId": Fake.FLOW_ID,
        "id": Fake.ALIAS_ID,
        "name": Fake.ALIAS_NAME,
        "routingConfiguration": Fake.ROUTING_CONFIG,
        "updatedAt": Fake.UPDATED_AT
    }

    bedrock_agent_stubber.stub_create_flow_alias(
        expected_params, response, error_code=error_code
    )

    if error_code is None:
        call_response = flow_alias.create_flow_alias(
            bedrock_agent_client, Fake.FLOW_ID, Fake.ALIAS_NAME, Fake.ALIAS_DESCRIPTION, Fake.ROUTING_CONFIG
        )
        assert call_response["id"] == Fake.ALIAS_ID
    else:
        with pytest.raises(ClientError) as exc_info:
            flow_alias.create_flow_alias(
                bedrock_agent_client, Fake.FLOW_ID, Fake.ALIAS_NAME, Fake.ALIAS_DESCRIPTION, Fake.ROUTING_CONFIG
            )
        assert exc_info.value.response["Error"]["Code"] == error_code


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_get_flow_alias(make_stubber, error_code):
    bedrock_agent_client = boto3.client("bedrock-agent")
    bedrock_agent_stubber = make_stubber(bedrock_agent_client)

    expected_params = {
        "flowIdentifier": Fake.FLOW_ID,
        "aliasIdentifier": Fake.ALIAS_ID
    }

    response = {
        "arn": Fake.ALIAS_ARN,
        "createdAt": Fake.CREATED_AT,
        "description": Fake.ALIAS_DESCRIPTION,
        "flowId": Fake.FLOW_ID,
        "id": Fake.ALIAS_ID,
        "name": Fake.ALIAS_NAME,
        "routingConfiguration": Fake.ROUTING_CONFIG,
        "updatedAt": Fake.UPDATED_AT
    }

    bedrock_agent_stubber.stub_get_flow_alias(
        expected_params, response, error_code=error_code
    )

    if error_code is None:
        call_response = flow_alias.get_flow_alias(
            bedrock_agent_client, Fake.FLOW_ID, Fake.ALIAS_ID
        )
        assert call_response["id"] == Fake.ALIAS_ID
    else:
        with pytest.raises(ClientError) as exc_info:
            flow_alias.get_flow_alias(
                bedrock_agent_client, Fake.FLOW_ID, Fake.ALIAS_ID
            )
        assert exc_info.value.response["Error"]["Code"] == error_code


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_delete_flow_alias(make_stubber, error_code):
    bedrock_agent_client = boto3.client("bedrock-agent")
    bedrock_agent_stubber = make_stubber(bedrock_agent_client)

    expected_params = {
        "flowIdentifier": Fake.FLOW_ID,
        "aliasIdentifier": Fake.ALIAS_ID
    }

    response = {
        "flowId": Fake.FLOW_ID,
        "id": Fake.ALIAS_ID
    }

    bedrock_agent_stubber.stub_delete_flow_alias(
        expected_params, response, error_code=error_code
    )

    if error_code is None:
        call_response = flow_alias.delete_flow_alias(
            bedrock_agent_client, Fake.FLOW_ID, Fake.ALIAS_ID
        )
        assert call_response["id"] == Fake.ALIAS_ID
    else:
        with pytest.raises(ClientError) as exc_info:
            flow_alias.delete_flow_alias(
                bedrock_agent_client, Fake.FLOW_ID, Fake.ALIAS_ID
            )
        assert exc_info.value.response["Error"]["Code"] == error_code


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_update_flow_alias(make_stubber, error_code):
    bedrock_agent_client = boto3.client("bedrock-agent")
    bedrock_agent_stubber = make_stubber(bedrock_agent_client)

    expected_params = {
        "flowIdentifier": Fake.FLOW_ID,
        "aliasIdentifier": Fake.ALIAS_ID,
        "name": Fake.ALIAS_NAME,
        "description": Fake.ALIAS_DESCRIPTION,
        "routingConfiguration": Fake.ROUTING_CONFIG
    }

    response = {
        "arn": Fake.ALIAS_ARN,
        "createdAt": Fake.CREATED_AT,
        "description": Fake.ALIAS_DESCRIPTION,
        "flowId": Fake.FLOW_ID,
        "id": Fake.ALIAS_ID,
        "name": Fake.ALIAS_NAME,
        "routingConfiguration": Fake.ROUTING_CONFIG,
        "updatedAt": Fake.UPDATED_AT
    }

    bedrock_agent_stubber.stub_update_flow_alias(
        expected_params, response, error_code=error_code
    )

    if error_code is None:
        call_response = flow_alias.update_flow_alias(
            bedrock_agent_client, Fake.FLOW_ID, Fake.ALIAS_ID, Fake.ALIAS_NAME, Fake.ALIAS_DESCRIPTION, Fake.ROUTING_CONFIG
        )
        assert call_response["id"] == Fake.ALIAS_ID
    else:
        with pytest.raises(ClientError) as exc_info:
            flow_alias.update_flow_alias(
                bedrock_agent_client, Fake.FLOW_ID, Fake.ALIAS_ID, Fake.ALIAS_NAME, Fake.ALIAS_DESCRIPTION, Fake.ROUTING_CONFIG
            )
        assert exc_info.value.response["Error"]["Code"] == error_code
