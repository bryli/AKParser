# Speed Trig Quiz Generator
![Python](https://img.shields.io/badge/python-v3.4+-blue.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Tool for the mobile game Arknights to calculate resource consumption by operators for both promotion and skill mastery level.

Running parser.py will use the JSON files from Aceship's site to perform calculations. Changing the default values for the reduce argument of the charCost function in calc.py will change the tracked materials. I may make the whole thing much easier to use in the future, but for now the code will have to remain in its messy state. The output is a CSV file (results.csv) that can be opened in other programs including Excel and Google Sheets.
