from troposphere.constants import NUMBER
from troposphere import FindInMap, GetAtt, Join, Output
from troposphere import Parameter, Ref, Template
from troposphere.awslambda import Function, Code, MEMORY_VALUES
from troposphere.cloudformation import CustomResource
from troposphere.ec2 import Instance
from troposphere.ec2 import SecurityGroup, SecurityGroupRule
from troposphere.iam import Role, Policy

LambdaRole="arn:aws:iam::087197281921:role/SNSRoleForSNS"
VpcID = "vpc-0a93272040286fd79"
SubnetId="subnet-07f69f1a00576f7de"

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
"sns_client = boto3.client('sns')\n",
"client_endpoint = 'jysz93@naver.com'\n",
"topicArn = 'arn:aws:sns:ap-northeast-2:087197281921:TestResultAlarm'\n",
"\n",
"def lambda_handler(evnet, contxt):\n",
"	response = sns_client.publish(\n",
"		TopicArn=topicArn,\n",
"		Message='Good news everyone!',\n",
"		Subject='Coding Test ',\n",
"		MessageAttributes={\n",
"			'email' :  {\n",
"				'DataType' : 'String.Array',\n",
"				'StringValue' : '[\"jysz93@naver.com\", \"jwsz93@naver.com\"]'\n",
"			}\n",
"		}\n",
"	)\n",
"\n",
"	print(response)\n"
]

security_param=t.add_resource(
	SecurityGroup(
		"SecurityGroup",
		GroupDescription="Allow SSH and TCP/{} access",
		GroupName="LambdaTestResultSNS-SG",
		VpcId=VpcID,
		SecurityGroupIngress=[
			SecurityGroupRule(
				IpProtocol="tcp",
				FromPort="22",
				ToPort="22",
				CidrIp="0.0.0.0/0",
			),
			SecurityGroupRule(
				IpProtocol="tcp",
				FromPort="80",
				ToPort="80",
				CidrIp="0.0.0.0/0",
			),
		],
		
	)
)

Function = t.add_resource(
	Function(
		"Function",
		FunctionName="TestResultSNS",
		Role=LambdaRole,
		Description="Send Test Result Email",
		Runtime="python3.7",
		Code=Code(
			ZipFile=Join("", code)
		),
		Handler="lndex.handler",
		MemorySize=Ref(MemorySize),
		Timeout=Ref(Timeout),
		#VpcConfig=VpcConfig(
		#	SecurityGroupIds=[Ref(security_param)],
		#	SubnetIds=[SubnetId],
		#)
	)
)


print(t.to_json())
