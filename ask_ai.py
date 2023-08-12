import click
import os
import pyperclip
import logging
import platform
from pynput.keyboard import Key, Controller
from provider import AIProvider

logging.basicConfig(format='%(message)s', level=logging.INFO)
LOGGER = logging.getLogger("ask_ai")

keyboard = Controller()

MODEL_CHOICES = [
    "notionai",
    # "openai",
    "openai_gpt-3.5-turbo",
    "openai_gpt-4",
    "openai_text-davinci-003",
    # "bingchat_creative",
    # "bingchat_precise",
    # "bingchat_balanced",
    # "ai21_j2-grande-instruct",
    # "ai21_j2-jumbo-instruct",
    # "alephalpha_luminous-base",
    # "alephalpha_luminous-extended",
    # "alephalpha_luminous-supreme",
    # "alephalpha_luminous-supreme-control",
    # "anthropic_claude-2",
    # "anthropic_claude-instant-1",
    # "anthropic_claude-instant-v1",
    # "anthropic_claude-instant-v1.1",
    # "anthropic_claude-v1",
    # "anthropic_claude-v1-100k",
    # "cohere_command",
    # "cohere_command-nightly",
    # "google_chat-bison",
    # "google_text-bison",
    # "huggingfacehub_hf_dolly",
    # "huggingfacehub_hf_falcon40b",
    # "huggingfacehub_hf_falcon7b",
    # "huggingfacehub_hf_llava",
    # "huggingfacehub_hf_mptchat",
    # "huggingfacehub_hf_mptinstruct",
    # "huggingfacehub_hf_pythia",
    # "huggingfacehub_hf_vicuna",
]


@click.group()
@click.option('--model-provider',
              is_flag=False,
              help='LLM provider, support notionai, openai',
              type=click.Choice(MODEL_CHOICES),
              multiple=True,
              default=['notionai'])
@click.option('--input-to-clipboard',
              is_flag=True,
              help='Copy input content to clipboard.')
@click.option('--combine-input-into-result',
              is_flag=True,
              help='Combine input content into result.')
@click.option('--result-to-keyboard',
              is_flag=True,
              help='Output result to keyboard instead of stdout.')
@click.option('--result-to-clipboard',
              is_flag=True,
              help='Copy result to clipboard.')
@click.option('--paste-result',
              is_flag=True,
              help='Paste result from clipboard.')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output.')
def cli(model_provider, input_to_clipboard, combine_input_into_result,
        result_to_keyboard, result_to_clipboard, paste_result, verbose):
    """Command line interface for Notion AI API."""
    global AI, INPUT_TO_CLIPBOARD, COMBINE_INPUT_INTO_RESULT, RESULT_TO_KEYBOARD, RESULT_TO_CLIPBOARD, PASTE_RESULT
    AI = AIProvider.build(model_provider)
    INPUT_TO_CLIPBOARD = input_to_clipboard
    COMBINE_INPUT_INTO_RESULT = combine_input_into_result
    RESULT_TO_KEYBOARD = result_to_keyboard
    RESULT_TO_CLIPBOARD = result_to_clipboard
    PASTE_RESULT = paste_result
    if verbose:
        LOGGER.level = logging.DEBUG


def output(context, result):
    if INPUT_TO_CLIPBOARD:
        pyperclip.copy(context)
    LOGGER.debug(f"notion ai result: {result}")
    if COMBINE_INPUT_INTO_RESULT:
        LOGGER.debug("output with input")
        result = f"{context}\n{result}"
    if RESULT_TO_CLIPBOARD:
        LOGGER.debug("write to clipboard")
        pyperclip.copy(result)
    if RESULT_TO_KEYBOARD:
        LOGGER.debug("write to keyboard")
        keyboard.type(result)
    if PASTE_RESULT:
        LOGGER.debug("paste result from clipboard")
        if platform.system() == 'Darwin':
            with keyboard.pressed(Key.cmd):
                keyboard.press('v')
                keyboard.release('v')
        else:
            with keyboard.pressed(Key.ctrl):
                keyboard.press('v')
                keyboard.release('v')
    else:
        LOGGER.debug("write using echo")
        click.echo(result)


@cli.command()
@click.argument('tone')
@click.argument('context')
def change_tone(tone, context):
    LOGGER.debug(f"change tone to {tone}, input: {context}")
    resp = AI.change_tone(context, tone)
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
    LOGGER.debug(
        f"continue writing input, context:{context}, page_title:{page_title}")
    resp = AI.continue_writing(context, page_title)
    output(context, resp)


@click.command()
@click.argument('language')
@click.argument('context')
def translate(language, context):
    LOGGER.debug(f"translate to {language}, input: {context}")
    resp = AI.translate(language, context)
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
