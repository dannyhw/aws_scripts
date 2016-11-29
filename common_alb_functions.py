import boto3
from alb_common_exceptions import NoEc2InstanceFoundException
from alb_common_exceptions import FailedToReachStateException
import time

EC2_RESOURCE = boto3.resource('ec2')
EC2_CLIENT = boto3.client('ec2')
ALB_CLIENT = boto3.client('elbv2')

""" Number of times to check for a resouce to be in the desired state. """
WAITER_ATTEMPTS = 60

""" Number of seconds to wait between attempts for resource to be in a state for ALB registration/deregistration. """
WAITER_INTERVAL = 10


def wait_for_state(target_group_arn, instance_id, state_name):
    """
    Wait for an instance to reach a specified state on a certain target group before continuing
    args:
        target_group_arn - amazon resource name of target group
        instance_id - id of instance
        state_name - desired state of instance
    """
    success = False
    print('Waiting for instance with id %s to reach state %s for target group with arn %s' %
          (instance_id, state_name, target_group_arn))
    for attempt in range(WAITER_ATTEMPTS):
        current_instance_state = get_instance_health(target_group_arn, instance_id)
        print('Instance with id %s Currently in state %s for target group with arn %s' %
              (instance_id, current_instance_state, target_group_arn))
        if current_instance_state == state_name:
            print('reached the desired state: %s' % state_name)
            success = True
            break
        time.sleep(WAITER_INTERVAL)
    if not success:
        raise FailedToReachStateException("failed to reach desired state: %s" % state_name)


def get_instance_health(target_group_arn, instance_id):
    """
    Get the health of an instance on a specific target group
    args:
        target_group_arn - amazon resource name of target group
        instance_id - id of instance
    """
    current_instance_state_info = ALB_CLIENT.describe_target_health(
        TargetGroupArn=target_group_arn,
        Targets=[
            {
                'Id': instance_id,
            }
        ]
    )
    return current_instance_state_info['TargetHealthDescriptions'][0]['TargetHealth']['State']


def deregister_instance(target_group_arn, instance_id):
    """
    Deregister an instance from a specific target group
    args:
        target_group_arn - amazon resource name of target group
        instance_id - id of instance
    """
    print('de-registering instance with id %s from targetgroup with arn %s' %
          (instance_id, target_group_arn))
    response = ALB_CLIENT.deregister_targets(
        TargetGroupArn=target_group_arn,
        Targets=[
            {
                'Id': instance_id
            }
        ]
    )


def register_instance(alb_name, instance_id):
    """
    Register an instance to a specific target group
    args:
        target_group_arn - amazon resource name of target group
        instance_id - id of instance
    """
    response = ALB_CLIENT.register_targets(
        TargetGroupArn=target_group_arn,
        Targets=[
            {
                'Id': instance_id
            }
        ]
    )


def get_instance_id_from_ip(instance_ip):
    """
    Get the id of an ec2 instance bases on its private ip address
    args:
        instance_ip - private ip address of instance
    """
    instance_description = EC2_CLIENT.describe_instances(
        Filters=[
            {
                'Name': 'private-ip-address',
                'Values': [
                    instance_ip
                ]
            },
        ]
    )
    if instance_description['Reservations']:
        return instance_description['Reservations'][0]['Instances'][0]['InstanceId']
    else:
        raise NoEc2InstanceFoundException("No instances found with this ip address")


def get_all_target_groups():
    """
    Return a list of all target group arns in the default region.
    """
    tg_descriptions = ALB_CLIENT.describe_target_groups()['TargetGroups']
    return [target_group['TargetGroupArn'] for target_group in tg_descriptions]


def get_targets_for_target_group(target_group_arn):
    """
    Return a list of all targets registered to a target group
    args:
        target_group_arn - amazon resource name of target group
    """
    target_health_descriptions = ALB_CLIENT.describe_target_health(TargetGroupArn=target_group_arn)[
        'TargetHealthDescriptions']
    return [target['Target']['Id'] for target in target_health_descriptions]


def get_arns_for_target_groups_containing_target(target_id):
    """
    Returns a list of all the arns for target groups which contain a specific instance
    args:
        target_id - id of the instance
    """
    target_groups = get_all_target_groups()
    return [target_group for target_group in target_groups if target_id in get_targets_for_target_group(target_group)]