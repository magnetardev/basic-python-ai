# Basic Python AI
This is a very rudamentary AI built in Python. It uses the Levenshtein distance algorithm to determine the accuracy and intent of the string and NLTK to parse the string for information useful to the intent. This is for a school project.

### Dependancies
All dependencies are installed via [pip](https://pypi.org).
- nltk

### Running
The Makefile is there just to make things simpler, you can just run it like normal if you feel (`python main.py`)
```shell
$ make run 	  # runs
$ make debug  # runs in debug mode
$ make run3   # runs via python3 (required on macOS)
$ make debug3 # runs in debug mode, via python3 (required on macOS)
```
