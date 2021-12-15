'''
Created on Dec 7, 2021

@author: bleem
'''
from src.orgs.AnOrganism import AnOrganism


class NullOrganism(AnOrganism):

	def __init__(self, json_data):
		super().__init__(json_data)
