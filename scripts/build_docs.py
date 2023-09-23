from argparse import ArgumentParser
from pathlib import Path

from sphinx.cmd.build import main as sphinx_main

p = ArgumentParser()
p.add_argument("languages", nargs="+")
args = p.parse_args()


def build(lang):
    target_directory = f"frescobaldi_app/userguide/build/{lang}"
    args = ["-E", "-D", f"language={lang}", "docs", target_directory]
    ret_code = sphinx_main(args)
    if ret_code:
        raise SystemExit(ret_code)


# Default to building English only
if not args.languages:
    args.languages = ["en"]
# The special language "all" stands for building all languages
elif "all" in args.languages:
    linguas = Path("i18n/userguide/LINGUAS")
    args.languages = linguas.read_text(encoding="utf-8").splitlines()

for lang in args.languages:
    build(lang)
