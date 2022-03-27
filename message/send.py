#!/usr/bin/env python3
import logging
import requests
import json
from string import Template


def getMsgContent(send_data):
    with open("configers/template.json") as f:
        msg_template = f.read()
    temp_Template = Template(msg_template)

    for key, value in send_data.items():
        if value is None or not value:
            send_data[key] = "-"

    msg = temp_Template.substitute(
        comment_time=send_data.get("comment_time", "-"),
        user=send_data.get("user", "-"),
        repo=send_data.get("repo", "-"),
        content=send_data.get("content", "-"),
        issues_link=send_data.get("issues_link", "https://github.com")
    )
    try:
        content = json.loads(msg, strict=False)
        return content
    except Exception as e:
        logging.error(f"Get msg content failed. {str(e)} {str(send_data)}")
    return


class LarkRobot:
    def __init__(self, webhook):
        self.webhook = webhook

    def sendMsg(self, send_data):
        content = getMsgContent(send_data)
        if not content:
            logging.error(f"Get msg failed: {send_data}")
        try:
            post_body = {
                "msg_type": "interactive",
                "card": content
            }
            req = requests.post(self.webhook, data=json.dumps(post_body))
            logging.info(f"Send msg status: {req.status_code} {req.text}")
            return req
        except Exception as e:
            logging.error(f"Send msg failed: {str(e)} - {content}")
        return

def send_msg(comment_time, user, repo, content, issues_link):
    wk = "https://open.feishu.cn/open-apis/bot/v2/hook/e003eada-b96d-4a1c-ab9f-72556ad35adf"
    robot = LarkRobot(wk)
    msg = {
        "comment_time": comment_time,
        "user": user,
        "repo": repo,
        "content": content,
        "issues_link": issues_link
    }
    robot.sendMsg(msg)