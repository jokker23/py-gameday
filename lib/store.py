from . import *
import MySQLdb
import sys
from ConfigParser import ConfigParser

class Store:
	def __init__(self, **args):
		parser = ConfigParser()
		parser.read('%s/db.ini' % sys.path[0])
		user = parser.get('db', 'user')
		password = parser.get('db', 'password')
		db = parser.get('db', 'db')
		
		args = {'user': user, 'passwd': password, 'db': db}

		if parser.has_option('db', 'host'):
			args['host'] = parser.get('db', 'host')
		
		self.db = MySQLdb.connect(**args)
		self.cursor = self.db.cursor()
		
	def save(self):
		self.db.commit()
	
	def finish(self):
		self.db.commit()
		self.db.close()
		
	def query(self, query, values = None):
		simplefilter("error", MySQLdb.Warning)
		
		try:
			res = self.cursor.execute(query, values)
			return self.cursor.fetchall()
		except (MySQLdb.Error, MySQLdb.Warning), e:
			if len(e.args > 1):
				msg = e.args[1]
			else:
				msg = e.args[0]
			logger.error('%s\nQUERY: %s\nVALUES: %s\n\n' % (msg, query, ','.join([str(v) for v in values])))
