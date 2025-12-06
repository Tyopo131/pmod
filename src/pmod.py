#!/usr/bin/env python3
# Shebang to use for generated scripts
SHEBANG: str = "#!/usr/bin/env bash"
import os
import sys
home: str = os.getenv("HOME")
modules = []
nosort_modules = []
overwrite_module = None
overwrite_module_2 = None
overwrite_set = False
overwrite_2_set = False
log_level = os.getenv("PMOD_LOG")
for root, dirs, files in os.walk(os.path.normpath(home + "/.prompt/mods/")):
    dirs[:] = [d for d in dirs if not d.startswith(".")]
    for file in files:
        cannot_load = False
        with open(os.path.normpath(root + "/" + file), mode="r") as f:
            moddef: str = f.readline()
            if not (moddef.startswith("#?") or moddef.startswith("#>")):
                if (log_level != "all"): continue
                print(f"Error loading module {file}, does not start with valid signal", file=sys.stderr)
                print("Is it a pmod module?", file=sys.stderr, end="\n\n")
                continue
            PS: int = None
            if (moddef.startswith("#>")):
                PS = 2 # Will modify PS2
                moddef = moddef.removeprefix("#>")
            else:
                moddef = moddef.removeprefix("#?")
                PS = 1 # Will modify PS1
            priority: int = None
            remcount: int = 0
            insert_at: int = None
            flag_manual = False
            flag_stderr = False
            flag_overwrite = False
            insert_at: int = None
            for char in moddef:
                remcount += 1
                if char == "o":
                    if (PS == 1 and overwrite_set):
                        if (log_level in ("yes", "loud", "all")): print(f"Error loading module {file}, tried to set o for PS1 when o was already set for PS1", file=sys.stderr)
                        cannot_load = True
                        break
                    if (PS == 2 and overwrite_2_set):
                        if (log_level in ("yes", "loud", "all")): print(f"Error loading module {file}, tried to set o for PS2 when o was already set for PS2", file=sys.stderr)
                        cannot_load = True
                        break
                    if PS == 1: overwrite_set = True
                    elif PS == 2: overwrite_2_set = True
                    flag_overwrite = True
                    continue
                elif char == "m":
                    flag_manual = True
                    continue
                elif char == "e":
                    flag_stderr = True
                    continue
                elif char == " ":
                    priority = -1
                    break
                elif char == "\n": continue
                else:
                    print(f"Non-fatal error loading module {file}, unknown flag {char}.", file=sys.stderr)
                    continue
            moddef = (moddef[remcount:]).strip("\n")
            path = os.path.normpath(root + "/" + file)
            if (cannot_load): continue
            if (log_level in ("loud", "all")): print(f"Loading {file} at {path}", file=sys.stderr)
            if (priority is None) or (insert_at is not None):
                if (insert_at is None):
                    nosort_modules.append({"manual": flag_manual, "stderr": flag_stderr, "overwrite": flag_overwrite, "path": path, "PS": PS})
                    continue
                if (flag_overwrite and PS == 1):
                    overwrite_module = {"manual": flag_manual, "stderr": flag_stderr, "overwrite": flag_overwrite, "path": path, "PS": PS}
                    continue
                if (flag_overwrite and PS == 2):
                    overwrite_module_2 = {"manual": flag_manual, "stderr": flag_stderr, "overwrite": flag_overwrite, "path": path, "PS": PS}
                    continue
                nosort_modules.insert(insert_at, {"manual": flag_manual, "stderr": flag_stderr, "overwrite": flag_overwrite, "path": path, "PS": PS})
                continue
            if not moddef.isdigit():
                print(f"Error loading module {path}, priority is not a number", file=sys.stderr)
                continue
            priority = int(moddef)
            modules.append({"manual": flag_manual, "stderr": flag_stderr, "overwrite": flag_overwrite, "path": path, "priority": priority, "PS": PS})
modules.sort(key=lambda m: m["priority"])
entry: str = ""
if (overwrite_module is not None):
    entry: str = ""
    # Build script line
    if (overwrite_module["manual"]):
        entry = "source " + overwrite_module["path"]
        print(entry)
    else:
        entry += f'export PS{overwrite_module["PS"]}="\\$(source {overwrite_module["path"]}'
        if (overwrite_module["stderr"]): entry += " 2>&1"
        entry += ')'
        if (not overwrite_module["overwrite"]):
            entry += f"$PS{overwrite_module["PS"]}"
        entry += '"'
        print(entry)
if (overwrite_module_2 is not None):
    entry: str = ""
    # Build script line
    if (overwrite_module_2["manual"]):
        entry = "source " + overwrite_module_2["path"]
        print(entry)
    else:
        entry += f'export PS{overwrite_module_2["PS"]}="\\$(source {overwrite_module_2["path"]}'
        if (overwrite_module_2["stderr"]): entry += " 2>&1"
        entry += ')'
        if (not overwrite_module_2["overwrite"]):
            entry += f"$PS{overwrite_module_2["PS"]}"
        entry += '"'
        print(entry)
for mod in modules:
    entry: str = ""
    # Build script line
    if (mod["manual"]):
        entry = "source " + mod["path"]
        print(entry)
        continue
    entry += f'export PS{mod["PS"]}="\\$(source {mod["path"]}'
    if (mod["stderr"]): entry += " 2>&1"
    entry += f')$PS{mod["PS"]}"'
    print(entry)
for mod in nosort_modules:
    entry: str = ""
    # Build script line
    if (mod["manual"]):
        entry = "source " + mod["path"]
        print(entry)
        continue
    entry += f'export PS{mod["PS"]}="\\$(source {mod["path"]}'
    if (mod["stderr"]): entry += " 2>&1"
    entry += ')'
    if (not mod["overwrite"]):
        entry += f"$PS{mod["PS"]}"
    entry += '"'
    print(entry)
