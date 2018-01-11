#------------------------------------------------------------------------------------------
#
# This README.TXT describes how to run the sample Tcl scripts.
#
#------------------------------------------------------------------------------------------
The directory structure of the test cases are as follows
C:\Program Files (x86)\Ixia\IxNetwork\<install-dir>\SampleScripts\IxNetwork\Classic\Tcl\<respective test case folder>\test.<test case name>.tcl

#------------------------------------------------------------------------------------------
# Test case directories are as follows:
#------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
# Procedure for running the test cases
#------------------------------------------------------------------------------------------
1. Select the folder from which you want to run the test case.
   The name of the folders briefly describes the category of the test cases.

2. Look for the test.<test case name>.tcl file inside the folder. 
   This file is the main test case file. 

3. Open the file with a text editor. Now change the chassis, card, port, TclServer
   <your IxNetwork client PC where TclServer is running> and Tcl Server port information
   in the "C:\Program Files (x86)\Ixia\IxNetwork\7.50.0.135-EB\SampleScripts\IxNetwork\Classic\Tcl\TestRun\config.tcl"
   file as per your need. As an example
   
   set ::chassis     10.205.28.195
   set ::card1       9
   set ::card2       9
   set ::port1       1
   set ::port2       2
   set ::client      "10.205.28.84"
   set ::tcpPort     8099
   set ::IXOS_BUILD  "6.90.0.208"
   set ::IX_NETWORK  "7.50.0.135-EB"

4. You can run the test cases either from wish console or from tclsh84.exe under 
   "C:\Program Files\Ixia\IxNetwork\tcl8.4\bin\" 

5. In either case you have to source the test case file. 
   5.1 To source the test case file from wish console, launch the wish console, 
       go to the file -> source menu and browse the file to be sourced

   5.1 To source the file from tclsh84.exe,using command prompt go to the path
       "C:\Program Files\Ixia\IxNetwork\tcl8.4\bin\". Then type tclsh84. You will
       get a % prompt. From the % prompt source the test case file using the 
       source command as below: source <absolute test case path>/test.<test cases>.tcl.
       As an example :
       source C:/Program Files/Ixia/IxNetwork/TclScripts/sample/integrated-test-data-plane/test.test.integrated-data-plane-1.2.tcl

#-------------------------------------------------------------------------------
# Additional Info***
#-------------------------------------------------------------------------------
* There can be some other files also inside the test case folders, like 
  config.<test case>.tcl or <test case>.ixncfg which are the tcl or binary 
  configuration file that is getting loaded from the corresponding to 
  test.<test case>.tcl file.

* There can be some hard coded values in some of the test cases which is dependent
  on chassis or some user setting values of IxNetwork.These are the modification 
  to make in the respective test cases.
   1. In the testcase test.All3QoSIpv4Traffic.tcl under Dscp-Tos in Line no 352 the
      IxOs build No is to be modified accordingly.

   2. In the testcase test.integrated-data-plane-1.2.tcl under integrated-test-data-plane
      we are assuming that the csv path location is to be the default one which is
      C:/Program Files/Ixia/IxNetwork/<username>//data/logs/ If the user is saving the csv
      files in some other location that specific path is to be mentioned in the test 
      case in line no 181 and 182.
#---------------------------------------------------------------------------------


