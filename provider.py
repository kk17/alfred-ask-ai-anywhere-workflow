import abc
import os
import logging

from notionai import NotionAI
from typing import List
import llms
from notionai.enums import ToneEnum, TranslateLanguageEnum, PromptTypeEnum
import asyncio

from sydney import SydneyClient

LOGGER = logging.getLogger("ask_ai")

PYLLM_PROVODERS = [
    "openai",
    "anthropic",
    "ai21",
    "cohere",
    "alephalpha",
    "huggingface_hub",
    "google",
]
OTHER_PROVIDERS = [
    "notionai",
    "bingchat",
]
PROVODERS = PYLLM_PROVODERS + OTHER_PROVIDERS

class AIProvider(abc.ABC):

    @abc.abstractmethod
    def complete(self, prompt: str, **kwargs) -> str:
        pass

    def complete_and_remove_prompt(self, prompt: str, **kwargs) -> str:
        result = self.complete(prompt, **kwargs)
        if result.startswith(prompt):
            result = result[len(prompt):]
        return result

    def change_tone(self, tone: str, context: str):
        promt = f"Change the tone to {tone}:\n{context}"
        return self.complete_and_remove_prompt(promt)

    def improve_writing(self, context):
        promt = f"Improve the writing:\n{context}"
        return self.complete_and_remove_prompt(promt)

    def continue_writing(self, context, page_title=""):
        promt = f"Continue writing:\n{context}"
        return self.complete_and_remove_prompt(promt)

    def translate(self, language, context):
        promt = f"Translate to {language}:\n{context}"
        return self.complete_and_remove_prompt(promt)

    def summarize(self, context):
        promp = f"Summarize:\n{context}"
        return self.complete_and_remove_prompt(promp)

    @classmethod
    def _build_one(cls, model_provoder: str):
        provider = model_provoder.split("_", 1)[0]
        if provider in PYLLM_PROVODERS:
            model = model_provoder.split("_", 1)[1]
            return PyLLMProvider(provider, model)
        elif provider == "notionai":
            return NotionAIProvider()
        elif provider == "bingchat":
            style = model_provoder.split("_", 1)[1]
            return BingChatProvider(style)
        else:
            raise Exception(f"not support provider {provider}")

    @classmethod
    def build(cls, provoders: List[str]):
        if len(provoders) == 1:
            return AIProvider._build_one(provoders[0])
        else:
            return MultiProvider(provoders)


class NotionAIProvider(AIProvider):

    def __init__(self):
        self.name = "notionai"
        TOKEN = os.getenv("NOTION_TOKEN")
        SPACE_ID = os.getenv("NOTION_SPACE_ID")
        if not TOKEN:
            LOGGER.error("NOTION_TOKEN is not set")
        if not SPACE_ID:
            LOGGER.error("NOTION_SPACE_ID is not set")
        logging.debug(f"Create NotionAIProvider with token {TOKEN} and space id {SPACE_ID}")
        self.ai = NotionAI(TOKEN, SPACE_ID)

    def complete(self, prompt: str, **kwargs) -> str:
        return self.ai.writing_with_prompt(PromptTypeEnum.continue_writing,
                                           context=prompt,
                                           **kwargs)
    
    def improve_writing(self, context):
        return self.ai.improve_writing(context)

    def continue_writing(self, context, page_title=""):
        return self.ai.continue_write(context)

    def translate(self, language, context):
        language_enum = TranslateLanguageEnum(language)
        return self.ai.translate(language_enum, context)

    def summarize(self, context):
        return self.ai.summarize(context)

class BingChatProvider(AIProvider):
    def __init__(self, style):
        self.name = "bingchat"
        LOGGER.debug(f"Create BingChatProvider with style {style}")
        self.sydney = SydneyClient(style=style)

    async def _async_complete(self, prompt: str, **kwargs) -> str:
        await self.sydney.start_conversation()
        result  = await self.sydney.ask(prompt, citations=False)
        # self.sydney.reset_conversation()
        return result
    
    def complete(self, prompt: str, **kwargs) -> str:
        answer = asyncio.run(self._async_complete(prompt, **kwargs))
        return answer

class PyLLMProvider(AIProvider):

    def __init__(self, provider:str, model: str):
        self.name = f"{provider}_{model}"
        LOGGER.debug(f"Create PyLLMProvider with provider {provider} and model {model}")
        self.ai = llms.init(model)

    def complete(self, prompt: str, **kwargs) -> str:
        return self.ai.complete(prompt, **kwargs).text


class MultiProvider(AIProvider):
    def __init__(self, providers: List[str]):
        self.providers = [AIProvider._build_one(p) for p in providers]
    
    def complete(self, prompt: str, **kwargs) -> str:
        results = []
        for provider in self.providers:
            results.append(f"{provider.name}:")
            results.append(provider.complete(prompt, **kwargs))
        return "\n".join(results)