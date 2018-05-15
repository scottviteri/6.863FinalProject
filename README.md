# 6.863J Semantics Framework.

Requirements in shell.nix

To get started:
``` nix-shell
``` python semantic.py --help
``` python semantic.py --batch_mode test/test_sentences.txt --validate_output test/valid_output.txt 

>>> from semantic import *

 Training
> John ate the potato
> John ate the tomato
> Mary ate the tomato

 Testing
{'Mary ate the potato': ['Mary ate the potato', 'Mary ate the tomato']}

