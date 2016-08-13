
#TODO: ssh func tomorrow, write unit tests and add exception handling 8/10/2016
import winrm #to be used for powershell/windows commands
import paramiko
import configparser
import argparse
import sys
import getpass
import os
parser = argparse.ArgumentParser()
parser.add_argument('-l', '--list', usage= 'list balls', action = 'store_true')
pasrer.add_argument('-b', '--ball', usage= 'ball you want to use', required=True)
parser.add_argument('-m','--machine', usage= 'machine adress' )
parser.add_argument('-g', '--group', useage= 'run ball against group from inventory file')
parser.add_argument('-h', '--help', usage= 'help', action= 'store_true')
parser.add_argument('-k', '--key', usage='select ssh key to use')
#QUICK AND DIRTY, USING GLOBALS (NOT BEST PRACTICE, PLS NO KILL)
#
config = configparser.ConfigParser()
config.read('balls')
inv = config.read('inventory')
args = parse_args()
# TODO: If this becomes a large-ish program, must get rid of globals
#

def check_ball(): #checks to make sure specified ball is in balls file
	if args.ball not in config.sections:
		print('specifed ball not in the ball file')
		sys.exit()

def list_balls_help():
	#checks if list or help was used
	if args.list:
		list_balls(config)
		list_balls
	elif args.help:
		parser.usage()
	else:
		input_error_check()

def input_error_check():
	#from here stuff gets dispatched
	if args.machine is not None:
		runner('machine')

	elif args.group is not None:
		runner('group')

	elif args.machine is None && args.group is None:
		print('You must enter a group or machine to run ball against')
		parser.usage()
	elif args.machine is not None && args.group is not None:
		print('You cannot use both tags')
		parser.usage()
	else:
		print('unspecified behavior')

def start():
	#kicks off program
	check_ball()

	list_balls_help()

	input_error_check()
	
		
def list_balls():
	sections = config.sections()
	for section in sections:
		print(section)
		print(config.get(section,'tag'))
		print(conifg.get(section,'description'))
		print('--------------------------------')	

def runner(group): #might combine with tag_check
	steps = sort_balls
 	if tag_check() == 'windows'
 		count = 0
		for machine in group:
			count = count + 1
			winrm_connect(machine, steps, count)
	if tag_check() == 'linux'
		for machine in group:
			ssh_connect(machine)


def winrm_connect(machine, steps, count):
	user = input('Enter username [>] ')
	passwrd = getpass.getpass('Enter password [>] ')
	session = winrm.Session(machine, auth=(user, passwrd))
	for step in steps:
		execute = session.run_cmd(step)
		if count == 1:
			print(execute.std_out)
		#add logging through execute.std_out
		if execute.std_err is not None:
			print('----------------------------')
			print(execute.std_err)
			sys.exit()
	print('[>] Success!')
	print('[>] Log saved')

def ssh_connect(machine, steps, count):
	client = paramiko.client.Client()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	if args.key is None:
		print('[>] No key selected for ssh')
		sys.exit()
	try:
		client.connect(machine, pkey=args.key)
	except paramiko.ssh_exception.AuthenticationException:
		print('[>] Auth error, check target machine name/ip address')
		sys.exit()
	for step in steps:
		stdin,stdout, stderr = client.exec_command(step)
		if count == 1:
			print(stdout)
		if stderr is not None: #this probably will get changed to len or something
			print('----------------------------')
			print(std_err)
			sys.exit()
	print('[>] Success!')
	print('[>] Log Saved')




def sort_balls(): #replace with list comprehension
	steps = [];
	options = config.options(args.ball)
	options.remove('description')
	options.remove('tag')
	for option in options:
		steps.append(config.get(args.ball, option)) #for each command
	return steps

def tag_check():
	if config.get(args.ball, 'tag') == 'windows':
		return 'windows'
	elif config.get(args.ball, 'tag') == 'linux':
		return 'linux'

def generate_log():
	directory = os.listdir()

	with open('log'+len(directory)+1,'w') as log:
		