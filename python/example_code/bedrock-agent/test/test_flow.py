# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Unit tests for flow.py.
"""


import boto3
from botocore.exceptions import ClientError
import pytest

from test.conftest import FakeFlowData as Fake

from flows import flow


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_create_flow(make_stubber, error_code):
    bedrock_agent_client = boto3.client("bedrock-agent")
    bedrock_agent_stubber = make_stubber(bedrock_agent_client)

    expected_params = {
        "name": Fake.FLOW_NAME,
        "description": Fake.FLOW_DESCRIPTION,
        "executionRoleArn": Fake.ROLE_ARN,
        "definition": Fake.FLOW_DEFINITION,
        "clientToken": None
    }

    response = {
        "id": Fake.FLOW_ID,
        "arn": Fake.FLOW_ARN,
        "name": Fake.FLOW_NAME,
        "description": Fake.FLOW_DESCRIPTION,
        "createdAt": Fake.CREATED_AT,
        "updatedAt": Fake.UPDATED_AT,
        "status": "NotPrepared",
        "executionRoleArn": Fake.ROLE_ARN,
        "definition": Fake.FLOW_DEFINITION
    }

    bedrock_agent_stubber.stub_create_flow(
        expected_params, response, error_code=error_code
    )

    if error_code is None:
        call_response = flow.create_flow(
            bedrock_agent_client, Fake.FLOW_NAME, Fake.FLOW_DESCRIPTION, Fake.ROLE_ARN, Fake.FLOW_DEFINITION
        )
        assert call_response["id"] == Fake.FLOW_ID
    else:
        with pytest.raises(ClientError) as exc_info:
            flow.create_flow(
                bedrock_agent_client, Fake.FLOW_NAME, Fake.FLOW_DESCRIPTION, Fake.ROLE_ARN, Fake.FLOW_DEFINITION
            )
        assert exc_info.value.response["Error"]["Code"] == error_code


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_get_flow(make_stubber, error_code):
    bedrock_agent_client = boto3.client("bedrock-agent")
    bedrock_agent_stubber = make_stubber(bedrock_agent_client)

    expected_params = {
        "flowIdentifier": Fake.FLOW_ID
    }

    response = {
        "id": Fake.FLOW_ID,
        "arn": Fake.FLOW_ARN,
        "name": Fake.FLOW_NAME,
        "description": Fake.FLOW_DESCRIPTION,
        "createdAt": Fake.CREATED_AT,
        "updatedAt": Fake.UPDATED_AT,
        "status": "NotPrepared",
        "executionRoleArn": Fake.ROLE_ARN,
        "definition": Fake.FLOW_DEFINITION
    }

    bedrock_agent_stubber.stub_get_flow(
        expected_params, response, error_code=error_code
    )

    if error_code is None:
        call_response = flow.get_flow(
            bedrock_agent_client, Fake.FLOW_ID
        )
        assert call_response["id"] == Fake.FLOW_ID
    else:
        with pytest.raises(ClientError) as exc_info:
            flow.get_flow(
                bedrock_agent_client, Fake.FLOW_ID
            )
        assert exc_info.value.response["Error"]["Code"] == error_code


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_delete_flow(make_stubber, error_code):
    bedrock_agent_client = boto3.client("bedrock-agent")
    bedrock_agent_stubber = make_stubber(bedrock_agent_client)

    expected_params = {
        "flowIdentifier": Fake.FLOW_ID,
        "skipResourceInUseCheck": False
    }

    response = {
        "id": Fake.FLOW_ID
    }

    bedrock_agent_stubber.stub_delete_flow(
        expected_params, response, error_code=error_code
    )

    if error_code is None:
        call_response = flow.delete_flow(
            bedrock_agent_client, Fake.FLOW_ID
        )
        assert call_response["id"] == Fake.FLOW_ID
    else:
        with pytest.raises(ClientError) as exc_info:
            flow.delete_flow(
                bedrock_agent_client, Fake.FLOW_ID
            )
        assert exc_info.value.response["Error"]["Code"] == error_code


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_update_flow(make_stubber, error_code):
    bedrock_agent_client = boto3.client("bedrock-agent")
    bedrock_agent_stubber = make_stubber(bedrock_agent_client)

    expected_params = {
        "flowIdentifier": Fake.FLOW_ID,
        "name": Fake.FLOW_NAME,
        "description": Fake.FLOW_DESCRIPTION,
        "executionRoleArn": Fake.ROLE_ARN,
        "definition": Fake.FLOW_DEFINITION
    }

    response = {
        "id": Fake.FLOW_ID,
        "arn": Fake.FLOW_ARN,
        "name": Fake.FLOW_NAME,
        "description": Fake.FLOW_DESCRIPTION,
        "createdAt": Fake.CREATED_AT,
        "updatedAt": Fake.UPDATED_AT,
        "status": "NotPrepared",
        "executionRoleArn": Fake.ROLE_ARN,
        "definition": Fake.FLOW_DEFINITION
    }

    bedrock_agent_stubber.stub_update_flow(
        expected_params, response, error_code=error_code
    )

    if error_code is None:
        call_response = flow.update_flow(
            bedrock_agent_client, Fake.FLOW_ID, Fake.FLOW_NAME, Fake.FLOW_DESCRIPTION, Fake.ROLE_ARN, Fake.FLOW_DEFINITION
        )
        assert call_response["id"] == Fake.FLOW_ID
    else:
        with pytest.raises(ClientError) as exc_info:
            flow.update_flow(
                bedrock_agent_client, Fake.FLOW_ID, Fake.FLOW_NAME, Fake.FLOW_DESCRIPTION, Fake.ROLE_ARN, Fake.FLOW_DEFINITION
            )
        assert exc_info.value.response["Error"]["Code"] == error_code
