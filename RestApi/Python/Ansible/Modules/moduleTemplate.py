"""
Description
   This is a sample custom module to show how to create your own Ansible 
   module.
"""

import logging
from ansible.module_utils.basic import AnsibleModule

import sys, traceback

sys.path.insert(0, '../Modules')
from IxNetRestApi import *
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiTraffic import Traffic
from IxNetRestApiProtocol import Protocol
from IxNetRestApiStatistics import Statistics

def main():
    logging.basicConfig(filename='../ansible.log', level=logging.DEBUG)

    # Define the available arguments/parameters that a user can pass to this module.
    params = {
        'osPlatform':             {'type':'str', 'required':False, 'default':'windows',
                                   'choices':['windows', 'windowsConnectionMgr', 'linux']},
        'forceTakePortOwnership': {'type':'bool', 'required':False, 'default':True},
        'releasePortsWhenDone':   {'type':'bool', 'required':False, 'default':False},
        'enableDebugTracing':     {'type':'bool', 'required':False, 'default':True},
        'deleteSessionAfterTest': {'type':'bool', 'required':False, 'default':True},
        'ixChassisIp':            {'type':'str', 'required':True, 'default':None},
        'portList':               {'type':'list', 'required':True, 'default':None},
        'apiServerIp':            {'type':'str', 'required':True, 'default':None},
        'apiServerIpPort':        {'type':'int', 'required':False, 'default':11009},
        'configLicense':          {'type':'str', 'required':False, 'default':'True', 'no_log':False},
        'linuxUsername':          {'type':'str', 'required':False, 'default':'admin', 'no_log':False},
        'linuxPassword':          {'type':'str', 'required':False, 'default':'password', 'no_log':False},
        'licenseServerIp':        {'type':'str', 'required':True, 'default':None},
        'licenseMode':            {'type':'str', 'required':False, 'default':'subscription'},
        'licenseTier':            {'type':'str', 'required':False, 'default':'tier3'}
    }

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec = params,
        supports_check_mode = False
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    #if module.check_mode:
    #    return result

    module.params['name'] = 'Custom BGP Module'
    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['message'] = 'A custom message'
    result['Result'] = 'Passed'

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    #if module.params['new']:
    #    result['changed'] = True
    #result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    #if module.params['name'] == 'fail me':
    #    module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    #module.exit_json(**result)
    #module.exit_json(changed=False, meta=module.params)

    # Default the API server to either windows or linux.
    osPlatform = module.params['osPlatform']

    if module.params['osPlatform'] not in ['windows', 'windowsConnectionMgr', 'linux']:
        raise IxNetRestApiException("\nError: %s is not a known option. Choices are 'windows' or 'linux'." % module.params['osPlatform'])
    
    try:
        #---------- Preference Settings --------------

        forceTakePortOwnership = module.params['forceTakePortOwnership']
        releasePortsWhenDone = module.params['releasePortsWhenDone']
        enableDebugTracing = module.params['enableDebugTracing']
        deleteSessionAfterTest = module.params['deleteSessionAfterTest'] ;# For Windows Connection Mgr and Linux API server only

        ixChassisIp = module.params['ixChassisIp']
        # [chassisIp, cardNumber, slotNumber]
        portList = module.params['portList']

        if module.params['osPlatform'] == 'linux':
              mainObj = Connect(apiServerIp = module.params['apiServerIp'],
                                serverIpPort = module.params['apiSeverIpPort'],
                                username = module.params['linuxUsername'],
                                password = module.params['linuxPassword'],
                                deleteSessionAfterTest = module.params['deleteSessionAfterTest'],
                                verifySslCert = False,
                                serverOs = module.params['osPlatform']
                            )

        if module.params['osPlatform'] in ['windows', 'windowsConnectionMgr']:
              mainObj = Connect(apiServerIp = module.params['apiServerIp'],
                                serverIpPort = module.params['apiServerIpPort'],
                                serverOs = module.params['osPlatform'],
                                deleteSessionAfterTest = module.params['deleteSessionAfterTest']
                            )

        #---------- Preference Settings End --------------

        portObj = PortMgmt(mainObj)
        portObj.connectIxChassis(module.params['ixChassisIp'], timeout=2)

        # Exit Ansible playbook test as passed.
        module.exit_json(changed=False)
        #module.exit_json(**result)

    except (IxNetRestApiException, Exception, KeyboardInterrupt) as errMsg:
        module.fail_json(msg=errMsg, **result)
        #module.fail_json(changed=False, meta=traceback.format_exc())

        if module.params['enableDebugTracing']:
            if not bool(re.search('ConnectionError', traceback.format_exc())):
                logging.ERROR('\nMY Failure: %s' % traceback.format_exc())
                #module.fail_json(changed=True, meta=traceback.format_exc())
                #exitArgs = {'module_stderr': traceback.format_exc()}
                #module.exit_json(**exitArgs)

        #logging.ERROR('\nException Error! %s\n' % errMsg)
        if 'mainObj' in locals() and module.params['osPlatform'] == 'linux':
            mainObj.linuxServerStopAndDeleteSession()

        if 'mainObj' in locals() and module.params['osPlatform'] in ['windows', 'windowsConnectionMgr']:
            if releasePortsWhenDone and forceTakePortOwnership:
                portObj.releasePorts(module.params['portList'])

            if module.params['osPlatform'] == 'windowsConnectionMgr':
                mainObj.deleteSession()

if __name__ == '__main__':
    main()
