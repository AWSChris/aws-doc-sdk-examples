# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Unit tests for flows.py.
"""


import boto3
from botocore.exceptions import ClientError
import pytest

from flows import flow


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_create_flow(make_stubber, error_code):
    bedrock_agent_client = boto3.client("bedrock-agent")
    bedrock_agent_stubber = make_stubber(bedrock_agent_client)

    flow_name = "Fake_flow"
    flow_description = "Playlist creator flow"
    flow_id = "XXXXXXXXXX"
    role_arn = f"arn:aws:iam::123456789012:role/BedrockFlowRole-{flow_name}"
    flow_arn = f"arn:aws:bedrock:us-east-1:123456789012:flow/{flow_id}"

    flow_definition = {}

    expected_params = {
        "name": flow_name,
        "description": flow_description,
        "executionRoleArn": role_arn,
        "definition": flow_definition
    }

    response = {
        "arn": flow_arn,
        "createdAt": "2025-03-29T21:34:43.048609+00:00",
        "definition": flow_definition,
        "description": flow_description,
        "executionRoleArn": role_arn,
        "id": flow_id,
        "name": flow_name,
        "status": "NotPrepared",
        "updatedAt": "2025-03-29T21:34:43.048609+00:00",
        "version": "DRAFT"
    }

    bedrock_agent_stubber.stub_create_flow(
        expected_params, response, error_code=error_code
    )

    if error_code is None:
        call_response = flow.create_flow(
            bedrock_agent_client, flow_name, flow_description, role_arn, flow_definition
        )
        assert call_response["status"] == "NotPrepared"

    else:
        with pytest.raises(ClientError) as exc_info:
            flow.create_flow(bedrock_agent_client, flow_name,
                             flow_description, role_arn, flow_definition)
        assert exc_info.value.response["Error"]["Code"] == error_code
