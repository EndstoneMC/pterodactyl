"""Validate a Pterodactyl egg JSON file against PTDL_v2 import rules.

Based on Pterodactyl Panel's EggImporterService.php validation rules:
https://github.com/pterodactyl/panel/blob/develop/app/Services/Eggs/Sharing/EggImporterService.php
"""

import json
import re
import sys

DOCKER_IMAGE_PATTERN = re.compile(r"^[\w#./\- ]*\|?~?[\w./\-:@ ]*$")
ENV_VARIABLE_PATTERN = re.compile(r"^\w{1,191}$")
RESERVED_ENV_NAMES = frozenset({
    "SERVER_MEMORY", "SERVER_IP", "SERVER_PORT", "ENV", "HOME",
    "USER", "STARTUP", "SERVER_UUID", "UUID",
})


def validate(path: str) -> list[str]:
    errors: list[str] = []

    # Parse JSON
    try:
        with open(path) as f:
            egg = json.load(f)
    except json.JSONDecodeError as e:
        return [f"Invalid JSON: {e}"]

    # meta.version
    meta = egg.get("meta")
    if not isinstance(meta, dict) or meta.get("version") != "PTDL_v2":
        errors.append("meta.version must be 'PTDL_v2'")

    # name
    name = egg.get("name")
    if not isinstance(name, str) or not name or len(name) > 191:
        errors.append("name is required (string, max 191 chars)")

    # author (valid email)
    author = egg.get("author")
    if not isinstance(author, str) or "@" not in author:
        errors.append("author is required (valid email address)")

    # startup
    startup = egg.get("startup")
    if not isinstance(startup, str) or not startup:
        errors.append("startup is required (non-empty string)")

    # docker_images
    images = egg.get("docker_images")
    if not isinstance(images, dict) or len(images) < 1:
        errors.append("docker_images is required (object with at least 1 entry)")
    elif images:
        for label, image in images.items():
            if not isinstance(image, str) or not DOCKER_IMAGE_PATTERN.match(image):
                errors.append(f"docker_images['{label}']: invalid image format: {image}")

    # features
    features = egg.get("features")
    if features is not None and not isinstance(features, list):
        errors.append("features must be an array or null")

    # file_denylist
    denylist = egg.get("file_denylist")
    if denylist is not None and not isinstance(denylist, list):
        errors.append("file_denylist must be an array or null")

    # config
    config = egg.get("config")
    if not isinstance(config, dict):
        errors.append("config is required (object)")
    else:
        # config.stop
        if not isinstance(config.get("stop"), str):
            errors.append("config.stop is required (string)")

        # config.files - must be valid JSON string
        files_str = config.get("files")
        if not isinstance(files_str, str):
            errors.append("config.files is required (JSON string)")
        else:
            try:
                json.loads(files_str)
            except json.JSONDecodeError as e:
                errors.append(f"config.files contains invalid JSON: {e}")

        # config.startup - must be valid JSON string
        startup_str = config.get("startup")
        if not isinstance(startup_str, str):
            errors.append("config.startup is required (JSON string)")
        else:
            try:
                json.loads(startup_str)
            except json.JSONDecodeError as e:
                errors.append(f"config.startup contains invalid JSON: {e}")

        # config.logs - must be valid JSON string
        logs_str = config.get("logs")
        if isinstance(logs_str, str):
            try:
                json.loads(logs_str)
            except json.JSONDecodeError as e:
                errors.append(f"config.logs contains invalid JSON: {e}")

    # scripts
    scripts = egg.get("scripts")
    if not isinstance(scripts, dict):
        errors.append("scripts is required (object)")
    else:
        install = scripts.get("installation")
        if not isinstance(install, dict):
            errors.append("scripts.installation is required (object)")
        else:
            if not isinstance(install.get("script"), str):
                errors.append("scripts.installation.script is required (string)")
            if not isinstance(install.get("container"), str):
                errors.append("scripts.installation.container is required (string)")
            if not isinstance(install.get("entrypoint"), str):
                errors.append("scripts.installation.entrypoint is required (string)")

    # variables
    variables = egg.get("variables")
    if not isinstance(variables, list):
        errors.append("variables is required (array)")
    else:
        for i, var in enumerate(variables):
            prefix = f"variables[{i}]"
            if not isinstance(var, dict):
                errors.append(f"{prefix}: must be an object")
                continue

            var_name = var.get("name")
            if not isinstance(var_name, str) or not var_name or len(var_name) > 191:
                errors.append(f"{prefix}.name is required (string, 1-191 chars)")

            env_var = var.get("env_variable")
            if not isinstance(env_var, str) or not ENV_VARIABLE_PATTERN.match(env_var):
                errors.append(f"{prefix}.env_variable is required (alphanumeric/underscore, 1-191 chars)")
            elif env_var in RESERVED_ENV_NAMES:
                errors.append(f"{prefix}.env_variable '{env_var}' is a reserved name")

            if not isinstance(var.get("user_viewable"), bool):
                errors.append(f"{prefix}.user_viewable is required (boolean)")

            if not isinstance(var.get("user_editable"), bool):
                errors.append(f"{prefix}.user_editable is required (boolean)")

            if not isinstance(var.get("rules"), str):
                errors.append(f"{prefix}.rules is required (string)")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <egg.json>")
        return 1

    errors = validate(sys.argv[1])
    if errors:
        print(f"Validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Egg validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())