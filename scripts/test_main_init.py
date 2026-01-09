import sys
sys.path.append(r'd:\src\upacube')
from PyQt6.QtWidgets import QApplication
from views.main_view import MainView

app = QApplication([])
mv = MainView()
print('MainView OK')
app.quit()

