#!/usr/bin/env python

import json
import requests


class KerioAPI:
	def __init__(self, ip, port, user, passwd):
		self.ip = ip
		self.port = port
		self.user = user
		self.passwd = passwd
	
####
	def sendRequest(self, data, headers):
		uri = "https://" + self.ip + ":" + self.port + "/admin/api/jsonrpc/"
		r = requests.post(uri, data, headers=headers, verify=False)
		if not r:
			writeLog("INFO: ", "Can't connect to kerio api, please check !")
		#
		return r
	
	####
	def createHeader(self, header_size):
		headers = {
			"Accept" : "application/json-rpc",
			"Content-type": "application/json-rpc",
			"Host" : self.ip+":"+self.port,
			"Content-Length" : header_size,
			"Connection" : "close",
			"X-Token" : settoken,
			"Cookie" : setcookie
		}
		#
		return headers
	
	####
	def login(self):
		# login json
		login = {
			"jsonrpc": "2.0",
			"id": 1,
			"method": "Session.login",
			"params": {
				"username": self.user,
				"password": self.passwd,
				"application": {
					"name": "Huynh Nang",
					"vendor": "VONLINE",
					"version": "1.0.0"
				}
			}
		}
		# login headers
		login_size = len(login)
		headers = {
			"Accept" : "application/json-rpc",
			"Content-type": "application/json-rpc",
			"Host" : self.ip+":"+self.port,
			"Content-Length" : login_size,
			"Connection" : "close",
			"X-Token" : "",
			"Cookie" : ""
		}
	
		data=json.dumps(login)
		r = self.sendRequest(data, headers)
		isOK = False
		if r:
			cookie1 = r.cookies["Session_admin80"]
			cookie2 = r.cookies["KWAT"]
			global setcookie
			setcookie = "Session_admin80=" + cookie1 + "; " + "KWAT=" + cookie2
			token = json.loads(r.text)
			global settoken
			settoken = token['result']['token']
			isOK = True
			writeLog("INFO: ", r.text)
		else:
			writeLog("INFO: ", "Can't send request to kerio api")
		#
		return isOK
			
		
		
	####
	def getDomainID(self, domain):
		getDomain = {
			"jsonrpc":"2.0","id":1,
			"method":"Domains.get",
			"params":{"query":{"conditions":[{"fieldName":"name","comparator":0,"value":domain}],"start":0,"limit":1,"fields":["id"]}}
		}
		data_size = len(getDomain)
		data = json.dumps(getDomain)
		r = self.sendRequest(data, self.createHeader(data_size))
		domainID = ''
		if r:
			idd = json.loads(r.text)
			domainID = idd['result']['list'][0]['id']
			writeLog("INFO: ", r.text)
		else:
			writeLog("INFO: ", "Can't send request to kerio api")
		#
		return domainID
	
	####
	def getUserID(self, username, domain):
		domainID = self.getDomainID(domain)
		getUser = {
			"jsonrpc":"2.0","id":1,
			"method":"Users.get",
			"params":{"query":{"conditions":[{"fieldName":"loginName","comparator":0,"value":username}],"combining":0,"start":0,"limit":-1,"fields":["id"]},"domainId":domainID}
		}
		data_size = len(getUser)
		data = json.dumps(getUser)
		r = self.sendRequest(data, self.createHeader(data_size))
		userID = ''
		if r:
			idd = json.loads(r.text)
			userID = idd['result']['list'][0]['id']
			writeLog("INFO: ", r.text)
		else:
			writeLog("INFO: ", "Can't send request to kerio api")
		#
		return userID
	
	
	####
	def updatePassword(self, username, newpassword, domain):
		userID = self.getUserID(username, domain)
		updatePassword = {
			"jsonrpc":"2.0","id":1,
			"method":"Users.set",
			"params":{"userIds":[userID],
			"pattern":{"password":newpassword}}
		}
				
		data_size = len(updatePassword)
		data = json.dumps(updatePassword)
		r = self.sendRequest(data, self.createHeader(data_size))
		isOK = False
		if r:
			#print r.text
			writeLog("INFO: ", r.text)
			isOK = True
		else:
			writeLog("INFO: ", "Can't send request to kerio api")
		#
		return isOK
	
	####
	def createUser(self, fullname, username, password, domain):
		domainID = self.getDomainID(domain)
		createUser = {
			"jsonrpc": "2.0",
			"id": 1,
			"method": "Users.create",
			"params":{
				"users":[{
					"loginName":username,"description":"","hasDefaultSpamRule":True,"publishInGal":True,"authType":0,"isPasswordReversible":True,"isEnabled":True,
					"domainId":domainID,"hasDomainRestriction":False,"password":password,"role":{"userRole":0,"publicFolderRight":False,"archiveFolderRight":False},"itemLimit":{"isActive":False,"limit":0},
					"diskSizeLimit":{"isActive":False,"limit":{"value":0,"units":2}},"outMessageLimit":{"isActive":False,"limit":{"value":"","units":2}},
					"cleanOutItems":{"isUsedDomain":True,"deletedItems":{"isEnabled":False,"days":30},"junkEmail":{"isEnabled":False,"days":30},
					"sentItems":{"isEnabled":False,"days":30},"autoDelete":{"isEnabled":False,"days":1095}},"fullName":fullname,"emailForwarding":{"mode":0,"emailAddresses":[]},"emailAddresses":[],"userGroups":[]
				}]
			}
		}
		data_size = len(createUser)
		data = json.dumps(createUser)
		r = self.sendRequest(data, self.createHeader(data_size))
		isOK = False
		if r:
			#print r.text
			writeLog("INFO: ", r.text)
			isOK = True
		else:
			writeLog("INFO: ", "Can't send request to kerio api")
		#
		return isOK
	
	####
	def removeUser(self, username, domain):
		userID = self.getUserID(username, domain)
		removeUser = {
			"jsonrpc":"2.0","id":1,"method":"Users.remove",
			"params":{"requests":[{"userId":userID,
			"method":0,"targetUserId":""}]}
		}
		data_size = len(removeUser)
		data = json.dumps(removeUser)
		r = self.sendRequest(data, self.createHeader(data_size))
		isOK = False
		if r:
			#print r.text
			writeLog("INFO: ", r.text)
			isOK = True
		else:
			writeLog("INFO: ", "Can't send request to kerio api")
		#
		return isOK
	
	####
	def enableUser(self, username, domain):
		userID = self.getUserID(username, domain)
		enableUser = {
			"jsonrpc":"2.0","id":1,"method":"Users.set",
			"params":{"userIds":[userID],"pattern":{"isEnabled":True}}
		}
		data_size = len(enableUser)
		data = json.dumps(enableUser)
		r = self.sendRequest(data, self.createHeader(data_size))
		isOK = False
		if r:
			#print r.text
			writeLog("INFO: ", r.text)
			isOK = True
		else:
			writeLog("INFO: ", "Can't send request to kerio api")
		#
		return isOK
		
	####
	def disableUser(self, username, domain):
		userID = self.getUserID(username, domain)
		disableUser = {
			"jsonrpc":"2.0","id":1,"method":"Users.set",
			"params":{"userIds":[userID],"pattern":{"isEnabled":False}}
		}
		data_size = len(disableUser)
		data = json.dumps(disableUser)
		r = self.sendRequest(data, self.createHeader(data_size))
		isOK = False
		if r:
			#print r.text
			writeLog("INFO: ", r.text)
			isOK = True
		else:
			writeLog("INFO: ", "Can't send request to kerio api")
		#
		return isOK
	
	####
	def logout(self):
		logout = {
			"jsonrpc": "2.0",
			"id": 1,
			"method": "Session.logout"
		}
		data_size = len(logout)
		data = json.dumps(logout)
		r = self.sendRequest(data, self.createHeader(data_size))
		isOK = False
		if r:
			#print r.text
			writeLog("INFO: ", r.text)
			isOK = True
		else:
			writeLog("INFO: ", "Can't send request to kerio api")
		#
		return isOK
	
	####
	def writeLog(self, prefix, content):
		logPath = '/var/log/kerioapi.log'
		try:
			fo = open(logPath, 'a')
			now = datetime.now()
			nowFormat = now.strftime('%Y/%m/%d %H:%M:%S')
			fo.writelines(nowFormat + "\t" + prefix + content + "\n")
		except IOError, e:
			pass
		finally:
			fo.close()
