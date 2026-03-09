from flask import Flask, request

from handlers.issue_handler import handle_issue
from handlers.pr_handler import handle_pr
from handlers.installation_handler import handle_install

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():

    event = request.headers.get("X-GitHub-Event")

    payload = request.json

    print("收到事件类型:", event)

    try:

        # Issue 事件
        if event == "issues":
            handle_issue(payload)

        # Pull Request 事件
        elif event == "pull_request":
            handle_pr(payload)

        # App 安装事件
        elif event == "installation":
            handle_install(payload)

        else:
            print("未处理的事件:", event)

    except Exception as e:
        print("处理 webhook 出错:", str(e))

    # GitHub webhook 必须返回 200
    return "", 200


if __name__ == "__main__":

    print("GitHub AI Assistant 已启动")
    print("Webhook 地址: http://127.0.0.1:5000/webhook")

    app.run(port=5000)