# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Unit tests for flows_alias.py.
"""


import boto3
from botocore.exceptions import ClientError
import pytest

from flows import flow_alias


ALIAS_NAME = "Fake_flow_alias"
ALIAS_DESCRIPTION = "Playlist creator flow alias"
FLOW_ID = "XXXXXXXXXX"
ALIAS_ID = "XXXXXXXXXX"
FLOW_VERSION = "1"
ALIAS_ARN = f"arn:aws:bedrock:us-east-1:123456789012:flow/{FLOW_ID}/alias/{ALIAS_ID}"



@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_create_flow_alias(make_stubber, error_code):
    bedrock_agent_client = boto3.client("bedrock-agent")
    bedrock_agent_stubber = make_stubber(bedrock_agent_client)

    expected_params = {
        "flowIdentifier" : FLOW_ID,
        "name" : ALIAS_NAME,
        "description" : ALIAS_DESCRIPTION,
        "routingConfiguration" : [
                {
                    "flowVersion": FLOW_VERSION
                }
            ]
            }

    response = {
   "arn": ALIAS_ARN,
   "createdAt": "2025-03-29T21:34:43.048609+00:00",
   "description": ALIAS_DESCRIPTION,
   "flowId": FLOW_ID,
   "id": ALIAS_ID,
   "name": ALIAS_DESCRIPTION,
   "routingConfiguration": [ 
      { 
         "flowVersion": FLOW_VERSION
      }
   ],
   "updatedAt": "2025-03-29T21:34:43.048609+00:00"
}

    bedrock_agent_stubber.stub_create_flow_alias(
        expected_params, response, error_code=error_code
    )

    if error_code is None:
        alias_id = flow_alias.create_flow_alias(
            bedrock_agent_client, FLOW_ID, FLOW_VERSION, ALIAS_NAME, ALIAS_DESCRIPTION
        )
        assert alias_id == ALIAS_ID

    else:
        with pytest.raises(ClientError) as exc_info:
            flow_alias.create_flow_alias(bedrock_agent_client, FLOW_ID, FLOW_VERSION, ALIAS_NAME, ALIAS_DESCRIPTION)
        assert exc_info.value.response["Error"]["Code"] == error_code



@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_delete_flow_alias(make_stubber, error_code):
    bedrock_agent_client = boto3.client("bedrock-agent")
    bedrock_agent_stubber = make_stubber(bedrock_agent_client)

    expected_params = {
        "aliasIdentifier" : ALIAS_ID,
        "flowIdentifier": FLOW_ID
    }

    response = {
        "flowId" : FLOW_ID,
        "id": ALIAS_ID
    }

    bedrock_agent_stubber.stub_delete_flow_alias(
        expected_params, response, error_code=error_code
    )

    if error_code is None:
        call_response = flow_alias.delete_flow_alias(
            bedrock_agent_client, FLOW_ID, ALIAS_ID)

        assert call_response["id"] == FLOW_ID

    else:
        with pytest.raises(ClientError) as exc_info:
            flow_alias.delete_flow_alias(bedrock_agent_client, FLOW_ID, ALIAS_ID)
        assert exc_info.value.response["Error"]["Code"] == error_code