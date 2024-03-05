# -*- coding: cp1252 -*-
#!/usr/bin/env python

################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications enhancements and updates thereto (whether      #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the users requirements or (ii) that the script will be without          #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND IXIA         #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF     #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR          #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR              #
# CONSEQUENTIAL DAMAGES EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF    #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g. any error corrections) in connection with the     #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script any such services are subject to the warranty and    #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

################################################################################
# Purpose : ixiangpf multivalue has option to read values from the from a csv  #
#           file. For a large config it will take too much effort to manually  #
#           create this csv file.This sample python scripts generates the csv  #
#           parameter files.                                                   #
#                                                                              #
# Description:                                                                 #
# Create a scaled csv file with Mac, Vlan, Ip and Gw addresses                 #
################################################################################

# create a simple script to generate a set pattern of routes
# this will be used to create a 1-bit (0,1) value csv file.

import optparse, random, os, sys, time, pdb, csv

class OneBitValue () : 
    def __init__ (self, csvFile, peer, route) :
        self.peer  = peer
        self.route = route
        self.csvFile = csvFile
    # end def
    
    def generate (self) :
        peers  = self.peer
        routes = self.route
        nw_adv = 0 
        try:
            with open(self.csvFile, "w") as csvFile:
                csvWriter = csv.writer(csvFile, delimiter=',', lineterminator='\n')
                csvWriter.writerow(["Overlay_1bit_value"])
                for count in range(0,peers):
                    nw_adv = (random.randint(0, routes))
                    for tr in range(0, nw_adv):
                        csvWriter.writerow(["True"])
                    # end for

                    for fr in range(0, routes-nw_adv):
                        csvWriter.writerow(["False"])
                    # end for
                # end for
            # end with
        except:
            print("creation of overlay csv file failed!")
            raise
        finally:
            pass
        # end try/except
    # end def
# end class

################################################################################
# Uncomment below lines to run it stand alone
################################################################################
parser = optparse.OptionParser()
parser.add_option('-p', action="store", dest="p", type="int", default="601")
parser.add_option('-r', action="store", dest="r", type="int", default="991")
options, args = parser.parse_args()

peers  = options.p
routes = options.r
csvFile = "onebit.csv"
myOneBitValue = OneBitValue(csvFile, peers, routes)
myOneBitValue.generate()
