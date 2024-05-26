
# Shop Project

## Overview

The Shop Project is a simulation game where players manage a sub shop. The game involves detailed inventory management, employee management, and customer interactions. The primary objective is to efficiently run the sub shop, making strategic decisions to maximize profit, customer satisfaction, and shop popularity.

## Features

- **Inventory Management**: Purchase ingredients, manage stock levels, and calculate costs.
- **Employee Management**: Hire and train employees to improve shop efficiency.
- **Customer Interaction**: Serve customers and manage orders.
- **Financial Tracking**: Track income, expenses, and overall financial health.
- **User Interface**: Interactive UI for a seamless gaming experience.

## Installation

### Prerequisites

- Python 3.8 or higher
- Pygame
- Required dependencies (listed in `requirements.txt`)

### Steps

1. Clone the repository:
    ```sh
    git clone https://github.com/DylanRayHastings/shop.git
    ```
2. Navigate to the project directory:
    ```sh
    cd shop
    ```
3. Create a virtual environment:
    ```sh
    python -m venv venv
    ```
4. Activate the virtual environment:
    - On Windows:
        ```sh
        venv\Scriptsctivate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```
5. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the main game script:
    ```sh
    python main.py
    ```
2. Use the interactive UI to manage your sub shop, including buying stock, hiring employees, and serving customers.

## Project Structure

```
shop/
│
├── assets/                   # Contains fonts and images used in the game
│   ├── Montserrat-Regular.ttf
│   ├── jm_background.png
│   └── jm_logo.png
│
├── data/                     # Contains game data files
│   └── ...
│
├── ui_elements/              # Contains UI-related Python scripts
│   └── ...
│
├── __pycache__/              # Contains Python bytecode files
│   └── ...
│
├── constants.py              # Defines game constants
├── data_handler.py           # Handles data operations
├── game_logic.py             # Contains game logic
├── main.py                   # Main entry point for the game
├── payroll.py                # Handles employee payroll calculations
├── customers.py              # Manages customer interactions
└── requirements.txt          # Lists required dependencies
```

## License

This project is licensed under The Unlicense

## Contact

For any questions or suggestions, feel free to contact me via GitHub.
