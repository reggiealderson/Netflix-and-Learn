import textacy
import googletrans
import textblob

def get_lang_model(language):
    
    if language == 'German':
        de = textacy.load_spacy_lang("de_core_news_sm", disable=("parser",))
        textacy_lang = de

    return textacy_lang 

def get_translation(language, dialogue_input):
    
    if language == 'German':
        textblob_string = textblob.TextBlob(dialogue_input)

        textblob_string_translated = textblob_string.translate(from_lang="de", to="en")

    return textblob_string_translated 

