"""
Just a convenience script for converting CSS to python dict.
I clearly know nothing about javascript, HTML or CSS lel

expecting inputs like this

    border-color: #000;
    border-width: 1px;
"""

while True:
    line_read = []
    while line := input(""):
        key, val = line.strip("; ").split(":")

        try:
            val = int(val)
        except ValueError:
            val = f'"{val.strip(" ")}"'

        line_read.append(f'"{key}": {val},')

    for line in line_read:
        print(line)
