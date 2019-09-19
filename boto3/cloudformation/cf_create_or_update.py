'Update or create a stack given a name and template + params'
from __future__ import division, print_function, unicode_literals

from datetime import datetime
import logging
import json
import sys

import boto3
import botocore

# Cloudformation Client 설정
cf = boto3.client('cloudformation')  # pylint: disable=C0103
log = logging.getLogger('deploy.cf.create_or_update')  # pylint: disable=C0103


def main(json_file, template):
	'Update or create stack'

	json_data = _parse_json(json_file)
	template_data = _parse_template(template)

	stack_name = json_data['Stack']['Properties']['StackName']

	params = {
		'StackName': stack_name,
		'TemplateBody': template_data,
		'Parameters': json_data['Stack']['Properties']['Parameters'],
	}

	try:
		if _stack_exists(stack_name):
			print('Updating {}'.format(stack_name))
			stack_result = cf.update_stack(**params)
			waiter = cf.get_waiter('stack_update_complete')
		else:
			print('Creating {}'.format(stack_name))
			stack_result = cf.create_stack(**params)
			waiter = cf.get_waiter('stack_create_complete')

		print("...waiting for stack to be ready...")
		waiter.wait(StackName=stack_name)

	except botocore.exceptions.ClientError as ex:
		error_message = ex.response['Error']['Message']
		if error_message == 'No updates are to be performed.':
			print("No changes")
		else:
			raise
	else:
		print(json.dumps(
		cf.describe_stacks(StackName=stack_result['StackId']),
		indent=2,
		default=json_serial
	))


def _parse_template(template):
	with open(template) as template_fileobj:
		template_data = template_fileobj.read()
	cf.validate_template(TemplateBody=template_data)
	return template_data


def _parse_json(json_file):
	with open(json_file) as json_fileobj:
		json_data = json.load(json_fileobj)
	return json_data	


def json_serial(obj):
	"""JSON serializer for objects not serializable by default json code"""
	if isinstance(obj, datetime):
		serial = obj.isoformat()
		return serial
	raise TypeError("Type not serializable")


if __name__ == '__main__':
	main(*sys.argv[1:])
