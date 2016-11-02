"""
Contains the ALBHelper class
"""

import boto3


class ALBHelper(object):

    """
    Class ALBHelper contains an extended version of the alb description from
    boto3's describe load balancer.
    """

    def __init__(self, alb_name):
        """
        Get ALB data and initialise the following variables:
          alb_client - boto3 client to request alb info (elbv2)

          ec2_resource - boto3 resource used for getting ec2 data

          alb_name - The name of the alb which we are working with

          alb_description_extended - alb description with target group
          information and targets included under ["TargetGroups"]

      params:
        alb_name - used to set the instance attribute with the same name

        """
        self.alb_client = boto3.client('elbv2')
        self.ec2_resource = boto3.resource('ec2')
        self.alb_name = alb_name
        self.alb_description_extended = self.get_alb_description_extended()


    def get_alb_description(self, alb_name):
        """
        Returns the alb data from aws
        """
        return self.alb_client.describe_load_balancers(Names=[alb_name])['LoadBalancers'][0]

    def get_alb_description_extended(self):
        """
        Returns the alb description with its associated target group information
        and targets attached to those.
        """
        alb_description = self.get_alb_description(self.alb_name)
        alb_arn = alb_description['LoadBalancerArn']
        target_group_descriptions = self.get_target_group_descriptions(alb_arn)
        target_group_descriptions_extended = self.get_target_group_descriptions_extended(target_group_descriptions)
        alb_description["TargetGroups"] = target_group_descriptions_extended
        return alb_description

    def update_alb_description_extended(self):
        self.alb_description_extended = self.get_alb_description_extended()

    def get_target_group_descriptions(self, alb_arn):
        """
        Returns the target group descriptions related to the alb that the
        class object was intitialised with.
        """
        return self.alb_client.describe_target_groups(LoadBalancerArn=alb_arn)['TargetGroups']

    def get_target_group_descriptions_extended(self, target_group_descriptions):
        """
        Returns the target group description with the targets added to the hash
        under "Targets"
        """
        for desc in target_group_descriptions:
            desc["Targets"] = self.get_targets_for_target_group(desc["TargetGroupArn"])
        return target_group_descriptions

    def get_targets_for_target_group(self, tg_arn):
        target_health_descriptions = self.alb_client.describe_target_health(TargetGroupArn=tg_arn)[
            'TargetHealthDescriptions']
        return [target['Target']['Id'] for target in target_health_descriptions]
