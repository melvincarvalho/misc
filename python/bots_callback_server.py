import os
import sys
import time
import logging
import datetime

from flask import Flask, request, session, render_template, jsonify, redirect, url_for, send_from_directory, jsonify, Response, make_response, render_template_string

from slackclient import SlackClient

logging.basicConfig()
log = logging.getLogger()
log.setLevel(10)

# MUST HAVE.
SLACK_CLIENT_ID = os.getenv("SLACK_CLIENT_ID", "6915687573.133727880087")
SLACK_CLIENT_SECRET = os.getenv("SLACK_CLIENT_SECRET", "86fbee294e8c48abd6d892eb5577375f")

# Must have if going to respond to events. Otherwise /slack/oauth
# can be used to get the access token and set this variable.
SLACK_BOT_ACCESS_TOKEN = os.getenv("SLACK_BOT_ACCESS_TOKEN",
                                   "xoxb-133750070710-BSsCrCYSWIjLqoQIcJB3kw8g")
# Required if messages to the bot using "@botname" need to be recognized.
# If not set, only direct messages to the bot will be recognized.
BOT_USER_ID = os.getenv("BOT_USER_ID", "U3XN222LW")
bot_user_id_token = "<@%s>" % (BOT_USER_ID,)

SLACK_TEAM_ID = os.getenv("SLACK_TEAM_ID", "")

app = Flask(__name__)
slackClient = None

# Make this call to do oauth for your bot.
# https://slack.com/oauth/authorize?scope=bot&client_id=<your app client id>

@app.route("/slack/oauth", methods=["GET","POST"])
def slack_oauth():
    log.debug("request.url: %s", request.url)
    log.debug("request.data: %s", request.data)

    if not SLACK_CLIENT_ID:
        log.error("no SLACK_CLIENT_ID available")
        return make_response(
            "could not do oauth", 200, {"X-Slack-No-Retry": 1})
    if not SLACK_CLIENT_SECRET:
        log.error("no SLACK_CLIENT_SECRET available")
        return make_response(
            "could not do oauth", 200, {"X-Slack-No-Retry": 1})
        
    codeArg = request.args.get('code')
    if not codeArg:
        log.warn("did not get 'code' to do oauth!")
        return make_response(
            "could not do oauth", 200, {"X-Slack-No-Retry": 1})
    client = SlackClient("")
    authResponse = client.api_call(
        "oauth.access",
        client_id=SLACK_CLIENT_ID,
        client_secret=SLACK_CLIENT_SECRET,
        code=codeArg
    )
    log.info("authResponse: %s", authResponse)
    teamId = authResponse["team_id"]
    botToken = authResponse["bot"]["bot_access_token"]
    SLACK_BOT_ACCESS_TOKEN = botToken
    SLACK_TEAM_ID = teamId
    fname = "/tmp/slack_credentials.%s" % (
            datetime.datetime.now().strftime("%Y%m%d-%H%M%S"),)
    with open(fname, "w") as f:
        f.write(("SLACK_BOT_ACCESS_TOKEN: %s\n"
                 "SLACK_TEAM_ID: %s\n") % (
                     SLACK_BOT_ACCESS_TOKEN, SLACK_TEAM_ID))

    return render_template_string("<html><head></head><body>Slack access confirmed.<p>Bot Access Token: %s<p>Team Id: %s</body></html>" % (botToken, teamId))

@app.route("/slack/callback", methods=["GET","POST"])
def slack_callback():
    r = request.json
    log.debug("request.json: %s", r)
    if not r:
        return make_response("no json payload found", 200)
    if "challenge" in r:
        return make_response(r["challenge"], 200)
    if "event" in r:
        slack_process_event(r)
    return make_response("ok", 200)

@app.route("/ping", methods=["GET","POST"])
def base():
    print "DICT: %s" % (request.__dict__,)
    print "\nDATA: %s" % (request.data,)
    print "\n\nFORM: %s" % (request.form,)
    print "\n\nrequest.url: %s" % (request.url,)
    return make_response("ok", 200)

def slack_process_event(r):
    # r: request.json
    # Only respond to two types of messages:
    # 1. Direct Messages
    # 2. Messages in channels directly addressed to the bot.
    e = r["event"]
    if "subtype" in e:
        log.debug("Not processing this event: %s", e)
        return
    channel = e.get("channel")
    processMsg = channel.startswith("D")
    msg = e.get("text", "")
    hasBotId = msg.find(bot_user_id_token)
    log.debug("hasBotId: %s", hasBotId)
    processMsg |= (channel.startswith("C") and hasBotId > -1)
    log.debug("processMsg: %s", processMsg)
    if processMsg:
        # Don't send back @BOT_USER_ID in the response!
        #responseMsg = " ".join(msg.split(bot_user_id_token,1))
        responseMsg = e.get("text")
        apiResult = slackClient.api_call(
            "chat.postMessage", channel=channel,
            text="Got your message: %s" % (responseMsg,))
        if not apiResult.get("ok"):
            log.error("Could not send back message: %s", apiResult)
        else:
            log.debug("sent message ok")
    else:
        log.debug("Not processing this event: %s", e)
        return
        


if __name__ == "__main__":
    global slackClient
    slackClient = SlackClient(SLACK_BOT_ACCESS_TOKEN)
    app.run(debug=False, port=8095)
