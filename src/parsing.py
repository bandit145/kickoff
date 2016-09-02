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
		for option in options:
			steps.append(self.config.get(self.args.ball, option)) #for each command
		return steps
		
	def tag_check(self):
		if self.config.get(self.args.ball, 'tag') == 'windows':
			return 'windows'
		elif self.config.get(self.args.ball, 'tag') == 'linux':
			return 'linux'

	def return_config(self):
		return self.config