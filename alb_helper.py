"""
Contains the ALBHelper class
"""

import boto3


class ALBHelper(object):

    """
    Class ALBHelper contains methods for accessing ALB information and related
    target group information
    """

    def __init__(self, alb_name):
        """
        Get ALB data and initialise the following variables:
          alb_client - boto3 client to request alb info (elbv2)

          ec2_resource - boto3 resource used for getting ec2 data

          alb_name - The name of the alb which we are working with

          alb_description - the raw data from aws about the alb

          alb_arn - the amazon resource identifier for this alb

          target_group_descriptions - a list of the target group information

          target_group_arns - a list of the target group unique idenitifiers

          targets_by_arn - a list of hashs containing the "TargetIds" per
          "TargetGroupArn"

      params:
        alb_name - used to set the instance attribute with the same name

        """
        self.alb_client = boto3.client('elbv2')
        self.ec2_resource = boto3.resource('ec2')
        self.alb_name = alb_name
        self.alb_description = None
        self.alb_arn = None
        self.target_group_descriptions = None
        self.target_group_arns = None
        self.targets_by_arn = None
        self.update_all_attributes()

    def update_all_attributes(self):
        """
        Updates all the instance attributes by querying aws
        """
        self.alb_description = self.get_alb_description()
        self.alb_arn = self.alb_description['LoadBalancerArn']
        self.target_group_descriptions = self.get_target_group_descriptions()
        self.target_group_arns = [target_group_description['TargetGroupArn']
                                  for target_group_description in self.target_group_descriptions['TargetGroups']]
        self.targets_by_arn = self.get_targets_by_arn()

    def get_alb_description(self):
        """
        Returns the alb data from aws
        """
        return self.alb_client.describe_load_balancers(Names=[self.alb_name])['LoadBalancers'][0]

    def get_target_group_descriptions(self):
        """
        Returns the target group descriptions related to the alb that the
        class object was intitialised with.
        """
        return self.alb_client.describe_target_groups(LoadBalancerArn=self.alb_arn)

    def get_targets_by_arn(self):
        """
        Returns a list of hashs containing "TargetGroupArn" and the "TargetIds"
        related to that target group
        """
        target_group_info = []
        for tg_arn in self.target_group_arns:
            temp_target_group_info_hash = {}
            temp_target_group_info_hash["TargetGroupArn"] = tg_arn
            target_health_descriptions = self.alb_client.describe_target_health(TargetGroupArn=tg_arn)[
                'TargetHealthDescriptions']
            temp_target_group_info_hash["TargetIds"] = [target['Target']['Id']
                                                        for target in target_health_descriptions]
            target_group_info.append(temp_target_group_info_hash)
        return target_group_info

    def get_all_unique_targets(self):
        """
        Returns a list of all the unique instance id's accross all target groups
        for the alb
        """
        ids_per_tg_arn = [x["TargetIds"] for x in self.targets_by_arn]
        id_intersection = set([item for sublist in ids_per_tg_arn for item in sublist])
        return list(id_intersection)

    def get_target_ip_addresses(self):
        """
        Returns the ip addresses of the unique targets across all target groups
         for the alb
        """
        return [self.ec2_resource.Instance(instance_id).private_ip_address for instance_id in self.get_all_unique_targets()]

    def get_target_host_names(self):
        """
        Returns the host names of the unique targets across all target groups
        for the alb
        """
        return [self.get_instance_name_tag_from_id(instance_id) for instance_id in self.get_all_unique_targets()]

    def get_instance_name_tag_from_id(self, instance_id):
        """
        gets the Name tag for an instance
        """
        instance = self.ec2_resource.Instance(instance_id)
        for tag in instance.tags:
            if tag["Key"] == 'Name':
                return tag["Value"]
