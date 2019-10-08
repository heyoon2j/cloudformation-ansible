
"""Generating CloudFormation template."""
from troposphere import(Base64, ec2, GetAtt, Join, Output, Parameter, Ref, Template, FindInMap)
from troposphere.iam import (InstanceProfile, PolicyType as IAMPolicy, Role)
from awacs.aws import (Action, Allow, Policy, PolicyDocument, Principal, Statement)
from awacs.sts import AssumeRole


AnsiblePlaybookFile = "ansible/deployServer.yml"
ApplicationPort = "80"
GithubAnsibleURL = "https://github.com/yoon2ix/cloudformation-ansible.git"
VpvID = "vpc-0a93272040286fd79"
SubnetID = "subnet-07f69f1a00576f7de"
SecurityGroupID = "sg-00a44143f9b9fe72c"
SecurityGroupName = "Deployment-SG"
HostFile = "inventory/deployServer_hosts"

t= Template()

t.add_description("Effective DevOps in AWS: Deploy Template")

# Deploy Server for Ansible
AnsiblePullCmd = "/usr/bin/ansible-pull -U {} {} -i {}".format(GithubAnsibleURL, AnsiblePlaybookFile, HostFile)


# AWS IAM Profile
cfnrole = t.add_resource(Role(
	"CFNRole",
	AssumeRolePolicyDocument=PolicyDocument(
		Statement=[
			Statement(
				Effect=Allow,
				Action=[AssumeRole],
				Principal=Principal("Service", ["ec2.amazonaws.com"])
			)
		]
	)
))

cfninstanceprofile = t.add_resource(InstanceProfile(
	"CFNInstanceProfile",
	Roles=[Ref(cfnrole)]
))


# Key Pair Setting
keyname_param=t.add_parameter(
	Parameter(
		"KeyPair",
		Description="Name of an existing EC2 KeyPair to SSH",
		Type="AWS::EC2::KeyPair::KeyName",
		ConstraintDescription="must be the name of an existing EC2 KeyPair.",
	)
)

# Security Group Setting
security_param=t.add_resource(
	ec2.SecurityGroup(
		"SecurityGroup",
		GroupDescription="Allow SSH and TCP/{} access".format(ApplicationPort),
		GroupName="DeployServer-SG",
		VpcId=VpvID,
		SecurityGroupIngress=[
			ec2.SecurityGroupRule(
				IpProtocol="tcp",
				FromPort="22",
				ToPort="22",
				CidrIp="0.0.0.0/0",
			),
			ec2.SecurityGroupRule(
				IpProtocol="tcp",
				FromPort="80",
				ToPort="80",
				CidrIp="0.0.0.0/0",
			),
		],
		
	)
)

# UserData
ud=Base64(
	Join('\n',[
		"#!/bin/bash",
		"sudo yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm",
		"yum install --enablerepo=epel -y git",
		"yum install -y python-pip",
		"pip install ansible",
		AnsiblePullCmd
	])
)


t.add_mapping(
	'RegionMap', {
		"us-west-1": {"AMI": "ami-951945d0"},
		"us-west-2": {"AMI": "ami-16fd7026"},
		"eu-west-1": {"AMI": "ami-24506250"},
		"sa-east-1": {"AMI": "ami-3e3be423"},
		"ap-southeast-1": {"AMI": "ami-74dda626"},
		"ap-northeast-1": {"AMI": "ami-dcfa4edd"},
		"ap-northeast-2": {"AMI": "ami-0d097db2fb6e0f05e"}
	}
)

ec2_instance=t.add_resource(
	ec2.Instance(
		"instance",
		ImageId=FindInMap("RegionMap",Ref("AWS::Region"),"AMI"),
		InstanceType="t2.micro",
		KeyName=Ref(keyname_param),
		SecurityGroupIds=[Ref(security_param)],
		SubnetId=SubnetID,
		UserData=ud,
		IamInstanceProfile=Ref(cfninstanceprofile),
		Tags=[
			{ "Key" : "Name", "Value" : "deployServer"}
		],
	)
)

# GetAtt: Fn::GetAtt

t.add_output([
	Output(
		"InstanceId",
		Description="InstanceId of the newly created EC2 instance",
		Value=Ref(ec2_instance),
	),
	Output(
		"PublicIp",
		Description="Public IP address of the created EC2 instance",
		Value=GetAtt(ec2_instance,"PublicIp"),
	),
	Output(
		"WebUrl",
		Description="Appliaction endpoint",
		Value=Join("",[
			"http://", GetAtt(ec2_instance, "PublicDnsName"),":",ApplicationPort
		]),
	),
])

print t.to_json()


