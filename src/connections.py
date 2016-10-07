import paramiko
import winrm
import sys
import getpass
import socket
import os
import datetime
from src.parsing import *
from colorama import Back, Style, init
#from src.parsing import ballhandling
#TODO: generate log from compiled list of output not from singular output
#TODO:  
class connections:
	def __init__(self, group, steps, count, args, remote_user):
		init()
		if group == list:
			self.group = group
		else:
			self.group = []  #might need redoing when groups get parsed from inventory
			self.group.append(group) #This wont work with an actual group (probably)
		self.steps = steps #For tracking steps
		self.count = count #for keeping count of how many machines have been run
		self.args = args #args from cmd line
		self.remote_user = remote_user #parsed user to use
		self.log = 0 #for telling the log when to log (might just rip the logging feature out.)

	def ssh_connect(self): #SSHs into machinesand runs ball
		try:
			for machine in self.group:
				client = paramiko.client.SSHClient()
				client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				if self.args.key is None:
					client.connect(machine, username=self.remote_user, password=self.args.password)
				else:
					key = paramiko.RSAKey(filename=self.args.key, password=self.args.password)
					client.connect(machine, username=self.remote_user ,pkey=key)# add user
				sudo = 1
				for step in self.steps:
					if self.count == 1:
						sudo = sudo + 1
						stdout, stderr = self.sudo_run(sudo, step, client)
						outlines = stdout.readlines()
						error = stderr.readlines()
						if len(error) < 5:
							print(Back.GREEN+''+step+' > PASSED')
							print(Style.RESET_ALL)
					else:
						self.log = 1
						sudo = sudo +1
						stdout, stderr = self.sudo_run(sudo, step, client)
						error = str(stderr.readlines())
					if len(error) > 5: #rewrite for actual proper output
						print(Back.RED+'[>]---ERROR---ERROR---ERROR---[<]')
						print(Style.RESET_ALL)
						for line in error:
							print(line)
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

	#NEEDS TESTING
	def winrm_connect(self): #winrms into windows machine and runs ball
		try:
			for machine in self.group:
				session = winrm.Session(machine, auth=(self.remote_user, self.args.password))
				for step in self.steps:
					execute = session.run_cmd(step)
					if self.count == 1:
						print(Back.GREEN+''+execute.std_out+' > PASSED')
						print(Style.RESET_ALL)
					#add logging through execute.std_out
					elif len(execute.stderr) > 5:
						print(Back.RED+'[>]---ERROR---ERROR---ERROR---[<]')
						print(Style.RESET_ALL)
						print(execute.stderr)
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

	def generate_log(self,stdout, stderr): #generates the log from a run. Currently only will log 1 full run.
		with open('log','a') as log:
			if self.log == 0:
				log.write(str(datetime.datetime.now()))
				log.write('\n \n')
				self.log = 1
			if len(stderr) > 5:
				for line in stderr:
					log.write(line)
			for line in stdout:
				log.write('\n \n')
				log.write(line)

	def sudo_run(self,sudo,step, client): #elevates to sudo (and normal execution), used in ssh_connect
		if sudo == 2:
			stdin, stdout, stderr = client.exec_command('sudo echo')
			stdin.write(self.args.password+'\n')
			stdin.flush()
			print(Back.GREEN +'Elevated')
			print(Style.RESET_ALL)
			stdin, stdout, stderr = client.exec_command(step)
		else: 
			stdin, stdout, stderr = client.exec_command(step)
		return stdout, stderr

