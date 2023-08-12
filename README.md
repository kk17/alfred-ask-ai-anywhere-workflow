# AskAI Anywhere - Alfred Workflow
[![Releases](https://img.shields.io/github/v/release/kk17/alfred-ask-ai-anywhere-workflow?include_prereleases)](https://github.com/kk17/alfred-ask-ai-anywhere-workflow/releases)
[![Issues](https://img.shields.io/github/issues/kk17/alfred-ask-ai-anywhere-workflow)](https://github.com/kk17/alfred-ask-ai-anywhere-workflow/issues)


A powerful workflow for using Notion's AskAI feature from anywhere.
![](docs/ask-ai-anywhere.gif)


## Installation

1. [Download the workflow](https://github.com/kk17/alfred-ask-ai-anywhere-workflow/releases/latest)
2. Double click the `.alfredworkflow` file to install and configure the workflow. Follow [this guide](https://github.com/Vaayne/notionai-py#get-notion-token-and-workspace-id) to get Notion token and workspace ID from you broswer.

Note that the [Alfred 5 Powerpack](https://www.alfredapp.com/powerpack/) and one of the LLM provider to use the workflow.
- [NotionAI](https://www.notion.so/product/ai)
- [OpenAI](https://platform.openai.com/account/api-keys)

## Usage
To use, select any text anywhere then press the hotkeys you configured to trigger this workflow. 
You can also add more option in to the List Filter.

`ask_ai.py` script usage:
```
/usr/bin/python3 ./ask_ai.py --help

Usage: ask_ai.py [OPTIONS] COMMAND [ARGS]...

  Command line interface for Notion AI API.

Options:
  --model-provider [notionai|openai_gpt-3.5-turbo|openai_gpt-4|openai_text-davinci-003]
                                  LLM provider, support notionai, openai
  --input-to-clipboard            Copy input content to clipboard.
  --combine-input-into-result     Combine input content into result.
  --result-to-keyboard            Output result to keyboard instead of stdout.
  --result-to-clipboard           Copy result to clipboard.
  --paste-result                  Paste result from clipboard.
  -v, --verbose                   Enable verbose output.
  --help                          Show this message and exit.

Commands:
  change-tone
  continue-writing
  improve-writing
  summarize
```

## Advanced Features
If no text is selected, this workflow will use the contents of your clipboard as input. 

You can create your own prompt using the `continue-writing` command, followed by a `#` symbol. For example, an option in the list script could be:

```
continue-writing #translate the following content into Singlish:
```

Additionally, some Text to Speech options have been added. If they are not working, you may need to download the necessary voice in your OS system preferences under Spoken Content -> System Voice -> Manage Voices.

## Troubleshooting
- [Using the Workflow Debugger - Alfred Help and Support](https://www.alfredapp.com/help/workflows/advanced/debugger/)


## Contributing

See [this README](CONTRIBUTING.md)


## Donating

Like this workflow? Consider donating! 😻

<a href="https://www.buymeacoffee.com/kk17" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Pizza" style="height: 60px !important;width: 217px !important;" ></a>


## Credits

- The Alfred workflow is using [notionai_py](https://github.com/Vaayne/notionai-py) python package.
- Icon from https://www.flaticon.com/