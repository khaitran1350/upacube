import sys, os
# ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.data_model import DataModel

m = DataModel()
print('Loaded', len(m.get_tasks()), 'tasks')
new = {'title':'Detailed task','description':'A full-featured task','deadline':'2026-01-10','priority':'High'}
t = m.add_task(new)
print('Added:', t.to_dict())
print('All tasks:')
for i,task in enumerate(m.get_tasks()):
    print(i, task.to_dict())

