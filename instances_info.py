from __future__ import print_function
import boto3
ec2 = boto3.client('ec2')
HEADERS = ["Instance Name", "Instance ID", "Instance Type",
           "Availability Zone", "Public IP address", "Security Group",
           "Subnet ID", "Private IP address"]


def get_name_tag(tags):
    for tag in tags:
        if tag['Key'] == 'Name':
            return tag['Value']
    return ""


def get_instance_info_list(instance):
    instance_name = get_name_tag(instance['Tags'])
    instance_id = instance['InstanceId']
    instance_type = instance['InstanceType']
    availability_zone = instance['Placement']['AvailabilityZone']
    # get public ip if it exists or return empty string
    public_ip_address = instance['NetworkInterfaces'][0].get(
        'Association', {'PublicIp': ''}).get('PublicIp', '')
    security_group = instance['SecurityGroups'][0]['GroupName']
    subnet_id = instance['NetworkInterfaces'][0]['SubnetId']
    private_ip_address = instance['NetworkInterfaces'][0][
        'PrivateIpAddress']
    str_list = [instance_name, instance_id, instance_type,
                availability_zone, public_ip_address, security_group,
                subnet_id, private_ip_address]
    return str_list


def print_ec2_info():
    instance_reservations = ec2.describe_instances()['Reservations']
    print(','.join(HEADERS))
    for reservation in instance_reservations:
        for instance in reservation['Instances']:
            print(','.join(get_instance_info_list(instance)))


def save_ec2_info_as_csv(filename):
    import csv
    with open(filename, 'wb') as my_file:
        wr = csv.writer(my_file)
        wr.writerow(HEADERS)
        instance_reservations = ec2.describe_instances()['Reservations']
        for reservation in instance_reservations:
            for instance in reservation['Instances']:
                wr.writerow(get_instance_info_list(instance))



if __name__ == '__main__':
    print_ec2_info()
    # save_ec2_info_as_csv("instances.csv")
