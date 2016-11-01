import boto3
import paramiko
from paramiko import SSHClient


def execute_remotely_on(instance_ip, scriptname, ssh_username, as_sudo=False):
    client = None
    sftp = None
    try:
        print "working on", instance_ip
        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(instance_ip, username=ssh_username)
        sftp = client.open_sftp()
        temp_file_name = "remove_me"
        sftp.put(scriptname, '/tmp/%s' % temp_file_name)
        command = 'bash /tmp/%s' % temp_file_name
        if as_sudo:
            command = 'sudo bash /tmp/%s' % temp_file_name
        _, stdout, stderr = client.exec_command(command)
        print "stdout: \n", stdout.read(), "stderr:", stderr.read()
        sftp.remove('/tmp/%s' % temp_file_name)
    except (paramiko.AuthenticationException, paramiko.SSHException) as message:
        print "ERROR: SSH connection to ", instance_ip, " failed: ", str(message)
        print "make sure you have you private key setup in ~/.ssh"
    finally:
        if client:
            client.close()
        if sftp:
            sftp.close()


def run_for_elb(elb_name, script_location, username, as_sudo=False):
    elb = boto3.client('elb')
    ec2 = boto3.resource('ec2')
    try:
        loadbalancers = elb.describe_load_balancers(
            LoadBalancerNames=[
                elb_name,
            ],
        )
    except:
        raise SystemExit(
            "Unable to get loabalancer %s, probably an incorrect name or aws isn't configured" % elb_name)
    loadbalancer_instances = loadbalancers['LoadBalancerDescriptions'][0]['Instances']
    for instance in loadbalancer_instances:
        if ec2.Instance(instance['InstanceId']).state['Name'] == 'running':
            execute_remotely_on(ec2.Instance(
                instance['InstanceId']).private_ip_address, script_location, username, as_sudo)
