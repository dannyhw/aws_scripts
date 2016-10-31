#!/bin/python

"""A script for printing information about security groups"""

import boto3
import collections

def get_sg_rule_info(sec_grp_in):
    """Iterate over a security group and return a dict containing the name of
    the group, a count of ip rules and a count of allow any rules.
    Args:
        sec_grp_in: The security group to iterate.

    Returns:
        Dict with name of the group, a count of ip rules
        and a count of allow any rules.
    """
    sg_rule_info = {}
    sg_rule_info['Name'] = sec_grp_in['GroupName']
    count_rules = collections.Counter()
    for permission in sec_grp_in['IpPermissions']:
        for ip_range in permission['IpRanges']:
            count_rules[ip_range['CidrIp']] += 1
    sg_rule_info['IpRules'] = count_rules
    sg_rule_info['AllowAnyRules'] = 0
    if count_rules['0.0.0.0/0']:
        sg_rule_info['AllowAnyRules'] = count_rules['0.0.0.0/0']
    return sg_rule_info


def print_security_rule_info(sgs=None):
    """Will print out security group information as follows:
    For every security group
      - Count of rules for each ip range
      - Count of allow any rules
    Number of security group rules unique by ip_range
    Number of security groups with an allow any rule
    """
    security_group_rules_list = []
    ec2_client = boto3.client('ec2')

    if sgs is not None and len(sgs) > 0:
        edge_security_groups = ec2_client.describe_security_groups(
            Filters=[
                {
                    'Name': 'group-name',
                    'Values': sgs
                }
            ]
        )
    else:
        edge_security_groups = ec2_client.describe_security_groups()

    for security_group in edge_security_groups['SecurityGroups']:
        security_group_rules_list.append(get_sg_rule_info(security_group))
    total = 0
    total_allow_any = 0
    for security_group_rule in security_group_rules_list:
        print 'Security Group: ', security_group_rule['Name']
        print 'Rules: ', security_group_rule['IpRules']
        print 'Allow any rules: ', security_group_rule['AllowAnyRules']
        total += len(security_group_rule['IpRules'])
        total_allow_any += security_group_rule['AllowAnyRules'] > 0

    print 'Number of security group rules unique by ip_range: ', total
    print 'Number of security groups with an allow any rule: ', total_allow_any

if __name__ == "__main__":
    print_security_rule_info()
