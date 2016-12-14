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
usage: expand_ec2_volume.py --snapshot-id <id> --new-size <number_GBS>

replace a volume with a larger one, requires that a snapshot has been created
prior to this

optional arguments:
  -h, --help            show this help message and exit
  --snapshot-id SNAPSHOT_ID
                        Id of the snapshot of the volume to expand
  --new-size NEW_SIZE   The new size of the volume
