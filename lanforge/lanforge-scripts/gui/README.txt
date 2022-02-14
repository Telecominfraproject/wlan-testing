
Notes on writing GUI automated tests (such as AP-Auto, TR-398, Dataplane, Capacity test, etc)

AP-Auto:

In the GUI, configure the AP-Auto test as wished, and save the test config on the
Advanced Configuration page.  In this example, I use the name: ap-auto-32-64-dual

In LANforge CLI, you can dump the saved configuration:

default@btbits>> show_text_blob Plugin-Settings AP-Auto-ap-auto-32-64-dual
TEXT-BLOB:Plugin-Settings.AP-Auto-ap-auto-32-64-dual::[BLANK]
show_events: 1
show_log: 1
port_sorting: 0
notes0: Chamber to Chamber test.
bg: 0xE0ECF8
test_rig: TR-398 test bed
....

Save this text to a file for later use:  AP-Auto-ap-auto-32-64-dual.txt

# Save AP-Auto configuration text using the ../lf_testmod.pl script:
../lf_testmod.pl --mgr 192.168.100.156 --action show --test_name AP-Auto-ap-auto-32-64-dual > test_configs/mytest.txt

# Save WiFi-Capacity configuration (saved as 'fb-192' using the ../lf_testmod.pl script:
../lf_testmod.pl --mgr 192.168.100.156 --action show --test_name Wifi-Capacity-fb-192 > test_configs/mytest.txt

# Save Chamber View scenario:
../lf_testmod.pl --mgr 192.168.100.156 --action show --test_name simpleThput --test_type Network-Connectivity > test_configs/myscenario.txt



# To load a test file into the LANforge server configuration:
../lf_testmod.pl --mgr 192.168.100.156 --action set --test_name AP-Auto-ben --file test_configs/mytest.txt



# Load a scenario into the LANforge server configuration
../lf_testmod.pl --mgr 192.168.100.156 --action set --test_type Network-Connectivity --test_name 64sta --file test_configs/myscenario.txt


###
Once test cases have been loaded into the server, you can tell the GUI to run tests for you, potentially modifying the
test configuration through the GUI.

# Tell the GUI to read the latest test config from the server.
../lf_gui_cmd.pl --manager localhost --port 3990 --cmd "cli show_text_blob"

# Tell the Chamber-View GUI widget to load and build the specified scenario.
../lf_gui_cmd.pl --manager localhost --port 3990 --load 64sta

# Now, tell the GUI to run a test with the new config.
# Note that the --tconfig option does not have the "AP-Auto-" prepended to it, that is automatically
# done by the GUI in order to make sure each test has its own namespace.
../lf_gui_cmd.pl --manager localhost --port 3990 --ttype "AP-Auto" --tname ap-auto-ben --tconfig ben --rpt_dest /tmp/lf_reports/


Check /tmp/lf_reports for the report files.


The cicd and testbeds directories contain some code that came from another CICD implementation
Candela worked on.  It is a good starting point, but will need modifications before it fully
works for your test bed.

