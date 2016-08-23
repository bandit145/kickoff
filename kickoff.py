
#TODO: ssh func tomorrow, write unit tests and add exception handling 8/10/2016
import winrm #to be used for powershell/windows commands
import paramiko
import configparser
import argparse
import sys
import getpass
import os
import socket #for error handling connections
from connection import *
from parsing import *
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

def input_error_check():
	#from here stuff gets dispatched
	if args.machine is not None:
		runner(args.machine)

	elif args.group is not None:
		group = inv.options(args.group)
		runner(group)

	elif args.machine is None and args.group is None:
		print('[>] You must enter a group or machine to run ball against')
		parser.usage()
	elif args.machine is not None and args.group is not None:
		print('[>] You cannot use both tags')
		parser.usage()
	else:
		print('[>] Unspecified behavior')

def start():
	ball_stuff = ballhandling(args)
	#kicks off program
	if args.list:
		ball_handling.list_balls()
	elif args.ball is None:
		print('[>] You must select a ball')
		sys.exit()
	elif args.ball not in config.sections():
		print('[>] specifed ball not in the ball file')
		sys.exit()
	else:
		print('[>] Unspecified behavior... ')
	#from here stuff gets dispatched
	if args.machine is not None:
		runner(args.machine, ball_stuff)
	elif args.group is not None:
		group = inv.options(args.group)
		runner(group, ball_stuff)
	elif args.machine is None and args.group is None:
		print('[>] You must enter a group or machine to run ball against...')
		parser.usage()
	elif args.machine is not None and args.group is not None:
		print('[>] You cannot use both tags...')
		parser.usage()
	else:
		print('[>] Unspecified behavior...')
	
		
def runner(group, ball_stuff): #might combine with tag_check
	steps = ball_stuff.sort_balls
	count = 0
	if ball_stuff.tag_check() == 'windows':
 		for machine in group:
 			count = count + 1
 			execution = connections(machine, steps, count, args)
 			execution.winrm_connect()
	elif ball_stuff.tag_check() == 'linux':
		for machine in group:
			count = count+1
			execution = connections(machine, steps, count, args)
			execution.ssh_connect(machine, steps, count)
	else:
		print('[>] No tag set/incorrect tag')

start()
	