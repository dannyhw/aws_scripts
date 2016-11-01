# aws_scripts
Just some scripts I use for various different things.

#For remotely executing bash on elb attached instances: 

Make sure you have authentication setup with rsa keys and your private key is is_rsa in ~/.ssh. Also aws cli should be configured correctly (authenication/ec2 iam role already setup) and default region set. Potentially further arguments can be added to this script to be more flexible (this is a to do). 

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

# ALB helper
This is used to get information on albs and the related target groups. I wrote this since the alb api methods don't directly allow you to access attached instances like the ELB did. This way I can get the attached instances (targets) and re-use the methods. I wrote it to allow you to load all the info once or just get it each time.
