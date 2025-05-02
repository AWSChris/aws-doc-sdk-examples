#!/usr/bin/env python3

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Unit tests for code_interpreter_example.py.
"""

import base64
import os
import sys
from io import BytesIO

import boto3
import pytest
from botocore.exceptions import ClientError

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from code_interpreter.code_interpreter_example import BedrockAgentCodeInterpreter


class TestBedrockAgentCodeInterpreter:
    """Tests for the BedrockAgentCodeInterpreter class."""

    @pytest.fixture
    def mock_bedrock_agent_runtime_client(self, make_stubber):
        """Create a mock Bedrock Agent Runtime client and return a stubber for it."""
        from test_tools.bedrock_agent_runtime_stubber import BedrockAgentRuntimeStubber
        bedrock_agent_runtime_client = boto3.client("bedrock-agent-runtime")
        stubber = BedrockAgentRuntimeStubber(bedrock_agent_runtime_client)
        yield stubber
        stubber.assert_no_pending_responses()

    @pytest.fixture
    def mock_file(self, monkeypatch, tmp_path):
        """Create a mock file for testing."""
        test_file = tmp_path / "test_data.csv"
        test_file.write_text("col1,col2\n1,2\n3,4")
        return str(test_file)

    def test_invoke_agent_with_file_success(self, mock_bedrock_agent_runtime_client, mock_file, monkeypatch):
        """Test successful invocation of agent with a file."""
        # Mock data
        agent_id = "test-agent-id"
        agent_alias_id = "test-alias-id"
        session_id = "test-session-id"
        prompt = "Analyze this CSV file"
        
        # Read the test file content
        with open(mock_file, 'rb') as file:
            file_content = file.read()
        
        # Expected request parameters
        expected_params = {
            "agentId": agent_id,
            "agentAliasId": agent_alias_id,
            "sessionId": session_id,
            "inputText": prompt,
            "sessionState": {
                "files": [{
                    "useCase": "CODE_INTERPRETER",
                    "name": os.path.basename(mock_file),
                    "source": {
                        "sourceType": "BYTE_CONTENT",
                        "byteContent": {
                            "data": file_content,
                            "mediaType": "text/csv"
                        }
                    }
                }]
            }
        }
        
        # Mock response
        response_text = "I've analyzed your CSV file. It contains 2 rows and 2 columns."
        mock_bedrock_agent_runtime_client.add_invoke_agent_response(
            expected_params=expected_params,
            response_chunks=[{"chunk": {"bytes": response_text.encode()}}],
            version="1.0"
        )
        
        # Create the code interpreter and invoke it
        code_interpreter = BedrockAgentCodeInterpreter(mock_bedrock_agent_runtime_client.client)
        response = code_interpreter.invoke_agent_with_file(
            agent_id, agent_alias_id, session_id, prompt, mock_file
        )
        
        # Verify the response
        assert response["text"] == response_text
        assert len(response["images"]) == 0

    def test_invoke_agent_with_file_and_image_response(self, mock_bedrock_agent_runtime_client, mock_file, monkeypatch):
        """Test invocation of agent with a file that returns an image."""
        # Mock data
        agent_id = "test-agent-id"
        agent_alias_id = "test-alias-id"
        session_id = "test-session-id"
        prompt = "Create a chart from this CSV file"
        
        # Read the test file content
        with open(mock_file, 'rb') as file:
            file_content = file.read()
        
        # Expected request parameters
        expected_params = {
            "agentId": agent_id,
            "agentAliasId": agent_alias_id,
            "sessionId": session_id,
            "inputText": prompt,
            "sessionState": {
                "files": [{
                    "useCase": "CODE_INTERPRETER",
                    "name": os.path.basename(mock_file),
                    "source": {
                        "sourceType": "BYTE_CONTENT",
                        "byteContent": {
                            "data": file_content,
                            "mediaType": "text/csv"
                        }
                    }
                }]
            }
        }
        
        # Mock response with text and image
        response_text = "I've created a chart from your CSV data."
        mock_image_data = b"mock_image_data"
        
        mock_bedrock_agent_runtime_client.add_invoke_agent_response(
            expected_params=expected_params,
            response_chunks=[
                {"chunk": {"bytes": response_text.encode()}},
                {"chunk": {"bytes": mock_image_data, "contentType": "image/png"}}
            ],
            version="1.0"
        )
        
        # Mock the display_images method to avoid actually displaying images
        monkeypatch.setattr(
            BedrockAgentCodeInterpreter, 
            "display_images", 
            lambda self, images: None
        )
        
        # Create the code interpreter and invoke it
        code_interpreter = BedrockAgentCodeInterpreter(mock_bedrock_agent_runtime_client.client)
        response = code_interpreter.invoke_agent_with_file(
            agent_id, agent_alias_id, session_id, prompt, mock_file
        )
        
        # Verify the response
        assert response["text"] == response_text
        assert len(response["images"]) == 1
        assert response["images"][0]["data"] == mock_image_data
        assert response["images"][0]["content_type"] == "image/png"

    def test_invoke_agent_with_file_error(self, mock_bedrock_agent_runtime_client, mock_file):
        """Test error handling when invoking agent with a file."""
        # Mock data
        agent_id = "test-agent-id"
        agent_alias_id = "test-alias-id"
        session_id = "test-session-id"
        prompt = "Analyze this CSV file"
        
        # Read the test file content
        with open(mock_file, 'rb') as file:
            file_content = file.read()
        
        # Expected request parameters
        expected_params = {
            "agentId": agent_id,
            "agentAliasId": agent_alias_id,
            "sessionId": session_id,
            "inputText": prompt,
            "sessionState": {
                "files": [{
                    "useCase": "CODE_INTERPRETER",
                    "name": os.path.basename(mock_file),
                    "source": {
                        "sourceType": "BYTE_CONTENT",
                        "byteContent": {
                            "data": file_content,
                            "mediaType": "text/csv"
                        }
                    }
                }]
            }
        }
        
        # Mock error response
        error_code = "ValidationException"
        error_message = "Invalid request parameters"
        mock_bedrock_agent_runtime_client.add_client_error(
            "invoke_agent",
            expected_params=expected_params,
            service_error_code=error_code,
            service_message=error_message
        )
        
        # Create the code interpreter
        code_interpreter = BedrockAgentCodeInterpreter(mock_bedrock_agent_runtime_client.client)
        
        # Verify that the expected error is raised
        with pytest.raises(ClientError) as exc_info:
            code_interpreter.invoke_agent_with_file(
                agent_id, agent_alias_id, session_id, prompt, mock_file
            )
        
        assert exc_info.value.response["Error"]["Code"] == error_code
        assert exc_info.value.response["Error"]["Message"] == error_message

    def test_get_content_type(self):
        """Test the _get_content_type method."""
        code_interpreter = BedrockAgentCodeInterpreter(None)
        
        # Test known file extensions
        assert code_interpreter._get_content_type('.csv') == 'text/csv'
        assert code_interpreter._get_content_type('.json') == 'application/json'
        assert code_interpreter._get_content_type('.py') == 'text/x-python'
        assert code_interpreter._get_content_type('.png') == 'image/png'
        
        # Test unknown file extension
        assert code_interpreter._get_content_type('.unknown') == 'application/octet-stream'
