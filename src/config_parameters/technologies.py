import os

TECHNOLOGIES_PATH = "./src/config_parameters"


def get_all_technologies() -> list:
    """
    Gets all available technologies based on the directory structure. 
    exclude the __pycache__ directory

    Returns:
        list: list of technologies available
    """
    technologies = [
        directory for directory in os.listdir(TECHNOLOGIES_PATH)
        if (os.path.isdir(os.path.join(TECHNOLOGIES_PATH, directory)) and directory != "__pycache__")
    ]

    return list(map(
        lambda x: {"key": x, "value": x},
        technologies))


def find_parameter(text: str, parameter_file: str) -> list:
    """
    Finds all the parameters of the file present in the text

    Args:
        text (str): text to be searched
        parameter_file (str): file containing the parameters

    Returns:
        list[str]: list of parameters present in the text
    """
    with open(parameter_file, "r") as f:
        parameters = f.read().splitlines()

    return list(set(text.split(" ")).intersection(parameters))
