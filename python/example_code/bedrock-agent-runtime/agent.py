# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

# snippet-start:[python.example_code.bedrock-agent-runtime.InvokeAgent.complete]
import logging
from uuid import uuid4
import boto3

from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_session_id():
    """Returns a unique ID for the chat session."""
    return str(uuid4())



def chat_with_agent(client, agent_id, agent_alias_id):
    """Chats with the Specified amazon Bedrock agent.
        Args:
        client: Boto3 client for Amazon Bedrock agent runtime.
        agent_id: The ID of the flow to invoke.
        agent_alias_id: The alias ID of the flow.
    """


    session_id = generate_session_id()


    print("Chat bot started (type 'quit' to exit)")
    print("-" * 50)

    while True:
        # Get user input
        user_message = input("You: ")

        if user_message.lower() == 'quit':
            print("Ending chat session...")
            break

        try:
            # Invoke the agent
            response = client.invoke_agent(
                agentId=agent_id,
                agentAliasId=agent_alias_id,
                sessionId=f'{session_id}',
                inputText=user_message
            )

            # Process the streaming response
            for event in response['completion']:
                if 'chunk' in event:
                    chunk = event['chunk']['bytes'].decode('utf-8')
                    print("Agent:", chunk, end='', flush=True)
            print("\n" + "-" * 50)

        except ClientError as e:
            print(f"Error occurred: {e.response['Error']['Message']}")
            break


def main():
    """Entry point for the example"""
    # Replace these with your actual agent ID and alias ID
    AGENT_ID = 'your-agent-id'
    AGENT_ALIAS_ID = 'your-agent-alias-id'


    try:
        client = boto3.client('bedrock-agent-runtime')

        chat_with_agent(client, AGENT_ID, AGENT_ALIAS_ID)

    except KeyboardInterrupt:
        print("\nChat session terminated by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()
 # snippet-end:[python.example_code.bedrock-agent-runtime.InvokeAgent.complete]
