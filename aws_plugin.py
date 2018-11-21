import json

import boto3
from slackbot import settings
from slackbot.bot import respond_to


def get_instance_informations_from_raw_data(raw_data: dict) -> list:

    instances = []
    raw_instances = raw_data['Reservations']

    for raw_instance in raw_instances:
        instance = raw_instance['Instances'][0]
        if not instance['State']['Name'] == 'running':
            continue

        tags = {
            tag['Key']: tag['Value'] for tag in instance['Tags']
        }
        host = {
            'hostname':
                instance['InstanceId'],
            'private_ip':
                instance['PrivateIpAddress'],
            'launch_time':
                instance['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S %Z'),
            'type':
                instance['InstanceType'],
            'stage':
                tags['suitebook:stage'],
            'group':
                tags['suitebook:role'].split('/'),
        }
        instances.append(host)

    return instances


def get_instance_infomation_by_id(instance_ids: dict) -> str:

    client = boto3.client(
        'ec2',
        aws_access_key_id=settings.AWS_ACCESS_KEY,
        aws_secret_access_key=settings.SECRET_KEY,
        region_name='ap-northeast-1'
    )
    raw_infomation = client.describe_instances(
        Filters=[
            {
                'Name': 'instance-id',
                'Values': instance_ids,
            },
        ],
    )
    instance_informations = \
        get_instance_informations_from_raw_data(raw_infomation)

    return json.dumps(instance_informations, indent=2)


@respond_to(r'^((i-[0-9a-zA-Z]+\s*)+)')
def instance_informations_from_ids(message, instance_ids_str, instance_id):
    instance_ids = instance_ids_str.split(' ')
    instance_info = get_instance_infomation_by_id(instance_ids)

    message.send(f'```\n{instance_info}\n```')
