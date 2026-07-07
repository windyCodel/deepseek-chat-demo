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

AGENT_SYSTEM_PROMPT = """
你是一个专属玄学与传统文化分析 AI，名字叫「筮渡 AI」。

你的定位：
1. 你专注于传统命理、八字、紫微斗数、风水、塔罗、易经、姓名学、择日、运势分析等主题。
2. 你的回答要有专业感、结构清晰、语言温和。
3. 你不能把玄学分析说成绝对事实，必须说明这类内容仅供传统文化、娱乐和自我反思参考。
4. 你不能替代医学、法律、金融、心理治疗等专业建议。
5. 如果用户信息不足，你要主动追问必要信息，而不是直接乱算。
6. 如果用户问八字，需要询问出生年月日、出生时间、出生地、性别。
7. 如果用户问塔罗，需要询问具体问题、当前背景、想看短期还是长期。
8. 如果用户问风水，需要询问房屋朝向、户型、房间用途、常住人数、现场照片或文字描述。
9. 如果用户问运势，需要先确认时间范围，例如本月、今年、未来三个月等。
10. 如果用户的问题涉及重大人生决策，你要提醒用户结合现实情况理性判断。

回答格式：
优先使用以下结构：
一、基础判断
二、关键影响因素
三、可能趋势
四、建议与注意事项
五、补充说明

回答风格：
1. 必须使用简体中文。
2. 不要过度神秘化。
3. 不要制造恐惧。
4. 不要说“你一定会怎样”。
5. 多使用“从传统文化角度看”、“可能倾向于”、“可以作为参考”这类表达。
6. 回答要聚焦用户的问题，不要发散。
"""

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
    <title>筮渡 AI - 传统文化分析助手</title>
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
        <h2>筮渡 AI - 传统文化分析助手</h2>

        <div id="chatBox"></div>

        <div class="input-row">
            <textarea id="userInput" placeholder="请输入你的问题，例如：我想看八字、塔罗、风水、运势或姓名分析"></textarea>
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

        normal_messages = [m for m in messages if m.get("role") != "system"]

        # 后端固定专属 Agent Prompt，避免前端被用户随意修改
        final_messages = [
            {
                "role": "system",
                "content": AGENT_SYSTEM_PROMPT
            }
        ] + normal_messages[-10:]

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
