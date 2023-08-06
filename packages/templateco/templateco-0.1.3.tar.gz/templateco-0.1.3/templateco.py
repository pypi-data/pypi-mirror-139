import logging
from pathlib import Path
from typing import List

from colorama import Fore, Style, init
from questionary import Choice, checkbox, unsafe_prompt

from templateco.exceptions import NoPluginsFoundException, PluginOperationException
from templateco.output import generate_output
from templateco.plugin import TemplatecoPlugin, list_compatible_plugins

logger = logging.getLogger(__name__)


def _execute_plugin(
    template: str, output_folder: str, plugin: TemplatecoPlugin
) -> None:
    """
    Execute a single Templateco plugin.

    This function prompts for the plugin's questions, runs the hooks and generates
    the template files.

    :param template:
    :param output_folder: Folder to output to.
    :param plugin: Plugin to execute.
    :return: None.
    """
    logger.debug(f"[{plugin.friendly_name}] Running plugin.")
    try:
        folder_name = Path(output_folder).name
        logger.debug(f"[{plugin.friendly_name}] Prompting for interaction.")

        data = unsafe_prompt(
            plugin.get_questions(template=template, folder_name=folder_name)
        )

        if plugin.pre_template_hook:
            logger.debug(f"[{plugin.friendly_name}] Running pre-template hook.")
            plugin.pre_template_hook(
                template=template, folder_name=folder_name, data=data
            )

        logger.debug(f"[{plugin.friendly_name}] Determining template from answers.")
        folders = plugin.folders_to_template(
            template=template, folder_name=folder_name, data=data
        )

        logger.debug(f"[{plugin.friendly_name}] Templating folder structure.")
        generate_output(plugin.path_to_module, Path() / output_folder, folders, data)
        logger.debug(f"[{plugin.friendly_name}] Successfully templated.")

        if plugin.post_template_hook:
            logger.debug(f"[{plugin.friendly_name}] Running post-template hook.")
            plugin.post_template_hook(
                template=template,
                folder_name=folder_name,
                output_folder=Path() / output_folder,
                data=data,
            )
    except PluginOperationException:
        logger.error(f"[{plugin.friendly_name}] Plugin raised Operation Exception.")
        logger.debug(
            f"[{plugin.friendly_name}] These exceptions should be raised to the user."
        )
        raise
    except Exception as err:
        logger.error(f"[{plugin.friendly_name}] Plugin raised an unhandled exception.")
        logger.error(err)


def templateco(
    template: str,
    output_folder: str,
    namespaces: List[str] = ["templateco"],
) -> None:
    """
    Execute Templateco, and produce a templated folder.

    :param template: Name of template to load plugins for.
    :param output_folder: Folder to generate e.g. $(PWD)/output_folder.
    :param namespaces: List of Templateco plugin namespaces to accept.
    :return: None.
    """
    # Initialise Colorama.
    init(autoreset=True)
    print(
        Fore.GREEN
        + Style.BRIGHT
        + "[ Templateco ]"
        + Style.RESET_ALL
        + " - A Templating Ecosystem"
    )

    logger.debug("Instantiating Templateco.")

    # Get a complete list of all compatible Templateco plugins.
    plugins = [
        plugin
        for plugin in list_compatible_plugins(namespaces)
        if template in plugin.compatible_templates
    ]

    logger.debug(f"Found {len(plugins)} plugin(s).")

    if len(plugins) == 0:
        logger.debug("Query resulted in zero plugins, raising NoPlugins exception.")
        raise NoPluginsFoundException()
    elif len(plugins) > 1:
        logger.debug("Multiple plugins found, asking user for choices.")
        # Ask the user which plugins should be executed.
        plugins = checkbox(
            "Select plugins to use",
            choices=[
                Choice(
                    plugin.friendly_name,
                    checked=plugin.selected_by_default,
                    value=plugin,
                )
                for plugin in plugins
            ],
        ).unsafe_ask()

    for plugin in plugins:
        print("\nConfiguring " + Fore.GREEN + Style.BRIGHT + f"{plugin.friendly_name}")
        _execute_plugin(template, output_folder, plugin)

    print("\nSuccessfully templated " + Style.BRIGHT + Fore.GREEN + output_folder)
