from troposphere import Output, Ref, Template,Tags
from troposphere.s3 import Bucket, PublicRead, VersioningConfiguration, BucketEncryption, ServerSideEncryptionRule, ServerSideEncryptionByDefault, WebsiteConfiguration


t = Template()

t.set_description(
    "AWS CloudFormation Sample Template S3_Bucket: Sample template showing "
    "how to create a publicly accessible S3 bucket. "
    "**WARNING** This template creates an Amazon S3 Bucket. "
    "You will be billed for the AWS resources used if you create "
    "a stack from this template.")

s3bucket = t.add_resource(
	Bucket(
		"S3Bucket",
		BucketName="codingtest-aws",
		VersioningConfiguration=VersioningConfiguration(
			Status="Enabled",
		),
		Tags=Tags({"codingtest":"webFront"}),
		BucketEncryption=BucketEncryption(
			ServerSideEncryptionConfiguration=[
				ServerSideEncryptionRule(
					ServerSideEncryptionByDefault=ServerSideEncryptionByDefault(
						SSEAlgorithm="AES256"
					)
				)
			]
		),
		AccessControl=PublicRead,
		WebsiteConfiguration=WebsiteConfiguration(
			ErrorDocument="error.html",
			IndexDocument="index.html"
		),
	)
)


t.add_output(Output(
    "BucketName",
    Value=Ref(s3bucket),
    Description="Name of S3 bucket to hold website content"
))

print(t.to_json())

