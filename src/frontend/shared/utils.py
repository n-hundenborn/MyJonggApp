"""
Shared utility functions for the frontend.
"""

def get_screen_name(screen_class):
    """Convert a screen class name to a screen name.
    Example: AddPointsScreen -> add_points_screen
    """
    name = screen_class.__name__
    return ''.join(['_' + c.lower() if c.isupper() else c for c in name])[1:]
