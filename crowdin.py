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
    BDD = TRANSLATIONS['BDD']

    


    def name():
        parts = NAME.title().split('-')
        return ''.join(parts)

    def doc():
        return Path(path).stem

    def header(name):
        values = TRANSLATIONS['Headers'][name]
        return f"'{values}'"

    def setting(name):
        return f"'{SETTINGS[name]}'"

    def bdd(name):
        values = TRANSLATIONS['BDD'][name]
        return f"{{'{values}'}}"

    def thruty():
        values = ', '.join(f"'{v}'" for v in TRANSLATIONS['TrueString'].values())
        return f'{{{values}}}'
    
    def falsy():
        values = ', '.join(f"'{v}'" for v in TRANSLATIONS['FalseString'].values())
        return f'{{{values}}}'

    return f'''\
class {name()}(Language):
    """{doc()}"""
    setting_header = {header(r'Settings')}
    variable_header = {header(r'Variable')}
    test_case_header = {header(r'Test Cases')}
    task_header = {header(r'Tasks')}
    keyword_header = {header(r'Keywords')}
    comment_header = {header(r'Comments')}
    library = {setting(r'Library')}
    resource = {setting(r'Resource')}
    variables = {setting(r'Variable')}
    documentation = {setting(r'Documentation')}
    metadata = {setting(r'Metadata')}
    suite_setup = {setting(r'Suite Setup')}
    suite_teardown = {setting(r'Suite Teardown')}
    test_setup = {setting(r'Test Setup')}
    test_teardown = {setting(r'Test Teardown')}
    test_template = {setting(r'Test Template')}
    test_timeout = {setting(r'Test Timeout')}
    test_tags = {setting(r'Test Tags')}
    task_setup = {setting(r'Task Setup')}
    task_teardown = {setting(r'Task Teardown')}
    task_template = {setting(r'Task Template')}
    task_timeout = {setting(r'Task Timeout')}
    task_tags = {setting(r'Task Tags')}
    keyword_tags = {setting(r'Keyword Tags')}
    tags = {setting(r'Tags')}
    setup = {setting(r'Setup')}
    teardown = {setting(r'Teardown')}
    template = {setting(r'Template')}
    timeout = {setting(r'Timeout')}
    arguments = {setting(r'Arguments')}
    given_prefix = {bdd(r'Given')}
    when_prefix = {bdd(r'When')}
    then_prefix = {bdd(r'Then')}
    and_prefix = {bdd(r'And')}
    but_prefix = {bdd(r'But')}
    true_strings = {thruty()}
    false_strings = {falsy()}
'''


with open(out_path, 'w', encoding='UTF-8') as f:
    f.write('from robot.conf import Language\n')
    for path in in_paths:
        code = convert(path)
        f.write('\n\n')
        f.write(code)

print(out_path)
