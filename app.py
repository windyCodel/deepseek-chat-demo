import os
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from lunardate import LunarDate

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
2. 你的回答必须使用简体中文，语言温和、结构清晰。
3. 玄学内容仅供传统文化、娱乐和自我反思参考，不能说成绝对事实。
4. 你不能替代医学、法律、金融、心理治疗等专业建议。
5. 不要制造恐惧，不要说“你一定会怎样”，多使用“可能倾向于”“可以作为参考”。

信息收集规则：
1. 不要一次性列出很多问题。
2. 如果需要补充信息，每次最多只问 1 个核心问题。
3. 用户回答后，再继续问下一步需要的信息。
4. 如果用户只是问通用运势，例如“今年运势怎么样”“2026年整体趋势”，可以直接给通用分析，不要强制索要出生信息。
5. 如果用户想做个人精准分析，再一步步收集信息。
6. 如果用户问八字或个人运势，信息收集顺序为：
   第一步：询问出生日期，并说明公历或农历都可以。
   第二步：询问出生时间。
   第三步：询问出生地。
   第四步：询问性别。
   第五步：询问重点关注方向，例如事业、财运、感情、健康或整体。
7. 如果用户问塔罗，先只询问一个具体问题，例如“你想看感情、事业还是某个人的想法？”
8. 如果用户问风水，先只询问房屋类型或想看的区域，例如“你想看客厅、卧室、办公室还是整体布局？”
9. 如果用户问择日，先只询问具体事项，例如搬家、结婚、开业、签约等。
10. 当信息不足时，不要长篇解释，只需要简短说明下一步需要什么。

