BASE = {
    "d": lambda mod: setattr(s, "dry_run", True),
    "o": lambda mod: setattr(s, "overwrite", True),
    "m": lambda mod: setattr(s, "manual", True),
    "e": lambda mod: setattr(s, "stderr", True)
}
PS1 = BASE.copy()
PS2 = BASE.copy()
