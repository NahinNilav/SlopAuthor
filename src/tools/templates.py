"""
Template management for SlopAuthor.
Provides functionality to list, load, and apply project templates.
"""

import os
import json
import shutil
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class Template:
    """Represents a project template."""
    name: str
    description: str
    category: str
    path: str
    files: List[Dict[str, str]] = field(default_factory=list)
    variables: Dict[str, Any] = field(default_factory=dict)
    writing_guidelines: str = ""
    default_structure: Dict[str, Any] = field(default_factory=dict)
    
    def __str__(self) -> str:
        return f"{self.name} ({self.category}): {self.description}"


class TemplateManager:
    """Manages project templates for the writing agent."""
    
    def __init__(self, templates_dir: Optional[str] = None):
        """
        Initialize the template manager.
        
        Args:
            templates_dir: Path to templates directory. If None, uses default location.
        """
        if templates_dir is None:
            # Default to templates/ in the project root
            self.templates_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                "templates"
            )
        else:
            self.templates_dir = templates_dir
        
        self._templates_cache: Dict[str, Template] = {}
    
    def get_templates_dir(self) -> str:
        """Returns the templates directory path."""
        return self.templates_dir
    
    def list_templates(self) -> List[Template]:
        """
        List all available templates.
        
        Returns:
            List of Template objects
        """
        templates = []
        
        if not os.path.exists(self.templates_dir):
            return templates
        
        for item in os.listdir(self.templates_dir):
            template_path = os.path.join(self.templates_dir, item)
            if os.path.isdir(template_path):
                template = self.load_template(item)
                if template:
                    templates.append(template)
        
        return sorted(templates, key=lambda t: t.name)
    
    def load_template(self, template_name: str) -> Optional[Template]:
        """
        Load a template by name.
        
        Args:
            template_name: Name of the template (folder name)
            
        Returns:
            Template object or None if not found
        """
        # Check cache first
        if template_name in self._templates_cache:
            return self._templates_cache[template_name]
        
        template_path = os.path.join(self.templates_dir, template_name)
        config_path = os.path.join(template_path, "template.json")
        
        if not os.path.exists(config_path):
            return None
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            template = Template(
                name=config.get("name", template_name),
                description=config.get("description", ""),
                category=config.get("category", "general"),
                path=template_path,
                files=config.get("files", []),
                variables=config.get("variables", {}),
                writing_guidelines=config.get("writing_guidelines", ""),
                default_structure=config.get("default_structure", {})
            )
            
            # Cache the template
            self._templates_cache[template_name] = template
            
            return template
            
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load template '{template_name}': {e}")
            return None
    
    def get_template_by_name(self, name: str) -> Optional[Template]:
        """
        Find a template by its display name or folder name.
        
        Args:
            name: Template name (case-insensitive)
            
        Returns:
            Template object or None if not found
        """
        name_lower = name.lower().replace(" ", "_").replace("-", "_")
        
        # Try direct folder name match first
        template = self.load_template(name_lower)
        if template:
            return template
        
        # Search all templates by display name
        for template in self.list_templates():
            if template.name.lower() == name.lower():
                return template
            if template.name.lower().replace(" ", "_") == name_lower:
                return template
        
        return None
    
    def apply_template(
        self, 
        project_path: str, 
        template: Template,
        variables: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Apply a template to a project folder.
        
        Args:
            project_path: Path to the project folder
            template: Template to apply
            variables: Variable values to substitute in templates
            
        Returns:
            Dictionary with results including created files and any errors
        """
        results = {
            "success": True,
            "files_created": [],
            "errors": [],
            "template_name": template.name,
            "writing_guidelines": template.writing_guidelines
        }
        
        # Merge provided variables with defaults
        final_variables = {}
        for var_name, var_config in template.variables.items():
            if isinstance(var_config, dict):
                final_variables[var_name] = var_config.get("default", "")
            else:
                final_variables[var_name] = var_config
        
        if variables:
            final_variables.update(variables)
        
        # Create each file from the template
        for file_config in template.files:
            file_name = file_config.get("name", "")
            template_file = file_config.get("template", "")
            
            if not file_name or not template_file:
                continue
            
            # Substitute variables in filename
            file_name = self._substitute_variables(file_name, final_variables)
            
            template_file_path = os.path.join(template.path, template_file)
            output_file_path = os.path.join(project_path, file_name)
            
            try:
                if os.path.exists(template_file_path):
                    with open(template_file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Substitute variables in content
                    content = self._substitute_variables(content, final_variables)
                    
                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    results["files_created"].append(file_name)
                else:
                    results["errors"].append(f"Template file not found: {template_file}")
                    
            except Exception as e:
                results["errors"].append(f"Error creating {file_name}: {str(e)}")
                results["success"] = False
        
        return results
    
    def _substitute_variables(self, text: str, variables: Dict[str, str]) -> str:
        """
        Substitute variables in text using {variable_name} format.
        
        Args:
            text: Text containing variable placeholders
            variables: Dictionary of variable values
            
        Returns:
            Text with variables substituted
        """
        for var_name, var_value in variables.items():
            placeholder = "{" + var_name + "}"
            text = text.replace(placeholder, str(var_value))
        
        return text
    
    def get_template_info(self, template_name: str) -> Optional[str]:
        """
        Get formatted information about a template.
        
        Args:
            template_name: Name of the template
            
        Returns:
            Formatted string with template info or None
        """
        template = self.get_template_by_name(template_name)
        if not template:
            return None
        
        info_lines = [
            f"📁 Template: {template.name}",
            f"   Category: {template.category}",
            f"   Description: {template.description}",
            "",
            "   Files included:"
        ]
        
        for file_config in template.files:
            file_name = file_config.get("name", "")
            file_desc = file_config.get("description", "")
            info_lines.append(f"   • {file_name} - {file_desc}")
        
        if template.writing_guidelines:
            info_lines.extend([
                "",
                "   Writing Guidelines:",
                f"   {template.writing_guidelines}"
            ])
        
        return "\n".join(info_lines)


# Module-level instance for convenience
_template_manager: Optional[TemplateManager] = None


def get_template_manager() -> TemplateManager:
    """Get or create the global template manager instance."""
    global _template_manager
    if _template_manager is None:
        _template_manager = TemplateManager()
    return _template_manager


def list_templates_impl() -> str:
    """
    List all available templates.
    
    Returns:
        Formatted string listing all templates
    """
    manager = get_template_manager()
    templates = manager.list_templates()
    
    if not templates:
        return "No templates found. Check if the templates/ directory exists."
    
    lines = [
        "📚 Available Templates:",
        "=" * 50,
        ""
    ]
    
    # Group by category
    categories: Dict[str, List[Template]] = {}
    for template in templates:
        cat = template.category.title()
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(template)
    
    for category, cat_templates in sorted(categories.items()):
        lines.append(f"### {category}")
        lines.append("")
        for template in cat_templates:
            lines.append(f"  • **{template.name}**")
            lines.append(f"    {template.description}")
            lines.append("")
        lines.append("")
    
    lines.extend([
        "=" * 50,
        "Use --template <name> to start with a template",
    ])
    
    return "\n".join(lines)


def apply_template_impl(
    project_path: str,
    template_name: str,
    variables: Optional[Dict[str, str]] = None
) -> str:
    """
    Apply a template to a project.
    
    Args:
        project_path: Path to the project folder
        template_name: Name of the template to apply
        variables: Optional variable overrides
        
    Returns:
        Success or error message
    """
    manager = get_template_manager()
    template = manager.get_template_by_name(template_name)
    
    if not template:
        available = manager.list_templates()
        available_names = ", ".join(t.name for t in available)
        return f"Template '{template_name}' not found. Available templates: {available_names}"
    
    results = manager.apply_template(project_path, template, variables)
    
    if results["success"]:
        files_list = ", ".join(results["files_created"])
        message = f"✓ Applied template '{template.name}' to project.\n"
        message += f"  Created files: {files_list}\n"
        
        if results["writing_guidelines"]:
            message += f"\n📝 Writing Guidelines:\n{results['writing_guidelines']}"
        
        return message
    else:
        errors = "; ".join(results["errors"])
        return f"✗ Error applying template: {errors}"


def get_template_guidelines(template_name: str) -> Optional[str]:
    """
    Get the writing guidelines for a specific template.
    
    Args:
        template_name: Name of the template
        
    Returns:
        Writing guidelines string or None
    """
    manager = get_template_manager()
    template = manager.get_template_by_name(template_name)
    
    if template:
        return template.writing_guidelines
    return None


def get_template_variables(template_name: str) -> Dict[str, Any]:
    """
    Get the variables defined for a template.
    
    Args:
        template_name: Name of the template
        
    Returns:
        Dictionary of variable configurations
    """
    manager = get_template_manager()
    template = manager.get_template_by_name(template_name)
    
    if template:
        return template.variables
    return {}
