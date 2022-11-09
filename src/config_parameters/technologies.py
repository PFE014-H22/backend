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
