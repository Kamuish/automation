import subprocess
import os 
import json 

network_names = [b'MEO-SILVA',b"CAUP-guest"]

if not os.path.exists('time.txt'):
	with open('time.txt', mode = 'w') as file:
		json.dump({}, file)

with open('time.txt', mode = 'r') as file:
	data = json.load(file)
	results = subprocess.check_output("netsh wlan show interfaces")
	for net in network_names:
		if net in results :

			print(net)
			try :
				data[net.decode('ascii')] += 1
			except:
				data[net.decode('ascii')] = 0

with open('time.txt', mode = 'w') as file:
	json.dump(data,file)

   