"""Generating CloudForamtion template."""
from ipaddress import ip_network
from ipify import get_ip
from troposphere import ( Base64, Export, Join, Output, Parameter, Ref, Sub, Template, ec2 )
from troposphere.autoscaling import( AutoScalingGroup, LaunchConfiguration, ScalingPolicy )
from troposphere.iam import ( InstanceProfile, Role )
from troposphere.elasticloadbalancingv2 import LoadBalancer, Listener, TargetGroup
#import troposphere.elasticloadbalancing as elb


t = Template()

t.add_description("Effective DevOps in AWS: Load Balancer")
# Load Balancer Basic Config
t.add_resource(
	LoadBalancer(
		"LoadBalancer",
		Name="manageServerELB",
		IpAddressType="ipv4",
		Scheme="internal",
		Type="application",
		Subnets=["subnet-090ecdfd567016a8f","subnet-029854ef7d7aa04d1"],
		SecurityGroups=Ref("SecurityGroup"),
	)
)

# Networking Config, VPC, Subnet, SecuritGroup
t.add_resource(
	ec2.SecurityGroup(
		"SecurityGroup",
		GroupDescription="Allow SSH and private network access",
		GroupName="manageServerELB-SG",
		SecurityGroupIngress=[
			ec2.SecurityGroupRule(
				IpProtocol="tcp",
				FromPort="8000",
				ToPort="8000",
				CidrIp="0.0.0.0/0"
			),
			ec2.SecurityGroupRule(
				IpProtocol="tcp",
				FromPort="80",
				ToPort="80",
				CidrIp="0.0.0.0/0"
			),
			ec2.SecurityGroupRule(
				IpProtocol="tcp",
				FromPort="22",
				ToPort="22",
				CidrIp="0.0.0.0/0",
			),
			ec2.SecurityGroupRule(
				IpProtocol="tcp",
				FromPort="9000",
				ToPort="9000",
				CidrIp="0.0.0.0/0",
                        ),
		],
		VpcId=Ref("VpcId")
	)
)
"""
# Listeners
t.add_resource(
	Listener(
		LoadBalancerArn=Ref("LoadBalancer"),
		Port=80,
		Protocol="HTTP",
	)
)
t.add_resource(
	Listener(
		LoadBalancerArn=Ref("LoadBalancer"),
		Port=22,
		Protocol="HTTP",
	)
)
t.add_resource(
	Listener(
		LoadBalancerArn=Ref("LoadBalancer"),
		Port=8000,
		Protocol="HTTP",
	)
)
t.add_resource(
	Listener(
		LoadBalancerArn=Ref("LoadBalancer"),
		Port=9000,
		Protocol="HTTP",
	)
)
""
t.add_resourec(
	TargetGroup(

		HealthCheckEnabled = true,
		HealthCheckIntervalSeconds  = 30,
		HealthCheckPath = "/",
		HealthCheckPort = "80",
		HealthCheckProtocol = "HTTP",
		HealthCheckTimeoutSeconds = 5,
		HealthyThresholdCount = 5, 
		Matcher = Matcher(
			HttpCode = "200"
		),
		Name = "manageServerELB_TargetGroup",
		Port = 80,
		Protocol = "HTTP",
		#TargetGroupAttributes,
		#Targets  =,
		TargetType  = "instance",
		UnhealthyThresholdCount = 2,
		VpcId = "vpc-0a93272040286fd79"
	)
)

"""
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
"""
print(t.to_json())
