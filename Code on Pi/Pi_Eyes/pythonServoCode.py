#!/usr/bin/python

import sys
import subprocess
import pi3d
from nbstreamreader import NonBlockingStreamReader as NBSR

mykeys = pi3d.Keyboard()
process = subprocess.Popen('sudo python ServoCode.py', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
nbsr = NBSR(process.stdout)

while(1):
	k = mykeys.read()
	if (k == 97):
		process.stdin.write('a\n')
		output = nbsr.readline(0.1)
		print(output)
