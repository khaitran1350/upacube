# PyQt MVC Project

This is a PyQt6 application structured using the MVC (Model-View-Controller) pattern.

## Project Structure

```
upacube/
│
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
│
├── models/                 # Data models and business logic
│   ├── __init__.py
│   └── data_model.py      # Example data model
│
├── views/                  # UI components
│   ├── __init__.py
│   └── main_view.py       # Main window view
│
└── controllers/            # Application logic
    ├── __init__.py
    └── main_controller.py # Main controller
```

## MVC Architecture

### Model (`models/`)
- Contains data and business logic
- Independent of the UI
- Emits signals when data changes
- Example: `DataModel` class manages application data

### View (`views/`)
- Contains UI components and layout
- Displays data from the model
- Emits signals for user actions
- Should NOT contain business logic
- Example: `MainView` class with Qt widgets

### Controller (`controllers/`)
- Connects Model and View
- Handles user input from View
- Updates Model based on user actions
- Updates View when Model changes
- Contains application logic
- Example: `MainController` class

## Installation

1. Create a virtual environment (if not already created):
   ```powershell
   python -m venv .venv
   ```

2. Activate the virtual environment:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```

3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Running the Application

```powershell
python main.py
```

## How It Works

1. **main.py** creates instances of Model, View, and Controller
2. **Controller** connects View signals to methods that update the Model
3. **Controller** connects Model signals to methods that update the View
4. When user interacts with the **View**, signals are emitted
5. **Controller** receives signals and updates the **Model**
6. **Model** emits signals when data changes
7. **Controller** updates the **View** to reflect changes

## Benefits of MVC Pattern

- **Separation of Concerns**: UI, data, and logic are separated
- **Maintainability**: Easy to modify each component independently
- **Testability**: Can test Model and Controller without UI
- **Reusability**: Models can be used with different Views
- **Scalability**: Easy to add new features

## Extending the Application

### Adding a New Model
1. Create a new file in `models/` directory
2. Inherit from `QObject` to use signals/slots
3. Define properties and methods for data management
4. Emit signals when data changes

### Adding a New View
1. Create a new file in `views/` directory
2. Inherit from appropriate Qt widget class
3. Define UI components in `init_ui()` method
4. Define signals for user actions

### Adding a New Controller
1. Create a new file in `controllers/` directory
2. Accept model and view in `__init__()`
3. Connect view signals to controller methods
4. Connect model signals to view updates
5. Implement business logic methods

## Example Usage

The provided example demonstrates:
- Text input and submission
- List management
- Status logging
- Button interactions
- Data synchronization between Model and View

Feel free to modify and extend this structure for your specific needs!

