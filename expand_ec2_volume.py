import sys
import boto3
from datetime import date
import argparse

def expand_volume_from_snapshot(snap_id, size):
    ec2 = boto3.resource('ec2')
    client = boto3.client('ec2')
    snapshot = ec2.Snapshot(snap_id)
    old_volume = snapshot.volume
    device_name = old_volume.attachments[0]['Device']
    attached_instance = old_volume.attachments[0]['InstanceId']
    availability_zone = old_volume.availability_zone
    volume_type = old_volume.volume_type

    print('creating volume with size %d, using snapshot %s, zone %s, volume type %s ' %
          (size, snap_id, availability_zone, volume_type))
    response = client.create_volume(
        Size=size,
        SnapshotId=snap_id,
        AvailabilityZone=availability_zone,
        VolumeType=volume_type
    )
    print(response)

    new_volume_id = response['VolumeId']
    new_volume = ec2.Volume(new_volume_id)
    new_volume_name = attached_instance + "_volume_expanded_" + date.today().isoformat()
    new_volume.create_tags(
        Tags=[
            {
                'Key': 'Name',
                'Value': new_volume_name
            }
        ]
    )

    instance = ec2.Instance(attached_instance)
    print("stopping instance %s" % instance.id)
    instance.stop()
    print("waiting till stopped")
    instance.wait_until_stopped()
    print("detaching volume %s " % old_volume.id)
    instance.detach_volume(old_volume.id)
    print("attaching new volume %s" % new_volume_id)
    instance.attach_volume(VolumeId=new_volume_id, Device=device_name)
    print("starting instance")
    instance.start()
    instance.wait_until_running()
    print("instance running, check new volume is working")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='replace a volume with a larger one, requires that a\
         snapshot has been created prior to this',
        usage='%(prog)s --snapshot-id <id> --new-size <number_GBS>')
    parser.add_argument(
        "--snapshot-id", help="Id of the snapshot of the volume to expand", required=True)
    parser.add_argument("--new-size",
                        help="The new size of the volume", type=int, required=True)

    if len(sys.argv[1:]) < 2:
        parser.print_help()
        parser.exit()
    args = parser.parse_args()

    size = args.new_size
    snap_id = args.snapshot_id
    expand_volume_from_snapshot(snap_id, size)
    
