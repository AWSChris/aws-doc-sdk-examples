# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
This module provides functionality delete an Amazon Bedrock flow.
"""
import logging
import boto3
from botocore.exceptions import ClientError

# Create a logger instance
logger = logging.getLogger(__name__)


def delete_flow_alias(client, flow_id, flow_alias_id):
    """
    Deletes Bedrock flow alias.

    Args:
        client: bedrock agent boto3 client.
        flow_id (str): The identifier of the flow.

    Returns:
        str: The ARN for the flow.
    """
    try:

        logger.info("Deleting flow alias %s for flow: %s.", flow_alias_id, flow_id)

        # Call DeleteFlowAlias operation
        response = client.delete_flow_alias(
            aliasIdentifier=flow_alias_id,
            flowIdentifier=flow_id
        )

        logging.info("Successfully deleted flow version for %s.", flow_id)
        return response

    except ClientError as e:
        logging.exception("Client error deleting flow version: %s", str(e))
        raise
    except Exception as e:
        logging.exception("Unexpected deleting flow version: %s", str(e))
        raise


def create_flow_alias(client, flow_id, flow_version, name, description):
    """
    Creates a flow alias for a version of a Bedrock flow.

    Args:
        client: bedrock agent boto3 client.
        flow_id (str): The identifier of the flow.

    Returns:
        str: The ARN for the flow.
    """

    try:
        logger.info("Creating flow alias for flow: %s.", flow_id)

        response = client.create_flow_alias(
            flowIdentifier=flow_id,
            name=name,
            description=description,
            routingConfiguration=[
                {
                    "flowVersion": flow_version
                }
            ]
        )
        logger.info("Successfully created flow alias for %s.", flow_id)

        return response['id']

    except ClientError as e:
        logging.exception("Client error creating alias for flow: %s - %s",
                flow_id, str(e))
        raise
    except Exception as e:
        logging.exception("Unexpected error creating alias for flow : %s - %s",
                flow_id, str(e))
        raise

