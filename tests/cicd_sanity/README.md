## Changes
- A directory has been added called test_bed_info. Any configuration file specific to your test bed should be added here
- All environment variables have been moved from bashrc to the test bed configuration files
- Some command line parameters have been removed such as tr_prefix and reports directory, and should now be specified in
the configuration file. This can be changed later if it poses any issues.
- Script was added for deleting profiles from UI. This script is for debugging purposes only. Script works by saving
profile id's to a dict in a seperate file which is cleared when profiles are deleted. If the file is cleared without the
profile deletion executed (eg. git pull is executed when profiles still remain in dictionary) then profile deletion will
fail. This ***will*** be changed in the future by querying rest api by profile name, and will be incorporated into
main nightly sanity script for profile deletion
- The info file ***must*** be changed to include your test rail credentials for making testrail API requests.
  
## Execute cicd_sanity

- 'python3 cicd_sanity.py -h' for help with command line parameters
- 'python3 cicd_sanity.py -i yes -f test_info_name' -i will run the sanity regardless of the load on the AP (If AP is upgraded
  to latest load and -i is not included, sanity will not run). -f specifies the configuration file name. By default, 
  it will look for the file name in test_bed_info directory. Alternatively you can give the path to the file,
  'python3 cicd_sanity.py -i yes -f /path/to/test_info_name'
- 'python3 delete_profiles.py -f test_info_name; python3 cicd_sanity.py -i yes -f test_info_name'. **Use this command most
of the time to make sure profiles are deleted prior to sanity execution**
  