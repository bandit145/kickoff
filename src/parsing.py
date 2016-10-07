#TODO: Add error handling for people that forgot to enter stuff in the config file
import configparser
class ballhandling:
	def __init__(self, args):
		self.config = configparser.ConfigParser()
		self.config.read('balls')
		self.args = args


	def list_balls(self):
		sections = self.config.sections()
		for section in sections:
			print('[>]--------------------------------[<]')
			print('Ball: ' + section)
			print('Tag: ' + self.config.get(section,'tag'))
			print('Description: '+ self.config.get(section,'description'))

	def sort_balls(self): #replace with list comprehension
		steps = [];
		options = self.config.options(self.args.ball)
		options.remove('description')
		options.remove('tag')
		options.remove('remote_user')
		for option in options:
			steps.append(self.config.get(self.args.ball, option)) #for each command
		return steps

	def remote_user(self):
		try:
			remote_user = self.config.get(self.args.ball, 'remote_user')
			return remote_user
		except configparser.NoOptionError:
			print('[>] Ball needs a remote user')
		
	def tag_check(self):
		if self.config.get(self.args.ball, 'tag') == 'windows':
			return 'windows'
		elif self.config.get(self.args.ball, 'tag') == 'linux':
			return 'linux'

	def return_config(self):
		return self.config