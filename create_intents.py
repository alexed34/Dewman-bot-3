import json
import os
from dotenv import load_dotenv
from google.cloud import dialogflow

load_dotenv()


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Заполняем тренировочные фразы в dialogflow"""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    message_texts = {message_texts}
    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)
    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )
    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )
    print("Intent created: {}".format(response))


def writer_json(path_json):
    with open(path_json, 'r', encoding='utf-8') as f:
        text_json = json.load(f)
    return text_json


def main():
    path_json_config = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    path_json_intent = 'questions.json'

    training_phrases = writer_json(path_json_intent)
    project_id = writer_json(path_json_config)['project_id']

    for key in training_phrases.keys():
        display_name = key
        training_phrases_parts = training_phrases[key]['questions']
        message_texts = (training_phrases[key]['answer'])
        create_intent(project_id, display_name, training_phrases_parts, message_texts)
        break


if __name__ == '__main__':
    main()
