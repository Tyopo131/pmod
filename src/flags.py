BASE = {
    "o": lambda mod: setattr(s, "overwrite", True),
    "d": lambda mod: setattr(s, "dry_run", True),
    "e": lambda mod: setattr(s, "stderr", True),
    "m": lambda mod: setattr(s, "manual", True)
}
PS1 = BASE.copy()
PS2 = BASE.copy()
