"""
Test script to verify all imports work correctly
"""
import sys
print("Testing PyQt MVC imports...")

try:
    from PyQt6.QtWidgets import QApplication
    print("✓ PyQt6.QtWidgets imported successfully")
except ImportError as e:
    print(f"✗ Failed to import PyQt6.QtWidgets: {e}")
    sys.exit(1)

try:
    from models.data_model import DataModel
    print("✓ DataModel imported successfully")
except ImportError as e:
    print(f"✗ Failed to import DataModel: {e}")
    sys.exit(1)

try:
    from views.main_view import MainView
    print("✓ MainView imported successfully")
except ImportError as e:
    print(f"✗ Failed to import MainView: {e}")
    sys.exit(1)

try:
    from controllers.main_controller import MainController
    print("✓ MainController imported successfully")
except ImportError as e:
    print(f"✗ Failed to import MainController: {e}")
    sys.exit(1)

print("\n✓ All imports successful!")
print("\nTesting MVC instantiation...")

try:
    # Don't create QApplication in test to avoid GUI
    model = DataModel()
    print("✓ DataModel instantiated")

    # Test model functionality
    model.data = "test"
    assert model.data == "test", "Data property failed"
    print("✓ DataModel.data property works")

    model.add_item("item1")
    assert len(model.get_items()) == 1, "add_item failed"
    print("✓ DataModel.add_item works")

    model.clear_items()
    assert len(model.get_items()) == 0, "clear_items failed"
    print("✓ DataModel.clear_items works")

    print("\n✅ All tests passed! Your PyQt MVC project is ready to run.")
    print("\nTo run the application:")
    print("  python main.py")

except Exception as e:
    print(f"✗ Error during testing: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

