from xml.dom import minidom
from . import *

class HitChart(list):
	
	def save(self):
		DB = store.Store()

		for hip in self:
			sql = 'REPLACE INTO hitchart (%s) VALUES(%s)' % (','.join(hip.keys()), ','.join(['%s'] * len(hip.keys())))
			DB.query(sql, hip.values())
		DB.save()
	
	def __init__(self, game_id):
		super(HitChart, self).__init__()

		year, month, day = game_id.split('_')[1:4]
		url = '%syear_%s/month_%s/day_%s/%s/inning/inning_hit.xml' % (CONSTANTS.BASE, year, month, day, game_id)

		contents = Fetcher.fetch(url)
		if contents is None:
			return

		doc = minidom.parseString(contents)
		for element in doc.getElementsByTagName('hip'):
			hip = {'game_id': game_id}
			for attr in element.attributes.keys():
				hip[attr] = element.attributes[attr].value
			self.append(hip)