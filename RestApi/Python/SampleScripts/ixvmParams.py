# DESCRIPTION
# 
#     This is an ixVm chassis builder parameters file used in conjunction with ixVmChassisBuilder.py.
# 
# NOTE
#   
#     For removing, you have TWO options.
#        1> Remove 'all'
#        2> Remove a list of mgmtIp.
#
#     You MUST uncomment vmMgmtCardListToRemove if you want to remove a list.

# MANDATORY PARAMETERS:
apiServerIp = '192.168.70.127'
apiServerIpPort = '11009'
hypervisorType = 'vmware' ;# vmware or qemu
vChassisIp = '192.168.70.11'
username = 'admin'
password = 'admin'


# For ADDING cards: Set ixvmCardPortList variable with a list of mgmtIp.
ixvmCardPortList = [
    {'mgmtIp': '192.168.70.12', 'promiscuousMode': False, 'mtu': '1500', 'keepAlive': '300'},
    {'mgmtIp': '192.168.70.13', 'promiscuousMode': False, 'mtu': '1500', 'keepAlive': '300'}
]


# For REMOVING cards: 
#    Method 1: To remove all cards by default, set vmMgmtCardListToRemove = 'all'
#    Method 2: To remove specific cards, state the mgmt IP addresses in a list.

# Method 1
vmMgmtCardListToRemove = 'all'


# Method 2 A list of all the IxVmCard mgmt IP addresses to remove.
#vmMgmtCardListToRemove = ['192.168.70.12', '192.168.70.13']

# Do you want to delete the virtual chassis? True or False
removeVChassis = True

