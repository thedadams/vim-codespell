# TODO: correct header
# Python 3
from collections import defaultdict
import re
from pathlib import Path
from subprocess import Popen, PIPE, STDOUT, run
import vim


def tokenize(line):
    words = [m.group(0) for m in re.finditer(r"[a-zA-Z]+", line)]
    # TODO: maybe merge the two regex or make this more efficient
    final_words = []
    for word in words:
        # Ref: https://stackoverflow.com/questions/29916065/how-to-do-camelcase-split-in-python
        final_words += [m.group(0) for m in re.finditer(
            ".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)", word)]

    return final_words


def filter_multi_occurrence(words):
    counts = defaultdict(lambda: 0)
    for word in words:
        counts[word] += 1
    filtered = []
    for word, count in counts.items():
        # TODO: make this configurable
        if count < 5:
            filtered.append(word)
    return filtered


def find_spell_errors_cs(words):
    # Must be executed from the top level
    script_dir = vim.eval("s:dir")
    lang = vim.eval("g:CodespellLang")
    dict_file = "cs-" + lang + ".dict"
    if not Path(script_dir + "/../dict/" + dict_file).is_file():
        build_new_dict(script_dir, lang)
    return find_spell_errors(words, ["-d", dict_file, "--dict-dir={dir}/../dict".format(dir=script_dir)])

def build_new_dict(script_dir, lang):
    run([script_dir + "/../dict/build.sh", lang], cwd=script_dir + "/../dict/")

def find_spell_errors(words, extra_args=[]):
    base_aspell_cmd = ["aspell", "--list"]
    # TODO: Make this configurable
    extra_aspell_args = [
        "-l", vim.eval('g:CodespellLang'), "-W", vim.eval('g:CodespellShortWord')]
    cmd = base_aspell_cmd + extra_aspell_args + extra_args

    p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT)

    stdout = p.communicate(input=str.encode(" ".join(words)))[0]
    output = stdout.decode()
    return output.rstrip().split("\n")


# Main
lines = " ".join(vim.current.buffer)
words = tokenize(lines)
words = filter_multi_occurrence(words)
unique_words = list(set(words))
for word in find_spell_errors(find_spell_errors_cs(unique_words)):
    # silently skip empty string, which is usually due to the dictionary not
    # working correctly
    if len(word) == 0:
        continue
    # We ignore words that has more lowercase char after it, because we
    # might be matching a prefix.
    vim.command("call matchadd('SpellBad', '{word}')".format(
        word=re.escape(word)))
