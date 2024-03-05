#!/usr/bin/python
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
# script [and all modifications, enhancements and updates thereto (whether     #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the user's requirements or (ii) that the script will be without         #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, AND IXIA        #
# DISCLAIMS ALL WARRANTIES, EXPRESS, IMPLIED, STATUTORY OR OTHERWISE,          #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF, OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF,   #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS, LOST BUSINESS, LOST OR        #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT, INCIDENTAL, PUNITIVE OR            #
# CONSEQUENTIAL DAMAGES, EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF   #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g., any error corrections) in connection with the    #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script, any such services are subject to the warranty and   #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This sample script                                                        #
#    - Contains a function to verify statistics                                #
#                                                                              #
################################################################################

class UtilsError(Exception): pass

class sm:

    @staticmethod
    def checkStats(statList, expList, strings = False):
        def logPass(expStName, stVal, op, expStVal, tlr='-'):
            fmt = "%-35s %20.2f %2s %20.2f %5s ...Passed"
            try:
                print(fmt % (expStName, stVal, op, expStVal, tlr))
            except TypeError:
                fmt = "%-35s %20s %2s %20s %5s ...Passed"
                print(fmt % (expStName, stVal, op, expStVal, tlr))
        def logFail(expStName, stVal, op, expStVal, tlr='-'):
            fmt = "%-35s %20.2f %2s %20.2f %5s ...FAILED"
            try:
                print(fmt % (expStName, stVal, op, expStVal, tlr))
            except TypeError:
                fmt = "%-35s %20s %2s %20s %5s ...FAILED"
                print(fmt % (expStName, stVal, op, expStVal, tlr))

        retFlag = 1

        if len(statList) == 0:
            raise UtilsError("Empty Statistics list!")

        someFail = 0
        for stItem, expItem in zip(statList, expList):
            if expItem == "":   # skip if exp list is shorter than stat list
                continue

            fmt = "%-35s %20s %2s %20s %5s"
            header = fmt % (expItem[0], "RETURNED", "", "EXPECTED", "TOL")
            print(header)
            temp = ''
            for i in range(len(header)+10):
                temp = temp + '-'
            print(temp)

            tmpVal = dict(stItem[1])
            missingStats = []
            for expStName, op, expStVal, tol in expItem[1]:
                try:
                    expStVal = float(expStVal)
                except ValueError:
                    if not strings:
                        continue # skip strings values
                try:
                    stVal = float(tmpVal[expStName])
                except NameError as nm:
                    missingStats.append(expStName) # stat column is missing
                    continue
                except ValueError as e:
                    if not strings or "empty string for float" in e:
                        stVal = -1 # set to something bad if empty
                    else:
                        stVal = tmpVal[expStName]
                except:
                    stVal = -1 # set to something bad if empty
                if not tol == None:
                    tol = float(tol)

                if op == '=':
                    if strings:
                        if stVal == expStVal:
                            logPass(expStName, stVal, op, expStVal)
                            retFlag = 0
                        elif not tol == None:
                            minExp = expStVal - abs(expStVal) * tol
                            maxExp = expStVal + abs(expStVal) * tol
                            if stVal >= minExp and stVal <= maxExp:
                                logPass(expStName, stVal, op, expStVal, tol)
                                retFlag = 0
                            else:
                                logFail(expStName, stVal, op, expStVal, tol)
                                someFail = 1
                        else:
                            logFail(expStName, stVal, op, expStVal)
                            someFail = 1
                    else:
                        if stVal == expStVal or (math.isnan(stVal) and math.isnan(expStVal)):
                            logPass(expStName, stVal, op, expStVal)
                            retFlag = 0
                        elif not tol == None:
                            minExp = expStVal - abs(expStVal) * tol
                            maxExp = expStVal + abs(expStVal) * tol
                            if stVal >= minExp and stVal <= maxExp:
                                logPass(expStName, stVal, op, expStVal, tol)
                                retFlag = 0
                            else:
                                logFail(expStName, stVal, op, expStVal, tol)
                                someFail = 1
                        else:
                            logFail(expStName, stVal, op, expStVal, tol)
                            someFail = 1
                elif op == '<':
                    if stVal < expStVal:
                        logPass(expStName, stVal, op, expStVal)
                        retFlag = 0
                    else:
                        logFail(expStName, stVal, op, expStVal)
                        someFail = 1
                elif op == '>':
                    if stVal > expStVal:
                        logPass(expStName, stVal, op, expStVal)
                        retFlag = 0
                    else:
                        logFail(expStName, stVal, op, expStVal)
                        someFail = 1
                elif op == '<=':
                    if stVal <= expStVal:
                        logPass(expStName, stVal, op, expStVal)
                        retFlag = 0
                    else:
                        logFail(expStName, stVal, op, expStVal)
                        someFail = 1
                elif op == '>=':
                    if stVal >= expStVal:
                        logPass(expStName, stVal, op, expStVal)
                        retFlag = 0
                    else:
                        logFail(expStName, stVal, op, expStVal)
                        someFail = 1
                elif op == '<>':
                    if stVal >= expStVal and stVal <= tol:     # use expStVal as lower limit and
                        logPass(expStName, stVal, op, expStVal, tol) # tol as interval upper limit
                        retFlag = 0
                    else:
                        logFail(expStName, stVal, op, expStVal, tol)
                        someFail = 1
                else:
                    fmt = "%-35s %20.2f %2s %20.2f %5s ...Ignored"
                    try:
                        print(fmt % (expStName, stVal, op, expStVal, "-"))
                    except TypeError:
                        fmt = "%-35s %20s %2s %20s %5s ...Ignored"
                        print(fmt % (expStName, stVal, op, expStVal, "-"))
                    retFlag = 0

            if len(missingStats) > 0:
                raise UtilsError("\nStatisitcs:\n '\n'.join(missingStats)\nmissing from stat view!")

            print("\n")
        if someFail == 1:
            return 1
        else:
            return 0
