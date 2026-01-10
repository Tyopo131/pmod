import headers
import logger
class ModDef: 
    def __init__(self, PS: int, flag_overwrite: bool = False, flag_dry_run: bool = False, flag_manual: bool = False, flag_stderr: bool = False):
        self.overwrite: bool = flag_overwrite
        self.dry_run: bool = flag_dry_run
        self.stderr: bool = flag_stderr
        self.manual: bool = flag_manual
        self.prompt: int = PS
class ParseError(RuntimeError): # Custom exception class for mod definition parsing errors
    def __init__(self, *args: object, header = None):
        super().__init__(*args)
        self.header = header
    def __str__(self):
        base = super().__str__()
        return f"while parsing '{self.header}': {base}"
def parse(header: str) -> ModDef:
    logger.debug(f"Parsing PS for string '{header}'")
    # PS parsing
    PS: int = None
    if (header.startswith(headers.PS1)):
        PS = 1
        header.removeprefix(headers.PS1)
    elif (header.startswith(headers.PS2)):
        PS = 2
        header.removeprefix(headers.PS2)
    else:
        logger.debug(f"Parsing PS for string {header} failed, raising exception")
        raise ParseError(f"Does not start with valid signal! ({headers.PS1} for PS1 or {headers.PS2} for PS2 supported)")
    logger.debug(f"Parsing PS for string {header}: Determined PS is {PS}")
    