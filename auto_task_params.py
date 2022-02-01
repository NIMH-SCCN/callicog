from os import listdir
from os.path import isfile, join
from database import DatabaseSession
from marmobox_schema import ProtocolParameter, Protocol

db = DatabaseSession()
mypath = './tasks'
task_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for task_filename in task_files:
	task_name = task_filename.split('.')[0]
	if task_name != 'blabla':
		try:
			mod = __import__(f'tasks.{task_name}', fromlist=['TaskInterface'])
			task_interface = getattr(mod, 'TaskInterface')()
			task_interface.generate_trials()
		except:
			print(f'bad format: {task_name}')
			continue

		protocols = db.query(Protocol).filter(Protocol.protocol_name == task_name).all()
		if len(protocols) > 0:
			protocol = protocols[0]
			task_parameters = task_interface.pseudorandom_parameters
			for key in task_parameters:
				if task_parameters[key]['pseudorandom']:
					protocol_parameter = ProtocolParameter(protocol=protocol, parameter_name=key)
					db.add(protocol_parameter)
					print(f'added for task({task_name}), param({key})')

db.commit()
print('migration finished')
