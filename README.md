# `pmod`
`pmod` allows adding extensions to the bash (or any shell that supports `source`) prompt
## Installing
|Requirement|Version|
|---|---|
|Python|3.9|
|A basic POSIX environment and shell|Any that supports `source` command|

1. Navigate into the `src` folder, and click the small download icon in the top right of the source view.
2. Create the `~/.prompt/` and `~/.prompt/mods` directories
3. Run `source <(your-python-interpreter [pmod-location])`
    - where \[pmod-location\] is the location of pmod and your-python-interpreter is the command used to run your python interpreter
4. _(optional)_ If you want it to run every time the shell starts, add the command to your shells startup file. (for bash, it's `~/.bashrc` by default)
