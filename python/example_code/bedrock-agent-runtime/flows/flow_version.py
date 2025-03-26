# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
This module provides functionality delete an Amazon Bedrock flow.
"""
import logging
import boto3
from flow_alias import create_flow_alias, delete_flow_alias

from botocore.exceptions import ClientError

# Create a logger instance
logging.basicConfig(
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def create_flow_version(client, flow_id, description):
    """
    Creates a version of a Bedrock flow.

    Args:
        client: bedrock agent boto3 client.
        flow_id (str): The identifier of the flow.

    Returns:
        str: The ARN for the flow.
    """
    try:

        logger.info("Creating flow version for flow: %s.", flow_id)

        # Call CreateFlowVersion operation
        response = client.create_flow_version(
            flowIdentifier=flow_id,
            description=description
        )

        logging.info("Successfully created flow version %s for flow %s.",
            response['version'], flow_id)
        
        return response['version']

    except ClientError as e:
        logging.exception("Client error creating flow: %s", str(e))
        raise
    except Exception as e:
        logging.exception("Unexpected error creating flow : %s", str(e))
        raise

def get_flow_version(client, flow_id, flow_version):
    """
    Gets information about a version of a Bedrock flow.

    Args:
        client: bedrock agent boto3 client.
        flow_id (str): The identifier of the flow.
        flow_version (str): The flow version of the flow.

    Returns:
        dict: The response from the call to GetFlowVersion.
    """
    try:

        logger.info("Deleting flow version for flow: %s.", flow_id)

        # Call DeleteFlowVersion operation
        response = client.get_flow_version(
            flowIdentifier=flow_id,
            flowVersion=flow_version
        )

        logging.info("Successfully got flow version %s information for flow %s.",
                    flow_version,
                    flow_id)
        
        return response

    except ClientError as e:
        logging.exception("Client error getting flow version: %s", str(e))
        raise
    except Exception as e:
        logging.exception("Unexpected error getting flow version: %s", str(e))
        raise


def delete_flow_version(client, flow_id, flow_version):
    """
    Deletes a version of a Bedrock flow.

    Args:
        client: bedrock agent boto3 client.
        flow_id (str): The identifier of the flow.

    Returns:
        dict: The response from DeleteFlowVersion.
    """
    try:

        logger.info("Deleting flow version %s for flow: %s.",flow_version, flow_id)

        # Call DeleteFlowVersion operation
        response = client.delete_flow_version(
            flowIdentifier=flow_id,
            flowVersion=flow_version
        )

        logging.info("Successfully deleted flow version %s for %s.",
                flow_version,
                flow_id)
        return response

    except ClientError as e:
        logging.exception("Client error deleting flow version: %s ", str(e))
        raise
    except Exception as e:
        logging.exception("Unexpected deleting flow version: %s", str(e))
        raise




def main():
    """
     Entry point that initializes AWS client and executes flow deletion.
     Uses default AWS profile for authentication.
     """

    # Replace with your flow ID
    flow_id = "5T1KFENVFI"


    session = boto3.Session(profile_name='default')
    bedrock_agent_client = session.client('bedrock-agent')

 
    # Create the flow version and alias
    flow_version = create_flow_version(bedrock_agent_client,
                        flow_id,
                        f"flow version for flow {flow_id}.")

    alias = create_flow_alias(bedrock_agent_client,
                        flow_id,
                        flow_version,
                        "latest",
                        f"Alias for flow {flow_id}, version {flow_version}")
    
    response2 = delete_flow_alias(bedrock_agent_client, flow_id, alias)
    response1 = delete_flow_version(bedrock_agent_client, flow_id, flow_version)


    

   


if __name__ == "__main__":
    main()
