"""
Quick verification script
"""
import sys

print("=" * 50)
print("PyQt MVC Project Verification")
print("=" * 50)

# Test 1: PyQt6
try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import QObject, pyqtSignal
    print("[OK] PyQt6 installed and importable")
except ImportError as e:
    print(f"[FAIL] PyQt6 import failed: {e}")
    sys.exit(1)

# Test 2: Model
try:
    from models.data_model import DataModel
    model = DataModel()
    model.data = "test data"
    assert model.data == "test data"
    # adapt to new API: add_task
    model.add_task("item1")
    assert model.get_task_count() == 1
    print("[OK] DataModel works correctly")
except Exception as e:
    print(f"[FAIL] DataModel failed: {e}")
    sys.exit(1)

# Test 3: View
try:
    from views.main_view import MainView
    print("[OK] MainView importable")
except Exception as e:
    print(f"[FAIL] MainView failed: {e}")
    sys.exit(1)

# Test 4: Controller
try:
    from controllers.main_controller import MainController
    print("[OK] MainController importable")
except Exception as e:
    print(f"[FAIL] MainController failed: {e}")
    sys.exit(1)

print("\n" + "=" * 50)
print("ALL TESTS PASSED")
print("=" * 50)
print("\nYour PyQt MVC project is ready!")
print("\nTo run the application:")
print("  python main.py")
print("\nOr press F5/Run in PyCharm")
print("=" * 50)
