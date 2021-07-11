from os import environ
from linebot import LineBotApi
from linebot.models import TextSendMessage
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name, get_slot_value


# 環境変数から設定値を取得
channel_access_token = environ.get("LINE_CHANNEL_ACCESS_TOKEN")
line_group_id = environ.get("LINE_GROUP_ID")
alexa_skill_id = environ.get("ALEXA_SKILL_ID")

# LINE BOT API
line_bot_api = LineBotApi(channel_access_token)


class LaunchRequestHandler(AbstractRequestHandler):
    """スキルを起動するハンドラー"""

    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speech_text = "メッセンジャーを起動します。"
        re_prompt_text = "メッセージは○○です、と言ってみてください。"
        # NOTE: askをつけることでsessionを継続できる
        return (
            handler_input.response_builder.speak(speech_text)
            .ask(re_prompt_text)
            .response
        )


class SendMessageIntentHandler(AbstractRequestHandler):
    """メッセージ送信インテント用ハンドラー"""

    INTENT_NAME = "messageBodyIntent"
    SLOT_NAME = "messageBodySlot"

    def can_handle(self, handler_input):
        return is_intent_name(self.INTENT_NAME)(handler_input)

    def handle(self, handler_input):
        message_body = get_slot_value(
            handler_input=handler_input, slot_name=self.SLOT_NAME
        )

        if message_body:
            line_bot_api.push_message(line_group_id, TextSendMessage(text=message_body))
            speech_text = "{}を送信します。".format(message_body)
        else:
            speech_text = "すみません、メッセージを取得できませんでした。"

        return handler_input.response_builder.speak(speech_text).response


# Alexaスキルのハンドラ設定
sb = SkillBuilder()

# スキルIDを設定
sb.skill_id = alexa_skill_id

# すべてのリクエストハンドラーをスキルに追加
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SendMessageIntentHandler())

# Lambdaに登録するLambdaハンドラーを提示
lambda_handler = sb.lambda_handler()
