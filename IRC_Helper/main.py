import os
import collections

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

nick = ""
nicks = findUsernamesByUsername(nick)
print (nicks)