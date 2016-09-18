# kickoff.py
A small config management utility I'm writing to get a better understanding of what goes into applications like chef/ansible.

kickoff.py is based more on Ansible with it's push style via winrm/ssh, The 'balls' are just a collection of commands exectued in order
against a machine or group of machines.

Currently the ssh function is working with password login (pkey login should work also), the log output is incorrect and must be fixed, 
and winrm execution needs testing.

Eventually this prject will end up with two versions, this one with the ini balls that are very simple and just lists of commands,
and a version that will use [TOML](https://github.com/toml-lang/toml) which will have a much more powerful config file like Ansible (That version of kickoff.py would also  have execution modules like Ansible).

#Usage
-h, --help            show this help message and exit

  -l, --list            Lists balls

-b BALL, --ball BALL  Ball to run

-m MACHINE, --machine MACHINE

Run against individual machine

-g GROUP, --group GROUP

Run against a group from the inventory file

-k KEY, --key KEY     SSH key to use if needed

-p PASSWORD, --password PASSWORD

 password for user elevation/access




#Ball Syntax

[INI](https://en.wikipedia.org/wiki/INI_file#Keys_.28properties.29) Syntax

>     [linux_setup];a ball declaration
  
>     remote_user=myusername
  
>     tag=linux;this determines execution through ssh or winrm
  
>     description=install python3-dev ;quick description of what the ball does
  
>     ;commands are listed 1,2,3,4,5,6 etc. for execution in order
  
>     1=DEBIAN_FRONTEND=noninteractive apt-get install  python3-dev
>     2=echo wat


>     [win_setup] ;other ball

>     remote_user=none

>     tag=windows

>     description= does a thing

>     1=wat
