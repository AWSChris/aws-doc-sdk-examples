# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Unit tests for bedrock_agent_wrapper.py.
"""

import boto3
from botocore.exceptions import ClientError
import pytest

from test.conftest import FakeData as Fake

import bedrock_agent_wrapper as wrapper


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_list_foundation_models(make_stubber, error_code):
    bedrock_client = boto3.client("bedrock")
    bedrock_stubber = make_stubber(bedrock_client)

    expected_params = {}

    response = {
        "modelSummaries": [
            {
                "modelId": Fake.FOUNDATION_MODEL_ID,
                "modelName": "Fake Foundation Model",
                "providerName": "Fake Provider",
                "inputModalities": ["TEXT"],
                "outputModalities": ["TEXT"],
                "responseStreamingSupported": True,
                "customizationsSupported": ["FINE_TUNING"],
                "inferenceTypesSupported": ["ON_DEMAND"],
                "modelLifecycle": {
                    "status": "ACTIVE"
                }
            }
        ]
    }

    bedrock_stubber.stub_list_foundation_models(
        expected_params, response, error_code=error_code
    )

    if error_code is None:
        models = wrapper.list_foundation_models(bedrock_client)
        assert len(models) == 1
        assert models[0]["modelId"] == Fake.FOUNDATION_MODEL_ID
    else:
        with pytest.raises(ClientError) as exc_info:
            wrapper.list_foundation_models(bedrock_client)
        assert exc_info.value.response["Error"]["Code"] == error_code


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_get_foundation_model(make_stubber, error_code):
    bedrock_client = boto3.client("bedrock")
    bedrock_stubber = make_stubber(bedrock_client)

    expected_params = {
        "modelIdentifier": Fake.FOUNDATION_MODEL_ID
    }

    response = {
        "modelDetails": {
            "modelId": Fake.FOUNDATION_MODEL_ID,
            "modelName": "Fake Foundation Model",
            "providerName": "Fake Provider",
            "inputModalities": ["TEXT"],
            "outputModalities": ["TEXT"],
            "responseStreamingSupported": True,
            "customizationsSupported": ["FINE_TUNING"],
            "inferenceTypesSupported": ["ON_DEMAND"],
            "modelLifecycle": {
                "status": "ACTIVE"
            }
        }
    }

    bedrock_stubber.stub_get_foundation_model(
        expected_params, response, error_code=error_code
    )

    if error_code is None:
        model = wrapper.get_foundation_model(bedrock_client, Fake.FOUNDATION_MODEL_ID)
        assert model["modelId"] == Fake.FOUNDATION_MODEL_ID
    else:
        with pytest.raises(ClientError) as exc_info:
            wrapper.get_foundation_model(bedrock_client, Fake.FOUNDATION_MODEL_ID)
        assert exc_info.value.response["Error"]["Code"] == error_code


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_create_agent(make_stubber, error_code):
    bedrock_agent_client = boto3.client("bedrock-agent")
    bedrock_agent_stubber = make_stubber(bedrock_agent_client)

    expected_params = {
        "agentName": Fake.AGENT_NAME,
        "foundationModel": Fake.FOUNDATION_MODEL_ID,
        "instruction": Fake.INSTRUCTION,
        "description": Fake.DESCRIPTION,
        "customerEncryptionKeyArn": None,
        "idleSessionTTLInSeconds": 1800,
        "promptOverrideConfiguration": None,
        "clientToken": None
    }

    response = {
        "agent": {
            "agentId": Fake.AGENT_ID,
            "agentName": Fake.AGENT_NAME,
            "agentArn": Fake.ARN,
            "agentStatus": "CREATING",
            "agentVersion": "DRAFT",
            "createdAt": Fake.TIMESTAMP,
            "description": Fake.DESCRIPTION,
            "foundationModel": Fake.FOUNDATION_MODEL_ID,
            "idleSessionTTLInSeconds": 1800,
            "instruction": Fake.INSTRUCTION,
            "updatedAt": Fake.TIMESTAMP
        }
    }

    bedrock_agent_stubber.stub_create_agent(
        expected_params, response, error_code=error_code
    )

    if error_code is None:
        agent = wrapper.create_agent(
            bedrock_agent_client,
            Fake.AGENT_NAME,
            Fake.FOUNDATION_MODEL_ID,
            Fake.INSTRUCTION,
            Fake.DESCRIPTION
        )
        assert agent["agentId"] == Fake.AGENT_ID
    else:
        with pytest.raises(ClientError) as exc_info:
            wrapper.create_agent(
                bedrock_agent_client,
                Fake.AGENT_NAME,
                Fake.FOUNDATION_MODEL_ID,
                Fake.INSTRUCTION,
                Fake.DESCRIPTION
            )
        assert exc_info.value.response["Error"]["Code"] == error_code


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_get_agent(make_stubber, error_code):
    bedrock_agent_client = boto3.client("bedrock-agent")
    bedrock_agent_stubber = make_stubber(bedrock_agent_client)

    expected_params = {
        "agentId": Fake.AGENT_ID,
        "agentVersion": "DRAFT"
    }

    response = {
        "agent": {
            "agentId": Fake.AGENT_ID,
            "agentName": Fake.AGENT_NAME,
            "agentArn": Fake.ARN,
            "agentStatus": "PREPARED",
            "agentVersion": "DRAFT",
            "createdAt": Fake.TIMESTAMP,
            "description": Fake.DESCRIPTION,
            "foundationModel": Fake.FOUNDATION_MODEL_ID,
            "idleSessionTTLInSeconds": 1800,
            "instruction": Fake.INSTRUCTION,
            "updatedAt": Fake.TIMESTAMP
        }
    }

    bedrock_agent_stubber.stub_get_agent(
        expected_params, response, error_code=error_code
    )

    if error_code is None:
        agent = wrapper.get_agent(bedrock_agent_client, Fake.AGENT_ID)
        assert agent["agentId"] == Fake.AGENT_ID
    else:
        with pytest.raises(ClientError) as exc_info:
            wrapper.get_agent(bedrock_agent_client, Fake.AGENT_ID)
        assert exc_info.value.response["Error"]["Code"] == error_code


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_delete_agent(make_stubber, error_code):
    bedrock_agent_client = boto3.client("bedrock-agent")
    bedrock_agent_stubber = make_stubber(bedrock_agent_client)

    expected_params = {
        "agentId": Fake.AGENT_ID,
        "skipResourceInUseCheck": False
    }

    response = {}

    bedrock_agent_stubber.stub_delete_agent(
        expected_params, response, error_code=error_code
    )

    if error_code is None:
        wrapper.delete_agent(bedrock_agent_client, Fake.AGENT_ID)
    else:
        with pytest.raises(ClientError) as exc_info:
            wrapper.delete_agent(bedrock_agent_client, Fake.AGENT_ID)
        assert exc_info.value.response["Error"]["Code"] == error_code


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_create_agent_action_group(make_stubber, error_code):
    bedrock_agent_client = boto3.client("bedrock-agent")
    bedrock_agent_stubber = make_stubber(bedrock_agent_client)

    expected_params = {
        "agentId": Fake.AGENT_ID,
        "agentVersion": "DRAFT",
        "actionGroupName": Fake.ACTION_GROUP_NAME,
        "apiSchema": {
            "payload": Fake.API_SCHEMA
        },
        "description": Fake.DESCRIPTION,
        "clientToken": None
    }

    response = {
        "actionGroup": {
            "actionGroupId": Fake.ACTION_GROUP_ID,
            "actionGroupName": Fake.ACTION_GROUP_NAME,
            "agentId": Fake.AGENT_ID,
            "agentVersion": "DRAFT",
            "createdAt": Fake.TIMESTAMP,
            "description": Fake.DESCRIPTION,
            "updatedAt": Fake.TIMESTAMP
        }
    }

    bedrock_agent_stubber.stub_create_agent_action_group(
        expected_params, response, error_code=error_code
    )

    if error_code is None:
        action_group = wrapper.create_agent_action_group(
            bedrock_agent_client,
            Fake.AGENT_ID,
            Fake.ACTION_GROUP_NAME,
            Fake.API_SCHEMA,
            Fake.DESCRIPTION
        )
        assert action_group["actionGroupId"] == Fake.ACTION_GROUP_ID
    else:
        with pytest.raises(ClientError) as exc_info:
            wrapper.create_agent_action_group(
                bedrock_agent_client,
                Fake.AGENT_ID,
                Fake.ACTION_GROUP_NAME,
                Fake.API_SCHEMA,
                Fake.DESCRIPTION
            )
        assert exc_info.value.response["Error"]["Code"] == error_code


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_delete_agent_action_group(make_stubber, error_code):
    bedrock_agent_client = boto3.client("bedrock-agent")
    bedrock_agent_stubber = make_stubber(bedrock_agent_client)

    expected_params = {
        "agentId": Fake.AGENT_ID,
        "agentVersion": "DRAFT",
        "actionGroupId": Fake.ACTION_GROUP_ID,
        "skipResourceInUseCheck": False
    }

    response = {}

    bedrock_agent_stubber.stub_delete_agent_action_group(
        expected_params, response, error_code=error_code
    )

    if error_code is None:
        wrapper.delete_agent_action_group(
            bedrock_agent_client, Fake.AGENT_ID, Fake.ACTION_GROUP_ID
        )
    else:
        with pytest.raises(ClientError) as exc_info:
            wrapper.delete_agent_action_group(
                bedrock_agent_client, Fake.AGENT_ID, Fake.ACTION_GROUP_ID
            )
        assert exc_info.value.response["Error"]["Code"] == error_code


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_prepare_agent(make_stubber, error_code):
    bedrock_agent_client = boto3.client("bedrock-agent")
    bedrock_agent_stubber = make_stubber(bedrock_agent_client)

    expected_params = {
        "agentId": Fake.AGENT_ID,
        "agentVersion": "DRAFT"
    }

    response = {
        "agent": {
            "agentId": Fake.AGENT_ID,
            "agentName": Fake.AGENT_NAME,
            "agentArn": Fake.ARN,
            "agentStatus": "PREPARING",
            "agentVersion": "DRAFT",
            "createdAt": Fake.TIMESTAMP,
            "description": Fake.DESCRIPTION,
            "foundationModel": Fake.FOUNDATION_MODEL_ID,
            "idleSessionTTLInSeconds": 1800,
            "instruction": Fake.INSTRUCTION,
            "updatedAt": Fake.TIMESTAMP
        }
    }

    bedrock_agent_stubber.stub_prepare_agent(
        expected_params, response, error_code=error_code
    )

    if error_code is None:
        agent = wrapper.prepare_agent(bedrock_agent_client, Fake.AGENT_ID)
        assert agent["agentId"] == Fake.AGENT_ID
    else:
        with pytest.raises(ClientError) as exc_info:
            wrapper.prepare_agent(bedrock_agent_client, Fake.AGENT_ID)
        assert exc_info.value.response["Error"]["Code"] == error_code


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_create_agent_alias(make_stubber, error_code):
    bedrock_agent_client = boto3.client("bedrock-agent")
    bedrock_agent_stubber = make_stubber(bedrock_agent_client)

    expected_params = {
        "agentId": Fake.AGENT_ID,
        "agentAliasName": Fake.ALIAS_NAME,
        "description": Fake.DESCRIPTION,
        "routingConfiguration": [
            {
                "agentVersion": "DRAFT"
            }
        ],
        "clientToken": None
    }

    response = {
        "agentAlias": {
            "agentAliasId": Fake.ALIAS_ID,
            "agentAliasName": Fake.ALIAS_NAME,
            "agentAliasArn": Fake.ARN,
            "agentAliasStatus": "CREATING",
            "agentId": Fake.AGENT_ID,
            "createdAt": Fake.TIMESTAMP,
            "description": Fake.DESCRIPTION,
            "routingConfiguration": [
                {
                    "agentVersion": "DRAFT"
                }
            ],
            "updatedAt": Fake.TIMESTAMP
        }
    }

    bedrock_agent_stubber.stub_create_agent_alias(
        expected_params, response, error_code=error_code
    )

    if error_code is None:
        agent_alias = wrapper.create_agent_alias(
            bedrock_agent_client, Fake.AGENT_ID, Fake.ALIAS_NAME, Fake.DESCRIPTION
        )
        assert agent_alias["agentAliasId"] == Fake.ALIAS_ID
    else:
        with pytest.raises(ClientError) as exc_info:
            wrapper.create_agent_alias(
                bedrock_agent_client, Fake.AGENT_ID, Fake.ALIAS_NAME, Fake.DESCRIPTION
            )
        assert exc_info.value.response["Error"]["Code"] == error_code


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_delete_agent_alias(make_stubber, error_code):
    bedrock_agent_client = boto3.client("bedrock-agent")
    bedrock_agent_stubber = make_stubber(bedrock_agent_client)

    expected_params = {
        "agentId": Fake.AGENT_ID,
        "agentAliasId": Fake.ALIAS_ID,
        "skipResourceInUseCheck": False
    }

    response = {}

    bedrock_agent_stubber.stub_delete_agent_alias(
        expected_params, response, error_code=error_code
    )

    if error_code is None:
        wrapper.delete_agent_alias(
            bedrock_agent_client, Fake.AGENT_ID, Fake.ALIAS_ID
        )
    else:
        with pytest.raises(ClientError) as exc_info:
            wrapper.delete_agent_alias(
                bedrock_agent_client, Fake.AGENT_ID, Fake.ALIAS_ID
            )
        assert exc_info.value.response["Error"]["Code"] == error_code
