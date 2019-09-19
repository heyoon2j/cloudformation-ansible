from datetime import datetime
import logging
import json
import sys

import boto3
import botocore


cf = boto3.client('cloudformation')  # pylint: disable=C0103
log = logging.getLogger('deploy.cf.create_or_update')


def main(json_file):

	json_data = _parse_json(json_file)

	stack_name = json_data['Stack']['Properties']['StackName']

	params = {
		'StackName' : stack_name,
		#'RetainResources' : ,
	}
	try:
		if _stack_exists(stack_name):
			print('Deleting {}'.format(stack_name))
			stack_result = cf.delete_stack(**params)
			waiter = cf.get_waiter('stack_delete_complete')
			
		else:
			print('No Stack!!!')

		print("...waiting for stack to be ready...")
		waiter.wait(StackName=stack_name)


	except botocore.exceptions.ClientError as ex:
		error_message = ex.response['Error']['Code']
		print("Error Code: {} ".format(error_message))

		raise

		#if error_message == 'No updates are to be performed.':
		#	print("No changes")
		#else:
		#	raise
	else:
		print(json.dumps(
			cf.describe_stacks(
				StackName=stack_result['StackId']),
				indent=2,
				default=json_serial
			)
		)


# parameter_data에 JSON 파일로 로드
def _parse_json(json_file):
	with open(json_file) as json_fileobj:
		json_data = json.load(json_fileobj)
	return json_data


def _stack_exists(stack_name):
	stacks = cf.list_stacks()['StackSummaries']
	for stack in stacks:
		if stack['StackStatus'] == 'DELETE_COMPLETE':
			continue
		if stack_name == stack['StackName']:
			return True
	return False


def json_serial(obj):
	"""JSON serializer for objects not serializable by default json code"""
	if isinstance(obj, datetime):
		serial = obj.isoformat()
		return serial
	raise TypeError("Type not serializable")


if __name__ == '__main__':
	main(*sys.argv[1:])
