from src.utilities import get_path


def get_version():
    to_return = None
    try:
        with open("pyproject.toml", "r") as pp:
            for i in pp.readlines():
                if "version" in i:
                    to_return = i.split(" ")[-1].replace('"', '')
    except Exception as ex:
        pyf = get_path().replace("/src", "/") + "pyproject.toml"
        with open(pyf, "r") as pp:
            for i in pp.readlines():
                if "version" in i:
                    to_return = i.split(" ")[-1].replace('"', '')
    return to_return
