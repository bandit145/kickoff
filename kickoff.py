
#TODO: make move to classes to accomodate larger program
import winrm #to be used for powershell/windows commands
import paramiko
import configparser
import argparse
import sys
import getpass
import os
import socket #for error handling connections
parser = argparse.ArgumentParser()
parser.add_argument('-l', '--list', action = 'store_true')
parser.add_argument('-b', '--ball', help= 'Ball to run')
parser.add_argument('-m','--machine', help= 'Run against individual machine')
parser.add_argument('-g', '--group', help= 'Run against a group from the inventory file')
parser.add_argument('-k', '--key', help= 'SSH key to use if needed')
#QUICK AND DIRTY, USING GLOBALS (NOT BEST PRACTICE, PLS NO KILL)
#
config = configparser.ConfigParser()
config.read('balls')
inv = config.read('inventory')
args = parser.parse_args()
# TODO: If this becomes a large-ish program, must get rid of globals
#
def check_ball(): #checks to make sure specified ball is in balls file
	if args.ball is None:
		print('[>] You must select a ball...')
		sys.exit()
	if args.ball not in config.sections():
		print('[>] specifed ball not in the ball file...')
		sys.exit()

def list_balls_help():
	#checks if list or help was used
	if args.list:
		list_balls(config)
		list_balls

def input_error_check():
	#from here stuff gets dispatched
	if args.machine is not None:
		runner(args.machine)

	elif args.group is not None:
		group = inv.options(args.group)
		runner(group)

	elif args.machine is None and args.group is None:
		print('[>] You must enter a group or machine to run ball against...')
		parser.usage()
	elif args.machine is not None and args.group is not None:
		print('[>] You cannot use both tags...')
		parser.usage()
	else:
		print('[>] Unspecified behavior...')

def start():
	#kicks off program
	list_balls_help()

	check_ball()

	input_error_check()
	
		
def list_balls():
	sections = config.sections()
	for section in sections:
		print(section)
		print(config.get(section,'tag'))
		print(conifg.get(section,'description'))
		print('[>]--------------------------------[<]')	

def runner(group): #might combine with tag_check
	steps = sort_balls
	count = 0
	if tag_check() == 'windows':
 		for machine in group:
 			count = count + 1
 			winrm_connect(machine, steps, count)
	elif tag_check() == 'linux':
		for machine in group:
			ssh_connect(machine, steps, count)
	else:
		print('[>] No tag set/incorrect tag')


def winrm_connect(machine, steps, count):
	user = input('[>] Enter username: ')
	passwrd = getpass.getpass('[>] Enter password: ')
	try:
		session = winrm.Session(machine, auth=(user, passwrd))
	except: #auth error:
		sys.exit()
	for step in steps:
		execute = session.run_cmd(step)
		if count == 1:
			print(execute.std_out)
		#add logging through execute.std_out
		if execute.std_err is not None:
			print('[>]--------------------------------[<]')
			print(execute.std_err)
			sys.exit()
	generate_log(execute.stdout, execute.stderr)
	print('[>] Success!')
	print('[>] Log saved')

def ssh_connect(machine, steps, count):
	#CHANGE TO ONE TRY/ACCEPT
	try:
		client = paramiko.client.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		if args.key is None:
			print('[>] No key selected for ssh...')
			print('[>] Switching to password auth...')
			user = input('[>] Enter Username: ')
			psswd = getpass.getpass('[>] Enter Password: ')
			client.connect(machine, username=user, password= psswd)
		else:
			client.connect(machine, pkey=args.key)

		for step in steps:
			stdin,stdout, stderr = client.exec_command(step)
			if count == 1:
				print(stdout.read())
			if stderr is not None: #this probably will get changed to len or something
				print('[>]--------------------------------[<]')
				print(std_err.read())
				sys.exit()
		generate_log(stdout, stderr)
		print('[>] Success!')
		print('[>] Log Saved...')
	except paramiko.ssh_exception.AuthenticationException:
		print('[>] Login creds incorrect')
		sys.exit()
	except socket.gaierror:
		print('[>] Network error. Is the machine address correct?')
		sys.exit()


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

def generate_log(stdout, stderr):
	directory = os.listdir()

	with open('log'+len(directory)+1,'w') as log:
		if stderr is not None:
			log.write(stderr.read())
		log.write('\n')
		log.write(stdout.read())

start()
	