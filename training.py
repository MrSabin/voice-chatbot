import argparse
import json

from environs import Env
from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts,
                  message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases,
        messages=[message],
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print(f"Intent created: {response}")


def main():
    env = Env()
    env.read_env()
    project_id = env.str("PROJECT_ID")

    parser = argparse.ArgumentParser(description="Script for batch create DialogFlow intents")
    parser.add_argument(
        "--json_path",
        help="Folder with JSON file",
        default="questions.json",
    )
    args = parser.parse_args()
    with open(args.json_path, "r") as questions:
        dump = json.load(questions)
    for group_name, phrases in dump.items():
        questions = phrases["questions"]
        answer = [phrases["answer"]]
        create_intent(project_id, group_name, questions, answer)


if __name__ == "__main__":
    main()