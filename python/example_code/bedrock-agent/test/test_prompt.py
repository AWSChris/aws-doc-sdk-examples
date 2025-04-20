# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Unit tests for prompt.py.
"""

import boto3
from botocore.exceptions import ClientError
import pytest

from conftest import FakeData

import sys
sys.path.append("../prompts")
from prompts import prompt


class FakePromptData:
    PROMPT_ID = "FAKE_PROMPT_ID"
    PROMPT_NAME = "FakePromptName"
    PROMPT_DESCRIPTION = "A fake prompt description"
    PROMPT_TEMPLATE = "This is a {{variable}} template"
    MODEL_ID = "anthropic.claude-v2"
    CREATED_AT = "2025-03-29T21:34:43.048609+00:00"
    UPDATED_AT = "2025-03-30T21:34:43.048609+00:00"
    PROMPT_ARN = f"arn:aws:bedrock:us-east-1:123456789012:prompt/{PROMPT_ID}"


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_create_prompt(make_stubber, error_code):
    bedrock_client = boto3.client("bedrock-agent")
    bedrock_stubber = make_stubber(bedrock_client)

    expected_params = {
        "name": FakePromptData.PROMPT_NAME,
        "description": FakePromptData.PROMPT_DESCRIPTION,
        "variants": [{
            "name": "default",
            "templateType": "TEXT",
            "templateConfiguration": {
                "text": {
                    "text": FakePromptData.PROMPT_TEMPLATE,
                    "inputVariables": [{"name": "variable"}]
                }
            },
            "modelId": FakePromptData.MODEL_ID
        }],
        "defaultVariant": "default"
    }

    response = {
        "id": FakePromptData.PROMPT_ID,
        "arn": f"arn:aws:bedrock:us-east-1:123456789012:prompt/{FakePromptData.PROMPT_ID}",
        "name": FakePromptData.PROMPT_NAME,
        "description": FakePromptData.PROMPT_DESCRIPTION,
        "createdAt": FakePromptData.CREATED_AT,
        "updatedAt": FakePromptData.UPDATED_AT,
        "version": "1"
    }

    if error_code is None:
        bedrock_stubber.stub_create_prompt(expected_params, response)
    else:
        bedrock_stubber.stub_create_prompt(expected_params, response, error_code=error_code)

    if error_code is None:
        result = prompt.create_prompt(
            bedrock_client,
            FakePromptData.PROMPT_NAME,
            FakePromptData.PROMPT_DESCRIPTION,
            FakePromptData.PROMPT_TEMPLATE,
            FakePromptData.MODEL_ID
        )
        assert result == response
    else:
        with pytest.raises(ClientError) as exc:
            prompt.create_prompt(
                bedrock_client,
                FakePromptData.PROMPT_NAME,
                FakePromptData.PROMPT_DESCRIPTION,
                FakePromptData.PROMPT_TEMPLATE,
                FakePromptData.MODEL_ID
            )
        assert exc.value.response["Error"]["Code"] == error_code


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_get_prompt(make_stubber, error_code):
    bedrock_client = boto3.client("bedrock-agent")
    bedrock_stubber = make_stubber(bedrock_client)

    expected_params = {
        "promptIdentifier": FakePromptData.PROMPT_ID
    }

    response = {
        "id": FakePromptData.PROMPT_ID,
        "arn": FakePromptData.PROMPT_ARN,
        "name": FakePromptData.PROMPT_NAME,
        "description": FakePromptData.PROMPT_DESCRIPTION,
        "createdAt": FakePromptData.CREATED_AT,
        "updatedAt": FakePromptData.UPDATED_AT,
        "version": "1",
        "defaultVariant": "default",
        "variants": [{
            "name": "default",
            "templateType": "TEXT",
            "templateConfiguration": {
                "text": {
                    "text": FakePromptData.PROMPT_TEMPLATE,
                    "inputVariables": [{"name": "variable"}]
                }
            },
            "modelId": FakePromptData.MODEL_ID
        }]
    }

    if error_code is None:
        bedrock_stubber.stub_get_prompt(expected_params, response)
    else:
        bedrock_stubber.stub_get_prompt(expected_params, response, error_code=error_code)

    if error_code is None:
        result = prompt.get_prompt(bedrock_client, FakePromptData.PROMPT_ID)
        assert result == response
    else:
        with pytest.raises(ClientError) as exc:
            prompt.get_prompt(bedrock_client, FakePromptData.PROMPT_ID)
        assert exc.value.response["Error"]["Code"] == error_code


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_update_prompt(make_stubber, error_code):
    bedrock_client = boto3.client("bedrock-agent")
    bedrock_stubber = make_stubber(bedrock_client)

    new_name = "UpdatedPromptName"
    new_description = "Updated prompt description"
    new_template = "Updated {{variable}} template"

    # The expected parameters for the API call
    expected_params = {
        "promptIdentifier": FakePromptData.PROMPT_ID,
        "name": new_name,
        "description": new_description,
        "variants": [{
            "name": "default",
            "templateType": "TEXT",
            "templateConfiguration": {
                "text": {
                    "text": new_template,
                    "inputVariables": [{"name": "variable"}]
                }
            }
        }]
    }

    # The response from the API
    response = {
        "id": FakePromptData.PROMPT_ID,
        "arn": FakePromptData.PROMPT_ARN,
        "name": new_name,
        "description": new_description,
        "createdAt": FakePromptData.CREATED_AT,
        "updatedAt": FakePromptData.UPDATED_AT,
        "version": "1"
    }

    if error_code is None:
        bedrock_stubber.stub_update_prompt(expected_params, response)
    else:
        bedrock_stubber.stub_update_prompt(expected_params, response, error_code=error_code)

    if error_code is None:
        result = prompt.update_prompt(
            bedrock_client,
            FakePromptData.PROMPT_ID,
            new_name,
            new_description,
            new_template
        )
        assert result == response
    else:
        with pytest.raises(ClientError) as exc:
            prompt.update_prompt(
                bedrock_client,
                FakePromptData.PROMPT_ID,
                new_name,
                new_description,
                new_template
            )
        assert exc.value.response["Error"]["Code"] == error_code


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_delete_prompt(make_stubber, error_code):
    bedrock_client = boto3.client("bedrock-agent")
    bedrock_stubber = make_stubber(bedrock_client)

    expected_params = {
        "promptIdentifier": FakePromptData.PROMPT_ID
    }

    response = {
        "id": FakePromptData.PROMPT_ID
    }

    if error_code is None:
        bedrock_stubber.stub_delete_prompt(expected_params, response)
    else:
        bedrock_stubber.stub_delete_prompt(expected_params, response, error_code=error_code)

    if error_code is None:
        result = prompt.delete_prompt(bedrock_client, FakePromptData.PROMPT_ID, True)
        assert result == response
    else:
        with pytest.raises(ClientError) as exc:
            prompt.delete_prompt(bedrock_client, FakePromptData.PROMPT_ID, True)
        assert exc.value.response["Error"]["Code"] == error_code


@pytest.mark.parametrize("error_code", [None, "TestException"])
def test_list_prompts(make_stubber, error_code):
    bedrock_client = boto3.client("bedrock-agent")
    bedrock_stubber = make_stubber(bedrock_client)

    max_results = 10
    expected_params = {
        "maxResults": max_results
    }

    response = {
        "promptSummaries": [
            {
                "id": FakePromptData.PROMPT_ID,
                "arn": f"arn:aws:bedrock:us-east-1:123456789012:prompt/{FakePromptData.PROMPT_ID}",
                "name": FakePromptData.PROMPT_NAME,
                "description": FakePromptData.PROMPT_DESCRIPTION,
                "createdAt": FakePromptData.CREATED_AT,
                "updatedAt": FakePromptData.UPDATED_AT,
                "version": "1"
            }
        ]
    }

    if error_code is None:
        bedrock_stubber.stub_list_prompts(expected_params, response)
    else:
        bedrock_stubber.stub_list_prompts(expected_params, response, error_code=error_code)

    if error_code is None:
        result = prompt.list_prompts(bedrock_client, max_results)
        assert result == response["promptSummaries"]
    else:
        with pytest.raises(ClientError) as exc:
            prompt.list_prompts(bedrock_client, max_results)
        assert exc.value.response["Error"]["Code"] == error_code
