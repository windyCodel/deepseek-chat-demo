import os
import random
import logging
import time
from collections import defaultdict, deque
from datetime import datetime
from uuid import uuid4
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from lunardate import LunarDate

from fastapi import FastAPI, Request
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

logger = logging.getLogger(__name__)

MAX_REQUEST_BODY_BYTES = 64 * 1024
MAX_CHAT_MESSAGES = 12
MAX_MESSAGE_LENGTH = 4_000
TAROT_SHUFFLE_TTL_SECONDS = 15 * 60
MAX_TAROT_SHUFFLES = 500
RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMITS = {
    "chat": 30,
    "tarot": 30,
}
RATE_LIMIT_BUCKETS: dict[str, deque[float]] = defaultdict(deque)

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
TAROT_SHUFFLES: dict[str, tuple[float, list[dict[str, str]]]] = {}


def add_security_headers(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "img-src 'self' data:; "
        "style-src 'self'; "
        "script-src 'self'; "
        "connect-src 'self'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'none'"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    return response


@app.middleware("http")
async def add_security_controls(request: Request, call_next):
    content_length = request.headers.get("content-length")
    if content_length:
        try:
            if int(content_length) > MAX_REQUEST_BODY_BYTES:
                return add_security_headers(
                    JSONResponse(
                        status_code=413,
                        content={"error": "请求内容过大，请缩短后重试。"},
                    )
                )
        except ValueError:
            return add_security_headers(
                JSONResponse(
                    status_code=400,
                    content={"error": "请求长度无效。"},
                )
            )

    return add_security_headers(await call_next(request))


def get_rate_limit_key(request: Request, scope: str) -> str:
    forwarded_for = request.headers.get("x-forwarded-for", "")
    client_host = forwarded_for.split(",", 1)[0].strip()
    if not client_host:
        client_host = request.client.host if request.client else "unknown"
    return f"{scope}:{client_host}"


def check_rate_limit(request: Request, scope: str):
    now = time.monotonic()
    for key, existing_bucket in list(RATE_LIMIT_BUCKETS.items()):
        while existing_bucket and now - existing_bucket[0] >= RATE_LIMIT_WINDOW_SECONDS:
            existing_bucket.popleft()
        if not existing_bucket:
            RATE_LIMIT_BUCKETS.pop(key, None)

    bucket = RATE_LIMIT_BUCKETS[get_rate_limit_key(request, scope)]
    while bucket and now - bucket[0] >= RATE_LIMIT_WINDOW_SECONDS:
        bucket.popleft()

    limit = RATE_LIMITS[scope]
    if len(bucket) >= limit:
        retry_after = max(1, int(RATE_LIMIT_WINDOW_SECONDS - (now - bucket[0])))
        return JSONResponse(
            status_code=429,
            content={"error": "请求过于频繁，请稍后再试。"},
            headers={"Retry-After": str(retry_after)},
        )

    bucket.append(now)
    return None


def clear_expired_tarot_shuffles():
    expires_before = time.monotonic() - TAROT_SHUFFLE_TTL_SECONDS
    expired_ids = [
        shuffle_id
        for shuffle_id, (created_at, _) in TAROT_SHUFFLES.items()
        if created_at < expires_before
    ]
    for shuffle_id in expired_ids:
        TAROT_SHUFFLES.pop(shuffle_id, None)


def validate_chat_messages(raw_messages) -> list[dict[str, str]]:
    if not isinstance(raw_messages, list):
        raise ValueError("消息格式无效。")

    cleaned_messages = []
    for message in raw_messages:
        if not isinstance(message, dict):
            raise ValueError("消息格式无效。")

        role = message.get("role")
        if role == "system":
            continue
        if role not in {"user", "assistant"}:
            raise ValueError("消息角色无效。")

        content = message.get("content")
        if not isinstance(content, str):
            raise ValueError("消息内容无效。")
        content = content.strip()
        if not content:
            continue
        if len(content) > MAX_MESSAGE_LENGTH:
            raise ValueError(f"单条消息不能超过 {MAX_MESSAGE_LENGTH} 个字符。")

        cleaned_messages.append({"role": role, "content": content})

    if not cleaned_messages:
        raise ValueError("请先输入消息。")
    if len(cleaned_messages) > MAX_CHAT_MESSAGES:
        cleaned_messages = cleaned_messages[-MAX_CHAT_MESSAGES:]

    return cleaned_messages


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
async def tarot_shuffle(request: Request):
    rate_limited = check_rate_limit(request, "tarot")
    if rate_limited:
        return rate_limited

    clear_expired_tarot_shuffles()
    if len(TAROT_SHUFFLES) >= MAX_TAROT_SHUFFLES:
        oldest_shuffle_id = next(iter(TAROT_SHUFFLES))
        TAROT_SHUFFLES.pop(oldest_shuffle_id, None)

    shuffle_id = str(uuid4())
    TAROT_SHUFFLES[shuffle_id] = (time.monotonic(), shuffle_tarot_deck())

    return {
        "shuffle_id": shuffle_id,
        "deck_size": len(TAROT_DECK),
        "message": "已洗好 78 张塔罗牌，请从 1-78 中选择 3 个不重复数字。",
    }


@app.post("/tarot/random-draw")
async def tarot_random_draw(request: Request):
    rate_limited = check_rate_limit(request, "tarot")
    if rate_limited:
        return rate_limited

    deck = shuffle_tarot_deck()
    numbers = random.sample(range(1, len(deck) + 1), 3)
    cards = reveal_tarot_cards(deck, numbers)

    return {
        "cards": cards,
        "numbers": numbers,
        "deck_size": len(deck),
    }


@app.post("/tarot/draw")
async def tarot_draw(req: TarotDrawRequest, request: Request):
    rate_limited = check_rate_limit(request, "tarot")
    if rate_limited:
        return rate_limited

    clear_expired_tarot_shuffles()
    shuffle = TAROT_SHUFFLES.get(req.shuffle_id)
    if not shuffle:
        return JSONResponse(
            status_code=400,
            content={"error": "洗牌已失效，请重新开始抽牌。"},
        )

    _, deck = shuffle

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
    <link rel="stylesheet" href="/static/style.css">
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
            <div id="serviceGrid" class="service-grid" aria-label="解答方向">
                <button type="button" class="service-card" data-static-skill-id="daily_fortune">
                    <div class="service-card-title">每日运势</div>
                    <div class="service-card-desc">看看今日、明日或本周的节奏与提示。</div>
                    <div class="service-card-meta">进入对话</div>
                </button>
                <button type="button" class="service-card" data-static-skill-id="tarot">
                    <div class="service-card-title">塔罗占卜</div>
                    <div class="service-card-desc">先写下问题，再抽三张牌进行解读。</div>
                    <div class="service-card-meta">进入对话</div>
                </button>
                <button type="button" class="service-card" data-static-skill-id="bazi">
                    <div class="service-card-title">八字分析</div>
                    <div class="service-card-desc">围绕出生信息和关注方向逐步分析。</div>
                    <div class="service-card-meta">进入对话</div>
                </button>
                <button type="button" class="service-card" data-static-skill-id="date_selection">
                    <div class="service-card-title">择日</div>
                    <div class="service-card-desc">为搬家、开业、签约等事项梳理时间。</div>
                    <div class="service-card-meta">进入对话</div>
                </button>
                <button type="button" class="service-card" data-static-skill-id="naming">
                    <div class="service-card-title">姓名分析</div>
                    <div class="service-card-desc">分析已有名字，或一起寻找合适的名字。</div>
                    <div class="service-card-meta">进入对话</div>
                </button>
                <button type="button" class="service-card" data-static-skill-id="">
                    <div class="service-card-title">通用咨询</div>
                    <div class="service-card-desc">还不确定方向时，从这里开始聊聊。</div>
                    <div class="service-card-meta">进入对话</div>
                </button>
            </div>
        </section>

        <section id="chatView" class="app-view chat-view">
            <div class="chat-header">
                <button id="backToServices" type="button" class="back-btn" aria-label="返回解答选择" title="返回解答选择">‹</button>
                <div class="chat-assistant">
                    <div class="chat-header-avatar" aria-hidden="true">筮</div>
                    <div>
                        <div class="chat-assistant-name">筮渡 AI</div>
                        <div id="skillHint" class="chat-status">正在对话</div>
                    </div>
                </div>
                <button id="clearChat" type="button" class="clear-chat-btn" aria-label="清空当前对话" title="清空当前对话">↺</button>
            </div>

            <div id="chatBox"></div>

            <div class="input-row">
                <textarea id="userInput" placeholder="请输入你的问题，例如：我想看每日运势、八字、塔罗、风水、运势或姓名分析"></textarea>
                <button id="sendMessage" class="send-btn" type="button">发送</button>
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

    <script src="/static/app.js" defer></script>
</body>
</html>
"""


@app.post("/chat")
async def chat(req: ChatRequest, request: Request):
    rate_limited = check_rate_limit(request, "chat")
    if rate_limited:
        return rate_limited

    try:
        normal_messages = validate_chat_messages(req.messages)

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

    except ValueError as error:
        return JSONResponse(
            status_code=400,
            content={"error": str(error)},
        )
    except Exception:
        logger.exception("Chat request failed")
        return JSONResponse(
            status_code=500,
            content={"error": "服务暂时不可用，请稍后再试。"},
        )
