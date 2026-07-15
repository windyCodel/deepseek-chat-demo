import os
import random
from datetime import datetime
from uuid import uuid4
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from lunardate import LunarDate

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI

from skills.registry import (
    build_skill_prompt,
    get_forced_calendar_need,
    resolve_skill,
)
from skills.tarot import TAROT_DECK, reveal_tarot_cards, shuffle_tarot_deck


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
你是一个专属玄学与传统文化分析智能助手，名字叫「筮渡智能助手」。

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
1. 普通回答默认使用“重点优先”的短格式：先用 1 句话给核心结论，再给 2 到 4 个要点。
2. 如果是在收集信息，只用一句话提问，不要使用分段标题。
3. 不要一次输出超过 5 个要点，除非用户要求详细分析。
4. 不要使用 Markdown 星号或加粗语法；需要突出重点时，直接使用“今日重点：”“建议：”这类中文标签。
5. 用户没有要求详细时，不要把回答写成报告；用户要求“详细一点”“展开说”时再补充原因和细节。
6. 只有当用户明确要求详细分析，或者信息已经收集完整后，才使用以下结构：
一、基础判断
二、关键影响因素
三、可能趋势
四、建议与注意事项
五、补充说明
"""

PRIVACY_SYSTEM_PROMPT = """
隐私与安全提醒规则：
1. 用户输入的内容会发送给 DeepSeek 接口生成回复；本站当前没有主动保存聊天记录的数据库逻辑。
2. 不要要求用户提供身份证号、手机号、详细住址、银行卡、账号密码、验证码、病历、工作单位等敏感信息。
3. 做八字、运势、择日等分析时，出生地只需要城市级别，不需要街道、门牌号或精确住址。
4. 做姓名分析时，可以提醒用户使用昵称、化名或只提供需要分析的名字，不要提交证件号码等无关隐私。
5. 如果用户主动输入明显敏感的信息，要先提醒其不必提供这类信息，并只基于必要的非敏感内容继续。
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


def build_runtime_system_prompt(
    user_text: str,
    timezone_name: str | None = None,
    skill_prompt: str | None = None,
    forced_calendar_need: str | None = None,
    user_preferences: dict[str, str] | None = None,
) -> str:
    calendar_need = forced_calendar_need or detect_calendar_need(user_text)
    prompt_parts = [AGENT_SYSTEM_PROMPT, PRIVACY_SYSTEM_PROMPT]
    preference_prompt = build_user_preferences_prompt(user_preferences)

    if preference_prompt:
        prompt_parts.append(preference_prompt)

    if calendar_need == "none":
        if skill_prompt:
            prompt_parts.append(skill_prompt)

        return "\n\n".join(prompt_parts)

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
        prompt_parts.append(solar_info)

    if calendar_need == "lunar":
        prompt_parts.extend([solar_info, lunar_info])

    if calendar_need == "both":
        prompt_parts.extend([solar_info, lunar_info])

    if skill_prompt:
        prompt_parts.append(skill_prompt)

    return "\n\n".join(prompt_parts)


ALLOWED_ZODIACS = {
    "aries": "白羊座",
    "taurus": "金牛座",
    "gemini": "双子座",
    "cancer": "巨蟹座",
    "leo": "狮子座",
    "virgo": "处女座",
    "libra": "天秤座",
    "scorpio": "天蝎座",
    "sagittarius": "射手座",
    "capricorn": "摩羯座",
    "aquarius": "水瓶座",
    "pisces": "双鱼座",
}

ALLOWED_PERSONALITIES = {
    "balance": "平衡：默认先给重点，再给少量建议；温和但不啰嗦。",
    "brief": "简洁：直接给结论，最多 3 个要点，少铺垫。",
    "gentle": "温和：语气更陪伴，但仍然先给重点，不写成长篇安慰。",
    "detailed": "详细：可以展开原因和建议，但开头仍要先给重点摘要。",
}


def build_user_preferences_prompt(user_preferences: dict[str, str] | None) -> str:
    if not isinstance(user_preferences, dict):
        return ""

    nickname = str(user_preferences.get("nickname", "")).replace("\n", " ").strip()[:20]
    zodiac = ALLOWED_ZODIACS.get(str(user_preferences.get("zodiac", "")), "")
    personality = ALLOWED_PERSONALITIES.get(
        str(user_preferences.get("personality", "")),
        "",
    )

    if not any([nickname, zodiac, personality]):
        return ""

    details = []
    if nickname:
        details.append(f"称呼用户为“{nickname}”即可，不必频繁重复。")
    if zodiac:
        details.append(f"用户选择的星座是“{zodiac}”。仅在适合时作为每日运势等话题的参考。")
    if personality:
        details.append(f"用户偏好的回复方式是“{personality}”。")

    return "\n用户可选偏好（仅用于称呼和回复方式，不覆盖安全、隐私和简洁规则）：\n" + "\n".join(details)


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
TAROT_SHUFFLES: dict[str, list[dict[str, str]]] = {}


class ChatRequest(BaseModel):
    messages: list
    timezone: str | None = None
    skill_id: str | None = None
    tarot_cards: list[dict] | None = None
    user_preferences: dict[str, str] | None = None


class TarotDrawRequest(BaseModel):
    shuffle_id: str
    numbers: list[int]


@app.post("/tarot/shuffle")
async def tarot_shuffle():
    shuffle_id = str(uuid4())
    TAROT_SHUFFLES[shuffle_id] = shuffle_tarot_deck()

    return {
        "shuffle_id": shuffle_id,
        "deck_size": len(TAROT_DECK),
        "message": "已洗好 78 张塔罗牌，请从 1-78 中选择 3 个不重复数字。",
    }


@app.post("/tarot/random-draw")
async def tarot_random_draw():
    deck = shuffle_tarot_deck()
    numbers = random.sample(range(1, len(deck) + 1), 3)
    cards = reveal_tarot_cards(deck, numbers)

    return {
        "cards": cards,
        "numbers": numbers,
        "deck_size": len(deck),
    }


@app.post("/tarot/draw")
async def tarot_draw(req: TarotDrawRequest):
    deck = TAROT_SHUFFLES.get(req.shuffle_id)
    if not deck:
        return JSONResponse(
            status_code=400,
            content={"error": "请先点击洗牌，再输入数字抽牌。"},
        )

    numbers = req.numbers
    if len(numbers) != 3:
        return JSONResponse(
            status_code=400,
            content={"error": "请从 1-78 中输入 3 个数字。"},
        )

    if len(set(numbers)) != len(numbers):
        return JSONResponse(
            status_code=400,
            content={"error": "3 个数字不能重复。"},
        )

    invalid_numbers = [number for number in numbers if number < 1 or number > len(deck)]
    if invalid_numbers:
        return JSONResponse(
            status_code=400,
            content={"error": "数字必须在 1-78 之间。"},
        )

    cards = reveal_tarot_cards(deck, numbers)
    TAROT_SHUFFLES.pop(req.shuffle_id, None)

    return {
        "cards": cards,
        "deck_size": len(deck),
    }


