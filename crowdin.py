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
    setting_headers = {header('Settings')}
    variable_headers = {header('Variable')}
    test_case_headers = {header('Test Cases')}
    task_headers = {header('Tasks')}
    keyword_headers = {header('Keywords')}
    comment_headers = {header('Comments')}
    library = {setting('Library')}
    resource = {setting('Resource')}
    variables = {setting('Variable')}
    documentation = {setting('Documentation')}
    metadata = {setting('Metadata')}
    suite_setup = {setting('Suite Setup')}
    suite_teardown = {setting('Suite Teardown')}
    test_setup = {setting('Test Setup')}
    test_teardown = {setting('Test Teardown')}
    test_template = {setting('Test Template')}
    test_timeout = {setting('Test Timeout')}
    test_tags = {setting('Test Tags')}
    task_setup = {setting('Task Setup')}
    task_teardown = {setting('Task Teardown')}
    task_template = {setting('Task Template')}
    task_timeout = {setting('Task Timeout')}
    task_tags = {setting('Task Tags')}
    keyword_tags = {setting('Keyword Tags')}
    tags = {setting('Tags')}
    setup = {setting('Setup')}
    teardown = {setting('Teardown')}
    template = {setting('Template')}
    timeout = {setting('Timeout')}
    arguments = {setting('Arguments')}
    bdd_prefixes = {bdd()}
'''


with open(out_path, 'w', encoding='UTF-8') as f:
    f.write('from robot.conf import Language\n')
    for path in in_paths:
        code = convert(path)
        f.write('\n\n')
        f.write(code)

print(out_path)
