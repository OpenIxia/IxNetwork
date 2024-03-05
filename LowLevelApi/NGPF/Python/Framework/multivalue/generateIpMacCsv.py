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
import random, csv

class MultivalueCsv () :
    def __init__ (self, csvFileName, scale) :
        self.csvFileName = csvFileName
        self.scale       = scale
    # end def  

    def generate (self) :
        # Provide a scale value incremented by 1 to pass to range function
        scale = self.scale
        csvFileName = self.csvFileName
        try:
            with open(csvFileName, "w+") as csvFile:
                csvWriter = csv.writer(csvFile, delimiter=',', lineterminator='\n')
                csvWriter.writerow(["SrcMac", "DstMac", "Vlan1", "Vlan2", "Ip", "Gw"])

                # Use the scale value in range
                for count in range(1,scale):
                    # Step 1: Create random values from 0 to 255 in hex and repeat that 
                    #         for all 6 octets to create Mac
                    # Step 2: Now map all these values using lambda and join them using
                    #         ":" to obtain Mac address
                    # Step 3: Generate vlan ids with random.randint to range from 1 to 4094
                    # Step 4: Repeat Step 1 and 2 in decimal for Ip and gateway address
                    # Step 5: Once ready write all values to csvFile  

                    srcMac = ":".join(map(lambda i: "%02x" %i, (random.randint(0x00, 0xFF) for k in range(0,6)))) 
                    dstMac = ":".join(map(lambda j: "%02x" %j, (random.randint(0x00, 0xFF) for l in range(0,6)))) 
                    vlan1  = random.randint(1, 4094)
                    vlan2  = random.randint(1, 4094)
                    ip     = ".".join(map (lambda x: "%03d" %x, (random.randint(1, 254) for m in range(0,4))))
                    gw     = ".".join(map (lambda y: "%03d" %y, (random.randint(1, 254) for n in range(0,4))))
                    csvWriter.writerow([srcMac, dstMac, vlan1, vlan2, ip, gw])
                # end for
            # end with
        except:
            print("creation of mac, vlan, ip, gw in csv file failed!")
        finally:
            pass
        # end try/except
    # end def
# end class

###############################################################################
# Uncomment below lines to run it stand alone
###############################################################################
myMultiValueCsv = MultivalueCsv("testMultivalue.csv", 2500)
myMultiValueCsv.generate()
    
