import paramiko
import winrm
import sys
import getpass
import socket
import os
#from src.parsing import ballhandling
#TODO: Add generate log ot this file instead of parsing
class connections:
	def __init__(self, group, steps, count, args):
		self.group = []  #might need redoing when groups get parsed from inventory
		self.group.append(group)
		self.steps = steps
		self.count = count
		self.args = args


	def ssh_connect(self):
		try:
			for machine in self.group:
				client = paramiko.client.SSHClient()
				client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				if self.args.key is None:
					print('[>] No key selected for ssh')
					print('[>] Switching to password auth')
					user = input('[>] Enter Username: ')
					psswd = getpass.getpass('[>] Enter Password: ')
					client.connect(machine, username=user, password= psswd)
				else:
					client.connect(machine, pkey=self.args.key)

				for step in self.steps:
					stdin, stdout, stderr = client.exec_command(step)
					if self.count == 1:
						stdout = str(stdout.read()) #might change to readlines depending
						stderr = str(stderr.read())
						print(stdout)
					if len(stderr) > 5: #this probably will get changed to len or something
						print('[>]--------------------------------[<]')
						print(stderr)
						sys.exit()
					self.generate_log(stdout, stderr)
				self.count =+1
			print('[>] Success!')
			print('[>] Log Saved')
		except paramiko.ssh_exception.AuthenticationException:
			print('[>] Login creds incorrect')
			sys.exit()
		except socket.gaierror:
			print('[>] Network error. Is the machine address correct?')
			sys.exit()
		except OSError:
			print('[>] Network error. Machine could not access network.')
			sys.exit()

#add socket exception
	def winrm_connect(self):
		user = input('[>] Enter username: ')
		passwrd = getpass.getpass('[>] Enter password: ')
		try:
			for machine in self.group:
				session = winrm.Session(machine, auth=(user, passwrd))
				for step in self.steps:
					execute = session.run_cmd(step)
					if self.count == 1:
						print(execute.std_out)
					#add logging through execute.std_out
					if execute.std_err is not None:
						print('[>]--------------------------------[<]')
						print(execute.std_err)
						sys.exit()
					self.generate_log(execute.stdout, execute.stderr)
				print('[>] Success!')
				print('[>] Log saved')
				self.count =+1
		except winrm.AuthenticationError: #Auth error
			sys.exit()
		except socket.gaierror:
			print('[>] Network error. Is the machine address correct?')
			sys.exit()

	def generate_log(self,stdout, stderr):
		directory = os.listdir()

		with open('log','w') as log:
			if len(stderr) > 5:
				log.write(stderr)
			log.write('\n')
			log.write(stdout)
