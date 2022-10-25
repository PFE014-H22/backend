from bs4 import BeautifulSoup
import requests


def fetch_params():
    """
    Fetches all the parameters from the cassandra documentation

    Returns:
        set(str): set of strings containing all the parameters
    """
    config_parameters = set()

    url = "https://cassandra.apache.org/doc/latest/cassandra/configuration/cass_yaml_file.html"
    html = get_html_from(url=url)
    extract_code_from(config_parameters, html, "h2")

    url = "https://cassandra.apache.org/doc/latest/cassandra/configuration/cass_rackdc_file.html"
    html = get_html_from(url=url)
    extract_code_from(config_parameters, html, "h3")

    url = "https://cassandra.apache.org/doc/latest/cassandra/configuration/cass_env_sh_file.html"
    html = get_html_from(url=url)
    extract_code_from(config_parameters, html, "h2")

    url = "https://cassandra.apache.org/doc/latest/cassandra/configuration/cass_cl_archive_file.html"
    html = get_html_from(url=url)
    extract_code_from(config_parameters, html, "h3")

    return "\n".join(config_parameters)


def get_html_from(url: str):
    """
    Gets the html from the url

    Args:
        url (str): url to fetch the html from

    Returns:
        str: html from the url
    """
    page = requests.get(url)
    return BeautifulSoup(page.content, "html.parser")


def extract_code_from(response_set, html, title_tag):
    """
    Extracts the parameters from the html
    On the cassandra documentation site, all parameters are in code tags
    and are either in h2 or h3 tags

    Args:
        response_set (str): set to which the parameters are added
        html (str): content of the html
        title_tag (str): Tag in which the parameter is in for this specific documentation page
    """
    tags = html.find_all(title_tag)
    for parameter_title in tags:
        title = parameter_title.find("code")
        if title is None:
            continue

        response_set.add(title.text.split("=")[0])


def write_to_file(file_name, content):
    """
    Writes the content to the file

    Args:
        file_name (str): path to the file to be written to
        content (str): content to be written to the file
    """
    with open(file_name, "w") as f:
        f.write(content)


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

if __name__ == "__main__":
    """
    File to run to populate the parameters file with the parameters from the cassandra documentation
    """
    config_parameters = fetch_params()
    write_to_file("./cassandra_parameters.txt", config_parameters)
