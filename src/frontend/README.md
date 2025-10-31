# Frontend Structure

This directory contains all frontend-related code for the MyJongApp application.

## Directory Structure

```
frontend/
├── components/           # Reusable UI components
│   ├── buttons.py       # Button components
│   ├── inputs.py        # Input components
│   ├── cards.py         # Card components
│   └── popups.py        # Popup components
├── screens/             # Screen components
│   └── ...             # Individual screen files
└── shared/             # Shared code
    ├── styles.py        # Styling code
    ├── config.py        # Constants and configuration
    └── utils.py         # Utility functions
```

## Components

The `components` directory contains reusable UI components that are used across different screens:
- `buttons.py`: Button components with consistent styling
- `inputs.py`: Input field components with consistent styling
- `cards.py`: Card container components
- `popups.py`: Popup components like error messages

## Screens

The `screens` directory contains all screen components, each in its own file. Each screen is a self-contained component that represents a full page in the application.

## Shared

The `shared` directory contains code that is used across multiple components and screens:
- `styles.py`: All styling-related code including colors, fonts, and component styles
- `config.py`: Application-wide constants and configuration
- `utils.py`: Shared utility functions
