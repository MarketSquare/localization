# localization
Tools to help with translation of Robot Framework

## Basic Usage
1. Download your language from [Crowdin](https://robotframework.crowdin.com/u/projects/1) or custom make your own yml file
2. Use crowdin.py as follows:

```your/folder> crowdin Dutch.yml Finnish.yml languages.py```

You can either use the output to create a PR in Robot Framework to have your language added, or you can use your language as follows:

Languages to use are specified when starting execution using the --language command line option. With languages supported by Robot Framework out-of-the-box it is possible to use just a language code like --language fi. With others it is possible to create a custom language file and use it like --language MyLang.py
