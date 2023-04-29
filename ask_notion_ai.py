import click
import os
from notionai import NotionAI
from notionai.enums import ToneEnum, TranslateLanguageEnum
import keyboard
import pyperclip
import logging


TOKEN = os.getenv("NOTION_TOKEN")
SPACE_ID = os.getenv("NOTION_SPACE_ID")

logging.basicConfig(format='%(message)s', level=logging.INFO)
LOGGER = logging.getLogger(__name__)


@click.group()
@click.option('--copy-input-content', is_flag=True, help='Copy input content to clipboard.')
@click.option('--keyboard-output', is_flag=True, help='Output result to keyboard instead of stdout.')
@click.option('--clipboard-output', is_flag=True, help='Copy result to clipboard.')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output.')
def cli(copy_input_content, keyboard_output, clipboard_output, verbose):
    """Command line interface for Notion AI API."""
    global COPY_CONTENT, KB_OUTPUT, CLIPBOARD_OUTPUT
    COPY_CONTENT = copy_input_content
    KB_OUTPUT = keyboard_output
    CLIPBOARD_OUTPUT = clipboard_output
    if verbose:
        LOGGER.level = logging.DEBUG

def copy_content_if_needed(context):
    if COPY_CONTENT:
        pyperclip.copy(context)

def output(result):
    LOGGER.debug(f"notion ai result: {result}")
    if CLIPBOARD_OUTPUT:
        LOGGER.debug("write to clipboard")
        pyperclip.copy(result)
    if KB_OUTPUT:
        LOGGER.debug("write to keyboard")
        keyboard.write(result)
    else:
        LOGGER.debug("write using echo")
        click.echo(result)


@cli.command()
@click.argument('tone')
@click.argument('context')
def change_tone(tone, context):
    ai = NotionAI(TOKEN, SPACE_ID)
    LOGGER.debug(f"change tone to {tone}, input: {context}")
    copy_content_if_needed(context)
    tone_enum = ToneEnum[tone]
    resp = ai.change_tone(context, tone_enum)
    output(resp)

@cli.command()
@click.argument('context')
def improve_writing(context):
    LOGGER.debug(f"improve writing input: {context}")
    copy_content_if_needed(context)
    ai = NotionAI(TOKEN, SPACE_ID)
    resp = ai.improve_writing(context)
    output(resp)

@click.command()
@click.argument('language')
@click.argument('context')
def translate(language, context):
    ai = NotionAI(TOKEN, SPACE_ID)
    LOGGER.debug(f"translate to {language}, input: {context}")
    copy_content_if_needed(context)
    lang_enum = TranslateLanguageEnum[language]
    resp = ai.translate(lang_enum, context)
    output(resp)

@click.command()
@click.argument('context')
def summarize(context):
    ai = NotionAI(TOKEN, SPACE_ID)
    LOGGER.debug(f"summarize input: {context}")
    copy_content_if_needed(context)
    resp = ai.summarize(context)
    output(resp)

cli.add_command(change_tone)
cli.add_command(improve_writing)
cli.add_command(translate)
cli.add_command(summarize)

if __name__ == '__main__':
    cli()
