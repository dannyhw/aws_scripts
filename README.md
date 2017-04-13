# aws_scripts
Just some scripts I use for various different things.

## For remotely executing bash on elb attached instances: 

Make sure you have authentication setup with rsa keys and your private key is id_rsa in ~/.ssh. Also aws cli should be configured correctly (authenication/ec2 iam role already setup) and default region set. Potentially further arguments can be added to this script to be more flexible (this is a to do). 

NOTE: About using sudo flag, THIS IS DANGEROUS, BE CAREFUL. Also using sudo non interactively likely depends on sudo not prompting you for a password, need to test this.

```
usage: execute_remote_on_lb.py --load-balancer <elb name> --script <filepath>

Execute bash script remotely on all instances attached to a (classic)
loadbalancer

optional arguments:
  -h, --help            show this help message and exit
  --load-balancer LOAD_BALANCER
                        The name of the Classic load balancer
  --script-location SCRIPT_LOCATION
                        File path of the script to execute
  --username USERNAME   Username for ssh
  --run-as-sudo         Use this flag if you want to execute the script
                        contents using sudo (root permissions)
```

## alb_helper.py
I've come to the conclustion that this isn't really a good candidate for a class and instead most of this functionality is now also in the common alb functions module.

This is a python module which contains the class ALBHelper used to get the alb description from boto3 but also add to it the related target group information and targets attached to those target groups. The class variable alb_description_extended is the main one here however it may also be useful to use get_alb_description_extended() if changes have been made or use update_alb_description_extended() before accessing the extended description. 

example usage:
```
from alb_helper import ALBHelper
alb = ALBHelper("MY-LOAD-BALANCER")
alb_description = alb.alb_description_extended
print alb_description["TargetGroups"][0]["Targets"]
```

## common_alb_functions.
A module with various functions which I use to help do automated deployments accross ALB's. Still in progress.

## expand_ec2_volume
```
usage: expand_ec2_volume.py --snapshot-id <id> --new-size <number_GBS>

replace a volume with a larger one, requires that a snapshot has been created
prior to this

optional arguments:
  -h, --help            show this help message and exit
  --snapshot-id SNAPSHOT_ID
                        Id of the snapshot of the volume to expand
  --new-size NEW_SIZE   The new size of the volume
  ```
## instances_info.py

I made this to create a csv file with information on current EC2 instances.
Has two uses:
- Print a comma separated table which can be used to generate a csv file `python instances_info.py > file.csv`  or just for reading in the terminal `python instances_info.py`
- Directly save to csv `python instances_info.py` (currently you'll have to un-comment the line in the module) TODO: add sys args

## see_recent_users.rb

I created this to try out a bit of ruby for scripting, it basically returns the recent users that have authenticated to the server by comparing the signature in /var/log/auth.log with the signatures which are generated when using the keys in .ssh/authorised keys. This requires that you have given each authorised key a useful comment since that's what gets printed out. 

## change_instance_type.py
This is for changing a running instance instance type. There is no specific checks here yet so be careful using this to use the correct instance type names.

usage: change_instance_type.py --instance-id <id> --target-instance-type <instance-type>

Change the instance type by instance id

optional arguments:
  -h, --help            show this help message and exit
  --instance-id INSTANCE_ID
                        Id of the snapshot of the volume to expand
  --target-instance-type TARGET_INSTANCE_TYPE
                        The new type of the instance

