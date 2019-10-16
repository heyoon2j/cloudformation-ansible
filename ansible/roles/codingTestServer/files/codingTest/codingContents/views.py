from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import os
import boto3
import json

my_region_name=os.environ.get('AWS_DEFAULT_REGION')
access_key_id=os.environ.get('AWS_ACCESS_KEY_ID')
secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')


# Create your views here.

def index(request):
	return HttpResponse("Hello, world.")


def sns(request):
	payload = {
		"client_endpoint":"jysz93@naver.com"		
	}

	client = boto3.client('lambda', region_name=my_region_name, aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
	response = client.invoke(
		FunctionName='SubscriptionSNS',
		InvocationType='RequestResponse',
		LogType='Tail',
		Payload=bytes(json.dumps(payload), encoding='utf8'),
	)
	return HttpResponse(response['StatusCode'])
	test=response['FunctionError']+'\n'+response['LogResult']+'\n'+response['Payload']+'\n'
	return HttpResponse(test)


def sns_r(request):
	payload={
		"client_endpoint":"jysz93@naver.com",
		"message":"Congraturation!!!"
	}

	client = boto3.client('lambda', region_name=my_region_name, aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
	response = client.invoke(
		FunctionName='TestResultSNS',
		InvocationType='RequestResponse',
		LogType='Tail',
		Payload=bytes(json.dumps(payload), encoding='utf8'),
	)
	return HttpResponse(response)




