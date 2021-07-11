# alexa-messenger

Alexaスキルを使用してLINEにメッセージを送信するためのLambda関数です。

AlexaスキルのエンドポイントにLambdaのARNを設定することで呼び出しています。

AWSのSAMをコマンドラインで操作してbuildやdeployを行います。

## Set profile

```
$ aws configure --profile {YOUR_PROFILE} 
```

## Environment variables

direnvの使用を推奨します。

SAMでLambdaに環境変数を渡すために `--parameter-overrides` オプションを使用します。

```
$ export ALEXA_SKILL_ID={YOUR_ALEXA_SKILL_ID}
$ export LINE_CHANNEL_ACCESS_TOKEN={YOUR_LINE_CHANNEL_ACCESS_TOKEN}
$ export LINE_GROUP_ID={YOUR_LINE_GROUP_ID}
```

## Build

```
$ sam build
```

## Deploy

```
$ sam deploy --profile {YOUR_PROFILE} \
  --parameter-overrides \
    AlexaSkillId=$ALEXA_SKILL_ID \
    LineChannelAccessToken=$LINE_CHANNEL_ACCESS_TOKEN \
    LineGroupId=$LINE_GROUP_ID
```
