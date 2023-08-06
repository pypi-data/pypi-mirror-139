def get_version():
    to_return = None
    try:
        with open("pyproject.toml", "r") as pp:
            for i in pp.readlines():
                if "version" in i:
                    to_return = i.split(" ")[-1].replace('"', '')
    except Exception as ex:
        with open("../pyproject.toml", "r") as pp:
            for i in pp.readlines():
                if "version" in i:
                    to_return = i.split(" ")[-1].replace('"', '')
    return to_return
