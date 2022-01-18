import json
import os
from google.cloud import dialogflow
from dotenv import load_dotenv


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
    intent = dialogflow.Intent(display_name=display_name, training_phrases=training_phrases, messages=[message])
    intents_client.create_intent(request={"parent": parent, "intent": intent})


def read_json(path_json):
    with open(path_json, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    load_dotenv()
    path_json_config = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    path_json_intent = 'questions.json'
    training_phrases = read_json(path_json_intent)
    project_id = read_json(path_json_config)['project_id']

    for phrase, examples in training_phrases.items():
        questions_for_phrase = examples['questions']
        answer_for_phrase = examples['answer']
        create_intent(project_id, phrase, questions_for_phrase, answer_for_phrase)


if __name__ == '__main__':
    main()
