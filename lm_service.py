import logging
import dspy

LOGGER = logging.getLogger("ask_ai")


class LMService:

    def __init__(self, lm_model: str):
        self.lm_model = lm_model
        self.lm = dspy.LM(model=lm_model)
        dspy.configure(lm=self.lm)

    def change_tone(self, tone: str, context: str):
        _change_tone = dspy.Predict(
            dspy.Signature("tone, input_text -> ouput_text").with_instructions(
                "tranfer the tone of the input text to the tone specified in the tone parameter"
            ))
        return _change_tone(tone=tone, input_text=context).ouput_text

    def improve_writing(self, context):
        _improve_writing = dspy.Predict(
            dspy.Signature("input_text -> ouput_text").with_instructions(
                "improve the writing of the input text"))
        return _improve_writing(input_text=context).ouput_text

    def continue_writing(self, context, page_title=None):
        _continue_writing = dspy.Predict(
            dspy.Signature("input_text, page_title:Optional[str] -> ouput_text"
                           ).with_instructions(
                               "continue writing the input text"))
        return _continue_writing(input_text=context,
                                 page_title=page_title).ouput_text

    def translate(self, language, context):
        _translate = dspy.Predict(
            dspy.Signature("text, target_language -> translation"))
        return _translate(text=context, target_language=language).translation

    def summarize(self, context):
        _summarize = dspy.Predict(dspy.Signature("text -> summary"))
        return _summarize(text=context).summary

    def chat(self, context):
        return self.lm(context)[0]
