from troposphere import Template, Ref
from troposphere.iam import Role, InstanceProfile, Policy
from awacs.aws import Allow, Statement, Principal,PolicyDocument, Action
from awacs.sts import AssumeRole

t = Template()

t.set_description("AWS CloudFormation Sample Template: This template "
                  "demonstrates the creation of IAM Roles.")

 
snsrole = t.add_resource(Role(
	"SNSRole",
	RoleName="SNSRoleForSNS",
	AssumeRolePolicyDocument=PolicyDocument(
		Statement=[
			Statement(
				Effect=Allow,
				Action=[AssumeRole],
				Principal=Principal("Service", ["lambda.amazonaws.com"])
			)
		]
	),
	Policies=[
		Policy(
			PolicyName="SNSPolicy",
			PolicyDocument=PolicyDocument(
				Statement=[
					Statement(
						Effect=Allow,
						Action=[Action("sns","*")],
						Resource=["*"]
					),
				],
			)
		),
                Policy(
                        PolicyName="CloudWatchLogsPolicy",
                        PolicyDocument=PolicyDocument(
                                Statement=[
                                        Statement(
                                                Effect=Allow,
                                                Action=[Action("logs","*")],
                                                Resource=["*"]
                                        ),
                                ],
                        )
                )
	]
))

print(t.to_json())
