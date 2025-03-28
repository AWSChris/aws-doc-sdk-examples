# Amazon Bedrock Agents Runtime code examples for the SDK for Python

## Overview

Shows how to use the AWS SDK for Python (Boto3) to work with Amazon Bedrock Agents Runtime.

<!--custom.overview.start-->
<!--custom.overview.end-->

_Amazon Bedrock Agents Runtime offers you the ability to run agents and flows in your application._

## ⚠ Important

* Running this code might result in charges to your AWS account. For more details, see [AWS Pricing](https://aws.amazon.com/pricing/) and [Free Tier](https://aws.amazon.com/free/).
* Running the tests might result in charges to your AWS account.
* We recommend that you grant your code least privilege. At most, grant only the minimum permissions required to perform the task. For more information, see [Grant least privilege](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#grant-least-privilege).
* This code is not tested in every AWS Region. For more information, see [AWS Regional Services](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services).

<!--custom.important.start-->
<!--custom.important.end-->

## Code examples

### Prerequisites

For prerequisites, see the [README](../../README.md#Prerequisites) in the `python` folder.

Install the packages required by these examples by running the following in a virtual environment:

```
python -m pip install -r requirements.txt
```

<!--custom.prerequisites.start-->
<!--custom.prerequisites.end-->

### Basics

Code example that shows how to create a simple flow that generates music playlists.

- [Learn the basics](flows/playlist_flow.py)

### Single actions

Code excerpts that show you how to call individual service functions.

- [InvokeAgent](bedrock_agent_runtime_wrapper.py#L33)
- [InvokeFlow](bedrock_agent_runtime_wrapper.py#L71)
- [CreateFlow](flows/flow.py#L18) 
- [PrepareFlow](flows/flow.py#L58) 
- [DeleteFlow](flows/flow.py#L114) 
- [CreateFlowVersion](flows/flow_version.py#L18) 
- [GetFlowVersion](flows/flow_version.py#L55) 
- [DeleteFlowVersion](flows/flow_version.py#L92) 
- [CreateFlowAlias](flows/flow_alias.py#L15) 
- [DeleteFlowAlias](flows/flow_alias.py#L56) 




<!--custom.examples.start-->
<!--custom.examples.end-->

## Run the examples

### Instructions


<!--custom.instructions.start-->
<!--custom.instructions.end-->


#### Learn the basics

Shows how to create a simple flow that generates music playlists.
The flow includes a prompt node that generates a playlist for a chosen genre
and number of songs. The example created the nodes and permissions
for the flow.

Start the example by running the following at a command prompt:

```
python flows/flow-playlist_flow.py
```
When prompted, enter the genre of music and the number of songs you want
in the playlist.
Optionally, the script can delete the resources that it creates. If you want to use the flow later, such as in the Amazon Bedrock console, enter `n` when the script prompts you to delete resources. Note that you will then need to manually delete the resources.




### Tests

⚠ Running tests might result in charges to your AWS account.


To find instructions for running these tests, see the [README](../../README.md#Tests)
in the `python` folder.



<!--custom.tests.start-->
<!--custom.tests.end-->

## Additional resources

- [Amazon Bedrock Agents Runtime User Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
- [Amazon Bedrock Agents Runtime API Reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Agents_for_Amazon_Bedrock_Runtime.html)
- [SDK for Python Amazon Bedrock Agents Runtime reference](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime.html)

<!--custom.resources.start-->
<!--custom.resources.end-->

---

Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.

SPDX-License-Identifier: Apache-2.0
