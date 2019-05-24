vim-codespell
---------------------
A vim plugin for checking the spelling for source code. The main difference from the built-in spell checker is that it handles CamelCase, snake_case better, and you can add custom words to it.

# Installation
* Enable vim python3 support
* Install [aspell][http://aspell.net/]
  * Mac: `brew install aspell`
  * Ubuntu: `sudo apt-get install aspell`
* Add it to vim with the vim plugin manager of your choice.
  * Vundle: Add `Plugin 'shinglyu/vim-codespell'` to your `~/.vimrc` and run `:PluginInstall`
  * vim-plug: Add `Plug 'shinglyu/vim-codespell'` to your `~/.vimrc` and run `:PlugInstall`

# Commands
* `:Codespell`: Run the spell checker once
* `:CodespellAddWord`: Add the word to the dictionary where the cursor is currently located

* To spell check every time you save a `*.py` file, add the following to your vimrc:
```
:autocmd BufWritePre *.py :Codespell
```

# Variables
* `g:CodespellLang`: Language to use, see aspell documentation, aspell dictionary automatically generated when changed (default: "en")
* `g:CodespellShortWord`: Don't spell check words of this length or shorter (default: 4)

# Testing
* `sudo pip3 install pytest pytest-benchmark` (Or use `virtualenv`)
* `py.test`

# Generating Dictionaries
You can add custom words to the dictionary.

* Change into `dict/` and create a text file (e.g. `personal.list`) of words, one word per line
* Generate the dictionary for the language you desire (English for example)
```
dict/build.sh en
```

A dictionary file like `cs-en.dict` will be generated in the current dir. The plugin will pick it up if `CodespellLang` is set to use that language. Note that you have to generate a separate dictionary for each language if you construct custom dictionaries this way.

* Test the dictionary locally:
```
cat file_to_be_checked.txt | aspell -l en -d cs.dict --dict-dir=./ --list
```

The `--dict-dir` must be specified otherwise `aspell` will check the default location.

# Tips
* Check if `python3` is supported in your vim build: `vim --version`, look for the string "+python3".
* To load it temporarily for test, `cd` to `plugin/`, run `vim -S codespell.vim`.
* `:match Error /\%2l\%>1c\%<4c./`: highlight line 2 (`\%2l`) and column 2 (`\%>1c`) to column 3 (`\%<4c`), the `.` is required because the match is 0 width.

# References
* Python's `vim` interface [doc](http://vimdoc.sourceforge.net/htmldoc/if_pyth.html)
* [Learn vimscript the hard way](http://learnvimscriptthehardway.stevelosh.com)
