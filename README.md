# Speed Trig Quiz Generator
![Python](https://img.shields.io/badge/python-v3.4+-blue.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Tool for the mobile game Arknights to calculate resource consumption by operators for both promotion and skill mastery level.

Running parser.py will use the JSON files from Aceship's site to perform calculations. Changing the "reduce" default values in calc.py (charCost function) will change the tracked materials. May make the whole thing much easier to use in the future, but currently that is how the code works; the output is a CSV file (results.csv) that can be opened in other programs including Excel and Google Sheets.
