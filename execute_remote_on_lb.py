import argparse
import sys
import remote_execute_tools


def main():
    parser = argparse.ArgumentParser(
        description='Execute bash script remotely on all instances attached to a (classic) loadbalancer',
        usage='%(prog)s --load-balancer <elb name> --script <filepath>')
    parser.add_argument(
        "--load-balancer", help="The name of the Classic load balancer", required=True)
    parser.add_argument("--script-location",
                        help="File path of the script to execute", required=True)
    parser.add_argument("--username", help="Username for ssh", required=True)
    parser.add_argument(
        "--run-as-sudo", help="Use this flag if you want to execute the script contents using sudo(root permissions)", action='store_true')
    # if no options, print help
    if len(sys.argv[1:]) < 3:
        parser.print_help()
        parser.exit()
    args = parser.parse_args()
    load_balancer_name = args.load_balancer
    script_location = args.script_location
    username = args.username
    run_as_sudo = args.run_as_sudo
    remote_execute_tools.run_for_elb(load_balancer_name, script_location, username, run_as_sudo)

if __name__ == '__main__':
    main()
