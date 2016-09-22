import paramiko
import winrm
import sys
import getpass
import socket
import os
import datetime
from src.parsing import *
#from src.parsing import ballhandling
#TODO: generate log from compiled list of output not from singular output
#TODO:  
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
		self.log = 0

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
						sudo = sudo + 1
						stdout, stderr = self.sudo_run(sudo, step, client)
						outlines = str(stdout.read())
						error = str(stderr.read())
						print(outlines)
					else:
						self.log = 1
						stdout, stderr = self.sudo_run(sudo, step, client)
						error = str(stderr.read())
					if len(error) > 5: #error should be longer then 5 chars
						print('[>]---ERROR---ERROR---ERROR---[<]')
						print(error.rstrip())
						sys.exit()
					self.generate_log(outlines, error) # need to log output into list and pass to log(only logs one thing now)
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
		except winrm.exceptions.InvalidCredentialsError: #Auth error
			print('[>] Auth Error')
			sys.exit()
		except socket.gaierror:
			print('[>] Network error. Is the machine address correct?')
			sys.exit()

	def generate_log(self,stdout, stderr):
		directory = os.listdir()

		with open('log','a') as log:
			if self.log == 0:
				log.write(str(datetime.datetime.now()))
				log.write('\n \n')
				self.log = 1
			if len(stderr) > 5:
				log.write(stderr)
			log.write('\n \n')
			log.write(stdout)

	def sudo_run(self,sudo,step, client):
		if sudo == 2:
			stdin, stdout, stderr = client.exec_command('sudo echo')
			stdin.write(self.args.password+'\n')
			stdin.flush()
			print('Elevated')
		else: 
			stdin, stdout, stderr = client.exec_command(step)
		return stdout, stderr

