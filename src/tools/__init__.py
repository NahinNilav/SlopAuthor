"""
Tools module for SlopAuthor.
Exports all available tools for the agent to use.
"""

from .writer import write_file_impl
from .project import create_project_impl, set_project_template, get_project_template
from .compression import compress_context_impl
from .templates import (
    list_templates_impl,
    apply_template_impl,
    get_template_manager,
    get_template_guidelines,
    get_template_variables,
    TemplateManager,
    Template,
)

__all__ = [
    'write_file_impl',
    'create_project_impl',
    'set_project_template',
    'get_project_template',
    'compress_context_impl',
    'list_templates_impl',
    'apply_template_impl',
    'get_template_manager',
    'get_template_guidelines',
    'get_template_variables',
    'TemplateManager',
    'Template',
]

