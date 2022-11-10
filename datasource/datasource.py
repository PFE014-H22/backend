
class Source:
    GOOGLE = 'google'
    STACKOVERFLOW = 'stackoverflow'
    UNKNOWN = 'unknown'


def get_data_source(link: str) -> Source:
    if Source.STACKOVERFLOW in link:
        return Source.STACKOVERFLOW
    elif Source.GOOGLE in link:
        return Source.GOOGLE

    return Source.UNKNOWN


if __name__ == "__main__":
    source = get_data_source("www.stackoverflow.com")
    print(source)
