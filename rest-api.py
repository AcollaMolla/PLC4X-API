from flask import Flask, request, jsonify
import json
app = Flask(__name__)

class Machine(object):
	def __init__(self, name, address, timeout):
		self.name = name
		self.address = address
		self.timeout = timeout
	def get_name(self):
		return self.name

machines = []

def object_decoder(obj):
	return Machine(obj['name'], obj['address'], obj['timeout'])



for line in open('config.json', 'r'):
	current = json.loads(line)
	machines.append(Machine(current['name'], current['address'], current['timeout']))

@app.route('/')
def index():
	return 'hello world'

@app.route('/getMachines')
def GetMachines():
	return json.dumps([ob.__dict__ for ob in machines])

@app.route('/newMachine', methods=['POST'])
def newMachine():
	content = request.json
	result = 0
	try:
		result = addMachine(content)
		#machines.append(Machine(content['name'], content['address'], content['timeout']))
	except KeyError:
		return "Error"
	if(result == 0):
		return "Already exist"
	else:
		WriteToConfig()
		return content['name']

def addMachine(machine):
	if(MachineAlreadyExist(machine['name'])):
		return 0
	else:
		machines.append(Machine(machine['name'], machine['address'], machine['timeout']))
		return 1

def MachineAlreadyExist(name):
	exist = False
	for machine in machines:
		if(machine.get_name() == name):
			exist = True
	return exist

def WriteToConfig():
	with open('config.json', 'w') as outfile:
		json.dump([ob.__dict__ for ob in machines], outfile)

app.run(host='0.0.0.0', port=81, debug=True)
