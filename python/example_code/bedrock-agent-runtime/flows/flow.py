# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to use the AWS SDK for Python (Boto3) with the Amazon Bedrock Agents Runtime 
to manage an Amazon Bedrock flow.
"""

import logging
from time import sleep
import boto3
from botocore.exceptions import ClientError

#from print_json import pretty_print_json

logging.basicConfig(
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# snippet-start:[python.example_code.bedrock-agent.create_flow]
def create_flow(client, flow_name, flow_description, role_arn, flow_def):
    """
    Creates an Amazon Bedrock flow.

    Args:
    client: bedrock agent boto3 client.
    flow_name (str): The name for the new flow.
    role_arn (str):  The ARN for the IAM role that use flow uses.
    flow_def (json): The JSON definition of the flow that you want to create.

    Returns:
        dict: Flow information if successful, None if an error occurs
    """
    try:

        logger.info("Creating flow: %s.", flow_name)

        response = client.create_flow(
            name=flow_name,
            description=flow_description,
            executionRoleArn=role_arn,
            definition=flow_def
        )

        logger.info("Successfully created flow: %s. ID: %s",
                    flow_name,
                    {response['id']})
        """
        print(flow_name)
        print(role_arn)
        pretty_print_json(flow_def)
        pretty_print_json(response)
        """
        return response

    except ClientError as e:
        logger.exception("Client error creating flow: %s", {str(e)})
        raise

    except Exception as e:
        logger.exception("Unexepcted error creating flow: %s", {str(e)})
        raise
# snippet-end:[python.example_code.bedrock-agent.create_flow]

# snippet-start:[python.example_code.bedrock-agent.prepare_flow]
def prepare_flow(flow_id):
    """
    Prepares an Amazon Bedrock Flow.
    
    Args:
        flow_id (str): The identifier of the flow that you want to prepare.
        
    Returns:
        dict: Flow information if successful, None if an error occurs.
    """
    try:
        # Create a Bedrock Agent client
        client = boto3.client('bedrock-agent')
        
        # Call GetFlow operation
        response = client.prepare_flow(
            flowIdentifier=flow_id
        )

        id= response.get('id')
        status = response.get('status')

        print(f"Flow ID: {id}")
        print(f"Flow Status: {status}")

        if status == "Preparing":
            while status == "Preparing":
                print(f"Preparing flow - {flow_id}")     
                sleep(5)
                response = client.get_flow(
                    flowIdentifier=flow_id
                )
                status = response.get('status')
                print(f"Flow Status: {status}")
        else:
            print(f"Flow {flow_id} is not preparing. Current status: {status}")


        return response

        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"Flow with ID {flow_id} not found")
        elif e.response['Error']['Code'] == 'AccessDeniedException':
            print("You don't have permission to access this flow")
        else:
            print(f"Error getting flow details: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None
# snippet-end:[python.example_code.bedrock-agent.prepare_flow]  


# snippet-start:[python.example_code.bedrock-agent.delete_flow]  
def delete_flow(client, flow_id):
    """
    Deletes a Bedrock flow.

    Args:
    client: bedrock agent boto3 client.
        flow_id (str): The identifier of the flow that you want to delete.

    Returns:
        dict: Flow information if successful, None if an error occurs
    """
    try:

        # Call DeleteFlow operation
        response = client.delete_flow(
            flowIdentifier=flow_id
        )

        print(f"Flow {flow_id} deleted successfully")
        return response

    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"Flow with ID {flow_id} not found")
        elif e.response['Error']['Code'] == 'AccessDeniedException':
            print("You don't have permission to delete this flow")
        else:
            print(f"Error deleting flow: {str(e)}")
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise
# snippet-end:[python.example_code.bedrock-agent.delete_flow]  
