import paramiko
import winrm
import sys
import getpass
import socket
import os
from src.parsing import *
#from src.parsing import ballhandling
#TODO: Add generate log ot this file instead of parsing
class connections:
	def __init__(self, group, steps, count, args, remote_user):
		if group == list:
			self.group = group
		else:
			self.group = []  #might need redoing when groups get parsed from inventory
			self.group.append(group) #This wont work with an actual group (probably)
		self.steps = steps
		self.count = count
		self.args = args
		self.remote_user = remote_user

	def ssh_connect(self):
		try:
			for machine in self.group:
				client = paramiko.client.SSHClient()
				client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				if self.args.key is None:
					client.connect(machine, username=self.remote_user, password=self.args.password)
				else:
					client.connect(machine, username=self.remote_user ,pkey=self.args.key)# add user
				sudo = 1	
				for step in self.steps:

					if self.count == 1:
						stdout, stderr = sudo_run(sudo, step)
						outlines = str(stdout.readlines()) #might change to readlines depending
						error = str(stderr.readlines())
						for out in stdout:
							print(out)
					else:
						stdout, stderr = sudo_run(sudo, step)
					if len(stderr) > 5: #error should be longer then 5 chars
						print('[>]--------------------------------[<]')
						for out in outlines:
							print(out)
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
#needs to be tested an fixed up
	def winrm_connect(self):
		user = input('[>] Enter username: ')
		passwrd = getpass.getpass('[>] Enter password: ')
		try:
			for machine in self.group:
				session = winrm.Session(machine, auth=(self.remote_user, self.args.password))
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

	def sudo_run(self,sudo,step):
		if sudo == 1:
			stdin, stdout, stderr = client.exec_command('sudo ' + step)
			stdin.write(self.args.password+'\n')
			stdin.flush()
		else: 
			stdin, stdout, stderr = client.exec_command(step)
		return stdout, stderr

