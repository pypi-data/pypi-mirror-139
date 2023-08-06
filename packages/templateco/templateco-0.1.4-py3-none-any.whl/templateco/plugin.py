import logging
from dataclasses import dataclass
from functools import lru_cache
from importlib import import_module
from pathlib import Path
from typing import Generator, Iterable, List, Optional

from importlib_metadata import Distribution, distributions

from templateco.exceptions import IncompatiblePluginException
from templateco.typing import (
    FoldersToTemplate,
    GetQuestions,
    PostTemplateHook,
    PreTemplateHook,
)

logger = logging.getLogger(__name__)


@dataclass
class TemplatecoPlugin:
    """
    Templateco Plugin.
    """

    friendly_name: str
    path_to_module: Path
    compatible_languages: List[str]
    selected_by_default: bool
    get_questions: GetQuestions
    folders_to_template: FoldersToTemplate
    pre_template_hook: Optional[PreTemplateHook]
    post_template_hook: Optional[PostTemplateHook]


@lru_cache(maxsize=None)
def import_templateco_plugin(name: str) -> TemplatecoPlugin:
    """
    Import a compatible Templateco package, and return a TemplatecoPlugin.

    :param name: Name of Python package.
    :return: Templateco Plugin.
    """
    module = import_module(name.replace("-", "_"))

    try:
        return TemplatecoPlugin(
            friendly_name=module.__dict__["friendly_name"],
            path_to_module=Path(str(module.__file__)).parent,
            compatible_languages=module.__dict__["compatible_languages"],
            selected_by_default=module.__dict__.get("selected_by_default", False),
            get_questions=module.__dict__["get_questions"],
            folders_to_template=module.__dict__["folders_to_template"],
            pre_template_hook=module.__dict__.get("pre_template_hook", None),
            post_template_hook=module.__dict__.get("post_template_hook", None),
        )
    except KeyError as err:
        logger.debug(f"[{name}] Failed to parse plugin information.")
        logger.debug(err)
        raise IncompatiblePluginException(err)


def list_compatible_plugins(
    namespaces: List[str],
) -> Generator[TemplatecoPlugin, None, None]:
    """
    Return a list of compatible Templateco plugins.

    :param namespaces: List of Templateco plugin namespaces to accept.
    :return: List of Templateco plugins.
    """
    logger.debug("Getting list of Python distributions.")

    installed_distributions: Iterable[Distribution] = distributions()  # type: ignore

    for distribution in installed_distributions:
        if "-" in distribution.name:
            split_package = distribution.name.split("-")
            if split_package[0] in namespaces and distribution.name[-6:] == "plugin":
                logger.debug(f"[{distribution.name}] Found potential plugin.")
                try:
                    yield import_templateco_plugin(distribution.name)
                    logger.debug(f"[{distribution.name}] Successfully loaded plugin.")
                except IncompatiblePluginException:
                    logger.debug(f"[{distribution.name}] Plugin incompatible.")
