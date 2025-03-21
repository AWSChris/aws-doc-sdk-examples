# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Amazon Bedrock Flow Runner for Playlist Generation

This module provides functionality to execute an existing Amazon Bedrock flow that generates
music playlists based on user-specified genre and number of songs. It handles flow invocation,
response streaming, and error handling.

The module interacts with a pre-configured Bedrock flow that expects:
    - Input: JSON document containing genre and number of songs
    - Output: Generated playlist as formatted text

Functions:
    invoke_flow(client, flow_id: str, flow_alias_id: str, input_data: dict) -> dict:
        Invokes a Bedrock flow and processes its streaming response.
        Returns a dictionary containing flow status and input requirements.

    run_playlist_flow(bedrock_agent_client, flow_id: str, flow_alias_id: str) -> None:
        Handles user input collection and flow execution for playlist generation.
        Prompts user for genre and number of songs.

    main() -> None:
        Entry point for the script. Sets up AWS client and initiates the flow execution.
"""

import logging
import boto3
import botocore

import botocore.exceptions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def invoke_flow(client, flow_id, flow_alias_id, input_data):
    """
    Invoke an Amazon Bedrock flow and handle the response stream.

    Args:
        client: Boto3 client for Amazon Bedrock agent runtime.
        flow_id: The ID of the flow to invoke.
        flow_alias_id: The alias ID of the flow.
        input_data: Input data for the flow.

    Returns:
        Dict containing flow_complete status, input_required info, and execution_id
    """

    response = None
    request_params = None

    request_params = {
            "flowIdentifier": flow_id,
            "flowAliasIdentifier": flow_alias_id,
            "inputs": [input_data],
            "enableTrace": True
        }


    response = client.invoke_flow(**request_params)


    input_required = None
    flow_status = ""

    # Process the streaming response
    for event in response['responseStream']:

        # Check if flow is complete.
        if 'flowCompletionEvent' in event:
            flow_status = event['flowCompletionEvent']['completionReason']

        # Print the model output.
        elif 'flowOutputEvent' in event:
            print(event['flowOutputEvent']['content']['document'])

        # Log trace events.
        elif 'flowTraceEvent' in event:
            logger.info("Flow trace:  %s", event['flowTraceEvent'])

    return {
        "flow_status": flow_status,
        "input_required": input_required,
    }


def run_playlist_flow(bedrock_agent_client, flow_id, flow_alias_id):
    """
    Runs the playlist generator flow.

    Args:
        bedrock_agent_client: Boto3 client for Amazon Bedrock agent runtime.
        flow_id: The ID of the flow to run.
        flow_alias_id: The alias ID of the flow.

    """


    print ("Welcome to the playlist generator flow.")
    # Get the initial prompt from the user.
    genre = input("Enter genre: ")
    number_of_songs = int(input("Enter number of songs: "))


    # Use prompt to create input data.
    flow_input_data = {
        "content": {
            "document": {
                "genre" : genre,
                "number" : number_of_songs
            }
        },
        "nodeName": "FlowInput",
        "nodeOutputName": "document"
    }

    try:


        result = invoke_flow(
                bedrock_agent_client, flow_id, flow_alias_id, flow_input_data)

        status = result['flow_status']
  
        if status == "SUCCESS":
                # The flow completed successfully.
                finished = True
                logger.info("The flow %s successfully completed.", flow_id)
        else:
            print (f"Status {status} not supported")

    except botocore.exceptions.ClientError as e:
        print(f"Client error: {str(e)}")
        logger.error("Client error: %s", {str(e)})

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        logger.error("An error occurred: %s", {str(e)})
        logger.error("Error type: %s", {type(e)})


def main():
    """
    Main entry point for the Bedrock flow playlist generator.

    This function:
    1. Sets up the Bedrock agent runtime client using the default AWS profile
    2. Initializes the flow with predefined Flow ID and Flow Alias ID
    3. Executes the playlist generation flow
    """

    # Replace these with your actual flow ID and flow alias ID.
    #FLOW_ID = 'D25PS1P3PA'
    FLOW_ALIAS_ID = 'TSTALIASID'

    FLOW_ID='YOUR_FLOW_ID'

    logger.info("Starting conversation with FLOW: %s ID: %s",
                FLOW_ID, FLOW_ALIAS_ID)

    # Get the Bedrock agent runtime client.
    session = boto3.Session(profile_name='default')
    bedrock_agent_client = session.client('bedrock-agent-runtime')

    # Start the conversation.
    run_playlist_flow(bedrock_agent_client, FLOW_ID, FLOW_ALIAS_ID)

    logger.info("Conversation with FLOW: %s ID: %s finished",
                FLOW_ID, FLOW_ALIAS_ID)


if __name__ == "__main__":
    main()


