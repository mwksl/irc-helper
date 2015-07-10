# -*- coding: utf-8 -*-
import os
import collections
import emoji
import re

path = os.getenv('APPDATA')+"\\HexChat\logs"
snoonet = path+"\\Snoonet"
askmen = snoonet + "\\#askmen.log"
f = open(askmen, 'r', encoding="utf8")


def getAllIPsUsedByName(name):
	ips = collections.Counter()
	iplist = []
	for line in f:
		if "has joined" in line and name.lower() in line.lower() and line[16] is '*':
			start = line.find('@')+1
			end =  line.find(')')
			ip = line[start:end]
			iplist.append(ip)
	ips.update(iplist)
	f.seek(0)
	return ips

def getAllNamesByIPs(ips):
	nicks = collections.Counter()
	nicklist = []
	for line in f:
		for ip in ips:
			if "has joined" in line and ip in line and line[16] is '*':
				start = line.find('*')+2
				end = line[start:].find(' ')+start
				username = line[start:end]
				nicklist.append(username)

	nicks.update(nicklist)
	f.seek(0)
	return nicks


def findUsernamesByUsername(nick): #Can be spoofed by a /me
	#Pretty sure emojis are ruining Python's day
        #That's why you declare the encoding at the beginning 😏
	try:
		ips = getAllIPsUsedByName(nick)
		join = getAllNamesByIPs(ips)
		return join
	#I should probably figure that out
	except UnicodeDecodeError:
		pass
	#But not right now, there's no
	except UnicodeEncodeError:
		pass

@TODO
#This isn't properly implemented yet
def stripEmojisFromName(nick):
	"""So, the issue is trying to convert the nick into Unicode.
	   If you attempt to return the nick as u'%s' % nick you'll
	   obviously get an ordinal range error. I don't know how to
	   fix this yet."""
    try:
        # UCS-4 - wide
        emoji_re = re.compile(u'[U00010000-U0010ffff]')
    except re.error: #don't be a hero, just try it
        # UCS-2 - narrow
        emoji_re = re.compile(u'[uD800-uDBFF][uDC00-uDFFF]')
    nick = emoji_re.sub(u'\u25FD', nick)
    return nick


nick = ""
#stripEmojisFromName(nick)
nicks = findUsernamesByUsername(nick)
print (nicks)
