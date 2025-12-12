import os
import logger
_cache_pmoddir: str = None
def get_pmod_dir():
    global _cache_pmoddir
    if _cache_pmoddir is not None:
        logger.debug("CACHE HIT on pmod mods directory")
        return _cache_pmoddir
    logger.debug("NO CACHE HIT on pmod mods directory")
    home = os.getenv("HOME")
    pm = os.getenv("PMOD_MODDIR")
    pmoddir: str = None
    if pm is not None: pmoddir = pm
    elif home is not None and home != "":
        pmoddir = home + "/.prompt/mods"
    else:
        logger.fatal(
            """No valid paths for pmod mods directory!
    Tried $PMOD_MODDIR but it isn't set!
    Tried $HOME + "/.prompt/mods" but $HOME isn't set!
            """
        )
        exit(-5)
    pmoddir = os.path.normpath(pmoddir)
    _cache_pmoddir = pmoddir
    return pmoddir
get_pmod_dir()
