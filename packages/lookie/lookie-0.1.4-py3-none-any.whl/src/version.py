def get_version():
    to_return = None
    with open("pyproject.toml", "r") as pp:
        for i in pp.readlines():
            if "version" in i:
                to_return = i.split(" ")[-1].replace('"', '')
    return to_return
