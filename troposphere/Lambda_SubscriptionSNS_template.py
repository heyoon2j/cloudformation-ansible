from troposphere.constants import NUMBER
from troposphere import FindInMap, GetAtt, Join, Output
from troposphere import Parameter, Ref, Template
from troposphere.awslambda import Function, Code, MEMORY_VALUES, VPCConfig
from troposphere.cloudformation import CustomResource
from troposphere.ec2 import Instance
from troposphere.ec2 import SecurityGroup, SecurityGroupRule
from troposphere.iam import Role, Policy

LambdaRole="arn:aws:iam::087197281921:role/SNSRoleForSNS"
VpcID = "vpc-0a93272040286fd79"
Pri_SubnetId1="subnet-090ecdfd567016a8f"
Pri_SubnetId2="subnet-029854ef7d7aa04d1"

t = Template()

t.add_version("2010-09-09")
"""
ExistingVPC = t.add_parameter(
	Parameter(
		"ExistingVPC",
		Type="AWS::EC2::VPC::Id",
		Description=(
			"The VPC ID that includes the security groups in the "
			"ExistingSecurityGroups parameter."
		),
	)
)
"""

MemorySize = t.add_parameter(
	Parameter(
		'LambdaMemorySize',
		Type=NUMBER,
		Description='Amount of memory to allocate to the Lambda Function',
		Default='128',
		AllowedValues=MEMORY_VALUES
	)
)

Timeout = t.add_parameter(
	Parameter(
		'LambdaTimeout',
		Type=NUMBER,
		Description='Timeout in seconds for the Lambda function',
		Default='60'
	)
)

t.add_mapping("AWSInstanceType2Arch",
              {u'm1.small': {u'Arch': u'PV64'},
               u't2.micro': {u'Arch': u'HVM64'}}
              )

t.add_mapping("AWSRegionArch2AMI",
              {u'ap-northeast-1': {u'HVM64': u'ami-cbf90ecb',
                                   u'PV64': u'ami-27f90e27'},
               u'ap-southeast-1': {u'HVM64': u'ami-68d8e93a',
                                   u'PV64': u'ami-acd9e8fe'},
               u'ap-southeast-2': {u'HVM64': u'ami-fd9cecc7',
                                   u'PV64': u'ami-ff9cecc5'},
               u'cn-north-1': {u'HVM64': u'ami-f239abcb',
                               u'PV64': u'ami-fa39abc3'},
               u'eu-central-1': {u'HVM64': u'ami-a8221fb5',
                                 u'PV64': u'ami-ac221fb1'},
               u'eu-west-1': {u'HVM64': u'ami-a10897d6',
                              u'PV64': u'ami-bf0897c8'},
               u'sa-east-1': {u'HVM64': u'ami-b52890a8',
                              u'PV64': u'ami-bb2890a6'},
               u'us-east-1': {u'HVM64': u'ami-1ecae776',
                              u'PV64': u'ami-1ccae774'},
               u'us-west-1': {u'HVM64': u'ami-d114f295',
                              u'PV64': u'ami-d514f291'},
               u'us-west-2': {u'HVM64': u'ami-e7527ed7',
                              u'PV64': u'ami-ff527ecf'}}
              )


code = [
"import boto3\n",
"import json\n",
"\n",
"def lambda_handler(event, context):\n",
"\n",
"       client_endpoint = event['client_endpoint']\n",
"       topicArn = 'arn:aws:sns:ap-northeast-2:087197281921:TestResultAlarm'\n",
"       filter_policy = {\n",
"              'email': [client_endpoint]\n",
"       }\n",
"\n",
"       delivery_policy = {\n",
"               'healthyRetryPolicy': {\n",
"                       'numRetries': 10,\n",
"                       'minDelayTarget': 10,\n",
"                       'maxDelayTarget': 30,\n",
"                       'numMinDelayRetries': 3,\n",
"                       'numMaxDelayRetries': 7,\n",
"                       'numNoDelayRetries': 0,\n",
"                       'backoffFunction': 'linear'\n",
"               }\n",
"       }\n",
"\n",
"       sns_client = boto3.client('sns')\n",
"       response = sns_client.subscribe(\n",
"               TopicArn=topicArn,\n",
"               Protocol='email',\n",
"               Endpoint=client_endpoint,\n",
"               Attributes={\n",
"                       'FilterPolicy': json.dumps(filter_policy),\n",
"                       'DeliveryPolicy': json.dumps(delivery_policy)\n",
"               },\n",
"               #ReturnSubscriptionArn=True|False\n",
"       )\n",
"\n",
"       print(response)\n"
]

security_param=t.add_resource(
	SecurityGroup(
		"SecurityGroup",
		GroupDescription="Allow SSH and TCP/80 access",
		GroupName="LambdaSubscriptionSNS-SG",
		VpcId=VpcID,
		SecurityGroupIngress=[
			SecurityGroupRule(
				IpProtocol="tcp",
				FromPort="22",
				ToPort="22",
				CidrIp="0.0.0.0/0",
			),	
			#SecurityGroupRule(
			#	IpProtocol="tcp",
			#	FromPort="80",
			#	ToPort="80",
			#	CidrIp="0.0.0.0/0",
			#),		
		],
		
	)
)

Function = t.add_resource(
	Function(
		"Function",
		FunctionName="SubscriptionSNS",
		Role=LambdaRole,
		Description="Send Subscription Email",
		Runtime="python3.7",
		Code=Code(
			ZipFile=Join("", code)
		),
		Handler="index.lambda_handler",
		MemorySize=Ref(MemorySize),
		Timeout=Ref(Timeout),		
		#VpcConfig=VPCConfig(
		#	SecurityGroupIds=Ref(security_param),
		#	SubnetIds=[Pri_SubnetId1,Pri_SubnetId2],
		#)
	)
)


print(t.to_json())
