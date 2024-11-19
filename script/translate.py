from deep_translator import GoogleTranslator


class Translate:

    @staticmethod
    def translate_google(text_, language, from_language="auto"):
        return GoogleTranslator(source=from_language, target=language).translate_batch(text_)

    @staticmethod
    def translate_google_single(text_, language, from_language="auto"):
        return GoogleTranslator(source=from_language, target=language).translate(text_)
