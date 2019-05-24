from subprocess import run
from os import remove, listdir
import vim

word = vim.eval("expand('<cword>')")
dict_dir = vim.eval("s:dir") + "/../dict/"
lang = vim.eval("g:CodespellLang")
file = open(dict_dir + "personal.list", 'a')
file.write(word + "\n")
file.close()
for file in listdir(dict_dir):
    if file.endswith(".dict"):
        remove(dict_dir + file)
