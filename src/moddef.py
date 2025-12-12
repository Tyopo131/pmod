import headers
class ModDef: 
    def __init__(self, PS: int, flag_overwrite: bool = False, flag_dry_run: bool = False, flag_manual: bool = False, flag_stderr: bool = False):
        self.overwrite: bool = flag_overwrite
        self.dry_run: bool = flag_dry_run
        self.stderr: bool = flag_stderr
        self.manual: bool = flag_manual
        self.prompt: int = PS
class ParseError(RuntimeError): # Custom exception class for mod definition parsing errors
    pass
def parse(header: str) -> ModDef:
    PS: int = None
    if (header.startswith(headers.PS1)):
        PS = 1
        header.removeprefix(headers.PS1)
    elif (header.startswith(headers.PS2)):
        PS = 2
        header.removeprefix(headers.PS2)
    else:
        raise ParseError(f"Does not start with valid signal! ({headers.PS1} for PS1 or {headers.PS2} for PS2 supported)")
    