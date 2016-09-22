#!/usr/bin/env python3 
#TODO: ssh func tomorrow, write unit tests and add exception handling 8/10/2016
import winrm #to be used for powershell/windows commands
import paramiko
import configparser
import argparse
import sys
import getpass
import os
import socket #for error handling connections
from src.parsing import *
from src.connections import *
parser = argparse.ArgumentParser()
parser.add_argument('-l', '--list', action = 'store_true', help='Lists balls')
parser.add_argument('-b', '--ball', help= 'Ball to run')
parser.add_argument('-m','--machine', help= 'Run against individual machine')
parser.add_argument('-g', '--group', help= 'Run against a group from the inventory file')
parser.add_argument('-k', '--key', help= 'SSH key to use if needed')
parser.add_argument('-p', '--password', help= 'password for user elevation/access')
#QUICK AND DIRTY, USING GLOBALS (NOT BEST PRACTICE, PLS NO KILL)

# TODO: Pass all ball steps to raw string to avoid OSERROR no.2
#


def start():
	args = parser.parse_args()
	ball_stuff = ballhandling(args)
	config = ball_stuff.return_config()
	#kicks off program
	#Check for cmd line arg errors and dispatch to methods
	if args.list:
		ball_stuff.list_balls()
	elif args.ball is None:
		print('[>] You must select a ball')
		parser.print_help()
		sys.exit()
	elif args.ball not in config.sections():
		print('[>] specifed ball not in the ball file')
		parser.print_help()
		sys.exit()
	#from here stuff gets dispatched
	elif args.machine is not None:
		runner(args.machine, ball_stuff, args)
	elif args.group is not None:
		group = inv.options(args.group)
		runner(group, ball_stuff, args)
	elif args.machine is None and args.group is None:
		print('[>] You must enter a group or machine to run ball against...')
		parser.print_help()
	elif args.machine is not None and args.group is not None:
		print('[>] You cannot use both tags...')
		parser.print_help()
	elif args.password is None and 'elevate' in ball_stuff.sort_balls():
		print('Specified ball requires a user elevation password')
		parser.print_help()
	else:
		print('[>] Unspecified behavior...')
		sys.exit()
	
		
def runner(group, ball_stuff, args): #might combine with tag_check
	steps = ball_stuff.sort_balls()
	remote_user = ball_stuff.remote_user()
	count = 1
	if ball_stuff.tag_check() == 'windows':
 			execution = connections(group, steps, count, args, remote_user)
 			execution.winrm_connect()
	elif ball_stuff.tag_check() == 'linux':
			execution = connections(group, steps, count, args, remote_user)
			execution.ssh_connect()
	else:
		print('[>] No tag set/incorrect tag')

start()
	