回答方式：
1. 普通回答要简洁，不要太长。
2. 如果是在收集信息，只用一句话提问，不要使用分段标题。
3. 不要一次输出超过 5 个要点，除非用户要求详细分析。
4. 不要使用 Markdown 加粗标题，例如不要输出 **一、基础判断**。
5. 只有当用户明确要求详细分析，或者信息已经收集完整后，才使用以下结构：
一、基础判断
二、关键影响因素
三、可能趋势
四、建议与注意事项
五、补充说明
"""

LUNAR_MONTH_NAMES = [
    "",
    "正月", "二月", "三月", "四月", "五月", "六月",
    "七月", "八月", "九月", "十月", "冬月", "腊月"
]

LUNAR_DAY_NAMES = [
    "",
    "初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
    "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
    "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"
]

WEEKDAY_NAMES = ["一", "二", "三", "四", "五", "六", "日"]


def get_current_calendar_context(timezone_name: str | None = None):
    if not timezone_name:
        timezone_name = "Asia/Shanghai"

    try:
        user_tz = ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError:
        user_tz = ZoneInfo("Asia/Shanghai")
        timezone_name = "Asia/Shanghai"

    now = datetime.now(user_tz)

    solar_date_text = now.strftime("%Y年%m月%d日")
    weekday_text = WEEKDAY_NAMES[now.weekday()]

    lunar = LunarDate.fromSolarDate(now.year, now.month, now.day)

    leap_text = "闰" if lunar.isLeapMonth else ""
    lunar_month_text = LUNAR_MONTH_NAMES[lunar.month]
    lunar_day_text = LUNAR_DAY_NAMES[lunar.day]

    lunar_date_text = f"农历{lunar.year}年{leap_text}{lunar_month_text}{lunar_day_text}"

    return {
        "timezone_name": timezone_name,
        "solar_year": now.year,
        "solar_date_text": solar_date_text,
        "weekday_text": weekday_text,
        "lunar_year": lunar.year,
        "lunar_date_text": lunar_date_text,
    }


def detect_calendar_need(text: str) -> str:
    """
    返回值：
    none  = 不需要日期
    solar = 只需要公历
    lunar = 需要农历，通常也同时需要公历
    both  = 公历和农历都需要
    """
    if not text:
        return "none"

    text = text.strip()

    lunar_keywords = [
        "农历", "阴历", "黄历", "择日", "吉日", "良辰",
        "八字", "四柱", "大运", "流年", "生肖", "属相",
        "节气", "立春", "命理", "紫微", "卦", "起卦",
        "搬家", "结婚", "开业", "入宅", "安床", "祭祀"
    ]

    solar_keywords = [
        "今天", "明天", "后天", "昨天",
        "今年", "明年", "去年",
        "本月", "这个月", "下个月", "上个月",
        "日期", "几号", "星期", "周几",
        "公历", "阳历", "生日", "现在", "当前"
    ]

    has_lunar = any(k in text for k in lunar_keywords)
    has_solar = any(k in text for k in solar_keywords)

    if has_lunar and has_solar:
        return "both"

    if has_lunar:
        return "lunar"

    if has_solar:
        return "solar"

    return "none"


def build_runtime_system_prompt(user_text: str, timezone_name: str | None = None) -> str:
    calendar_need = detect_calendar_need(user_text)

    if calendar_need == "none":
        return AGENT_SYSTEM_PROMPT

    calendar_context = get_current_calendar_context(timezone_name)

    solar_info = (
        f"\n\n当前公历日期信息：\n"
        f"1. 当前用户时区：{calendar_context['timezone_name']}。\n"
        f"2. 当前公历日期：{calendar_context['solar_date_text']}，星期{calendar_context['weekday_text']}。\n"
        f"3. 当前公历年份：{calendar_context['solar_year']}年。\n"
        f"4. 当用户说“今年”时，如果没有特别说明，默认指当前用户时区下的公历年份：{calendar_context['solar_year']}年。"
    )

    lunar_info = (
        f"\n\n当前农历日期信息：\n"
        f"1. 当前农历日期：{calendar_context['lunar_date_text']}。\n"
        f"2. 当前农历年份：农历{calendar_context['lunar_year']}年。\n"
        f"3. 当用户说“农历今年”“流年”“生肖年”“命理年份”时，需要参考当前农历日期。\n"
        f"4. 八字、四柱、流年、节气换年可能涉及立春分界；如果没有排盘工具，不要武断判断，需要提示用户提供出生年月日、出生时间、出生地。"
    )

    if calendar_need == "solar":
        return AGENT_SYSTEM_PROMPT + solar_info

    if calendar_need == "lunar":
        return AGENT_SYSTEM_PROMPT + solar_info + lunar_info

    if calendar_need == "both":
        return AGENT_SYSTEM_PROMPT + solar_info + lunar_info

    return AGENT_SYSTEM_PROMPT


app = FastAPI()


class ChatRequest(BaseModel):
    messages: list
    timezone: str | None = None


@app.get("/", response_class=HTMLResponse)
async def index():
    return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>筮渡 AI - 传统文化分析助手</title>
    <style>
        * {
            box-sizing: border-box;
        }

        html {
            height: 100%;
        }

        body {
            font-family: Arial, "Microsoft YaHei", sans-serif;
            background: #f5f5f5;
            margin: 0;
            padding: 24px 12px;
            min-height: 100%;
        }

        .container {
            width: min(760px, 100%);
            margin: 16px auto;
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 0 12px rgba(0,0,0,0.08);
        }

        h2 {
            margin-top: 0;
            margin-bottom: 16px;
            font-size: 22px;
            line-height: 1.35;
        }

        #chatBox {
            height: 480px;
            max-height: calc(100vh - 220px);
            min-height: 320px;
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
            overflow-wrap: anywhere;
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
            text-align: left;
            word-break: break-word;
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
            min-width: 0;
            width: 100%;
            padding: 10px;
            font-size: 15px;
            line-height: 1.5;
            resize: none;
            border: 1px solid #ddd;
            border-radius: 8px;
        }

        button {
            width: 100px;
            min-height: 44px;
            font-size: 16px;
            cursor: pointer;
            border: 0;
            border-radius: 8px;
            background: #1a73e8;
            color: white;
        }

        .small-btn {
            width: 100px;
            height: 36px;
            margin-top: 10px;
            background: #eeeeee;
            color: #333;
        }

        @media (max-width: 600px) {
            body {
                background: white;
                padding: 0;
            }

            .container {
                display: flex;
                flex-direction: column;
                width: 100%;
                min-height: 100vh;
                min-height: 100dvh;
                margin: 0;
                padding: 14px;
                border-radius: 0;
                box-shadow: none;
            }

            h2 {
                font-size: 20px;
                margin-bottom: 12px;
            }

            #chatBox {
                flex: 1;
                height: auto;
                min-height: 0;
                max-height: none;
            }

            .bubble {
                max-width: 92%;
            }

            .input-row {
                flex-direction: column;
            }

            #userInput {
                height: 88px;
                font-size: 16px;
            }

            button,
            .small-btn {
                width: 100%;
            }

            .small-btn {
                height: 42px;
                margin-top: 8px;
            }
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
                        messages: messages,
                        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
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

        latest_user_text = ""
        for m in reversed(normal_messages):
            if m.get("role") == "user":
                latest_user_text = m.get("content", "")
                break

        runtime_system_prompt = build_runtime_system_prompt(latest_user_text, req.timezone)

        final_messages = [
            {
                "role": "system",
                "content": runtime_system_prompt
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