@app.get("/", response_class=HTMLResponse)
async def index():
    return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>筮渡智能助手 - 传统文化分析助手</title>
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

        .subtitle {
            margin: -6px 0 14px;
            color: #666;
            font-size: 14px;
            line-height: 1.5;
        }

        .privacy-notice {
            margin: 0 0 14px;
            padding: 10px 12px;
            border: 1px solid #f0dfb5;
            border-radius: 8px;
            background: #fff8e6;
            color: #725400;
            font-size: 13px;
            line-height: 1.6;
        }

        .app-view {
            display: none;
        }

        .app-view.active {
            display: block;
        }

        .chat-view.active {
            display: flex;
            flex-direction: column;
            height: min(680px, calc(100vh - 150px));
            min-height: 520px;
        }

        .service-hero {
            margin: 6px 0 14px;
        }

        .service-hero h3 {
            margin: 0 0 6px;
            font-size: 18px;
            line-height: 1.4;
        }

        .service-hero p {
            margin: 0;
            color: #666;
            font-size: 14px;
            line-height: 1.6;
        }

        .service-hero-top {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 12px;
        }

        .preference-trigger {
            flex: 0 0 auto;
            width: auto;
            min-height: 34px;
            padding: 0 10px;
            border: 1px solid #d7dbe8;
            background: #f8f9ff;
            color: #3154a3;
            font-size: 13px;
        }

        .preference-summary {
            margin-top: 10px !important;
            color: #52617c !important;
            font-size: 13px !important;
        }

        .service-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 12px;
        }

        .service-card {
            width: 100%;
            min-height: 148px;
            padding: 16px;
            border: 1px solid #e3e6ef;
            border-radius: 10px;
            background: #ffffff;
            color: #222;
            text-align: left;
            box-shadow: 0 4px 14px rgba(20, 30, 60, 0.06);
        }

        .service-card:hover {
            border-color: #1a73e8;
            box-shadow: 0 8px 22px rgba(26, 115, 232, 0.12);
        }

        .service-card-title {
            margin-bottom: 8px;
            font-size: 17px;
            font-weight: 700;
            line-height: 1.35;
        }

        .service-card-desc {
            color: #555;
            font-size: 14px;
            line-height: 1.55;
        }

        .service-card-meta {
            margin-top: 12px;
            color: #1a73e8;
            font-size: 13px;
            font-weight: 600;
        }

        .chat-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
            padding: 4px 0 12px;
            border-bottom: 1px solid #eceaf2;
        }

        .back-btn {
            flex: 0 0 36px;
            width: 36px;
            min-height: 36px;
            padding: 0;
            border: 1px solid #e3e0eb;
            border-radius: 50%;
            background: #ffffff;
            color: #4a4361;
            font-size: 22px;
            line-height: 1;
        }

        .chat-assistant {
            display: flex;
            align-items: center;
            gap: 9px;
            min-width: 0;
            flex: 1;
        }

        .chat-header-avatar,
        .assistant-avatar {
            display: grid;
            place-items: center;
            flex: 0 0 auto;
            border-radius: 50%;
            background: #4f46a5;
            color: #ffffff;
            font-family: "Microsoft YaHei", sans-serif;
            font-weight: 700;
        }

        .chat-header-avatar {
            width: 36px;
            height: 36px;
            font-size: 15px;
        }

        .chat-assistant-name {
            color: #29243a;
            font-size: 15px;
            font-weight: 700;
            line-height: 1.4;
        }

        .chat-status {
            margin-top: 1px;
            color: #7b7590;
            font-size: 12px;
            line-height: 1.35;
        }

        .clear-chat-btn {
            flex: 0 0 36px;
            width: 36px;
            min-height: 36px;
            padding: 0;
            border: 1px solid transparent;
            border-radius: 50%;
            background: transparent;
            color: #6f6980;
            font-size: 20px;
            line-height: 1;
        }

        .tarot-secondary-btn {
            background: #eeeeee;
            color: #333;
        }

        .tarot-number-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
        }

        .tarot-number-field span {
            display: block;
            margin-bottom: 5px;
            color: #666;
            font-size: 13px;
        }

        .tarot-number-field input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
        }

        #chatBox {
            flex: 1;
            min-height: 0;
            overflow-y: auto;
            padding: 8px 2px 14px;
        }

        .msg {
            display: flex;
            align-items: flex-end;
            gap: 8px;
            margin: 14px 0;
            line-height: 1.6;
            overflow-wrap: anywhere;
        }

        .user {
            justify-content: flex-end;
            color: #ffffff;
        }

        .assistant {
            color: #222;
        }

        .message-main {
            min-width: 0;
            max-width: min(85%, 620px);
        }

        .user .message-main {
            display: flex;
            justify-content: flex-end;
        }

        .assistant-avatar {
            width: 30px;
            height: 30px;
            margin-bottom: 1px;
            font-size: 12px;
        }

        .msg.grouped .assistant-avatar {
            visibility: hidden;
        }

        .message-sender {
            margin: 0 0 4px 2px;
            color: #7a748b;
            font-size: 12px;
            line-height: 1.3;
        }

        .msg.grouped .message-sender {
            display: none;
        }

        .bubble {
            display: inline-block;
            max-width: 100%;
            padding: 10px 13px;
            border-radius: 14px;
            text-align: left;
            word-break: break-word;
        }

        .rich-bubble {
            display: block;
            width: 100%;
        }

        .user .bubble {
            background: #4f46a5;
            border-bottom-right-radius: 4px;
        }

        .assistant .bubble {
            background: #f7f6fa;
            border: 1px solid #e7e4ee;
            border-bottom-left-radius: 4px;
            color: #302d3b;
        }

        .assistant .rich-bubble {
            background: white;
        }

        .assistant-text p {
            margin: 0 0 10px;
        }

        .assistant-text p:last-child {
            margin-bottom: 0;
        }

        .assistant-text strong {
            color: #28233a;
            font-weight: 700;
        }

        .assistant-heading {
            margin: 2px 0 8px;
            color: #2b2540;
            font-size: 15px;
            font-weight: 700;
            line-height: 1.45;
        }

        .assistant-list {
            margin: 4px 0 10px;
            padding-left: 20px;
        }

        .assistant-list:last-child {
            margin-bottom: 0;
        }

        .assistant-list li + li {
            margin-top: 4px;
        }

        .guide-card,
        .tarot-inline-card {
            color: #333;
            font-size: 14px;
            line-height: 1.6;
        }

        .tarot-inline-title {
            margin-bottom: 6px;
            font-size: 15px;
            font-weight: 700;
        }

        .tarot-inline-card p {
            margin: 6px 0;
            color: #555;
        }

        .guide-card p {
            margin: 0;
            color: #4c465b;
        }

        .prompt-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }

        .prompt-chip {
            width: auto;
            min-height: 32px;
            padding: 0 10px;
            border: 1px solid #d7dbe8;
            background: #f8f9ff;
            color: #3154a3;
            font-size: 13px;
        }

        .tarot-inline-question {
            margin-top: 8px;
            padding: 8px 10px;
            border-radius: 8px;
            background: #f7f4ff;
            color: #3f2f66;
        }

        .tarot-inline-actions {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }

        .tarot-inline-actions button {
            width: auto;
            min-height: 36px;
            padding: 0 12px;
            font-size: 14px;
        }

        .tarot-number-grid.inline {
            margin-top: 10px;
        }

        .tarot-flip-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-top: 10px;
        }

        .tarot-flip-card {
            width: 100%;
            height: auto;
            min-height: 0;
            padding: 0;
            border: 0;
            background: transparent;
            color: #222;
            perspective: 1000px;
        }

        .tarot-flip-inner {
            position: relative;
            width: 100%;
            aspect-ratio: 240 / 420;
            transition: transform 0.7s ease;
            transform-style: preserve-3d;
        }

        .tarot-flip-card.flipped .tarot-flip-inner {
            transform: rotateY(180deg);
        }

        .tarot-card-face {
            position: absolute;
            inset: 0;
            display: flex;
            align-items: stretch;
            justify-content: center;
            overflow: hidden;
            border: 1px solid #ddd6e8;
            border-radius: 8px;
            background: #21183c;
            backface-visibility: hidden;
            box-shadow: 0 8px 18px rgba(25, 20, 40, 0.16);
        }

        .tarot-card-face img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }

        .tarot-card-front {
            transform: rotateY(180deg);
            background: #faf7ed;
        }

        .tarot-card-front img.reversed-card-image {
            transform: rotate(180deg);
        }

        .tarot-flip-meta {
            margin-top: 8px;
            color: #333;
            font-size: 13px;
            line-height: 1.45;
            text-align: center;
        }

        .tarot-flip-position {
            color: #666;
            font-size: 12px;
        }

        .tarot-flip-name {
            margin-top: 2px;
            font-weight: 600;
        }

        .input-row {
            display: flex;
            align-items: flex-end;
            gap: 8px;
            padding: 8px;
            border: 1px solid #dedbe8;
            border-radius: 16px;
            background: #ffffff;
            box-shadow: 0 6px 20px rgba(38, 29, 72, 0.08);
        }

        #userInput {
            flex: 1;
            height: 48px;
            min-width: 0;
            width: 100%;
            padding: 12px 10px;
            font-size: 15px;
            line-height: 1.5;
            resize: none;
            border: 0;
            border-radius: 10px;
            outline: none;
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

        .send-btn {
            flex: 0 0 70px;
            min-height: 48px;
            border-radius: 11px;
            background: #4f46a5;
            font-size: 14px;
            font-weight: 700;
        }

        .thinking-bubble {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            min-height: 40px;
            color: #716b80;
            font-size: 13px;
        }

        .thinking-dots {
            display: inline-flex;
            gap: 3px;
        }

        .thinking-dots span {
            width: 5px;
            height: 5px;
            border-radius: 50%;
            background: #7569b5;
            animation: thinking-bounce 1s infinite ease-in-out;
        }

        .thinking-dots span:nth-child(2) {
            animation-delay: 0.15s;
        }

        .thinking-dots span:nth-child(3) {
            animation-delay: 0.3s;
        }

        @keyframes thinking-bounce {
            0%, 60%, 100% { transform: translateY(0); opacity: 0.45; }
            30% { transform: translateY(-3px); opacity: 1; }
        }

        .preference-dialog[hidden] {
            display: none;
        }

        .preference-dialog {
            position: fixed;
            inset: 0;
            z-index: 20;
            display: grid;
            place-items: center;
            padding: 18px;
        }

        .preference-backdrop {
            position: absolute;
            inset: 0;
            background: rgba(15, 23, 42, 0.58);
        }

        .preference-panel {
            position: relative;
            width: min(680px, 100%);
            max-height: min(760px, calc(100vh - 36px));
            overflow-y: auto;
            padding: 22px;
            border-radius: 10px;
            background: #ffffff;
            box-shadow: 0 22px 64px rgba(15, 23, 42, 0.26);
        }

        .preference-close {
            position: absolute;
            top: 12px;
            right: 12px;
            width: 34px;
            min-height: 34px;
            padding: 0;
            border: 0;
            background: transparent;
            color: #667085;
            font-size: 24px;
            line-height: 1;
        }

        .preference-panel h3 {
            margin: 0 42px 6px 0;
            color: #172033;
            font-size: 20px;
        }

        .preference-intro,
        .preference-privacy {
            margin: 0;
            color: #667085;
            font-size: 13px;
            line-height: 1.6;
        }

        .preference-current-selection {
            margin: 16px 0 0;
            color: #52617c;
            font-size: 13px;
            line-height: 1.6;
        }

        .preference-field {
            display: block;
            margin-top: 18px;
            color: #344054;
            font-size: 14px;
            font-weight: 700;
        }

        .preference-field input {
            display: block;
            width: 100%;
            margin-top: 8px;
            padding: 10px 12px;
            border: 1px solid #d0d5dd;
            border-radius: 8px;
            color: #172033;
            font: inherit;
            font-weight: 400;
        }

        .preference-group {
            min-width: 0;
            margin: 20px 0 0;
            padding: 0;
            border: 0;
        }

        .preference-group legend {
            margin-bottom: 8px;
            color: #344054;
            font-size: 14px;
            font-weight: 700;
        }

        .preference-group legend span {
            color: #98a2b3;
            font-size: 12px;
            font-weight: 400;
        }

        .zodiac-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 8px;
        }

        .zodiac-option {
            display: flex;
            min-width: 0;
            min-height: 112px;
            padding: 8px 6px 9px;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            border: 1px solid #d0d5dd;
            border-radius: 8px;
            background: #ffffff;
            color: #30205b;
            font-size: 13px;
            line-height: 1.3;
        }

        .zodiac-option:hover,
        .zodiac-option.selected {
            border-color: #30205b;
            background: #ffffff;
        }

        .zodiac-emoji {
            display: block;
            height: 70px;
            margin-bottom: 5px;
            font-size: 42px;
            line-height: 1;
        }

        .personality-options {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .personality-option {
            width: auto;
            min-height: 36px;
            padding: 0 11px;
            border: 1px solid #d0d5dd;
            background: #ffffff;
            color: #475467;
            font-size: 13px;
        }

        .personality-option.selected {
            border-color: #1a73e8;
            background: #eef5ff;
            color: #1558b0;
        }

        .preference-privacy {
            margin-top: 18px;
            padding: 9px 10px;
            border-radius: 8px;
            background: #f8fafc;
        }

        .preference-actions {
            display: flex;
            justify-content: flex-end;
            gap: 8px;
            margin-top: 18px;
        }

        .preference-actions button {
            width: auto;
            min-height: 40px;
            padding: 0 14px;
            font-size: 14px;
        }

        .preference-skip {
            background: #eef0f4;
            color: #475467;
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

            .subtitle {
                margin-bottom: 12px;
            }

            .privacy-notice {
                font-size: 12px;
            }

            .service-grid {
                grid-template-columns: 1fr;
            }

            .service-card {
                min-height: 132px;
            }

            .service-hero-top {
                align-items: stretch;
                flex-direction: column;
            }

            .preference-trigger {
                width: 100%;
            }

            .chat-view.active {
                flex: 1;
                min-height: 0;
                height: auto;
            }

            .chat-header {
                align-items: center;
            }

            .back-btn {
                flex-basis: 36px;
                width: 36px;
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

            .message-main {
                max-width: calc(100% - 38px);
            }

            .input-row {
                gap: 6px;
                padding: 6px;
            }

            .tarot-number-grid,
            .tarot-flip-grid {
                grid-template-columns: 1fr;
            }

            .rich-bubble {
                width: 100%;
            }

            #userInput {
                height: 48px;
                font-size: 16px;
            }

            .send-btn {
                flex-basis: 62px;
                min-height: 48px;
            }

            .preference-dialog {
                align-items: end;
                padding: 0;
            }

            .preference-panel {
                width: 100%;
                max-height: min(88dvh, 760px);
                padding: 20px 14px 16px;
                border-radius: 12px 12px 0 0;
            }

            .zodiac-grid {
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 7px;
            }

            .zodiac-option {
                min-height: 98px;
            }

            .zodiac-emoji {
                height: 59px;
                font-size: 36px;
            }

            .preference-actions {
                flex-direction: column-reverse;
            }

            .preference-actions button {
                width: 100%;
            }
        }
    </style>
</head>

<body>
    <div class="container">
        <h2>筮渡智能助手 - 传统文化分析助手</h2>
        <p class="subtitle">先选择你想进行的解答方向，我会进入对应流程一步步引导。</p>
        <p class="privacy-notice">隐私提示：你输入的内容会发送给 DeepSeek 接口用于生成回复。聊天记录会保存在当前浏览器本地，方便刷新后恢复；清空对话、清理浏览器数据或更换设备后不会保留。请勿填写身份证号、手机号、详细住址、银行卡、密码、验证码、病历等敏感信息；八字出生地写到城市即可。</p>

        <section id="serviceView" class="app-view service-view active">
            <div class="service-hero">
                <div class="service-hero-top">
                    <div>
                        <h3>你这次想先看什么？</h3>
                        <p>选一个方向后再进入对话。每个方向都会有自己的提问顺序，不需要一次把所有信息都写完。</p>
                    </div>
                    <button id="openPreferences" type="button" class="preference-trigger">偏好设置</button>
                </div>
                <p id="preferenceSummary" class="preference-summary"></p>
            </div>
            <div id="serviceGrid" class="service-grid" aria-label="解答方向"></div>
        </section>

        <section id="chatView" class="app-view chat-view">
            <div class="chat-header">
                <button type="button" class="back-btn" onclick="showServiceView()" aria-label="返回解答选择" title="返回解答选择">‹</button>
                <div class="chat-assistant">
                    <div class="chat-header-avatar" aria-hidden="true">筮</div>
                    <div>
                        <div class="chat-assistant-name">筮渡 AI</div>
                        <div id="skillHint" class="chat-status">正在对话</div>
                    </div>
                </div>
                <button type="button" class="clear-chat-btn" onclick="clearChat()" aria-label="清空当前对话" title="清空当前对话">↺</button>
            </div>

            <div id="chatBox"></div>

            <div class="input-row">
                <textarea id="userInput" placeholder="请输入你的问题，例如：我想看每日运势、八字、塔罗、风水、运势或姓名分析"></textarea>
                <button class="send-btn" onclick="sendMessage()">发送</button>
            </div>
        </section>

        <div id="preferenceDialog" class="preference-dialog" hidden aria-hidden="true">
            <div class="preference-backdrop"></div>
            <section class="preference-panel" role="dialog" aria-modal="true" aria-labelledby="preferenceTitle">
                <button id="closePreferences" type="button" class="preference-close" aria-label="关闭偏好设置">×</button>
                <h3 id="preferenceTitle">先认识一下你</h3>
                <p class="preference-intro">这些选项都可以跳过，之后也能随时修改。</p>

                <label class="preference-field" for="preferenceNickname">
                    我该怎么称呼你？
                    <input id="preferenceNickname" type="text" maxlength="20" placeholder="昵称或化名即可">
                </label>

                <fieldset class="preference-group">
                    <legend>你的星座 <span>可跳过</span></legend>
                    <div id="zodiacGrid" class="zodiac-grid" aria-label="选择星座"></div>
                </fieldset>

                <fieldset class="preference-group">
                    <legend>回复偏好 <span>可跳过</span></legend>
                    <div id="personalityOptions" class="personality-options" aria-label="选择回复偏好"></div>
                </fieldset>

                <p id="preferenceCurrentSelection" class="preference-current-selection"></p>
                <p class="preference-privacy">昵称、星座和回复偏好只保存在当前浏览器；在你发起聊天时，它们会随请求发送给 DeepSeek，用来调整称呼和回答方式。</p>
                <div class="preference-actions">
                    <button id="skipPreferences" type="button" class="preference-skip">暂时跳过</button>
                    <button id="savePreferences" type="button">保存偏好</button>
                </div>
            </section>
        </div>
    </div>

    <script>
        const skillConfigs = {
            "": {
                placeholder: "请输入你的问题，例如：我想看每日运势、八字、塔罗、择日或姓名分析",
                hint: "通用咨询：直接描述你的问题，我会尽量判断适合的方向。",
                serviceTitle: "通用咨询",
                serviceDesc: "还不确定该选哪类时，从这里开始。你可以先说大概情况，我会帮你归类。",
                serviceMeta: "适合模糊问题",
                guideTitle: "通用咨询",
                guideText: "你可以直接描述想问的事情。如果更适合每日运势、八字、塔罗、择日或姓名分析，我会引导你补充必要信息。",
                guidePoints: ["不用一开始就选得很准", "尽量少提交敏感隐私", "玄学内容只作传统文化和自我反思参考"],
                examples: ["我最近有点迷茫，不知道适合看什么", "我想看看事业和感情的大方向", "帮我判断这个问题适合用哪种方式分析"]
            },
            daily_fortune: {
                placeholder: "例如：帮我看今天运势",
                hint: "每日运势：输入星座、生肖或生日，快速生成今日参考和幸运提示。",
                serviceTitle: "每日运势",
                serviceDesc: "用星座、生肖或生日作为入口，快速查看今日综合、感情、事业、财运和幸运提示。",
                serviceMeta: "适合每天打开看一眼",
                guideTitle: "每日运势",
                guideText: "可以直接告诉我你的星座、生肖，或输入出生日期自动识别。默认看今天，也可以问明日或本周。",
                guidePoints: ["星座入口最轻量", "生肖入口更偏传统", "不需要出生时间和详细地址"],
                examples: ["帮我看今天运势", "属龙，今天适合做什么", "我是1998年5月20日出生，看看今日运势"]
            },
            bazi: {
                placeholder: "例如：我想看八字，重点看今年事业和财运",
                hint: "八字分析：像成熟排盘工具一样逐项收集信息，但只问必要内容。",
                serviceTitle: "八字分析",
                serviceDesc: "按出生日期、时间、城市、性别和关注方向，做传统命理角度的分析。",
                serviceMeta: "适合事业、感情、整体运势",
                guideTitle: "八字分析",
                guideText: "我会按出生日期、时间、出生城市、性别、关注方向一步步问，不需要真实姓名和详细住址。",
                guidePoints: ["出生地写到城市即可", "不知道具体时间可以说“不清楚”", "玄学分析只作传统文化参考"],
                examples: ["我想看八字，重点看今年事业", "我是公历1998年5月20日出生，想看感情", "不知道出生时间，也能大概分析吗"]
            },
            tarot: {
                placeholder: "请写下本次塔罗问题，例如：我想看看这三个月感情会怎么发展",
                hint: "塔罗：先在对话中写下问题，再选择系统随机抽牌或自己选牌，点击三张牌背翻牌后再解读。",
                serviceTitle: "塔罗占卜",
                serviceDesc: "先写下具体问题，再选择系统抽牌或自己选牌，翻开三张牌后解读。",
                serviceMeta: "适合当下状态、关系、短期趋势",
                guideTitle: "塔罗三张牌",
                guideText: "直接在下方输入你想问的问题。之后可以让系统随机抽 3 张，也可以自己从 1-78 中选择 3 个数字。",
                guidePoints: ["问题尽量具体", "可系统抽牌，也可自己选牌", "三张牌都翻开后自动解读"],
                examples: ["我想看看这三个月感情会怎么发展", "我想问现在这份工作接下来适合继续吗", "对方现在对我的真实想法是什么"]
            },
            date_selection: {
                placeholder: "例如：我想给搬家择日，时间大概在下个月",
                hint: "择日：先明确事项、日期范围和避开条件，再给传统文化参考。",
                serviceTitle: "择日",
                serviceDesc: "用于搬家、开业、签约、结婚等事项，结合可选时间和现实限制给建议。",
                serviceMeta: "适合选日期、排优先级",
                guideTitle: "择日助手",
                guideText: "我会先确认你要办什么事，再看可选时间范围、避开日期和现实限制。",
                guidePoints: ["适合搬家、结婚、开业、签约等", "先给日期范围，不需要一次说很多信息", "不会把日期说成绝对保证"],
                examples: ["我想给搬家择日，时间在下个月", "帮我看开业日期，最好避开周末", "我想选一个签约日，本周内都可以"]
            },
            naming: {
                placeholder: "例如：帮我分析名字“林知夏”，看看寓意和风格",
                hint: "姓名分析：先明确用途和风格，再分析读音、字义、记忆点和实用性。",
                serviceTitle: "姓名分析",
                serviceDesc: "分析已有名字，或按用途、风格、寓意生成备选名。",
                serviceMeta: "适合人名、店名、品牌名、账号名",
                guideTitle: "姓名分析",
                guideText: "你可以分析已有名字，也可以让我按用途和风格给备选。可以使用昵称或化名。",
                guidePoints: ["适合宝宝名、个人名、店名、公司名、账号名", "优先看好读、好记、寓意清楚", "避免证件号码等无关隐私"],
                examples: ["帮我分析名字“林知夏”", "想给女孩起名，风格清冷古典", "帮我想 5 个适合茶饮店的名字"]
            }
        };

        const TAROT_CARD_BACK = "/static/tarot/card-back.svg";
        const SERVICE_ORDER = ["daily_fortune", "tarot", "bazi", "date_selection", "naming", ""];
        const SESSION_STORAGE_KEY = "shidu_ai_sessions_v1";
        const PREFERENCE_STORAGE_KEY = "shidu_ai_preferences_v1";
        const ZODIAC_OPTIONS = [
            { id: "aries", name: "白羊座", emoji: "♈" },
            { id: "taurus", name: "金牛座", emoji: "♉" },
            { id: "gemini", name: "双子座", emoji: "♊" },
            { id: "cancer", name: "巨蟹座", emoji: "♋" },
            { id: "leo", name: "狮子座", emoji: "♌" },
            { id: "virgo", name: "处女座", emoji: "♍" },
            { id: "libra", name: "天秤座", emoji: "♎" },
            { id: "scorpio", name: "天蝎座", emoji: "♏" },
            { id: "sagittarius", name: "射手座", emoji: "♐" },
            { id: "capricorn", name: "摩羯座", emoji: "♑" },
            { id: "aquarius", name: "水瓶座", emoji: "♒" },
            { id: "pisces", name: "双鱼座", emoji: "♓" }
        ];
        const PERSONALITY_OPTIONS = [
            { id: "balance", name: "平衡" },
            { id: "brief", name: "简洁" },
            { id: "gentle", name: "温和" },
            { id: "detailed", name: "详细" }
        ];

        let activeSkillId = "";
        let tarotFlowState = "idle";
        let tarotShuffleId = "";
        let currentTarotCards = null;
        let currentTarotQuestion = "";
        let currentTarotNumbers = [];
        let currentTarotDrawMode = "";
        let currentTarotMethodCard = null;
        let revealedTarotIndexes = [];
        let tarotReadingRequested = false;
        let chatSessions = loadStoredSessions();
        let userPreferences = loadStoredPreferences();
        let editingPreferences = null;

        let messages = initialMessages();

        function initialMessages() {
            return [
                {
                    role: "system",
                    content: "你是一个中文智能助手。请使用简体中文回答，回答要清晰、实用。"
                }
            ];
        }

        function loadStoredSessions() {
            try {
                return JSON.parse(localStorage.getItem(SESSION_STORAGE_KEY) || "{}");
            } catch (error) {
                console.warn("无法读取本地聊天记录，已忽略旧数据。", error);
                return {};
            }
        }

        function saveStoredSessions() {
            try {
                localStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(chatSessions));
            } catch (error) {
                console.warn("本地聊天记录保存失败。", error);
            }
        }

        function defaultUserPreferences() {
            return {
                nickname: "",
                zodiac: "",
                personality: "",
                setupComplete: false
            };
        }

        function findOption(options, id) {
            return options.find(function(option) {
                return option.id === id;
            }) || null;
        }

        function normalizePreferences(value) {
            const defaults = defaultUserPreferences();
            if (!value || typeof value !== "object") {
                return defaults;
            }

            const nickname = typeof value.nickname === "string" ? value.nickname.trim().slice(0, 20) : "";
            const zodiac = findOption(ZODIAC_OPTIONS, value.zodiac) ? value.zodiac : "";
            const personality = findOption(PERSONALITY_OPTIONS, value.personality) ? value.personality : "";

            return {
                nickname: nickname,
                zodiac: zodiac,
                personality: personality,
                setupComplete: Boolean(value.setupComplete)
            };
        }

        function loadStoredPreferences() {
            try {
                return normalizePreferences(JSON.parse(localStorage.getItem(PREFERENCE_STORAGE_KEY) || "{}"));
            } catch (error) {
                console.warn("无法读取本地偏好，已使用空白偏好。", error);
                return defaultUserPreferences();
            }
        }

        function saveStoredPreferences() {
            try {
                localStorage.setItem(PREFERENCE_STORAGE_KEY, JSON.stringify(userPreferences));
            } catch (error) {
                console.warn("本地偏好保存失败。", error);
            }
        }

        function getZodiacName(id) {
            const option = findOption(ZODIAC_OPTIONS, id);
            return option ? option.name : "";
        }

        function getSkillConfig(skillId) {
            const config = skillConfigs[skillId] || skillConfigs[""];
            if (skillId !== "daily_fortune") {
                return config;
            }

            return Object.assign({}, config, {
                placeholder: "例如：帮我看今天运势",
                guideText: "可以直接告诉我你想看的时间，也可以补充星座、生肖或生日。默认看今天，还可以问明日或本周。",
                examples: ["帮我看今天运势", "属龙，今天适合做什么", "我是1998年5月20日出生，看看今日运势"]
            });
        }

        function getPersonalityName(id) {
            const option = findOption(PERSONALITY_OPTIONS, id);
            return option ? option.name : "";
        }

        function getChatPreferences() {
            return {
                nickname: userPreferences.nickname,
                zodiac: userPreferences.zodiac,
                personality: userPreferences.personality
            };
        }

        function renderPreferenceSummary() {
            const summary = document.getElementById("preferenceSummary");
            const hasPreferences = Boolean(
                userPreferences.nickname
                || userPreferences.zodiac
                || userPreferences.personality
            );
            summary.textContent = hasPreferences
                ? "已应用你的偏好"
                : "可选：设置称呼、星座和回复偏好，让对话更贴近你。";
        }

        function renderPreferenceCurrentSelection() {
            const summary = document.getElementById("preferenceCurrentSelection");
            if (!editingPreferences) {
                summary.textContent = "";
                return;
            }

            const details = [];
            const zodiacName = getZodiacName(editingPreferences.zodiac);
            const personalityName = getPersonalityName(editingPreferences.personality);
            if (zodiacName) {
                details.push("你选择的星座：" + zodiacName);
            }
            if (personalityName) {
                details.push("回复偏好：" + personalityName);
            }
            summary.textContent = details.length ? details.join(" · ") : "尚未选择星座或回复偏好。";
        }

        function refreshActiveSkillPresentation() {
            setSkill(activeSkillId);
            document.querySelectorAll(".guide-card[data-skill-id]").forEach(function(card) {
                if (card.dataset.skillId === activeSkillId) {
                    card.replaceWith(createGuideCard(getSkillConfig(activeSkillId), activeSkillId));
                }
            });
            persistCurrentSession();
        }

        function renderZodiacOptions() {
            const grid = document.getElementById("zodiacGrid");
            grid.innerHTML = "";

            ZODIAC_OPTIONS.forEach(function(option) {
                const button = document.createElement("button");
                button.type = "button";
                button.className = "zodiac-option" + (editingPreferences.zodiac === option.id ? " selected" : "");
                button.setAttribute("aria-pressed", String(editingPreferences.zodiac === option.id));

                const emoji = document.createElement("span");
                emoji.className = "zodiac-emoji";
                emoji.setAttribute("aria-hidden", "true");
                emoji.textContent = option.emoji;

                const label = document.createElement("span");
                label.textContent = option.name;

                button.appendChild(emoji);
                button.appendChild(label);
                button.addEventListener("click", function() {
                    editingPreferences.zodiac = editingPreferences.zodiac === option.id ? "" : option.id;
                    renderZodiacOptions();
                    renderPreferenceCurrentSelection();
                });
                grid.appendChild(button);
            });
        }

        function renderPersonalityOptions() {
            const container = document.getElementById("personalityOptions");
            container.innerHTML = "";

            PERSONALITY_OPTIONS.forEach(function(option) {
                const button = document.createElement("button");
                button.type = "button";
                button.className = "personality-option" + (editingPreferences.personality === option.id ? " selected" : "");
                button.setAttribute("aria-pressed", String(editingPreferences.personality === option.id));
                button.textContent = option.name;
                button.addEventListener("click", function() {
                    editingPreferences.personality = editingPreferences.personality === option.id ? "" : option.id;
                    renderPersonalityOptions();
                    renderPreferenceCurrentSelection();
                });
                container.appendChild(button);
            });
        }

        function openPreferences() {
            editingPreferences = Object.assign({}, userPreferences);
            document.getElementById("preferenceNickname").value = editingPreferences.nickname;
            renderZodiacOptions();
            renderPersonalityOptions();
            renderPreferenceCurrentSelection();
            const dialog = document.getElementById("preferenceDialog");
            dialog.hidden = false;
            dialog.setAttribute("aria-hidden", "false");
            document.getElementById("preferenceNickname").focus();
        }

        function closePreferences() {
            const dialog = document.getElementById("preferenceDialog");
            dialog.hidden = true;
            dialog.setAttribute("aria-hidden", "true");
            editingPreferences = null;
        }

        function savePreferences() {
            if (!editingPreferences) {
                return;
            }

            editingPreferences.nickname = document.getElementById("preferenceNickname").value.trim().slice(0, 20);
            editingPreferences.setupComplete = true;
            userPreferences = normalizePreferences(editingPreferences);
            userPreferences.setupComplete = true;
            saveStoredPreferences();
            renderPreferenceSummary();
            refreshActiveSkillPresentation();
            closePreferences();
        }

        function skipPreferences() {
            userPreferences.setupComplete = true;
            saveStoredPreferences();
            renderPreferenceSummary();
            closePreferences();
        }

        function cloneMessages(value) {
            if (!Array.isArray(value)) {
                return initialMessages();
            }
            return value.map(function(message) {
                return {
                    role: message.role,
                    content: message.content
                };
            });
        }

        function getTarotState() {
            return {
                tarotFlowState: tarotFlowState,
                tarotShuffleId: tarotShuffleId,
                currentTarotCards: currentTarotCards,
                currentTarotQuestion: currentTarotQuestion,
                currentTarotNumbers: currentTarotNumbers,
                currentTarotDrawMode: currentTarotDrawMode,
                revealedTarotIndexes: revealedTarotIndexes,
                tarotReadingRequested: tarotReadingRequested
            };
        }

        function restoreTarotState(state) {
            resetTarotFlowState();
            if (!state) {
                return;
            }

            tarotFlowState = state.tarotFlowState || "idle";
            tarotShuffleId = state.tarotShuffleId || "";
            currentTarotCards = state.currentTarotCards || null;
            currentTarotQuestion = state.currentTarotQuestion || "";
            currentTarotNumbers = Array.isArray(state.currentTarotNumbers) ? state.currentTarotNumbers : [];
            currentTarotDrawMode = state.currentTarotDrawMode || "";
            currentTarotMethodCard = null;
            revealedTarotIndexes = Array.isArray(state.revealedTarotIndexes) ? state.revealedTarotIndexes : [];
            tarotReadingRequested = Boolean(state.tarotReadingRequested);
        }

        function persistCurrentSession() {
            const skillId = activeSkillId || "";
            const chatBox = document.getElementById("chatBox");
            const input = document.getElementById("userInput");

            chatSessions[skillId] = {
                messages: cloneMessages(messages),
                chatHtml: chatBox ? chatBox.innerHTML : "",
                inputValue: input ? input.value : "",
                tarotState: getTarotState(),
                updatedAt: new Date().toISOString()
            };
            saveStoredSessions();
        }

        function rehydrateChatInteractions() {
            document.querySelectorAll(".prompt-chip").forEach(function(chip) {
                chip.addEventListener("click", function() {
                    fillPrompt(chip.textContent);
                });
            });

            document.querySelectorAll(".tarot-inline-actions button").forEach(function(button) {
                button.addEventListener("click", function() {
                    const card = button.closest(".tarot-inline-card");
                    const label = button.textContent.trim();
                    if (label === "系统随机抽牌") {
                        drawTarotRandom(card, true);
                    } else if (label === "我自己选牌") {
                        startManualTarotDraw(card, true);
                    } else if (label === "确认抽牌") {
                        drawTarotNumbers(parseTarotNumbersFromCard(card), true, card);
                    } else if (label === "换个问题") {
                        resetTarotFlowState();
                        tarotFlowState = "waiting_question";
                        addMessage("assistant", "好的，请在下方输入新的塔罗问题。");
                        document.getElementById("userInput").focus();
                    }
                });
            });

            document.querySelectorAll(".tarot-flip-card").forEach(function(button) {
                button.addEventListener("click", function() {
                    flipTarotCard(Number(button.dataset.tarotIndex), button);
                });
            });

        }

        function resetConversation(options = {}) {
            messages = initialMessages();
            document.getElementById("chatBox").innerHTML = "";
            document.getElementById("userInput").value = "";
            resetTarotFlowState();

            if (options.persist !== false) {
                persistCurrentSession();
            }
        }

        function restoreConversation(skillId) {
            const session = chatSessions[skillId || ""];
            const chatBox = document.getElementById("chatBox");
            const input = document.getElementById("userInput");

            if (!session) {
                resetConversation({ persist: false });
                return false;
            }

            messages = cloneMessages(session.messages);
            chatBox.innerHTML = session.chatHtml || "";
            input.value = session.inputValue || "";
            restoreTarotState(session.tarotState);
            rehydrateChatInteractions();
            chatBox.scrollTop = chatBox.scrollHeight;
            return Boolean(session.chatHtml);
        }

        function renderServiceCards() {
            const grid = document.getElementById("serviceGrid");
            grid.innerHTML = "";

            SERVICE_ORDER.forEach(function(skillId) {
                const config = getSkillConfig(skillId);
                const card = document.createElement("button");
                card.type = "button";
                card.className = "service-card";
                card.addEventListener("click", function() {
                    enterChat(skillId);
                });

                const title = document.createElement("div");
                title.className = "service-card-title";
                title.textContent = config.serviceTitle || config.guideTitle;

                const desc = document.createElement("div");
                desc.className = "service-card-desc";
                desc.textContent = config.serviceDesc || config.hint;

                const meta = document.createElement("div");
                meta.className = "service-card-meta";
                meta.textContent = config.serviceMeta || "进入对话";

                card.appendChild(title);
                card.appendChild(desc);
                card.appendChild(meta);
                grid.appendChild(card);
            });
        }

        function showServiceView() {
            persistCurrentSession();
            document.getElementById("chatView").classList.remove("active");
            document.getElementById("serviceView").classList.add("active");
        }

        function showChatView() {
            document.getElementById("serviceView").classList.remove("active");
            document.getElementById("chatView").classList.add("active");
        }

        function enterChat(skillId) {
            persistCurrentSession();
            setSkill(skillId);
            const hadSession = restoreConversation(activeSkillId);
            showChatView();
            if (!hadSession) {
                showSkillGuide(activeSkillId);
            }
            document.getElementById("userInput").focus();
        }

        function setSkill(skillId) {
            activeSkillId = skillId || "";

            const config = getSkillConfig(activeSkillId);
            document.getElementById("userInput").placeholder = config.placeholder;
            document.getElementById("skillHint").textContent = "正在对话";
        }

        function createMessageShell(role) {
            const chatBox = document.getElementById("chatBox");
            const previous = chatBox.lastElementChild;
            const grouped = Boolean(
                previous
                && previous.classList.contains("msg")
                && previous.classList.contains(role)
                && !previous.classList.contains("thinking-message")
            );

            const div = document.createElement("div");
            div.className = "msg " + role + (grouped ? " grouped" : "");

            const main = document.createElement("div");
            main.className = "message-main";

            if (role === "assistant") {
                const avatar = document.createElement("div");
                avatar.className = "assistant-avatar";
                avatar.setAttribute("aria-hidden", "true");
                avatar.textContent = "筮";
                div.appendChild(avatar);

                const sender = document.createElement("div");
                sender.className = "message-sender";
                sender.textContent = "筮渡 AI";
                main.appendChild(sender);
            }

            const bubble = document.createElement("div");
            bubble.className = "bubble";
            main.appendChild(bubble);
            div.appendChild(main);

            return { chatBox: chatBox, message: div, bubble: bubble };
        }

        function addMessage(role, content) {
            const shell = createMessageShell(role);
            if (role === "assistant") {
                shell.bubble.classList.add("assistant-text");
                shell.bubble.innerHTML = renderAssistantText(content);
            } else {
                shell.bubble.textContent = content;
            }

            shell.chatBox.appendChild(shell.message);

            shell.chatBox.scrollTop = shell.chatBox.scrollHeight;
            persistCurrentSession();
        }

        function escapeHtml(value) {
            return String(value)
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#39;");
        }

        function renderAssistantText(content) {
            const lines = String(content || "").replace(/\\r\\n?/g, "\\n").split("\\n");
            const blocks = [];
            let listItems = [];

            function renderInline(value) {
                return escapeHtml(value).replace(/\\*\\*([^*\\n][^*\\n]*?)\\*\\*/g, "<strong>$1</strong>");
            }

            function flushList() {
                if (!listItems.length) {
                    return;
                }
                blocks.push("<ul class=\"assistant-list\">" + listItems.map(function(item) {
                    return "<li>" + renderInline(item) + "</li>";
                }).join("") + "</ul>");
                listItems = [];
            }

            lines.forEach(function(line) {
                const trimmed = line.trim();
                if (!trimmed) {
                    flushList();
                    return;
                }

                const heading = trimmed.match(/^#{1,3}\\s+(.+)$/);
                const listItem = trimmed.match(/^(?:[-*•]|\\d+[.)])\\s+(.+)$/);
                const label = trimmed.match(/^([^：:]{1,16}[：:])\\s*(.*)$/);
                if (heading) {
                    flushList();
                    blocks.push("<div class=\"assistant-heading\">" + renderInline(heading[1]) + "</div>");
                } else if (listItem) {
                    listItems.push(listItem[1]);
                } else {
                    flushList();
                    if (label) {
                        blocks.push("<p><strong>" + renderInline(label[1]) + "</strong>" + (label[2] ? " " + renderInline(label[2]) : "") + "</p>");
                    } else {
                        blocks.push("<p>" + renderInline(trimmed) + "</p>");
                    }
                }
            });
            flushList();
            return blocks.join("") || "<p>暂时没有可显示的内容。</p>";
        }

        function addRichAssistantNode(node) {
            const shell = createMessageShell("assistant");
            shell.bubble.classList.add("rich-bubble");
            shell.bubble.appendChild(node);
            shell.chatBox.appendChild(shell.message);
            shell.chatBox.scrollTop = shell.chatBox.scrollHeight;
            persistCurrentSession();
        }

        function addThinkingMessage() {
            const shell = createMessageShell("assistant");
            shell.message.classList.add("thinking-message");
            shell.bubble.classList.add("thinking-bubble");
            shell.bubble.innerHTML = "<span>筮渡正在整理思路</span><span class=\"thinking-dots\" aria-label=\"正在思考\"><span></span><span></span><span></span></span>";
            shell.chatBox.appendChild(shell.message);
            shell.chatBox.scrollTop = shell.chatBox.scrollHeight;
            return shell.message;
        }

        function fillPrompt(text) {
            const input = document.getElementById("userInput");
            input.value = text;
            input.focus();
            persistCurrentSession();
        }

        function createGuideCard(config, skillId) {
            const card = document.createElement("div");
            card.className = "guide-card";
            card.dataset.skillId = skillId;

            const text = document.createElement("p");
            const welcomeMessages = {
                "": "你好呀，今天想一起看看什么？你可以从下面选一个方向，或直接说说近况。",
                daily_fortune: "你好呀，今天想看看哪方面的运势？你可以直接说今天、明日或本周。",
                tarot: "你好呀，先把这次想问的问题告诉我。问题越具体，后面的抽牌与解读就越贴近你。",
                bazi: "你好呀，想先从哪个方向看看？你可以慢慢补充出生信息和最关心的事情。",
                date_selection: "你好呀，先告诉我准备做什么事和大概时间，我陪你一步步梳理。",
                naming: "你好呀，想分析已有的名字，还是一起想几个新名字？"
            };
            text.textContent = welcomeMessages[skillId] || config.guideText;
            card.appendChild(text);

            const chips = document.createElement("div");
            chips.className = "prompt-chips";
            config.examples.forEach(function(example) {
                const chip = document.createElement("button");
                chip.type = "button";
                chip.className = "prompt-chip";
                chip.textContent = example;
                chip.addEventListener("click", function() {
                    fillPrompt(example);
                });
                chips.appendChild(chip);
            });
            card.appendChild(chips);

            return card;
        }

        function showSkillGuide(skillId) {
            const config = getSkillConfig(skillId);
            if (!config || !config.guideTitle) {
                return;
            }

            if (skillId === "tarot") {
                resetTarotFlowState();
                tarotFlowState = "waiting_question";
            }

            addRichAssistantNode(createGuideCard(config, skillId));

        }

        async function sendMessage(options = {}) {
            const input = document.getElementById("userInput");
            const text = options.text || input.value.trim();

            if (!text) {
                return;
            }

            input.value = "";

            if (!options.bypassSkillFlow && activeSkillId === "tarot") {
                const handled = await handleTarotFlowInput(text);
                if (handled) {
                    return;
                }
            }

            messages.push({
                role: "user",
                content: text
            });

            if (options.showUser !== false) {
                addMessage("user", options.displayText || text);
            }
            const thinkingMessage = addThinkingMessage();

            try {
                const response = await fetch("/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        messages: messages,
                        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                        skill_id: activeSkillId || null,
                        tarot_cards: options.tarotCards || null,
                        user_preferences: getChatPreferences()
                    })
                });

                const data = await response.json();

                if (thinkingMessage.isConnected) {
                    thinkingMessage.remove();
                }

                if (!response.ok) {
                    addMessage("assistant", data.error || "请求失败");
                    return;
                }

                if (data.skill_id && data.skill_id !== activeSkillId) {
                    setSkill(data.skill_id);
                }

                messages.push({
                    role: "assistant",
                    content: data.reply
                });

                addMessage("assistant", data.reply);

            } catch (error) {
                if (thinkingMessage.isConnected) {
                    thinkingMessage.remove();
                }
                addMessage("assistant", "请求异常：" + error);
            }
        }

        async function handleTarotFlowInput(text) {
            if (tarotFlowState === "idle") {
                tarotFlowState = "waiting_question";
            }

            if (tarotFlowState === "waiting_question") {
                addMessage("user", text);
                await startTarotQuestion(text);
                return true;
            }

            if (tarotFlowState === "choosing_method") {
                addMessage("user", text);
                if (/系统|随机|自动|帮我抽|你抽/.test(text)) {
                    await drawTarotRandom(null, false);
                    return true;
                }
                if (/自己|手动|数字|我选/.test(text)) {
                    await startManualTarotDraw(null, false);
                    return true;
                }
                addMessage("assistant", "请选择上方的“系统随机抽牌”或“我自己选牌”，也可以直接回复“系统抽牌”或“自己抽牌”。");
                return true;
            }

            if (tarotFlowState === "shuffling") {
                addMessage("user", text);
                addMessage("assistant", "我正在处理这次抽牌，请稍等一下。");
                return true;
            }

            if (tarotFlowState === "waiting_numbers") {
                addMessage("user", text);
                const numbers = parseTarotNumbersFromText(text);
                await drawTarotNumbers(numbers, false, null);
                return true;
            }

            if (tarotFlowState === "waiting_reveal" || tarotFlowState === "reading") {
                addMessage("user", text);
                addMessage("assistant", "请先点击三张牌背完成翻牌，三张都翻开后我会自动解读。");
                return true;
            }

            return false;
        }

        function resetTarotFlowState() {
            tarotFlowState = "idle";
            tarotShuffleId = "";
            currentTarotCards = null;
            currentTarotQuestion = "";
            currentTarotNumbers = [];
            currentTarotDrawMode = "";
            currentTarotMethodCard = null;
            revealedTarotIndexes = [];
            tarotReadingRequested = false;
        }

        async function startTarotQuestion(question) {
            resetTarotFlowState();
            tarotFlowState = "choosing_method";
            currentTarotQuestion = question;
            addTarotMethodPrompt();
        }

        function disableTarotInlineCard(card) {
            if (!card) {
                return;
            }
            card.querySelectorAll("input, button").forEach(function(element) {
                element.disabled = true;
            });
        }

        function addTarotMethodPrompt() {
            const card = document.createElement("div");
            card.className = "tarot-inline-card";
            currentTarotMethodCard = card;

            const title = document.createElement("div");
            title.className = "tarot-inline-title";
            title.textContent = "请选择抽牌方式";
            card.appendChild(title);

            const question = document.createElement("div");
            question.className = "tarot-inline-question";
            question.textContent = "本次问题：" + currentTarotQuestion;
            card.appendChild(question);

            const desc = document.createElement("p");
            desc.textContent = "系统随机抽牌会重新洗好 78 张牌并随机抽出 3 张；自己选牌会先洗牌，再让你从 1-78 中输入 3 个数字。";
            card.appendChild(desc);

            const actions = document.createElement("div");
            actions.className = "tarot-inline-actions";

            const randomButton = document.createElement("button");
            randomButton.type = "button";
            randomButton.textContent = "系统随机抽牌";
            randomButton.addEventListener("click", function() {
                drawTarotRandom(card, true);
            });

            const manualButton = document.createElement("button");
            manualButton.type = "button";
            manualButton.className = "tarot-secondary-btn";
            manualButton.textContent = "我自己选牌";
            manualButton.addEventListener("click", function() {
                startManualTarotDraw(card, true);
            });

            const restart = document.createElement("button");
            restart.type = "button";
            restart.className = "tarot-secondary-btn";
            restart.textContent = "换个问题";
            restart.addEventListener("click", function() {
                resetTarotFlowState();
                tarotFlowState = "waiting_question";
                addMessage("assistant", "好的，请在下方输入新的塔罗问题。");
                document.getElementById("userInput").focus();
            });

            actions.appendChild(randomButton);
            actions.appendChild(manualButton);
            actions.appendChild(restart);
            card.appendChild(actions);

            addRichAssistantNode(card);
        }

        async function drawTarotRandom(sourceCard, showUserSelection) {
            if (!currentTarotQuestion) {
                tarotFlowState = "waiting_question";
                addMessage("assistant", "请先写下本次塔罗想问的问题。");
                return;
            }

            if (showUserSelection) {
                addMessage("user", "系统随机抽牌");
            }

            disableTarotInlineCard(sourceCard || currentTarotMethodCard);
            tarotFlowState = "shuffling";
            addMessage("assistant", "正在为这个问题重新洗牌，并随机抽出 3 张牌...");

            try {
                const response = await fetch("/tarot/random-draw", {
                    method: "POST"
                });
                const data = await response.json();

                if (!response.ok) {
                    tarotFlowState = "choosing_method";
                    addMessage("assistant", data.error || "系统抽牌失败，请稍后再试。");
                    return;
                }

                currentTarotCards = data.cards;
                currentTarotNumbers = data.numbers;
                currentTarotDrawMode = "system";
                revealedTarotIndexes = [];
                tarotReadingRequested = false;
                tarotShuffleId = "";
                tarotFlowState = "waiting_reveal";
                addTarotRevealMessage();
            } catch (error) {
                tarotFlowState = "choosing_method";
                addMessage("assistant", "系统抽牌异常：" + error);
            }
        }

        async function startManualTarotDraw(sourceCard, showUserSelection) {
            if (!currentTarotQuestion) {
                tarotFlowState = "waiting_question";
                addMessage("assistant", "请先写下本次塔罗想问的问题。");
                return;
            }

            if (showUserSelection) {
                addMessage("user", "我自己选牌");
            }

            disableTarotInlineCard(sourceCard || currentTarotMethodCard);
            tarotFlowState = "shuffling";
            addMessage("assistant", "正在为这次问题洗好 78 张牌...");

            try {
                const response = await fetch("/tarot/shuffle", {
                    method: "POST"
                });
                const data = await response.json();

                if (!response.ok) {
                    tarotFlowState = "choosing_method";
                    addMessage("assistant", data.error || "洗牌失败，请稍后再试。");
                    return;
                }

                tarotShuffleId = data.shuffle_id;
                currentTarotDrawMode = "manual";
                tarotFlowState = "waiting_numbers";
                addTarotNumberPrompt();
            } catch (error) {
                tarotFlowState = "choosing_method";
                addMessage("assistant", "洗牌异常：" + error);
            }
        }

        function parseTarotNumbersFromText(text) {
            return text
                .split(/[,\\s，、]+/)
                .filter(Boolean)
                .map(function(value) {
                    return Number(value);
                });
        }

        function parseTarotNumbersFromCard(card) {
            return Array.from(card.querySelectorAll("input")).map(function(input) {
                return Number(input.value.trim());
            });
        }

        function validateTarotNumbers(numbers) {
            if (numbers.length !== 3 || numbers.some(function(number) { return !Number.isInteger(number); })) {
                return "请填入 3 个 1-78 的整数。";
            }
            if (new Set(numbers).size !== numbers.length) {
                return "3 个数字不能重复，请重新选择。";
            }
            if (numbers.some(function(number) { return number < 1 || number > 78; })) {
                return "数字必须在 1-78 之间。";
            }
            return "";
        }

        function addTarotNumberPrompt() {
            const card = document.createElement("div");
            card.className = "tarot-inline-card";

            const title = document.createElement("div");
            title.className = "tarot-inline-title";
            title.textContent = "已洗好牌，请选择 3 个数字";
            card.appendChild(title);

            const question = document.createElement("div");
            question.className = "tarot-inline-question";
            question.textContent = "本次问题：" + currentTarotQuestion;
            card.appendChild(question);

            const desc = document.createElement("p");
            desc.textContent = "从 1-78 中选择 3 个不重复数字。你可以在这里填，也可以直接在下方输入，例如：7 24 66。";
            card.appendChild(desc);

            const grid = document.createElement("div");
            grid.className = "tarot-number-grid inline";
            [1, 2, 3].forEach(function(index) {
                const label = document.createElement("label");
                label.className = "tarot-number-field";

                const span = document.createElement("span");
                span.textContent = "第 " + index + " 张";

                const input = document.createElement("input");
                input.type = "number";
                input.min = "1";
                input.max = "78";
                input.inputMode = "numeric";
                input.placeholder = "1-78";

                label.appendChild(span);
                label.appendChild(input);
                grid.appendChild(label);
            });
            card.appendChild(grid);

            const actions = document.createElement("div");
            actions.className = "tarot-inline-actions";

            const confirm = document.createElement("button");
            confirm.type = "button";
            confirm.textContent = "确认抽牌";
            confirm.addEventListener("click", function() {
                const numbers = parseTarotNumbersFromCard(card);
                drawTarotNumbers(numbers, true, card);
            });

            const restart = document.createElement("button");
            restart.type = "button";
            restart.className = "tarot-secondary-btn";
            restart.textContent = "换个问题";
            restart.addEventListener("click", function() {
                resetTarotFlowState();
                tarotFlowState = "waiting_question";
                addMessage("assistant", "好的，请在下方输入新的塔罗问题。");
                document.getElementById("userInput").focus();
            });

            actions.appendChild(confirm);
            actions.appendChild(restart);
            card.appendChild(actions);

            addRichAssistantNode(card);
            const firstInput = card.querySelector("input");
            if (firstInput) {
                firstInput.focus();
            }
        }

        async function drawTarotNumbers(numbers, showUserSelection, sourceCard) {
            const error = validateTarotNumbers(numbers);
            if (error) {
                addMessage("assistant", error);
                return;
            }

            if (!tarotShuffleId) {
                addMessage("assistant", "这次洗牌已经失效了，请重新输入问题开始一次新的抽牌。");
                tarotFlowState = "waiting_question";
                return;
            }

            if (showUserSelection) {
                addMessage("user", "我选择：" + numbers.join("、"));
            }

            disableTarotInlineCard(sourceCard);

            addMessage("assistant", "已确认你的 3 个数字，正在从洗好的牌序中抽出对应牌面...");

            try {
                const response = await fetch("/tarot/draw", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        shuffle_id: tarotShuffleId,
                        numbers: numbers
                    })
                });
                const data = await response.json();

                if (!response.ok) {
                    addMessage("assistant", data.error || "抽牌失败");
                    return;
                }

                currentTarotCards = data.cards;
                currentTarotNumbers = numbers;
                currentTarotDrawMode = "manual";
                revealedTarotIndexes = [];
                tarotReadingRequested = false;
                tarotShuffleId = "";
                tarotFlowState = "waiting_reveal";
                addTarotRevealMessage();
            } catch (error) {
                addMessage("assistant", "抽牌异常：" + error);
            }
        }

        function addTarotRevealMessage() {
            const card = document.createElement("div");
            card.className = "tarot-inline-card";

            const title = document.createElement("div");
            title.className = "tarot-inline-title";
            title.textContent = "请点击牌背翻牌";
            card.appendChild(title);

            const question = document.createElement("div");
            question.className = "tarot-inline-question";
            const drawLabel = currentTarotDrawMode === "system" ? "系统抽到：" : "你选择了：";
            question.textContent = "本次问题：" + currentTarotQuestion + "｜" + drawLabel + currentTarotNumbers.join("、");
            card.appendChild(question);

            const desc = document.createElement("p");
            desc.textContent = "三张牌都翻开后，我会自动开始解读。";
            card.appendChild(desc);

            const grid = document.createElement("div");
            grid.className = "tarot-flip-grid";
            currentTarotCards.forEach(function(item, index) {
                grid.appendChild(createTarotFlipCard(item, index));
            });
            card.appendChild(grid);

            addRichAssistantNode(card);
        }

        function createTarotFlipCard(item, index) {
            const button = document.createElement("button");
            button.type = "button";
            button.className = "tarot-flip-card";
            button.dataset.tarotIndex = String(index);
            button.addEventListener("click", function() {
                flipTarotCard(index, button);
            });

            const inner = document.createElement("div");
            inner.className = "tarot-flip-inner";

            const back = document.createElement("div");
            back.className = "tarot-card-face tarot-card-back";
            const backImage = document.createElement("img");
            backImage.src = TAROT_CARD_BACK;
            backImage.alt = "塔罗牌背，点击翻牌";
            back.appendChild(backImage);

            const front = document.createElement("div");
            front.className = "tarot-card-face tarot-card-front";
            const frontImage = document.createElement("img");
            frontImage.src = item.image;
            frontImage.alt = item.card + " " + item.orientation;
            if (item.orientation === "逆位") {
                frontImage.className = "reversed-card-image";
            }
            front.appendChild(frontImage);

            inner.appendChild(back);
            inner.appendChild(front);

            const meta = document.createElement("div");
            meta.className = "tarot-flip-meta";

            const position = document.createElement("div");
            position.className = "tarot-flip-position";
            position.textContent = item.position + " · " + item.choice;

            const name = document.createElement("div");
            name.className = "tarot-flip-name";
            name.textContent = "点击翻牌";

            meta.appendChild(position);
            meta.appendChild(name);

            button.appendChild(inner);
            button.appendChild(meta);
            return button;
        }

        function flipTarotCard(index, button) {
            if (!currentTarotCards || revealedTarotIndexes.includes(index) || tarotReadingRequested) {
                return;
            }

            const item = currentTarotCards[index];
            revealedTarotIndexes.push(index);
            button.classList.add("flipped");
            button.querySelector(".tarot-flip-name").textContent = item.card + "（" + item.orientation + "）";
            persistCurrentSession();

            if (revealedTarotIndexes.length === currentTarotCards.length && !tarotReadingRequested) {
                tarotReadingRequested = true;
                tarotFlowState = "reading";
                persistCurrentSession();
                requestTarotReading();
            }
        }

        async function requestTarotReading() {
            const cardSummary = currentTarotCards.map(function(item) {
                return item.position + "（" + item.choice + "）：" + item.card + "（" + item.orientation + "）";
            }).join("\\n");
            const drawSummary = currentTarotDrawMode === "system"
                ? "系统从重新洗好的 78 张牌里随机抽到：" + currentTarotNumbers.join("、")
                : "我从洗好的 78 张牌里选择了：" + currentTarotNumbers.join("、");
            const userText = "我的塔罗问题：" + currentTarotQuestion
                + "\\n" + drawSummary
                + "\\n抽牌结果：\\n" + cardSummary;

            await sendMessage({
                text: userText,
                showUser: false,
                tarotCards: currentTarotCards,
                bypassSkillFlow: true
            });

            tarotFlowState = "done";
            persistCurrentSession();
        }

        function clearChat() {
            resetConversation();
            showSkillGuide(activeSkillId);
            document.getElementById("userInput").focus();
        }

        document.getElementById("userInput").addEventListener("input", function() {
            persistCurrentSession();
        });

        document.getElementById("userInput").addEventListener("keydown", function(event) {
            if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        });

        renderServiceCards();
        renderPreferenceSummary();

        document.getElementById("openPreferences").addEventListener("click", openPreferences);
        document.getElementById("closePreferences").addEventListener("click", closePreferences);
        document.querySelector(".preference-backdrop").addEventListener("click", closePreferences);
        document.getElementById("savePreferences").addEventListener("click", savePreferences);
        document.getElementById("skipPreferences").addEventListener("click", skipPreferences);

        if (!userPreferences.setupComplete) {
            openPreferences();
        }
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

        active_skill = resolve_skill(req.skill_id, latest_user_text)
        skill_prompt = build_skill_prompt(
            active_skill,
            latest_user_text,
            normal_messages,
            req.tarot_cards,
        )
        forced_calendar_need = get_forced_calendar_need(active_skill)
        runtime_system_prompt = build_runtime_system_prompt(
            latest_user_text,
            req.timezone,
            skill_prompt,
            forced_calendar_need,
            req.user_preferences,
        )

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
            "reply": reply,
            "skill_id": active_skill["id"] if active_skill else None,
            "skill_name": active_skill["name"] if active_skill else None,
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": f"请求失败：{type(e).__name__}: {str(e)}"
            }
        )
