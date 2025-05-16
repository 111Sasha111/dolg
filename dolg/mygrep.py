# Команда для запуска python mygrep.py -i "hello" file.txt

import sys
import re
import os

def parse_args():
    args = sys.argv[1:]
    options = {
        'i': False,
        'v': False,
        'c': False,
        'l': False,
        'n': False,
        'e': None
    }
    template = None
    files = []

    i = 0
    while i < len(args):
        arg = args[i]
        if arg.startswith('-'):
            for flag in arg[1:]:
                if flag == 'e':
                    if i + 1 < len(args):
                        options['e'] = args[i + 1]
                        i += 1
                    else:
                        print("Error: -e requires a pattern.")
                        sys.exit(1)
                elif flag in options:
                    if flag == 'e':
                        continue
                    options[flag] = True
                else:
                    print(f"Unknown option: {arg}")
                    sys.exit(1)
        else:
            if template is None:
                template = arg
            else:
                files.append(arg)
        i += 1

    if options['e']:
        template = options['e']
    elif template is None:
        print("Error: No pattern provided.")
        sys.exit(1)

    if not files:
        files = [None]

    return options, template, files


def match_line(line, pattern, ignore_case):
    if ignore_case:
        line = line.lower()
        pattern = pattern.lower()
    return re.search(pattern, line)


def grep_file(file_name, pattern, options):
    try:
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        else:
            lines = sys.stdin.readlines()
            file_name = "<stdin>"
    except Exception as e:
        print(f"Error reading {file_name}: {e}")
        return

    matched_lines = []
    match_count = 0
    for idx, line in enumerate(lines):
        is_match = bool(match_line(line, pattern, options['i']))
        if options['v']:
            is_match = not is_match
        if is_match:
            match_count += 1
            if not options['c'] and not options['l']:
                output_line = ""
                if options['n']:
                    output_line += f"{idx + 1}:"
                output_line += line.rstrip('\n')
                matched_lines.append(output_line)

    if options['c']:
        print(f"{file_name}:{match_count}")
    elif options['l']:
        if match_count > 0:
            print(file_name)
    else:
        for line in matched_lines:
            print(line)


def main():
    options, pattern, files = parse_args()
    multiple_files = len(files) > 1 or files[0] is None and len(files) > 1

    for file in files:
        grep_file(file, pattern, options)


if __name__ == "__main__":
    main()