"""
A Python library for open neuroscience data access and manipulation.
"""

__version__ = "0.9.4"


def check_version():
    """
    Tells you if you have an old version of intern.
    """
    import requests
    r = requests.get('https://pypi.python.org/pypi/intern/json').json()
    r = r['info']['version']
    if r != __version__:
        print("You are using version {}. A newer version of intern is available: {} ".format(__version__, r) +
              "\n\n'pip install -U intern' to update.")
    return r
