# LANforge API Python Library

---

This library provides a set of methods to operate the [LANforge JSON REST API](http://www.candelatech.com/cookbook.php?vol=cli&book=JSON:+Querying+the+LANforge+Client+for+JSON+Data). This is a generated library that includes JSON POST commands for every [LANforge CLI command](https://www.candelatech.com/lfcli_ug.php). If you are new to this API, please start at the beginning of the [LANforge Scripting Cookbook](http://www.candelatech.com/scripting_cookbook.php). 

## Requirements

* Python 3.7 -- this library should operate on Fedora 30 and later which ships with Python 3.7. We discourage operation on earlier (Fedora 27) releases of Fedora. 
* pip3 -- You will likely be using py-scripts and you will need to do a `pip3 install -r` [requirements.txt](https://github.com/greearb/lanforge-scripts/blob/master/requirements.txt)
* LANforge GUI 5.4.5

## Features

The **lanforge_client** package contains both the CLI compatibility plus a logging and REST classes.

* `logg.py` defines the standard logger methods found in library
* `strutil.py` defines string utility methods
* `lanforge_api`module
* `LFJsonQuery(JsonQuery)` defines methods for the GET requests supported by the LANforge GUI. Methods in this class start with `get_`.
* `LFJsonCommand(JsonCommand)` defines methods for the POST requests supported by the LANforge GUI. 
* `LFSession` script session tracking. This provides diagnostic tracing between the scripts and the LANforge GUI. It also provides the basis for callback IDs for specific types of CLI commands

## Intended Usage

This library can be used directly, plus it can be used in conjunction with the LANforge [Realm](https://github.com/greearb/lanforge-scripts/blob/master/py-json/realm.py) class. It is different than than the *Realm*class. *Realm* extends the [lfcli_base](https://github.com/greearb/lanforge-scripts/blob/master/py-json/LANforge/lfcli_base.py) class that provides its own (nearly identical) REST API. The lanforge_client REST methods are built into the *BaseLFJsonRequest* class. 

You would use the *Realm* class to execute high-level operations like:

* creating groups of stations
* creating numerous connections
* reporting KPI events like test results

You would use the *lanforge_client* package in places where:

* you want direct LANforge CLI control that hides the URLs
  * port specific flags
  * endpoint specific flags
* to get session tracking and using callback keys
* you want an API that hides the REST URLs

The Realm class is useful. As the *lanforge_client* package stabilizes, we anticipate replacing lower level parts of the *Realm* based operations to call into the *lanforge_client* package.

## Getting started

Below is an example of instantiating a LFSession object and getting the LFJsonQuery (for GETs) and LFJsonCommand (for POSTs).

```python
import lanforge_api
import lanforge_api.LFJsonCommand
import lanforge_api.LFJsonQuery

def main():
    session = lanforge_api.LFSession(lfclient_url="http://%s:8080" % args.host,
                                     debug=args.debug,
                                     connection_timeout_sec=2.0,
                                     stream_errors=True,
                                     stream_warnings=True,
                                     require_session=True,
                                     exit_on_error=True)
    command: LFJsonCommand
    command = session.get_command()
    query: LFJsonQuery
    query = session.get_query()

    command.post_rm_text_blob(p_type=args.type, name=args.name,
                              debug=args.debug, suppress_related_commands=True)
    command.post_show_text_blob(name='ALL', p_type='ALL', brief='yes')
    command.post_add_text_blob(p_type=args.type, name=args.name, text=txt_blob,
                               debug=True, suppress_related_commands=True)
    command.post_show_text_blob(name='ALL', p_type='ALL', brief='no')
    eid_str="%s.%s" % (args.type, args.name)
    print ("List of text blobs:")
    diagnostics=[]
    result = query.get_text(eid_list=eid_str, debug=True, errors_warnings=diagnostics)
    pprint.pprint(diagnostics)
    pprint.pprint(result)

```

