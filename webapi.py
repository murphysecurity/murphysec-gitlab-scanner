# -*- coding:utf-8 -*-
from fastapi import FastAPI, Header, Request, Response
import uvicorn
import hmac
from libs.git import MyGitlab
from libs.murphy import MurphyScan
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
import configs

app = FastAPI()
APP_NAME = "webhook-listener"
WEBHOOK_SECRET = "My precious"


class WebhookData(BaseModel):
    username: str
    data: dict
    event: str
    timestamp: datetime
    model: str
    request_id: UUID


@app.post("/gitlab/webhook")
async def webhook(
    request: Request,
    response: Response,
    content_length: int = Header(...),
    x_hook_signature: str = Header(None)
):
    if content_length > 1000000:
        response.status_code = 400
        return {"result": "Content too long"}
    if x_hook_signature:
        raw_input = await request.body()
        input_hmac = hmac.new(
            key=WEBHOOK_SECRET.encode(),
            msg=raw_input,
            digestmod="sha512"
        )
        if not hmac.compare_digest(input_hmac.hexdigest(), x_hook_signature):
            #logger.error("Invalid message signature")
            response.status_code = 400
            return {"result": "Invalid message signature"}
        #logger.info("Message signature checked ok")
    else:
        pass
        #logger.info("No message signature to check")
    body = await request.json()
    if body['event_name'] == 'event_name':
        branch = body['body'].split('/')[-1]
        user_name = body['user_name']
        git_http_url = body['git_http_url']
        my_gl = MyGitlab(addr=configs.gitlab.address, token=configs.gitlab.token)
        mf = MurphyScan(token=configs.murphy.token)
        path = my_gl.clone_branch(git_http_url, branch)
        scan_res = mf.scan(path)
        my_gl.del_code(path)
    else:
        pass
    return {"result": "ok"}


if __name__ == "__main__":
    uvicorn.run("webapi:app", host="0.0.0.0", port=8888)
