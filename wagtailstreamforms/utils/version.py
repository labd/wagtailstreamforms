def get_version(version):  # pragma: no cover
    """ Returns a PEP 386-compliant version number from VERSION. """

    main = get_main_version(version)

    sub = ""
    if version[3] != "final":
        mapping = {"alpha": "a", "beta": "b", "rc": "c"}
        sub = mapping[version[3]] + str(version[4])

    return main + sub


def get_main_version(version):  # pragma: no cover
    """ Returns main version (X.Y[.Z]) from VERSION. """

    parts = 2 if version[2] == 0 else 3
    return ".".join(str(x) for x in version[:parts])
