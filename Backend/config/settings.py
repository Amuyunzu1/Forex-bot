"""
Settings module for Hunter Bot.
Handles loading and validation of configuration.
"""

import os
import yaml
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def load_settings(config_path="config/settings.yaml"):
    """
    Load settings from YAML configuration file with environment variable support.
    
    Args:
        config_path (str): Path to the configuration file
        
    Returns:
        dict: Settings dictionary
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_file, 'r') as file:
        settings = yaml.safe_load(file)
    
    # Replace environment variable placeholders
    _process_env_vars(settings)
    
    # Validate required settings
    _validate_settings(settings)
    
    return settings


def load_trade_instructions(file_path="config/trade_instructions.json"):
    """
    Load trade instructions from JSON file.
    
    Args:
        file_path (str): Path to trade instructions file
        
    Returns:
        list: List of trade instruction dictionaries
    """
    instructions_file = Path(file_path)
    
    if not instructions_file.exists():
        return []
    
    with open(instructions_file, 'r') as file:
        instructions = json.load(file)
    
    # Validate trade instructions
    for instruction in instructions:
        _validate_trade_instruction(instruction)
    
    return instructions


def save_trade_instructions(instructions, file_path="config/trade_instructions.json"):
    """
    Save trade instructions to JSON file.
    
    Args:
        instructions (list): List of trade instruction dictionaries
        file_path (str): Path to save trade instructions
    """
    instructions_file = Path(file_path)
    instructions_file.parent.mkdir(exist_ok=True)
    
    with open(instructions_file, 'w') as file:
        json.dump(instructions, file, indent=2)


def _process_env_vars(config_dict):
    """
    Recursively process dictionary and replace ${ENV_VAR} with environment variable values.
    
    Args:
        config_dict (dict): Configuration dictionary to process
    """
    for key, value in config_dict.items():
        if isinstance(value, dict):
            _process_env_vars(value)
        elif isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            env_var = value[2:-1]
            env_value = os.environ.get(env_var)
            if env_value is not None:
                config_dict[key] = env_value
            else:
                raise ValueError(f"Environment variable not found: {env_var}")


def _validate_settings(settings):
    """
    Validate that all required settings are present.
    
    Args:
        settings (dict): Settings dictionary to validate
        
    Raises:
        ValueError: If required settings are missing
    """
    # Validate broker settings
    required_broker_settings = ["platform", "server", "login", "password"]
    if "broker" not in settings:
        raise ValueError("Broker settings are missing")
    
    for setting in required_broker_settings:
        if setting not in settings["broker"]:
            raise ValueError(f"Required broker setting missing: {setting}")
    
    # Validate other required settings
    if "general" not in settings:
        raise ValueError("General settings are missing")
    
    if "update_interval" not in settings["general"]:
        raise ValueError("Update interval setting is missing")


def _validate_trade_instruction(instruction):
    """
    Validate trade instruction format.
    
    Args:
        instruction (dict): Trade instruction to validate
        
    Raises:
        ValueError: If required fields are missing
    """
    required_fields = ["symbol", "entry_price", "exit_price", "stop_loss", "lot_size"]
    
    for field in required_fields:
        if field not in instruction:
            raise ValueError(f"Required trade instruction field missing: {field}")
    
    # Validate numeric fields
    for field in ["entry_price", "exit_price", "stop_loss", "lot_size"]:
        try:
            float(instruction[field])
        except (ValueError, TypeError):
            raise ValueError(f"Trade instruction field must be numeric: {field}")