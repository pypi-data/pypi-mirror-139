import re
from typing import Any, Dict, Iterable, List, Mapping, Tuple, Union

from templateco import (
    PluginOperationException,
    folders_to_template_decorator,
    get_questions_decorator,
    post_template_hook_decorator,
    pre_template_hook_decorator,
)

# Plugin configuration.
friendly_name = "Templateco Plugin"
compatible_languages = ["templateco"]
selected_by_default = True


def _parse_folder_to_templateco(folder: str) -> Tuple[str, ...]:
    """
    Parse the folder_name using regex, and determine if it can be used.

    Return a tuple containing the prefix and plugin name.
    If it cannot be parsed, raise a PluginOperationError which is fed up to the user.
    """
    parsed_folder = re.fullmatch(r"^([a-z]+)_([a-z_]*)_plugin$", folder)

    if not folder.islower():
        raise PluginOperationException("Folder name should be lower-case only")

    if "-" in folder:
        raise PluginOperationException(
            "Folder name should use underscores instead of dashes."
        )

    if not parsed_folder:
        raise PluginOperationException(
            'Please use proper format: "prefix_name_plugin" e.g. templateco_foo_plugin.'
        )

    return parsed_folder.groups()


def _validate_prefix_name(text: str) -> Union[str, bool]:
    """
    Validate that the entered prefix and name is lower-case letters only.

    :param text: Input string.
    :return: Questionary expected string or True.
    """
    if len(text) == 0:
        return "You must enter a value"
    elif not re.fullmatch(r"^([a-z_]+)$", text):
        return "You can only use lowercase characters and underscores"
    return True


def _validate_comma_separated_entries(text: str) -> Union[str, bool]:
    """
    Validate that the input is lowercase letters or commas only.

    :param text: Input string.
    :return: Questionary expected string or True.
    """
    if len(text) == 0:
        return "You must enter a value"
    elif not re.fullmatch(r"^([a-z,]+)$", text):
        return "You can only enter lower-case letters and commas. No spaces allowed."
    return True


def _validate_not_empty(text: str) -> Union[str, bool]:
    """
    Validate that the input string is not empty.

    :param text: Input string.
    :return: Questionary expected string or True.
    """
    if len(text) == 0:
        return "You must enter a value"
    return True


@get_questions_decorator
def get_questions(folder: str, **_: Any) -> Iterable[Mapping[str, Any]]:
    """
    Query the user for how the plugin will work.
    """
    (prefix, name) = _parse_folder_to_templateco(folder)

    return [
        {
            "type": "text",
            "name": "prefix",
            "message": "Templateco Prefix",
            "default": prefix,
            "validate": _validate_prefix_name,
        },
        {
            "type": "text",
            "name": "name",
            "message": "Plugin name",
            "default": name,
            "validate": _validate_prefix_name,
        },
        {
            "type": "text",
            "name": "cs_templates",
            "message": "Comma separated list of templates",
            "validate": _validate_comma_separated_entries,
        },
        {
            "type": "confirm",
            "message": "Do you want to use a sub-folder for your package?",
            "name": "use_subfolder",
            "default": True,
        },
        {
            "type": "select",
            "name": "package_manager",
            "message": "Select Package Manager:",
            "choices": ["None", "Poetry"],
        },
        {
            "type": "confirm",
            "message": "Do you want to add tooling to this folder?",
            "name": "tooling",
            "default": True,
            "when": lambda x: x["package_manager"] == "Poetry",
        },
        {
            "type": "text",
            "name": "author_name",
            "message": "Package Author Name",
            "when": lambda x: x["package_manager"] == "Poetry",
            "validate": _validate_not_empty,
        },
        {
            "type": "text",
            "name": "author_email",
            "message": "Package Author Email",
            "when": lambda x: x["package_manager"] == "Poetry",
            "validate": _validate_not_empty,
        },
    ]


@pre_template_hook_decorator
def pre_template_hook(data: Dict[str, Any], **_: Any) -> None:
    """
    Convert the cs_templates variable into a Python list.
    """
    data["templates"] = data["cs_templates"].replace(",", '", "')


@folders_to_template_decorator
def folders_to_template(data: Dict[str, Any], **_: Any) -> List[str]:
    """
    Determine which folders to template.

    By default, always return the "template" folder.
    If Poetry is selected, append that.
    """
    templates = ["template"]

    if data["package_manager"] == "Poetry":
        templates.append("poetry")

    return templates


@post_template_hook_decorator
def post_template_hook(**_: Any) -> None:
    """
    Run some code after it has been templated.
    """
    pass
