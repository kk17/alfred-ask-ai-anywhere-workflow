# Contributing

## Requirements
- python 3.9.x

## install package
```
/usr/bin/pip3 install --target=lib -r requirements.txt
```

## Installation
Clone the repository and update the `SCRIPT_PATH` environment variable with the path to the script file in the repository.

Afterwards, you can invoke the Alfred workflow from your cloned repository.

You can also test the script in the terminal command line.

```bash
export PYTHONPATH=.:lib
/usr/bin/python3 \
    ask_ai.py \
    -v \
    --model-provider openai_text-davinci-003 \
    translate chinese \
    "python code to use keyboard package to trigger the cmd+v shortcut. the code should works on mac os and windows os and linux."
```