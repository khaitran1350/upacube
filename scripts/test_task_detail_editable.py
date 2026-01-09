import sys
sys.path.append(r'd:\src\upacube')
from PyQt6.QtWidgets import QApplication
from views.task_detail_dialog import TaskDetailDialog

app = QApplication([])
# Simulate a completed task
data = {'title': 'Done Task', 'description': 'Already finished', 'deadline': None, 'priority': 'Normal', 'completed': True, 'index': 1}
dlg = TaskDetailDialog(None, task_data=data)
# Check if edit button is enabled
print('edit_enabled:', dlg.edit_btn.isEnabled())
app.quit()

