#!/usr/bin/env python3
# Shebang to use for generated scripts
SHEBANG: str = "#!/usr/bin/env bash"
import os
import sys
home: str = os.getenv("HOME")
modules = []
nosort_modules = []
overwrite_set = False
for root, dirs, files in os.walk(os.path.normpath(home + "/.prompt/mods/")):
    for file in files:
        cannot_load = False
        with open(os.path.normpath(root + "/" + file), mode="r") as f:
            moddef: str = f.readline()
            if not moddef.startswith("#?"):
                print(f"Error loading module {file}, does not start with '#?'", file=sys.stderr)
                print("Is it a pmod module?", file=sys.stderr, end="\n\n")
                continue
            moddef = moddef.removeprefix("#?")
            priority: int = None
            remcount: int = 0
            flag_manual = False
            flag_stderr = False
            flag_overwrite = False
            for char in moddef:
                remcount += 1
                insert_at: int = None
                if char == "o":
                    if (overwrite_set == True):
                        print(f"Error loading module {file}, tried to set o when o was already set", file=sys.stderr)
                        cannot_load = True
                        break
                    insert_at = 1
                    overwrite_set = True
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
            moddef = (moddef[remcount:]).strip("\n")
            print(moddef)
            path = os.path.normpath(root + "/" + file)
            if (cannot_load): continue
            print(f"root: {root}, path: {path}, overwrite: {flag_overwrite}, stderr: {flag_stderr}, manual: {flag_manual}, priority: {priority}")
            if (priority is None) or (insert_at is not None):
                if (insert_at is None):
                    nosort_modules.append({"manual": flag_manual, "stderr": flag_stderr, "overwrite": flag_overwrite, "path": path})
                    continue
                nosort_modules.insert(insert_at, {"manual": flag_manual, "stderr": flag_stderr, "overwrite": flag_overwrite, "path": path})
                continue
            if not moddef.isalnum():
                print(f"Error loading module {path}, priority is not a number", file=sys.stderr)
                continue
            priority = int(moddef)
            modules.append({"manual": flag_manual, "stderr": flag_stderr, "overwrite": flag_overwrite, "path": path, "priority": priority})
            print(f"root: {root}, path: {path}, overwrite: {flag_overwrite}, stderr: {flag_stderr}, manual: {flag_manual}, priority: {priority}")

with open(os.path.normpath(home + "/.prompt/.list.sh"), "w") as f:
    for mod in modules:
        flags: str = ""
        if (mod["overwrite"]): flags += "o"
        if (mod["stderr"]): flags += "e"
        if (mod["manual"]): flags += "m"
        entry = flags + ";" + mod["path"] + "\n"
        f.write(entry)
    for mod in nosort_modules:
        flags: str = ""
        if (mod["overwrite"]): flags += "o"
        if (mod["stderr"]): flags += "e"
        if (mod["manual"]): flags += "m"
        entry = flags + ";" + mod["path"] + "\n"
        f.write(entry)
