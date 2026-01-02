"""
Project folder management tool.
"""

import os
import re
from typing import Optional


# Global variable to track the active project folder
_active_project_folder: Optional[str] = None

# Global variable to track the selected template for the project
_active_project_template: Optional[str] = None


def sanitize_folder_name(name: str) -> str:
    """
    Sanitizes a folder name for filesystem compatibility.
    
    Args:
        name: The proposed folder name
        
    Returns:
        Sanitized folder name
    """
    # Replace spaces with underscores
    name = name.strip().replace(' ', '_')
    # Remove any characters that aren't alphanumeric, underscore, or hyphen
    name = re.sub(r'[^\w\-]', '', name)
    # Remove leading/trailing hyphens or underscores
    name = name.strip('-_')
    # Ensure it's not empty
    if not name:
        name = "untitled_project"
    return name


def get_active_project_folder() -> Optional[str]:
    """
    Returns the currently active project folder path.
    
    Returns:
        Path to active project folder or None if not set
    """
    return _active_project_folder


def set_active_project_folder(folder_path: str) -> None:
    """
    Sets the active project folder.
    
    Args:
        folder_path: Path to the project folder
    """
    global _active_project_folder
    _active_project_folder = folder_path


def set_project_template(template_name: Optional[str]) -> None:
    """
    Sets the template to use for the project.
    
    Args:
        template_name: Name of the template or None
    """
    global _active_project_template
    _active_project_template = template_name


def get_project_template() -> Optional[str]:
    """
    Gets the currently selected project template.
    
    Returns:
        Template name or None if not set
    """
    return _active_project_template


def create_project_impl(project_name: str, template: Optional[str] = None) -> str:
    """
    Creates a new project folder in the output directory.
    Optionally applies a template to the project.
    
    Args:
        project_name: The desired project name
        template: Optional template name to apply
        
    Returns:
        Success message with folder path or error message
    """
    global _active_project_folder, _active_project_template
    
    # Use the globally set template if not provided
    if template is None:
        template = _active_project_template
    
    # Sanitize the folder name
    sanitized_name = sanitize_folder_name(project_name)
    
    # Get the project root directory (go up from src/tools/ to root)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(os.path.dirname(script_dir))  # Go up from src/tools/ to root
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(root_dir, "output")
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            return f"Error creating output directory: {str(e)}"
    
    # Create the full path inside output directory
    project_path = os.path.join(output_dir, sanitized_name)
    
    # Check if folder already exists
    folder_existed = os.path.exists(project_path)
    
    if not folder_existed:
        # Create the folder
        try:
            os.makedirs(project_path, exist_ok=True)
        except Exception as e:
            return f"Error creating project folder: {str(e)}"
    
    _active_project_folder = project_path
    
    # Apply template if specified
    template_message = ""
    if template:
        from .templates import apply_template_impl
        template_result = apply_template_impl(project_path, template)
        template_message = f"\n{template_result}"
    
    if folder_existed:
        return f"Project folder already exists at '{project_path}'. Set as active project folder.{template_message}"
    else:
        return f"Successfully created project folder at '{project_path}'. This is now the active project folder.{template_message}"

