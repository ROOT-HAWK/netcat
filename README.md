# netcat
netcat 
# the purpose is only for education
  Please use the tools wisely

# requirements
* python2

# installation
 * https://github.com/R00T-H4WK/next
 * chmod +x netcat2.py
 * python2 netcat.py

# Use assistance
* python2 netcat2.py -h
Net Tool

* Usage: netcat2.py -t target_host -P target_port
* -l --listen                  - listen on [host]:[port] for                               incoming connections
* -e --execute=file_to_run     - execute the given file upon                               receiving a connection
* -c --command                 - initialize a command shell
* -u --upload=destination      - upon receiving connection upload a                               file and write to [destination]


* Examples:
* netcat2.py -t 192.168.0.1 -p 5555 -l -c
* netcat2.py -t 192.168.0.1 -p 5555 -l -u=c:\target.exe
* netcat2.py -t 192.168.0.1 -p 5555 -l -e="cat /etc/passwd"
