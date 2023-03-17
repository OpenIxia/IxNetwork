"""
PyTest fixture library file for IxNetwork

Requirements:
   - Python 3.7 minimum
   - pytest
"""
import os, sys, yaml, requests
import pytest
from pprint import pprint

from ixnetwork_restpy import *

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()
 
def readYaml(yamlFile):
    """
    Read YAML data

    :returns: YAML data
    """
    if os.path.exists(yamlFile) == False:
        print(f'Config file does not exists: {yamlFile}')
        return None

    with open(yamlFile, mode='r', encoding='utf8') as yamlData:
        try:
            # For yaml version >5.1
            return yaml.load(yamlData, Loader=yaml.FullLoader)
            
        except yaml.YAMLError as exception:
            # Show the Yaml syntax error
            raise exception
        
        except:
            return yaml.safe_load(yamlData)

                           
class Middleware:
    """
    Share common variables across fixtures and across pytest modules
    """
    ixNetworkSession = None
    ixNetworkObj = None
    configFile = None
    params = None
    

def pytest_addoption(parser):
    """
    Parse CLI arg input
    
    Usage:
       In sandboxConfigs fixture:
          configFile = request.config.getoption("--configFile")
    """
    parser.addoption("--configFile", action="store", default=None)
    
@pytest.fixture
def connectIxNetwork(request):
    """
    Connect to an IxNetwork API server.
    
    Return
        IxNetwork RestPy session Object
    """    
    configFile = request.config.getoption("--configFile")
    Middleware.configFile = configFile
    params = readYaml(configFile)
    Middleware.params = params

    print(f'\nconnectIxNetwork fixture: apiServer: {params["apiServerIp"]}')
    print(f'connectIxNetwork fixture: chassisList:{params["ixChassisIpList"]}   portList: {params["portList"]}')

    session = SessionAssistant(IpAddress=params['apiServerIp'], RestPort=None, UserName=params['username'], Password=params['password'], 
                               SessionName=None, SessionId=None, ApiKey=None,
                               ClearConfig=True, LogLevel='all', LogFilename='restpy.log')

    # For each session's name, use the sandbox name and append the ID
    #session.Session.Name = f'{sessionName}-{session.Session.Id}'
    
    # Store the session in Middleware so other fixtures could access IxNetwork
    Middleware.ixNetworkSession = session

@pytest.fixture
def ixNetworkSessionObj():
    """
    For pytest modules to get the connected IxNetwork session object
    """
    return Middleware.ixNetworkSession

@pytest.fixture
def ixNetworkObj():
    """
    For pytest modules to get the connected IxNetwork RestPy object
    """
    Middleware.ixNetworkObj = getattr(Middleware.ixNetworkSession, 'Ixnetwork')
    return getattr(Middleware.ixNetworkSession, 'Ixnetwork')

@pytest.fixture
def middleware():
    return Middleware
    

    
