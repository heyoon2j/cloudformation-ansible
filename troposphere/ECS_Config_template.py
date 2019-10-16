"""Generating CloudForamtion template."""
from ipaddress import ip_network
from ipify import get_ip
from troposphere import ( Base64, Export, Join, Output, Parameter, Ref, Sub, Template, ec2 )
from troposphere.autoscaling import( AutoScalingGroup, LaunchConfiguration, ScalingPolicy )
from troposphere.cloudwatch import ( Alarm, MetricDimension )
from troposphere.ecs import Cluster
from troposphere.iam import ( InstanceProfile, Role )

PublicCidrIp = str(ip_network(get_ip()))

t = Template()

t.add_description("Effective DevOps in AWS: ECS Cluster")

t.add_parameter(
	Parameter(
		"KeyPair",
		Description="Name of an existing EC2 KeyPair to SSH",
		Type="AWS::EC2::KeyPair::KeyName",
		ConstraintDescription="must be the name of an existing EC2 KeyPair.",
	)
)

t.add_parameter(
	Parameter(
		"VpcId",
		Type="AWS::EC2::VPC::Id",
		Description="VPC"
	)
)

t.add_parameter(
	Parameter(
		"PublicSubnet",
		Type="List<AWS::EC2::Subnet::Id>",
		Description="PublicSubnet",
		ConstraintDescription="PublicSubnet"
	)
)

# Cluster Config
t.add_resource(
	Cluster(
		"ECSCluster",
		ClusterName="CodingTestCluster",
	)
)


# Networking Config, VPC, Subnet, SecuritGroup
t.add_resource(
	ec2.SecurityGroup(
		"SecurityGroup",
		GroupDescription="Allow SSH and private network access",
		GroupName="CodingTestCluster-SG",
		SecurityGroupIngress=[
			ec2.SecurityGroupRule(
				IpProtocol="tcp",
				FromPort=0,
				ToPort=65535,
				CidrIp="10.0.64.0/18"
			),
			ec2.SecurityGroupRule(
				IpProtocol="tcp",
				FromPort=0,
				ToPort=65535,
				CidrIp="10.0.192.0/18"
			),
			ec2.SecurityGroupRule(
				IpProtocol="tcp",
				FromPort="22",
				ToPort="22",
				CidrIp=PublicCidrIp,
			),
		],
		VpcId=Ref("VpcId")
	)
)

# Container IAM Role 
t.add_resource(
	Role(
		"EcsClusterRole",
		ManagedPolicyArns=[
			'arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM',
			'arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly',
			'arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role',
			'arn:aws:iam::aws:policy/CloudWatchFullAccess'
		],
		AssumeRolePolicyDocument={
			'Version' : '2012-10-17',
			'Statement' : [
				{
					'Action' : 'sts:AssumeRole',
					'Principal' : { 'Service' : 'ec2.amazonaws.com'},
					'Effect' : 'Allow',
				},
			]	
		}
	)
)

t.add_resource(
	InstanceProfile(
		'EC2InstanceProfile',
		Roles=[Ref('EcsClusterRole')],
	)
)





# ClouWatch Container Insite







# Instance Config
t.add_resource(
	LaunchConfiguration(
		'ContainerInstances',
		InstanceType='t2.micro',
		ImageId='ami-093714bddebb6d7e1',
		KeyName=Ref("KeyPair"),
		SecurityGroups=[Ref("SecurityGroup")],
		IamInstanceProfile=Ref("EC2InstanceProfile"),
		AssociatePublicIpAddress='true',
		UserData=Base64(
			Join('',
				[
					"#!bin/bash -xe\n",
					"ehco ECS_CLUSTER=",
					Ref('ECSCluster'),
					" >> /etc/ecs/ecs.config\n",
					"yum install -y aws-cfn-bootstrap\n",
					"/opt/aws/bin/cfn-siganl -e $? ",
					"	--stack ",
					Ref('AWS::StackName'),
					"	--resource ECSAutoScalingGroup",
					"	--region ",
					Ref('AWS::Region'),
					"\n"
				]
			)
		)
	)
)


# AutoScalingGroup
t.add_resource(
	AutoScalingGroup(
		'ECSAutoScalingGroup',
		DesiredCapacity='1',
		MinSize='1',
		MaxSize='5',
		VPCZoneIdentifier=Ref("PublicSubnet"),
		LaunchConfigurationName=Ref('ContainerInstances'),
		AvailabilityZones=['ap-northeast-2a', 'ap-northeast-2c'],
	)
)


print(t.to_json())

