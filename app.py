import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from openai import OpenAI


DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not DEEPSEEK_API_KEY:
    raise RuntimeError("Missing environment variable DEEPSEEK_API_KEY")


client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
    timeout=120.0,
    max_retries=1,
)

app = FastAPI()


class ChatRequest(BaseModel):
    messages: list


@app.get("/", response_class=HTMLResponse)
async def index():
    return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>DeepSeek 聊天 Demo</title>
    <style>
        body {
            font-family: Arial, "Microsoft YaHei", sans-serif;
            background: #f5f5f5;
            margin: 0;
            padding: 0;
        }

        .container {
            width: 760px;
            margin: 40px auto;
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 0 12px rgba(0,0,0,0.08);
        }

        h2 {
            margin-top: 0;
        }

        #chatBox {
            height: 480px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 12px;
            background: #fafafa;
            margin-bottom: 12px;
        }

        .msg {
            margin: 10px 0;
            line-height: 1.6;
            white-space: pre-wrap;
        }

        .user {
            text-align: right;
            color: #1a73e8;
        }

        .assistant {
            text-align: left;
            color: #222;
        }

        .bubble {
            display: inline-block;
            max-width: 85%;
            padding: 10px 12px;
            border-radius: 10px;
        }

        .user .bubble {
            background: #e8f0fe;
        }

        .assistant .bubble {
            background: #eeeeee;
        }

        .input-row {
            display: flex;
            gap: 8px;
        }

        #userInput {
            flex: 1;
            height: 70px;
            padding: 10px;
            font-size: 15px;
            resize: none;
        }

        button {
            width: 100px;
            font-size: 16px;
            cursor: pointer;
        }

        .small-btn {
            width: 100px;
            height: 36px;
            margin-top: 10px;
        }
    </style>
</head>

<body>
    <div class="container">
        <h2>DeepSeek 文字聊天 Demo</h2>

        <div id="chatBox"></div>

        <div class="input-row">
            <textarea id="userInput" placeholder="请输入你的问题，例如：帮我解释一下 FastAPI 是什么"></textarea>
            <button onclick="sendMessage()">发送</button>
        </div>

        <button class="small-btn" onclick="clearChat()">清空对话</button>
    </div>

    <script>
        let messages = [
            {
                role: "system",
                content: "你是一个中文 AI 助手。请使用简体中文回答，回答要清晰、实用。"
            }
        ];

        function addMessage(role, content) {
            const chatBox = document.getElementById("chatBox");

            const div = document.createElement("div");
            div.className = "msg " + role;

            const bubble = document.createElement("div");
            bubble.className = "bubble";
            bubble.textContent = content;

            div.appendChild(bubble);
            chatBox.appendChild(div);

            chatBox.scrollTop = chatBox.scrollHeight;
        }

        async function sendMessage() {
            const input = document.getElementById("userInput");
            const text = input.value.trim();

            if (!text) {
                return;
            }

            input.value = "";

            messages.push({
                role: "user",
                content: text
            });

            addMessage("user", text);
            addMessage("assistant", "思考中...");

            try {
                const response = await fetch("/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        messages: messages
                    })
                });

                const data = await response.json();

                const chatBox = document.getElementById("chatBox");
                chatBox.lastChild.remove();

                if (!response.ok) {
                    addMessage("assistant", data.error || "请求失败");
                    return;
                }

                messages.push({
                    role: "assistant",
                    content: data.reply
                });

                addMessage("assistant", data.reply);

            } catch (error) {
                const chatBox = document.getElementById("chatBox");
                chatBox.lastChild.remove();
                addMessage("assistant", "请求异常：" + error);
            }
        }

        function clearChat() {
            messages = [
                {
                    role: "system",
                    content: "你是一个中文 AI 助手。请使用简体中文回答，回答要清晰、实用。"
                }
            ];

            document.getElementById("chatBox").innerHTML = "";
        }

        document.getElementById("userInput").addEventListener("keydown", function(event) {
            if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        });
    </script>
</body>
</html>
"""


@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        messages = req.messages

        system_messages = [m for m in messages if m.get("role") == "system"]
        normal_messages = [m for m in messages if m.get("role") != "system"]

        # 保留 system + 最近 10 条消息，防止上下文越来越长导致 token 消耗过快
        final_messages = system_messages[:1] + normal_messages[-10:]

        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=final_messages,
            temperature=0.7,
            max_tokens=1200,
            extra_body={
                "thinking": {
                    "type": "disabled"
                }
            }
        )

        reply = response.choices[0].message.content

        return {
            "reply": reply
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": f"请求失败：{type(e).__name__}: {str(e)}"
            }
        )