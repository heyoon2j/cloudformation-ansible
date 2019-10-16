from troposphere import GetAtt, Output, Ref, Template
from troposphere.sns import Subscription, Topic
from awacs.aws import (Action, Allow, Policy, Principal, Statement, PolicyDocument)


t = Template()

t.set_description("AWS CloudFormation Sample Template: This template ")


snstopic = t.add_resource(
	Topic(
		"SNSTopic",
		TopicName = "TestResultAlarm",
		DisplayName = "TestResultAlarm"
	)
)

print(t.to_json())
