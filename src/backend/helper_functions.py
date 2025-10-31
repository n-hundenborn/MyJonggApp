import logging
from logging import getLogger, DEBUG


def setup_logger(logger_name: str, file_name: str = 'app.log', verbose: bool = True) -> logging.Logger:
    """Configure and return a logger that saves logs to a file.
    
    Args:
        logger_name: Name of the logger to create
        verbose: If True, includes timestamp and metadata. If False, logs only the message
        
    Returns:
        Configured logger instance
    """
    logger = getLogger(logger_name)
    logger.setLevel(DEBUG)

    # Create a file handler which logs even debug messages, overwriting old logs
    file_handler = logging.FileHandler(file_name, mode='w', encoding='utf-8')
    file_handler.setLevel(DEBUG)

    # Create console handler for simple logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(DEBUG)

    # Choose format based on verbose flag
    if verbose:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    else:
        formatter = logging.Formatter('%(message)s')

    # Apply formatters to handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def calculate_ranks(items, key_func=lambda x: x.points):
    """Calculate ranks for items, handling ties correctly (1,2,2,4).
    
    Args:
        items: Sequence of items to be ranked
        key_func: Function to extract the value to rank by (default: x.points)
    
    Returns:
        Dictionary mapping items to their ranks
    """
    # Create mapping of values to items
    value_to_items = {}
    for item in items:
        value = key_func(item)
        value_to_items.setdefault(value, []).append(item)
    
    # Sort unique values in descending order
    sorted_values = sorted(value_to_items.keys(), reverse=True)
    
    # Create rank mapping
    rank_map = {}
    current_rank = 1
    for value in sorted_values:
        # All items with same value get same rank
        items_at_this_value = value_to_items[value]
        for item in items_at_this_value:
            rank_map[item] = current_rank
        # Skip ranks based on how many items were tied
        current_rank += len(items_at_this_value)
    
    return rank_map
