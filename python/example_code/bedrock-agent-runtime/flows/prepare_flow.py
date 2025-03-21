import boto3
import json
from botocore.exceptions import ClientError
from time import sleep

def prepare_flow(flow_id):
    """
    Prepares an Amazon Bedrock Flow.
    
    Args:
        flow_id (str): The identifier of the flow that you want to prepare.
        
    Returns:
        dict: Flow information if successful, None if an error occurs
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




def main():
    # Replace with your flow ID
    flow_id = "YMNI7EF04U"
    
    # Get and display flow details
    prepare_flow(flow_id)



if __name__ == "__main__":
    main()
