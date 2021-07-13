from os import environ
# NOTE: LINEは一旦やめる
# from linebot import LineBotApi
# from linebot.models import TextSendMessage
from slack_sdk.web import WebClient
from slack_sdk.errors import SlackApiError
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name, get_slot_value


# 環境変数から設定値を取得
# channel_access_token = environ.get("LINE_CHANNEL_ACCESS_TOKEN")
# line_group_id = environ.get("LINE_GROUP_ID")
alexa_skill_id = environ.get("ALEXA_SKILL_ID")
slack_token = environ.get("SLACK_TOKEN")
conversation_id = environ.get("SLACK_CONVERSATION_ID")

# LINE BOT API
# line_bot_api = LineBotApi(channel_access_token)

# Slack API Client
slack_client = WebClient(token=slack_token)


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
            # line_bot_api.push_message(line_group_id, TextSendMessage(text=message_body))

            # Slackに送信
            try:
                slack_client.chat_postMessage(
                    text=message_body, channel=conversation_id
                )
                speech_text = "{}を送信します。".format(message_body)
            except SlackApiError:
                speech_text = "Slackでメッセージ送信に失敗しました。"
        else:
            speech_text = "すみません、メッセージを取得できませんでした。"

        return handler_input.response_builder.speak(speech_text).response


class ReceiveMessageIntentHandler(AbstractRequestHandler):
    """メッセージ受信インテント用ハンドラー"""

    INTENT_NAME = "ReceiveMessageIntent"

    def can_handle(self, handler_input):
        return is_intent_name(self.INTENT_NAME)(handler_input)

    def handle(self, handler_input):
        speech_text = "すみません、メッセージを取得できませんでした。"
        try:
            # Slackで最新のメッセージのみ取得
            response = slack_client.conversations_history(
                channel=conversation_id, inclusive=True, limit=1
            )
            message = response.get("messages")[0].get("text")
            if message:
                speech_text = "最新のメッセージは{}です。".format(message)
        except SlackApiError:
            speech_text = "Slackでメッセージの受信に失敗しました。"
        return handler_input.response_builder.speak(speech_text).response


# Alexaスキルのハンドラ設定
sb = SkillBuilder()

# スキルIDを設定
sb.skill_id = alexa_skill_id

# すべてのリクエストハンドラーをスキルに追加
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SendMessageIntentHandler())
sb.add_request_handler(ReceiveMessageIntentHandler())

# Lambdaに登録するLambdaハンドラーを提示
lambda_handler = sb.lambda_handler()
