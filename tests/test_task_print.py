from models.data_model import DataModel

m = DataModel()
print('Loaded tasks count:', m.get_task_count())
for t in m.get_tasks():
    if hasattr(t, 'get'):
        completed = t.get('completed')
        title = t.get('title')
        tid = t.get('id')
    else:
        completed = getattr(t, 'completed', False)
        title = getattr(t, 'title', str(t))
        tid = getattr(t, 'id', None)
    print(f"{tid}: [{'x' if completed else ' '}] {title}")

