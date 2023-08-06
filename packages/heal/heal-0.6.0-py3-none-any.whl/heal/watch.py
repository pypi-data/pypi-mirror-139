import json
import subprocess
from operator import itemgetter
from pathlib import Path
from typing import List, Any, Tuple

import yaml

from heal.util import ENCODING


def read_config(directory: Path) -> List[Any]:
    """
    Extracts every JSON or YAML configuration element from the files in the given directory.

    :param directory: Path to the configuration directory
    :return: aggregated list of configuration elements
    """

    print("reading configuration")
    config = []

    for path in directory.iterdir():
        try:
            text = path.read_text(encoding=ENCODING)
        except (OSError, ValueError) as error:
            print(f"'{path.relative_to(directory)}' ignored: {error}")
            continue

        data = yaml.load(text, Loader=yaml.BaseLoader)
        if not isinstance(data, list):
            print(f"'{path.relative_to(directory)}' ignored: not a proper yaml or json list")
        else:
            config.extend(data)

    return config


def filter_modes_and_checks(config: List[Any]) -> Tuple[List[dict], List[dict]]:
    """
    Validates and splits the given configuration elements into modes and checks.

    :param config: list of configuration elements
    :return: two sorted lists, one of modes and one of checks
    """

    print("filtering modes and checks")
    modes, checks = [], []

    for item in config:
        if not isinstance(item, dict):
            print("ignored, not a dictionary:", json.dumps(item))
            continue

        try:
            keys = item.keys()
            if keys == {"mode", "if", "order"}:  # "mode", "if" and "order" are mandatory for modes
                item["order"] = int(item["order"])  # raises ValueError or TypeError below
                if any(not isinstance(item[key], str) for key in ["mode", "if"]):
                    print('ignored, values for "mode" and "if" can only be strings:', json.dumps(item))
                else:
                    modes.append(item)
            elif keys == {"check", "fix", "order"} or keys == {"check", "fix", "order", "when"}:  # "check", "fix" and "order" are mandatory for checks, "when" is optional
                item["order"] = int(item["order"])  # raises ValueError or TypeError below
                if "when" in keys and isinstance(item["when"], str):  # a single mode as a string is tolerated, but converted into a list for technical purposes
                    item["when"] = [item["when"]]
                if "when" in keys and (not isinstance(item["when"], list) or any(not isinstance(value, str) for value in item["when"])):
                    print('ignored, value for "when" can only be a string or a list of strings:', json.dumps(item))
                elif any(not isinstance(item[key], str) for key in ["check", "fix"]):
                    print('ignored, values for "check" and "fix" can only be strings:', json.dumps(item))
                else:
                    checks.append(item)
            else:
                print('ignored, keys must match {"mode", "if", "order"} or {"check", "fix", "order"} or {"check", "fix", "order", "when"}:', json.dumps(item))
        except (ValueError, TypeError):
            print('ignored, value for "order" can only be an integer:', json.dumps(item))

    return sorted(modes, key=itemgetter("order")), sorted(checks, key=itemgetter("order"))  # modes and checks are sorted by order


def get_active_mode(modes: List[dict]) -> str:
    """
    Executes the given modes' condition one after the other and returns the name of the first one that succeeds, or a "default" mode.

    :param modes: ordered list of available modes
    :return: the name of the first mode whose condition executed successfully, or "default"
    """

    for mode in modes:
        if subprocess.run(mode.get("if"), shell=True).returncode == 0:
            return mode.get("mode")
    return "default"


def filter_active_checks(active_mode: str, checks: List[dict]) -> List[dict]:
    """
    :param active_mode: name of the active mode
    :param checks: list of available checks
    :return: the list of active checks, i.e. checks without any mode or whose modes include the active one
    """

    print("filtering active checks")
    active_checks = []

    for check in checks:
        if not check.get("when") or active_mode in check.get("when"):
            print("active:", json.dumps(check))
            active_checks.append(check)

    return active_checks


class Watcher:
    """
    Will watch over the given configuration directory and monitor possible changes:

    * directory timestamp
    * checks
    * active mode
    * active checks

    :param configuration_directory: obviously
    """

    def __init__(self, configuration_directory: Path):
        self.configuration_directory = configuration_directory
        self.mtime = 0
        self.modes = []
        self.checks = []
        self.active_mode = "default"
        self.active_checks = []

    def configuration_directory_has_changed(self) -> bool:
        """
        :return: whether or not the configuration directory has changed since last call
        """

        # monitoring the directory modification timestamp doesn't cover every possible file change but it's very cheap
        new_mtime = self.configuration_directory.stat().st_mtime
        if new_mtime == self.mtime:
            return False
        print("configuration directory has changed")
        self.mtime = new_mtime
        return True

    def checks_have_changed(self) -> bool:
        """
        :return: whether or not the checks have changed since last call
        """

        # caution: here modes are refreshed as a prerequisite for monitoring the active modes
        self.modes, new_checks = filter_modes_and_checks(read_config(self.configuration_directory))
        if new_checks == self.checks:
            return False
        print("checks have changed")
        self.checks = new_checks
        return True

    def active_mode_has_changed(self) -> bool:
        """
        :return: whether or not the active mode has changed since last call
        """

        new_active_mode = get_active_mode(self.modes)
        if new_active_mode == self.active_mode:
            return False
        print("active mode has changed:", new_active_mode)
        self.active_mode = new_active_mode
        return True

    def refresh_active_checks_if_necessary(self) -> None:
        """
        Refreshes the active checks only if the configuration directory, the checks or the active mode have changed.
        It may not be the most performant, but the logs are much clearer.
        """

        # the order is important: active_modes_have_changed() needs the modes refreshed by checks_have_changed()
        # also: every function needs to be called, hence the use of "|" instead of "or" which would be lazily evaluated
        if (self.configuration_directory_has_changed() and self.checks_have_changed()) | self.active_mode_has_changed():
            self.active_checks = filter_active_checks(self.active_mode, self.checks)
