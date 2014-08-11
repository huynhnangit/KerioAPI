#!/usr/bin/env python

import kerioapi

connectAPI = kerioapi.KerioAPI(kerio_ip, "4040", kerio_user, kerio_passwd)
if connectAPI.login():
	rsl = connectAPI.updatePassword(getUser, newpassword, getDomain)
	if rsl:
		print "Change password is successful !"
	connectAPI.logout()