"""An AWS Python Pulumi program"""
import requests
import pulumi
from pulumi_aws import get_availability_zones, ec2

def get_my_ip():
    r = requests.get('https://api.ipify.org?format=json')
    response = r.json()

    return response["ip"]

def get_username():
    r = requests.get('https://randomuser.me/api/')
    response = r.json()

    return response["results"][0]["login"]["username"]

# Retrieve the current region AZs
azones = get_availability_zones(state="available")

# Get a random username for tags
userName = get_username()
myTag = 'pulumi-' + userName

# Create VPC
vpc = ec2.Vpc(
            "myvpc",
            cidr_block="10.0.0.0/16",
            tags = {"Name": myTag+"-vpc"}
            )

# Create subnets in each AZs
subnets = []
for azname in azones.names:
    n = str(azones.names.index(azname)+1)
    cidrblk = "10.0."+str(n)+".0/24"
    subnet = ec2.Subnet("mysubnet"+str(n),
                    vpc_id=vpc.id,
                    availability_zone=azname,
                    cidr_block=cidrblk,
                    tags={
                        "Name": myTag+"-subnet"+str(n)}
                    )
    subnets.append(subnet)
# subnet1 = ec2.Subnet("mysubnet1",
#                     vpc_id=vpc.id,
#                     availability_zone="us-east-2a",
#                     cidr_block="10.0.0.0/24",
#                     tags={
#                         "Name": "dcb-subnet1",}
#                     )
# subnet2 = ec2.Subnet("mysubnet2",
#                     vpc_id=vpc.id,
#                     availability_zone="us-east-2b",
#                     cidr_block="10.0.1.0/24",
#                     tags={
#                         "Name": "dcb-subnet2",}
#                     )
# subnet3 = ec2.Subnet("mysubnet3",
#                     vpc_id=vpc.id,
#                     availability_zone="us-east-2c",
#                     cidr_block="10.0.2.0/24",
#                     tags={
#                         "Name": "dcb-subnet3",}
#                     )

myIp = get_my_ip()
myCidrBlk = myIp + '/32'

ingress1 = ec2.SecurityGroupIngressArgs(from_port=22,
                                        to_port=22,
                                        protocol="tcp",
                                        cidr_blocks=[myCidrBlk]
                                        )
egress1 = ec2.SecurityGroupEgressArgs(from_port=0,
                                    to_port=0,
                                    protocol="tcp",
                                    cidr_blocks=['0.0.0.0/0'])

sg = ec2.SecurityGroup("mysecuritygroup",
                        vpc_id=vpc.id,
                        ingress=[ingress1],
                        egress=[egress1],
                        description="dcb-sg",
                        tags={"Name":myTag+"-sg"}
                        )

amiFilter1 = ec2.GetAmiFilterArgs(name = "name", values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"])
amiFilter2 = ec2.GetAmiFilterArgs(name = "virtualization-type", values = ["hvm"])

ami = ec2.get_ami(owners=["099720109477"],
                most_recent=True,
                filters=[amiFilter1,amiFilter2]
                )

instance = ec2.Instance('myinstance',
                        instance_type="t2.micro",
                        vpc_security_group_ids=[sg.id],
                        subnet_id=subnets[0].id,
                        ami=ami.id,
                        tags={"Name":myTag+"-instance"}
                        )

pulumi.export("aznames",azones.names)
pulumi.export("vpc_id",vpc.id)
for subnet in subnets:
    pulumi.export("subnet"+str(subnets.index(subnet)+1)+"_id",subnet.id)
# pulumi.export("subnet1_id",subnet1.id)
# pulumi.export("subnet2_id",subnet2.id)
# pulumi.export("subnet3_id",subnet3.id)
pulumi.export("securitygroup_id",sg.id)
pulumi.export("ami_id",ami.id)
pulumi.export("instance_id",instance.id)