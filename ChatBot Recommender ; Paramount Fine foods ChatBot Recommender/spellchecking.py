from rasa.nlu.components import Component
from rasa.nlu import utils
from rasa.nlu.model import Metadata
import pickle
from spellchecker import SpellChecker


class CorrectSpelling(Component):

    name = "Spell_checker"
    provides = ["message"]
    requires = ["message"]
    language_list = ["en"]

    def __init__(self, component_config=None):
        super(CorrectSpelling, self).__init__(component_config)

    def train(self, training_data, cfg, **kwargs):
        """Not needed, because the the model is pretrained"""
        pass

    def process(self, message, **kwargs):
        """Retrieve the text message, do spelling correction word by word,
        then append all the words and form the sentence,
        pass it to next component of pipeline"""

        try:
            textdata = message.data['text']

            with open('spell_checker_model', 'rb') as f:
                clf = pickle.load(f)
            textdata = textdata.split()
            new_message = ' '.join(clf.correction(word) for word in textdata)
            message.data['text'] = new_message
        except KeyError:
            pass

    def persist(self,file_name, model_dir):
        """Pass because a pre-trained model is already persisted"""
        pass