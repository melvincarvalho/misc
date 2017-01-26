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

SLACK_CLIENT_ID = os.getenv("SLACK_CLIENT_ID", "6915687573.133727880087")
SLACK_CLIENT_SECRET = os.getenv("SLACK_CLIENT_SECRET", "86fbee294e8c48abd6d892eb5577375f")

SLACK_BOT_ACCESS_TOKEN = os.getenv("SLACK_BOT_ACCESS_TOKEN", "")
SLACK_TEAM_ID = os.getenv("SLACK_TEAM_ID", "")

app = Flask(__name__)

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
    return make_response("ok", 200)

@app.route("/ping", methods=["GET","POST"])
def base():
    print "DICT: %s" % (request.__dict__,)
    print "\nDATA: %s" % (request.data,)
    print "\n\nFORM: %s" % (request.form,)
    print "\n\nrequest.url: %s" % (request.url,)
    return make_response("ok", 200)

if __name__ == "__main__":
    app.run(debug=True, port=8095)
