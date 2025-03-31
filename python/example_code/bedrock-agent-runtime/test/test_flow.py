# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Unit tests for flows.py.
"""


import boto3
from botocore.exceptions import ClientError
import pytest

from flows import flow


FLOW_NAME = "Fake_flow"
FLOW_DESCRIPTION = "Playlist creator flow"
FLOW_ID = "XXXXXXXXXX"
ROLE_ARN = f"arn:aws:iam::123456789012:role/BedrockFlowRole-{FLOW_NAME}"
FLOW_ARN = f"arn:aws:bedrock:us-east-1:123456789012:flow/{FLOW_ID}"
FLOW_DEFINITION = {}


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_create_flow(make_stubber, error_code):
    bedrock_agent_client = boto3.client("bedrock-agent")
    bedrock_agent_stubber = make_stubber(bedrock_agent_client)

    expected_params = {
        "name": FLOW_NAME,
        "description": FLOW_DESCRIPTION,
        "executionRoleArn": ROLE_ARN,
        "definition": FLOW_DEFINITION
    }

    response = {
        "arn": FLOW_ARN,
        "createdAt": "2025-03-29T21:34:43.048609+00:00",
        "definition": FLOW_DEFINITION,
        "description": FLOW_DESCRIPTION,
        "executionRoleArn": ROLE_ARN,
        "id": FLOW_ID,
        "name": FLOW_NAME,
        "status": "NotPrepared",
        "updatedAt": "2025-03-29T21:34:43.048609+00:00",
        "version": "DRAFT"
    }

    bedrock_agent_stubber.stub_create_flow(
        expected_params, response, error_code=error_code
    )

    if error_code is None:
        call_response = flow.create_flow(
            bedrock_agent_client, FLOW_NAME, FLOW_DESCRIPTION, ROLE_ARN, FLOW_DEFINITION
        )
        assert call_response["status"] == "NotPrepared"

    else:
        with pytest.raises(ClientError) as exc_info:
            flow.create_flow(bedrock_agent_client, FLOW_NAME,
                             FLOW_DESCRIPTION, ROLE_ARN, FLOW_DEFINITION)
        assert exc_info.value.response["Error"]["Code"] == error_code


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_prepare_flow(make_stubber, error_code):
    bedrock_agent_client = boto3.client("bedrock-agent")
    bedrock_agent_stubber = make_stubber(bedrock_agent_client)



    expected_params = {
        "flowIdentifier": FLOW_ID,
    }


    if error_code is None:

        # First stub - Flow starts preparing
        bedrock_agent_stubber.stub_prepare_flow(
            expected_params,
            {
                "id": FLOW_ID,
                "status": "Preparing"
            }
        )

        # Second stub - Get flow status for prepared flow.
        bedrock_agent_stubber.stub_get_flow(
            expected_params,
            {
        "arn": FLOW_ARN,
        "createdAt": "2025-03-29T21:34:43.048609+00:00",
        "definition": FLOW_DEFINITION,
        "description": FLOW_DESCRIPTION,
        "executionRoleArn": ROLE_ARN,
        "id": FLOW_ID,
        "name": FLOW_NAME,
        "status": "Prepared",
        "updatedAt": "2025-03-29T21:34:43.048609+00:00",
        "version": "DRAFT"
    }

        )

        # Third stub - Flow is prepared.
        bedrock_agent_stubber.stub_prepare_flow(
            expected_params,
            {
                "id": FLOW_ID,
                "status": "Prepared"
            }
        )

        call_response = flow.prepare_flow(bedrock_agent_client, FLOW_ID)
        assert call_response == "Prepared"

    else:
        bedrock_agent_stubber.stub_prepare_flow(
            expected_params,
            {"id": FLOW_ID},
            error_code=error_code
        )
        with pytest.raises(ClientError) as exc_info:
            flow.prepare_flow(bedrock_agent_client, FLOW_ID)
        assert exc_info.value.response["Error"]["Code"] == error_code


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_get_flow(make_stubber, error_code):
    bedrock_agent_client = boto3.client("bedrock-agent")
    bedrock_agent_stubber = make_stubber(bedrock_agent_client)

    expected_params = {
        "flowIdentifier": FLOW_ID
    }

    response = {
        "arn": FLOW_ARN,
        "createdAt": "2025-03-29T21:34:43.048609+00:00",
        "definition": FLOW_DEFINITION,
        "description": FLOW_DESCRIPTION,
        "executionRoleArn": ROLE_ARN,
        "id": FLOW_ID,
        "name": FLOW_NAME,
        "status": "NotPrepared",
        "updatedAt": "2025-03-29T21:34:43.048609+00:00",
        "version": "DRAFT"
    }

    bedrock_agent_stubber.stub_get_flow(
        expected_params, response, error_code=error_code
    )

    if error_code is None:
        call_response = flow.get_flow(
            bedrock_agent_client, FLOW_ID)

        assert call_response["status"] == "NotPrepared"

    else:
        with pytest.raises(ClientError) as exc_info:
            flow.get_flow(bedrock_agent_client, FLOW_ID)
        assert exc_info.value.response["Error"]["Code"] == error_code


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_delete_flow(make_stubber, error_code):
    bedrock_agent_client = boto3.client("bedrock-agent")
    bedrock_agent_stubber = make_stubber(bedrock_agent_client)

    expected_params = {
        "flowIdentifier": FLOW_ID,
        "skipResourceInUseCheck" : True
    }

    response = {
        "id": FLOW_ID
    }

    bedrock_agent_stubber.stub_delete_flow(
        expected_params, response, error_code=error_code
    )

    if error_code is None:
        call_response = flow.delete_flow(
            bedrock_agent_client, FLOW_ID)

        assert call_response["id"] == FLOW_ID

    else:
        with pytest.raises(ClientError) as exc_info:
            flow.delete_flow(bedrock_agent_client, FLOW_ID)
        assert exc_info.value.response["Error"]["Code"] == error_code