#!/usr/bin/env python3

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Purpose

Shows how to use the AWS SDK for Python (Boto3) with Amazon Bedrock Agent Runtime
to use the code interpreter feature with the InvokeAgent action.
"""

import argparse
import base64
import json
import logging
import os
import sys
import uuid
from io import BytesIO

import boto3
from botocore.exceptions import ClientError
import matplotlib.pyplot as plt
from PIL import Image

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = logging.getLogger(__name__)


# snippet-start:[python.example_code.bedrock-agent-runtime.CodeInterpreterExample.class]
class BedrockAgentCodeInterpreter:
    """Encapsulates Amazon Bedrock Agent Runtime code interpreter actions."""

    def __init__(self, runtime_client):
        """
        :param runtime_client: A low-level client representing the Amazon Bedrock Agents Runtime.
        """
        self.agents_runtime_client = runtime_client

    def invoke_agent_with_file(self, agent_id, agent_alias_id, session_id, prompt, file_path):
        """
        Sends a prompt and a file for the agent to process using code interpreter.

        :param agent_id: The unique identifier of the agent to use.
        :param agent_alias_id: The alias of the agent to use.
        :param session_id: The unique identifier of the session.
        :param prompt: The prompt that you want the agent to process.
        :param file_path: Path to the file to be processed by the code interpreter.
        :return: Response from the agent including any generated content.
        """
        try:
            # Read the file
            with open(file_path, 'rb') as file:
                file_content = file.read()
                file_name = os.path.basename(file_path)
                file_extension = os.path.splitext(file_name)[1].lower()
                
                # Determine content type based on file extension
                content_type = self._get_content_type(file_extension)
            
            # Prepare the input file for code interpreter
            input_file = {
                "useCase": "CODE_INTERPRETER",
                "name": file_name,
                "source": {
                    "sourceType": "BYTE_CONTENT",
                    "byteContent": {
                        "data": file_content,
                        "mediaType": content_type
                    }
                }
            }
            
            # Invoke the agent with the file
            response = self.agents_runtime_client.invoke_agent(
                agentId=agent_id,
                agentAliasId=agent_alias_id,
                sessionId=session_id,
                inputText=prompt,
                sessionState={
                    "files": [input_file]
                }
            )
            
            # Process the response
            completion = ""
            images = []
            
            # Handle completion chunks
            for event in response.get("completion", []):
                # Check if this event contains a chunk
                if "chunk" in event:
                    chunk = event["chunk"]
                    
                    # Handle text response
                    if "bytes" in chunk:
                        completion += chunk["bytes"].decode()
                    

                # Check if this event contains files
                if "files" in event:
                    for file_info in event["files"]["files"]:
                                image_data = file_info.get("bytes")
                                if image_data:
                                    images.append({
                                        "data": image_data,
                                        "content_type": file_info["type"]
                                    })
            
            return {
                "text": completion,
                "images": images
            }
            
        except ClientError as err:
            logger.error("Couldn't invoke agent with code interpreter. %s", err)
            raise
    
    def _get_content_type(self, file_extension):
        """
        Determine the content type based on file extension.
        
        :param file_extension: The file extension.
        :return: The corresponding content type.
        """
        content_types = {
            '.csv': 'text/csv',
            '.json': 'application/json',
            '.txt': 'text/plain',
            '.py': 'text/x-python',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.xls': 'application/vnd.ms-excel',
            '.pdf': 'application/pdf'
        }
        
        return content_types.get(file_extension, 'application/octet-stream')
    
    def display_images(self, images):
        """
        Display images returned from the code interpreter.
        
        :param images: List of image data dictionaries.
        """
        if not images:
            return
        
        for i, image_info in enumerate(images):
            image_data = image_info["data"]
            image = Image.open(BytesIO(image_data))
            
            plt.figure(figsize=(10, 8))
            plt.imshow(image)
            plt.axis('off')
            plt.title(f"Generated Image {i+1}")
            plt.show()
# snippet-end:[python.example_code.bedrock-agent-runtime.CodeInterpreterExample.class]


# snippet-start:[python.example_code.bedrock-agent-runtime.CodeInterpreterExample.main]
def main():
    """
    Shows how to use the Amazon Bedrock Agent code interpreter feature.
    """
    parser = argparse.ArgumentParser(
        description="Demonstrates Amazon Bedrock Agent code interpreter capabilities"
    )
    parser.add_argument(
        "--agent-id", 
        default="6VRFLO2QKU",
        help="The ID of the Bedrock agent to use"
    )
    parser.add_argument(
        "--agent-alias-id", 
        default="WNXOWBKRHW",
        help="The alias ID of the Bedrock agent to use"
    )
    parser.add_argument(
        "--file-path",
        default="/Users/reesch/coding/code-interpreter/song_plays.csv",

        help="Path to the file to be processed by the code interpreter"
    )
    parser.add_argument(
        "--prompt", 
        default="Tell me the most popular 10 songs and visualize them in a bar chart.",
        help="The prompt to send to the agent"
    )
    parser.add_argument(
        "--region",
        default="us-east-1",
        help="The AWS Region where the Bedrock agent is deployed"
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    bedrock_agent_runtime = boto3.client("bedrock-agent-runtime", region_name=args.region)
    code_interpreter = BedrockAgentCodeInterpreter(bedrock_agent_runtime)
    
    # Generate a unique session ID
    session_id = str(uuid.uuid4())
    
    try:
        logger.info("Invoking Bedrock agent with code interpreter...")
        response = code_interpreter.invoke_agent_with_file(
            args.agent_id,
            args.agent_alias_id,
            session_id,
            args.prompt,
            args.file_path
        )
        
        # Display the text response
        print("\nAgent Response:")
        print("-" * 40)
        print(response["text"])
        print("-" * 40)
        
        # Display any generated images
        if response["images"]:
            logger.info("Displaying %d generated images...", len(response["images"]))
            code_interpreter.display_images(response["images"])
        else:
            logger.info("No images were generated in the response.")
            
    except ClientError as err:
        logger.error("Error: %s", err)
        return 1
        
    return 0
# snippet-end:[python.example_code.bedrock-agent-runtime.CodeInterpreterExample.main]


if __name__ == "__main__":
    sys.exit(main())
