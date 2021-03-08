## Changes
- A directory has been added called test_bed_info. Any configuration file specific to your test bed should be added here
- All environment variables have been moved from bashrc to the test bed configuration files
- Some command line parameters have been removed such as tr_prefix and reports directory, and should now be specified in
the configuration file. This can be changed later if it poses any issues.
- Profile deletion added to start of main cicd_sanity script. This will search profile names with a string subset 
of the profile being created, and delete the corresponding profiles.
- The info file ***must*** be changed to include your test rail credentials for making testrail API requests.
  
## Execute cicd_sanity

- 'python3 cicd_sanity.py -h' for help with command line parameters
- 'python3 cicd_sanity.py -i yes -f test_info_name' -i will run the sanity regardless of the load on the AP (If AP is upgraded
  to latest load and -i is not included, sanity will not run). -f specifies the configuration file name. By default, 
  it will look for the file name in test_bed_info directory. Alternatively you can give the path to the file,
  'python3 cicd_sanity.py -i yes -f /path/to/test_info_name'
  
