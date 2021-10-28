#!/usr/bin/python3
'''

make sure pexpect is installed:
$ sudo yum install python3-pexpect

You might need to install pexpect-serial using pip:
$ pip3 install pexpect-serial

./openwrt_ctl.py -l stdout -u root -p TIP -s serial --tty ttyUSB0

# Set up reverse ssh tunnel
./openwrt_ctl.py --tty /dev/ttyAP1 --action ssh-tunnel \
        --value "ssh -y -y -f -N -T -M -R 9999:localhost:22 lanforge@10.28.3.100" \
        --value2 password-for-10.28.3.100 --log stdout --scheme serial --prompt root@Open
'''


import sys
if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()

import re
import logging
import time
from time import sleep
import pprint
import telnetlib
import argparse
import pexpect

default_host = "localhost"
default_ports = {
   "serial": None,
   "ssh":   22,
   "telnet": 23
}
NL = "\n"
CR = "\r\n"
Q = '"'
A = "'"
FORMAT = '%(asctime)s %(name)s %(levelname)s: %(message)s'
prompt = "root@OpenWrt:"

def usage():
   print("$0 used connect to OpenWrt AP or similar Linux machine:")
   print("-d|--dest  IP address of the OpenWrt AP, for ssh/telnet scheme")
   print("-o|--port  IP port of the OpenWrt AP, for ssh/telnet scheme")
   print("-t|--tty   Serial port, if using serial scheme")
   print("-u|--user  login name")
   print("-p|--pass  password")
   print("--prompt   Prompt to look for when commands are done (default: root@OpenWrt)")
   print("-s|--scheme (serial|telnet|ssh): connect via serial, ssh or telnet")
   print("-l|--log file log messages here")
   print("--action (logread | journalctl | lurk | sysupgrade | download | upload | reboot | cmd | ssh-tunnel")
   print("--value (option to help complete the action")
   print("--value2 (option to help complete the action, dest filename for download, passwd for ssh-tunnel")
   print("-h|--help")

# see https://stackoverflow.com/a/13306095/11014343
class FileAdapter(object):
    def __init__(self, logger):
        self.logger = logger
    def write(self, data):
        # NOTE: data can be a partial line, multiple lines
        data = data.strip() # ignore leading/trailing whitespace
        if data: # non-blank
           self.logger.info(data)
    def flush(self):
        pass  # leave it to logging to flush properly

