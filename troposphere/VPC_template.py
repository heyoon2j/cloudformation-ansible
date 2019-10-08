"""
1. Create VPC
   1) IPv4 CIDR block Set => "CidrBlock": "10.0.0.0/16", 
   2) IPv6 CIDR block(No IPv6 CIDR Block, Amazon provided IPv6 CIDR block) => "AmazonProvidedIpv6CidrBlock": false, 
   3) VPC Name => "Tags" :  [ {"Key":"Name","Value":"My VPC"} ] 
   4) Dry Run => "DryRun": true, 
   5) Tenanacy Set(default, dedicated, host) => "InstanceTenancy": "default"

2. Create Subnet
   1) CIDR => "CidrBlock": "10.0.0.0/18", 
   2) AvailabilityZone => "AvailabilityZone": "us-east-2c",
   3) VpcId => "VpcId": "vpc-081ec835f3EXAMPLE",

3. Create InternetGateway
4. Connect VPC to InternetGateway
5. Create Route Table
6. Connect Subnet to Route Table

"""
"""Generating CloudFormation template."""
from troposphere import(Base64, ec2, GetAtt, Join, Output, Parameter, Ref, Template, FindInMap)
from troposphere.ec2 import PortRange, NetworkAcl, Route, \
    VPCGatewayAttachment, SubnetRouteTableAssociation, Subnet, RouteTable, \
    VPC, NetworkInterfaceProperty, NetworkAclEntry, \
    SubnetNetworkAclAssociation, EIP, Instance, InternetGateway, \
    SecurityGroupRule, SecurityGroup
from troposphere.policies import CreationPolicy, ResourceSignal
from troposphere.cloudformation import Init, InitFile, InitFiles, \
    InitConfig, InitService, InitServices


t= Template()

t.add_description("Effective DevOps in AWS: VPC Template")


ref_region = Ref('AWS::Region')


### Create VPC
VPC = t.add_resource(
	VPC(
		"VPC",
		CidrBlock="10.0.0.0/16",
		EnableDnsHostnames="true",
		EnableDnsSupport="true",
		InstanceTenancy="default",
		Tags=[
			{ "Key" : "Name", "Value" : "DevOpsVPC"}
		]
	)
)


### Create Subnet
pub1_subnet = t.add_resource(
	Subnet(
		"Pub1Subnet",
		AvailabilityZone="ap-northeast-2a",
		CidrBlock="10.0.0.0/18",
		VpcId=Ref(VPC),
		MapPublicIpOnLaunch="true",
		Tags=[
			{ "Key" : "Name", "Value" : "Pub1_Subnet"}
		]
	)
)
pri1_subnet = t.add_resource(
	Subnet(
		'Pri1Subnet',
		AvailabilityZone="ap-northeast-2a",
		CidrBlock='10.0.64.0/18',
		VpcId=Ref(VPC),
		MapPublicIpOnLaunch="false",
		Tags=[
			{ "Key" : "Name", "Value" : "Pri1_Subnet"}
		]
	)
)

pub2_subnet = t.add_resource(
	Subnet(
		'Pub2Subnet',
		AvailabilityZone="ap-northeast-2c",
		CidrBlock='10.0.128.0/18',
		VpcId=Ref(VPC),
		MapPublicIpOnLaunch="true",
		Tags=[
			{ "Key" : "Name", "Value" : "Pub2_Subnet"}
		]
	)
)
pri2_subnet = t.add_resource(
	Subnet(
		'Pri2Subnet',
		AvailabilityZone="ap-northeast-2c",
		CidrBlock='10.0.192.0/18',
		VpcId=Ref(VPC),
		MapPublicIpOnLaunch="false",
		Tags=[
			{ "Key" : "Name", "Value" : "Pri2_Subnet"}
		]
	)
)


### Create InternetGateway

internetGateway = t.add_resource(
	InternetGateway(
		'InternetGateway',
		Tags=[
			{ "Key" : "Name", "Value" : "DevOpsInternetGateway"}
		]
	)
)

### Connect VPC to InternetGateway

gatewayAttachment = t.add_resource(
	VPCGatewayAttachment(
		'AttachGateway',
		VpcId=Ref(VPC),
		InternetGatewayId=Ref(internetGateway)
	)
)


### Create Routing Table
pub_routeTable = t.add_resource(
	RouteTable(
		'PublicRouteTable',
		VpcId=Ref(VPC),
		Tags=[
			{ "Key" : "Name", "Value" : "Public Route Table"}
		]
	)
)

pri_routeTable = t.add_resource(
	RouteTable(
		'PrivateRouteTable',
		VpcId=Ref(VPC),
		Tags=[
			{ "Key" : "Name", "Value" : "Private Route Table"}
		]
	)
)

### Routing
pub_internet_route = t.add_resource(
	Route(
		'PubInternetRoute',
		GatewayId=Ref('InternetGateway'),
		DestinationCidrBlock='0.0.0.0/0',
		RouteTableId=Ref(pub_routeTable),
	)
)

pri_internet_route = t.add_resource(
	Route(
		'PriInternetRoute',
		GatewayId=Ref('InternetGateway'),
		DestinationCidrBlock='0.0.0.0/0',
		RouteTableId=Ref(pri_routeTable),
	)
)


### Connect Subnet to Routing Table
pub1_subnetRouteTableAssociation = t.add_resource(
	SubnetRouteTableAssociation(
		'Pub1SubnetRouteTableAssociation',
		SubnetId=Ref(pub1_subnet),
		RouteTableId=Ref(pub_routeTable),
	)
)

pub2_subnetRouteTableAssociation = t.add_resource(
	SubnetRouteTableAssociation(
		'Pub2SubnetRouteTableAssociation',
		SubnetId=Ref(pub2_subnet),
		RouteTableId=Ref(pub_routeTable),
	)
)

pri1_subnetRouteTableAssociation = t.add_resource(
	SubnetRouteTableAssociation(
		'Pri1SubnetRouteTableAssociation',
		SubnetId=Ref(pri1_subnet),
		RouteTableId=Ref(pri_routeTable),
	)
)

pri2_subnetRouteTableAssociation = t.add_resource(
	SubnetRouteTableAssociation(
		'Pri2SubnetRouteTableAssociation',
		SubnetId=Ref(pri2_subnet),
		RouteTableId=Ref(pri_routeTable),
	)
)

print(t.to_json())
