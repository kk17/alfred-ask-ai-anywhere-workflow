import click
import os
from notionai import NotionAI
from notionai.enums import ToneEnum, TranslateLanguageEnum, PromptTypeEnum
import keyboard
import pyperclip
import logging


logging.basicConfig(format='%(message)s', level=logging.INFO)
LOGGER = logging.getLogger(__name__)

TOKEN = os.getenv("NOTION_TOKEN")
SPACE_ID = os.getenv("NOTION_SPACE_ID")
AI = NotionAI(TOKEN, SPACE_ID)

@click.group()
@click.option('--copy-input-content', is_flag=True, help='Copy input content to clipboard.')
@click.option('--keyboard-output', is_flag=True, help='Output result to keyboard instead of stdout.')
@click.option('--keyboard-output-with-input', is_flag=True, help='make input content as the front part of keyboard output')
@click.option('--clipboard-output', is_flag=True, help='Copy result to clipboard.')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output.')
def cli(copy_input_content, keyboard_output, keyboard_output_with_input, clipboard_output, verbose):
    """Command line interface for Notion AI API."""
    global COPY_CONTENT, KB_OUTPUT, CLIPBOARD_OUTPUT, KEYBOARD_OUTPUT_WITH_INPUT
    COPY_CONTENT = copy_input_content
    KB_OUTPUT = keyboard_output
    CLIPBOARD_OUTPUT = clipboard_output
    KEYBOARD_OUTPUT_WITH_INPUT = keyboard_output_with_input
    if verbose:
        LOGGER.level = logging.DEBUG

def output(context, result):
    if COPY_CONTENT:
        pyperclip.copy(context)
    LOGGER.debug(f"notion ai result: {result}")
    if CLIPBOARD_OUTPUT:
        LOGGER.debug("write to clipboard")
        pyperclip.copy(result)
    if KB_OUTPUT:
        if KEYBOARD_OUTPUT_WITH_INPUT:
            LOGGER.debug("output with input")
            result = f"{context}\n{result}"
        LOGGER.debug("write to keyboard")
        keyboard.write(result)
    else:
        LOGGER.debug("write using echo")
        click.echo(result)


@cli.command()
@click.argument('tone')
@click.argument('context')
def change_tone(tone, context):
    LOGGER.debug(f"change tone to {tone}, input: {context}")
    tone_enum = ToneEnum[tone]
    resp = AI.change_tone(context, tone_enum)
    output(context, resp)

@cli.command()
@click.argument('context')
def improve_writing(context):
    LOGGER.debug(f"improve writing input: {context}")
    resp = AI.improve_writing(context)
    output(context, resp)

@cli.command()
@click.argument('context')
def continue_writing(context, page_title=""):
    LOGGER.debug(f"continue writing input, context:{context}, page_title:{page_title}")
    resp = AI.writing_with_prompt(PromptTypeEnum.continue_writing, context, page_title)
    output(context, resp)

@click.command()
@click.argument('language')
@click.argument('context')
def translate(language, context):
    LOGGER.debug(f"translate to {language}, input: {context}")
    lang_enum = TranslateLanguageEnum[language]
    resp = AI.translate(lang_enum, context)
    output(context, resp)

@click.command()
@click.argument('context')
def summarize(context):
    LOGGER.debug(f"summarize input: {context}")
    resp = AI.summarize(context)
    output(context, resp)

cli.add_command(change_tone)
cli.add_command(improve_writing)
cli.add_command(continue_writing)
cli.add_command(translate)
cli.add_command(summarize)

if __name__ == '__main__':
    cli()
