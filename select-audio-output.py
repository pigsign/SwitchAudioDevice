#!/usr/bin/python2
# -*- coding: utf8 -*-

from subprocess import call
import os
import sys
import re
import shutil


if (not call('cat /proc/asound/cards', shell=True)):
	cardNumber = input('\n要選擇哪個作為 Audio Output 裝置??(數字): ')
	cardNumber = str(cardNumber)
else:
	print 'Error: cat /proc/asound/cardsd'
	sys.exit()

if (os.path.isfile('/usr/share/alsa/alsa.conf')):
	shutil.copy2('/usr/share/alsa/alsa.conf', '/tmp/alsa.conf.bk')
	newConfFile = open('/usr/share/alsa/alsa.conf', 'w')
	for line in open('/tmp/alsa.conf.bk'):
		if (re.compile(r'defaults.ctl.card').findall(line)):
			newConfFile.write('defaults.ctl.card %s\n' % cardNumber)
		elif (re.compile(r'defaults.pcm.card').findall(line)):
			newConfFile.write('defaults.pcm.card %s\n' % cardNumber)
		else:
			newConfFile.write(line)
	
	newConfFile.close()
	call('/etc/rc.d/alsa restart', shell=True)

else:
	print 'Error: 找不到 /usr/share/alsa/alsa.conf 檔案'

