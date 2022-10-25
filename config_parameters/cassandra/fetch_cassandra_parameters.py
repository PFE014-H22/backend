from bs4 import BeautifulSoup
import requests


def fetch_params():
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

    write_to_file("./cassandra_parameters.txt", "\n".join(config_parameters))


def get_html_from(url: str):
    page = requests.get(url)
    return BeautifulSoup(page.content, "html.parser")


def extract_code_from(response_set, html, title_tag="h2"):
    h2_list = html.find_all(title_tag)
    for h2 in h2_list:
        title = h2.find("code")
        if title is None:
            continue

        response_set.add(title.text.split("=")[0])


def write_to_file(file_name, content):
    with open(file_name, "w") as f:
        f.write(content)


if __name__ == "__main__":
    fetch_params()
