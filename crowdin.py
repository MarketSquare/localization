#!/usr/bin/env python3

"""Robot Framework's Crowdin-to-Python converter.

Converts Robot Framework translations created at Crowdin [1] to Python
code that can be used with Robot Framework.

  Usage: python crowdin.py Lang.yml [lang2.yml ...] Lang.py

Input files must be YAML files got from Crowdin and the output file
specifies where to write the generated Python code.

Generated language files can be used with Robot Framework 5.1 like this:

  robot --language Lang.py tests.robot

To get the language added to Robot Framework itself, submit a pull request
where the generated language class is added to the `languages` module [2].

[1] https://robotframework.crowdin.com/robot-framework
[2] https://github.com/robotframework/robotframework/blob/master/src/robot/conf/languages.py
"""

from pathlib import Path
import sys
import yaml


if len(sys.argv) < 3 or '--help' in sys.argv:
    sys.exit(__doc__)

*in_paths, out_path = sys.argv[1:]


def convert(path):
    with open(path, encoding='UTF-8') as file:
        data = yaml.safe_load(file)

    NAME, TRANSLATIONS = data.popitem()
    SETTINGS = TRANSLATIONS['Settings']
    SETTINGS.update(TRANSLATIONS['Setup'])
    SETTINGS.update(TRANSLATIONS['Keywords'])

    def name():
        parts = NAME.title().split('-')
        return ''.join(parts)

    def doc():
        return Path(path).stem

    def header(name):
        values = ', '.join(f"'{v}'" for v in TRANSLATIONS['Headers'][name].values())
        return f'{{{values}}}'

    def setting(name):
        return f"'{SETTINGS[name]}'"

    def bdd():
        values = ', '.join(f"'{v}'" for v in TRANSLATIONS['BDD'].values())
        return f'{{{values}}}'

    return f'''\
class {name()}(Language):
    """{doc()}"""
    setting_headers = {header(Settings)!r}
    variable_headers = {header(Variable)!r}
    test_case_headers = {header(Test Cases)!r}
    task_headers = {header(Tasks)!r}
    keyword_headers = {header(Keywords)!r}
    comment_headers = {header(Comments)!r}
    library = {setting(Library)!r}
    resource = {setting(Resource)!r}
    variables = {setting(Variable)!r}
    documentation = {setting(Documentation)!r}
    metadata = {setting(Metadata)!r}
    suite_setup = {setting(Suite Setup)!r}
    suite_teardown = {setting(Suite Teardown)!r}
    test_setup = {setting(Test Setup)!r}
    test_teardown = {setting(Test Teardown)!r}
    test_template = {setting(Test Template)!r}
    test_timeout = {setting(Test Timeout)!r}
    test_tags = {setting(Test Tags)!r}
    task_setup = {setting(Task Setup)!r}
    task_teardown = {setting(Task Teardown)!r}
    task_template = {setting(Task Template)!r}
    task_timeout = {setting(Task Timeout)!r}
    task_tags = {setting(Task Tags)!r}
    keyword_tags = {setting(Keyword Tags)!r}
    tags = {setting(Tags)!r}
    setup = {setting(Setup)!r}
    teardown = {setting(Teardown)!r}
    template = {setting(Template)!r}
    timeout = {setting(Timeout)!r}
    arguments = {setting(Arguments)!r}
    bdd_prefixes = {bdd()}
'''


with open(out_path, 'w', encoding='UTF-8') as f:
    f.write('from robot.conf import Language\n')
    for path in in_paths:
        code = convert(path)
        f.write('\n\n')
        f.write(code)

print(out_path)
