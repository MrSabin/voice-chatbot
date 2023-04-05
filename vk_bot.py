from random import randint

import vk_api as vk
from environs import Env
from vk_api.longpoll import VkEventType, VkLongPoll

from detect_intent import detect_intent_texts

LANGUAGE_CODE = 'ru-RU'


def reply(event, vk_api, project_id):
    session_id = event.user_id
    answer = detect_intent_texts(
        project_id, session_id, event.text, LANGUAGE_CODE)
    if not answer.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer.fulfillment_text,
            random_id=randint(1, 100000)
        )


if __name__ == "__main__":
    env = Env()
    env.read_env()
    vk_token = env.str("VK_TOKEN")
    project_id = env.str("PROJECT_ID")
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reply(event, vk_api, project_id)