#!/usr/bin/python
# -*- coding: utf-8 -*-

from OracleDatabase import OracleDatabase
import logging,cx_Oracle
from Utils import ErrorSQLRequest, checkOptionsGivenByTheUser
from Constants import *
from PasswordGuesser import PasswordGuesser, runPasswordGuesserModule

class UsernameLikePassword (OracleDatabase):
	'''
	Allow to connect to the database using each Oracle username like the password 
	'''
	def __init__(self,args):
		'''
		Constructor
		'''
		logging.debug("UsernameLikePassword object created")
		OracleDatabase.__init__(self,args)
		self.allUsernames = []
		self.validAccountsList = []

	def __loadAllUsernames__(self):
		'''
		Get all usernames from the ALL_USERS table
		'''
		logging.info('Get all usernames from the ALL_USERS table')
		query = "select username from ALL_USERS"
		response = self.__execQuery__(query=query,ld=['username'])
		if isinstance(response,Exception) :
			logging.info('Error with the SQL request {0}: {1}'.format(query,str(response)))
			return response
		else :
			if response == []: self.allUsernames = []
			else:
				for e in response : self.allUsernames.append(e['username']) 
		logging.info("Oracle usernames stored in the ALL_USERS table: {0}".format(self.allUsernames))

	def tryUsernameLikePassword(self):
		'''
		Try to connect to the DB with each Oracle username using the username like the password
		'''
		accounts = []
		self.__loadAllUsernames__()
		passwordGuesser = PasswordGuesser(self.args,"",timeSleep=self.args['timeSleep'])
		for usern in self.allUsernames: accounts.append([usern,usern])
		passwordGuesser.accounts = accounts
		passwordGuesser.searchValideAccounts()
		self.validAccountsList = passwordGuesser.valideAccounts	

	def testAll (self):
		'''
		Test all functions
		'''
		pass

def runUsernameLikePassword(args):
	'''
	Run the UsernameLikePassword module
	'''
	status = True
	usernameLikePassword = UsernameLikePassword(args)
	status = usernameLikePassword.connection(stopIfError=True)
	#Option 1: UsernameLikePassword
	if args['run'] !=None :
		args['print'].title("Oracle users have not the password identical to the username ?")
		usernameLikePassword.tryUsernameLikePassword()
		if usernameLikePassword.validAccountsList == {}:
			args['print'].badNews("No found a valid account on {0}:{1}/{2}".format(args['server'], args['port'], args['sid']))
		else :
			args['print'].goodNews("Accounts found on {0}:{1}/{2}: {3}".format(args['server'], args['port'], args['sid'],usernameLikePassword.validAccountsList))