def main():
   global prompt

   parser = argparse.ArgumentParser(description="OpenWrt AP Control Script")
   parser.add_argument("-d", "--dest",    type=str, help="address of the cisco controller")
   parser.add_argument("-o", "--port",    type=int, help="control port on the controller")
   parser.add_argument("-u", "--user",    type=str, help="credential login/username")
   parser.add_argument("-p", "--passwd",  type=str, help="credential password")
   parser.add_argument("-P", "--prompt",  type=str, help="Prompt to look for")
   parser.add_argument("-s", "--scheme",  type=str, choices=["serial", "ssh", "telnet"], help="Connect via serial, ssh or telnet")
   parser.add_argument("-t", "--tty",     type=str, help="tty serial device")
   parser.add_argument("-l", "--log",     type=str, help="logfile for messages, stdout means output to console")
   parser.add_argument("--action",        type=str, help="perform action",
      choices=["logread", "journalctl", "lurk", "sysupgrade", "sysupgrade-n", "download", "upload", "reboot", "cmd", "ssh-tunnel" ])
   parser.add_argument("--value",         type=str, help="set value")
   parser.add_argument("--value2",        type=str, help="set value2")
   tty = None

   args = None
   try:
      args = parser.parse_args()
      host = args.dest
      scheme = args.scheme
      port = args.port
      #port = (default_ports[scheme], args.port)[args.port != None]
      user = args.user
      passwd = args.passwd
      logfile = args.log
      tty = args.tty;
      if (args.prompt != None):
          prompt = args.prompt
      filehandler = None
   except Exception as e:
      logging.exception(e);
      usage()
      exit(2);

   console_handler = logging.StreamHandler()
   formatter = logging.Formatter(FORMAT)
   logg = logging.getLogger(__name__)
   logg.setLevel(logging.DEBUG)
   file_handler = None
   if (logfile is not None):
       if (logfile != "stdout"):
           file_handler = logging.FileHandler(logfile, "w")
           file_handler.setLevel(logging.DEBUG)
           file_handler.setFormatter(formatter)
           logg.addHandler(file_handler)
           logging.basicConfig(format=FORMAT, handlers=[file_handler])
       else:
           # stdout logging
           logging.basicConfig(format=FORMAT, handlers=[console_handler])

   CCPROMPT=prompt

   ser = None
   egg = None # think "eggpect"
   try:
      if (scheme == "serial"):
         #eggspect = pexpect.fdpexpect.fdspan(telcon, logfile=sys.stdout.buffer)
         import serial
         from pexpect_serial import SerialSpawn
         ser = serial.Serial(tty, 115200, timeout=5)

         egg = SerialSpawn(ser);
         egg.logfile = FileAdapter(logg)
         egg.sendline(NL)
         has_reset = False
         try:
             logg.info("prompt: %s user: %s  passwd: %s"%(prompt, user, passwd))
             while True:
                i = egg.expect([prompt, "Please press Enter to activate", "login:", "Password:", "IPQ6018#"], timeout=3)
                logg.info("expect-0: %i"%(i))
                if (i == 0):
                    logg.info("Found prompt, login complete.")
                    break
                if (i == 1):
                    logg.info("Sending newline")
                    egg.setdline(NL)
                if (i == 2):
                    logg.info("Sending username: %s"%(user))
                    egg.sendline(user)
                if (i == 3):
                    logg.info("Sending password: %s"%(passwd))
                    egg.sendline(passwd)
                if (i == 4): # in bootloader
                    if has_reset:
                        logg.info("ERROR:  Have reset once already, back in bootloader?")
                        sys.exit(1)
                    has_reset = True
                    logg.info("In boot loader, will reset and sleep 30 seconds")
                    egg.sendline("reset")
                    time.sleep(30)
                    egg.sendline(NL)

         except Exception as e:
             # maybe something like 'logread -f' is running?
             # send ctrl-c
             egg.send(chr(3))

      elif (scheme == "ssh"):
         # Not implemented/tested currently. --Ben
         if (port is None):
            port = 22
         cmd = "ssh -p%d %s@%s"%(port, user, host)
         logg.info("Spawn: "+cmd+NL)
         egg = pexpect.spawn(cmd)
         #egg.logfile_read = sys.stdout.buffer
         egg.logfile = FileAdapter(logg)
         i = egg.expect(["password:", "continue connecting (yes/no)?"], timeout=3)
         time.sleep(0.1)
         if i == 1:
            egg.sendline('yes')
            egg.expect('password:')
         sleep(0.1)
         egg.sendline(passwd)

      elif (scheme == "telnet"):
         # Not implemented/tested currently. --Ben
         if (port is None):
            port = 23
         cmd = "telnet %s %d"%(host, port)
         logg.info("Spawn: "+cmd+NL)
         egg = pexpect.spawn(cmd)
         egg.logfile = FileAdapter(logg)
         time.sleep(0.1)
         egg.sendline(' ')
         egg.expect('User\:')
         egg.sendline(user)
         egg.expect('Password\:')
         egg.sendline(passwd)
         egg.sendline('config paging disable')
      else:
         usage()
         exit(1)
   except Exception as e:
      logging.exception(e);

   command = None

   CLOSEDBYREMOTE = "closed by remote host."
   CLOSEDCX = "Connection to .* closed."

   try:
       egg.expect(CCPROMPT)
   except Exception as e:
       egg.sendline(NL)

   TO=10
   wait_forever = False

   # Clean pending output
   egg.sendline("echo __hello__")
   egg.expect("__hello__")
   egg.expect(CCPROMPT)

   logg.info("Action[%s] Value[%s] Value2[%s]"%(args.action, args.value, args.value2))

   if (args.action == "reboot"):
      command = "reboot"
      TO=60

   if (args.action == "cmd"):
       if (args.value is None):
           raise Exception("cmd requires value to be set.")
       command = "%s"%(args.value)

   if (args.action == "logread"):
      command = "logread -f"
      TO=1
      wait_forever = True

   if (args.action == "journalctl"):
      command = "journalctl -f"
      TO=1
      wait_forever = True

   if (args.action == "lurk"):
      command = "date"
      TO=1
      wait_forever = True

   if (args.action == "ssh-tunnel"):
       command = "%s"%(args.value)
       passwd = "%s"%(args.value2)
       logg.info("Command[%s]"%command)
       egg.sendline(command);

       i = egg.expect(["password:", "Do you want to continue connecting"], timeout=5)
       if i == 1:
           egg.sendline("y")
           egg.expect("password:", timeout=5)
       egg.sendline(passwd)
       egg.expect(CCPROMPT, timeout=20)
       return

   if ((args.action == "sysupgrade") or (args.action == "sysupgrade-n")):
       command = "scp %s /tmp/new_img.bin"%(args.value)
       logg.info("Command[%s]"%command)
       egg.sendline(command);

       i = egg.expect(["password:", "Do you want to continue connecting"], timeout=5)
       if i == 1:
           egg.sendline("y")
           egg.expect("password:", timeout=5)
       egg.sendline("lanforge")
       egg.expect(CCPROMPT, timeout=20)
       if (args.action == "sysupgrade-n"):
           egg.sendline("sysupgrade -n /tmp/new_img.bin")
       else:
           egg.sendline("sysupgrade /tmp/new_img.bin")
       egg.expect("link becomes ready", timeout=100)
       return

   if (args.action == "download"):
       command = "scp %s /tmp/%s"%(args.value, args.value2)
       logg.info("Command[%s]"%command)
       egg.sendline(command);

       i = egg.expect(["password:", "Do you want to continue connecting", "Network unreachable"], timeout=5)
       if i == 2:
           print("Network unreachable, wait 15 seconds and try again.")
           time.sleep(15)
           command = "scp %s /tmp/%s"%(args.value, args.value2)
           logg.info("Command[%s]"%command)
           egg.sendline(command);

           i = egg.expect(["password:", "Do you want to continue connecting", "Network unreachable"], timeout=5)
       if i == 2:
           print("ERROR:  Could not connect to LANforge to get download file")
           exit(2)
       if i == 1:
           egg.sendline("y")
           egg.expect("password:", timeout=5)
       egg.sendline("lanforge")
       egg.expect(CCPROMPT, timeout=20)
       return

   if (args.action == "upload"):
       command = "scp %s %s"%(args.value, args.value2)
       logg.info("Command[%s]"%command)
       egg.sendline(command);

       i = egg.expect(["password:", "Do you want to continue connecting", "Network unreachable"], timeout=5)
       if i == 2:
           print("Network unreachable, wait 15 seconds and try again.")
           time.sleep(15)
           command = "scp /tmp/%s %s"%(args.value, args.value2)
           logg.info("Command[%s]"%command)
           egg.sendline(command);

           i = egg.expect(["password:", "Do you want to continue connecting", "Network unreachable"], timeout=5)
       if i == 2:
           print("ERROR:  Could not connect to LANforge to put upload file")
           exit(2)
       if i == 1:
           egg.sendline("y")
           egg.expect("password:", timeout=5)
       egg.sendline("lanforge")
       egg.expect(CCPROMPT, timeout=20)
       return

   if (command is None):
      logg.info("No command specified, going to log out.")
   else:
      logg.info("Command[%s]"%command)
      egg.sendline(command);
      while True:
          try:
              i = egg.expect([CCPROMPT, "kmodloader: done loading kernel", "\n"], timeout=TO)
              print (egg.before.decode('utf-8', 'ignore'))
              if i == 1:
                  egg.sendline(' ')
                  egg.expect(CCPROMPT, timeout=20)
                  print (egg.before.decode('utf-8', 'ignore'))
              if i == 2: # new line of text, just print and continue
                  continue

              if not wait_forever:
                  break
          
          except Exception as e:
              # Some commands take a long time (logread -f)
              if not wait_forever:
                  logging.exception(e)
                  break

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
if __name__ == '__main__':
    main()

####
####
####
