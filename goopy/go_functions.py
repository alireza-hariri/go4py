import json
import os
import subprocess
from pathlib import Path
import logging
from goopy.types import GoFunction


logger = logging.getLogger(__name__)


def get_go_functions():
    # Get the project root directory
    project_root = Path(__file__).parent.parent

    # Path to the parser executable
    parser_path = project_root / "build" / "parsing"

    # Run the parser executable
    logger.debug(f"Running parser: {parser_path}")
    result = subprocess.run([parser_path], cwd=project_root, check=True)

    if result.returncode != 0:
        logger.error(f"Parser failed with exit code {result.returncode}")
        return

    # Path to the generated functions.json file
    functions_json_path = project_root / "functions.json"

    # Check if the functions.json file was generated
    if not functions_json_path.exists():
        logger.error(f"Error: {functions_json_path} was not generated")
        return

    # Read the functions.json file
    logger.debug(f"Reading functions from: {functions_json_path.name}")
    with open(functions_json_path, "r") as f:
        functions_data = json.load(f)

    # Generate GoFunction objects from the JSON data
    go_functions = []
    for func_data in functions_data:
        try:
            go_function = GoFunction.model_validate(func_data)
            go_functions.append(go_function)
            # print(f"Parsed function: {go_function.name}")
        except Exception as e:
            logger.warning(f"function skipped: {func_data['name']}")
            logger.debug(f"Error: {e}")

    logger.info(f"Successfully parsed {len(go_functions)} functions")

    # Return the list of GoFunction objects for further processing
    return go_functions
