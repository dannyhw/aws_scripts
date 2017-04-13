import boto3
import argparse
import sys
client = boto3.client('ec2')


def change_instance_type(instance_id, instance_type):
    client.stop_instances(InstanceIds=[instance_id])
    stop_waiter = client.get_waiter('instance_stopped')
    stop_waiter.wait(InstanceIds=[instance_id])
    client.modify_instance_attribute(
        DryRun=False, InstanceId=instance_id, Attribute='instanceType',
        Value=instance_type)
    client.start_instances(InstanceIds=[instance_id])
    start_waiter = client.get_waiter('instance_running')
    start_waiter.wait(InstanceIds=[instance_id])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Change the instance type by instance id',
        usage=('%(prog)s --instance-id <id> ' +
               '--target-instance-type <instance-type>'))
    parser.add_argument("--instance-id",
                        help="Id of the snapshot of the volume to expand",
                        required=True)
    parser.add_argument("--target-instance-type",
                        help="The new type of the instance",
                        required=True)

    if len(sys.argv[1:]) < 2:
        parser.print_help()
        parser.exit()
    args = parser.parse_args()

    target_instance_type = args.target_instance_type
    instance_id = args.instance_id
    change_instance_type(instance_id, target_instance_type)
