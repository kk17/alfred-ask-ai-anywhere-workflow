import abc
import os
from notionai import NotionAI
from typing import List
import llms
from notionai.enums import ToneEnum, TranslateLanguageEnum, PromptTypeEnum

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

    def change_tone(self, tone: str, context: str):
        promt = f"Change the tone to {tone}:\n{context}"
        return self.complete(promt)

    def improve_writing(self, context):
        promt = f"Improve the writing:\n{context}"
        return self.complete(promt)

    def continue_writing(self, context, page_title=""):
        promt = f"Continue writing:\n{context}"
        return self.complete(promt)

    def translate(self, language, context):
        promt = f"Translate to {language}:\n{context}"
        return self.complete(promt)

    def summarize(self, context):
        promp = f"Summarize:\n{context}"
        return self.complete(promp)

    @classmethod
    def _build_one(cls, model_provoder: str):
        provider = model_provoder.split("_", 1)[0]
        if provider in PYLLM_PROVODERS:
            model = model_provoder.split("_", 1)[1]
            return PyLLMProvider(provider, model)
        elif provider == "notionai":
            return NotionAIProvider()
        elif provider == "bingchat":
            return BingChatProvider()
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
        self.ai = NotionAI(TOKEN, SPACE_ID)

    def complete(self, prompt: str, **kwargs) -> str:
        return self.ai.writing_with_prompt(PromptTypeEnum.continue_writing,
                                           context=prompt,
                                           **kwargs)

class BingChatProvider(AIProvider):
    pass

class PyLLMProvider(AIProvider):

    def __init__(self, provider:str, model: str):
        self.name = f"{provider}_{model}"
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