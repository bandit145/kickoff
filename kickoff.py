import winrm #to be used for powershell/windows commands
import paramiko
import configparser
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-l', '--list', usage= 'list balls', action = 'store_true')
pasrer.add_argument('-b', '--ball', usage= 'ball you want to use', required=True)
parser.add_argument('-m','--machine', usage= 'machine adress' )
parser.add_argument('-g', '--group', useage= 'run ball against group from inventory file')
parser.add_argument('-h', '--help', usage= 'help', action= 'store_tru')



def check_ball(ball, config):
	if ball not in config.sections:
		print('specifed ball not in the ball file')

def list_balls_help(args):
	if args.list:
		list_balls(config)
	elif args.help:
		parser.usage()
	else:
		a = 0
def input_error_check(args):

	if args.machine is not None:
		runner(args.machine, config, args.ball)

	elif args.group is not None:
		runner(args.group, config, args.ball)

	elif args.machine None && args.group is None:
		print('You must enter a group or machine to run ball against')
		parser.usage()
	elif args.machine is not None && args.group is not None:
		print('You cannot enter use both tags')
		parser.usage()
	else:
		print('unspecified beavior')

def main():
	#checking for help/list
	config = configparser.ConfigParser()
	config.read('balls')
	inv = config.read('inventory')
	args = parser.parse_args()

	check_ball(args.ball, config)

	list_balls_help(args)
	#test to make sure user has not entered information incorrectly
	input_error_check(args)
	



		
def list_balls(config):
	sections = config.sections()
	for section in sections:
		print(section)
		print(config.get(section,'tag'))
		print(conifg.get(section,'description'))
		print('--------------------------------')	

def runner(args,config, ball):
	if args == list:
		githu
		for machine in args



def winrm_connect():
	if 
	session = winrm.Session()


def ssh_connect():
