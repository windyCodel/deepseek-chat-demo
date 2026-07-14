from . import bazi, daily_fortune, date_selection, naming, tarot


SKILL_MODULES = [daily_fortune, tarot, bazi, date_selection, naming]
SKILLS = {module.SKILL["id"]: module.SKILL for module in SKILL_MODULES}


def get_skill_options() -> list[dict[str, str]]:
    return [
        {
            "id": skill["id"],
            "name": skill["name"],
            "description": skill["description"],
            "placeholder": skill["placeholder"],
        }
        for skill in SKILLS.values()
    ]


def resolve_skill(requested_skill_id: str | None, latest_user_text: str) -> dict | None:
    if requested_skill_id in SKILLS:
        return SKILLS[requested_skill_id]

    text = latest_user_text or ""

    routing_priority = [
        (
            "bazi",
            ["八字", "四柱", "命理", "大运", "流年", "排盘"],
        ),
        (
            "tarot",
            ["塔罗", "抽牌", "牌阵", "复合", "暧昧", "对方想法", "对方态度", "他怎么想", "她怎么想"],
        ),
        (
            "daily_fortune",
            ["每日运势", "今日运势", "今天运势", "明日运势", "星座运势", "生肖运势"],
        ),
        (
            "date_selection",
            ["择日", "黄道吉日", "吉日", "良辰", "搬家", "入宅", "开业", "签约", "领证"],
        ),
        (
            "naming",
            ["起名", "取名", "名字", "姓名", "改名", "宝宝名", "公司名", "店名", "艺名"],
        ),
    ]

    for skill_id, keywords in routing_priority:
        if any(keyword in text for keyword in keywords):
            return SKILLS[skill_id]

    best_skill = None
    best_score = 0

    for skill in SKILLS.values():
        score = sum(1 for keyword in skill["keywords"] if keyword in text)
        if score > best_score:
            best_skill = skill
            best_score = score

    if best_score == 0:
        return None

    return best_skill


def get_forced_calendar_need(skill: dict | None) -> str | None:
    if not skill:
        return None

    calendar_need = skill.get("calendar_need")
    if calendar_need == "none":
        return None

    return calendar_need


def build_skill_prompt(
    skill: dict | None,
    latest_user_text: str,
    messages: list,
    tarot_cards: list[dict] | None = None,
) -> str:
    if not skill:
        return ""

    prompt = skill["prompt"].strip()

    if skill["id"] == "tarot":
        if tarot_cards:
            prompt += tarot.build_tarot_context(tarot_cards)
        elif any("抽牌结果" in (message.get("content") or "") for message in messages):
            prompt += "\n\n当前对话里已有塔罗抽牌结果。用户后续追问时，请基于前文牌面继续解释，不要要求重新抽牌。"
        else:
            prompt += "\n\n当前还没有抽牌结果。请引导用户先写下问题，再选择系统随机抽牌或自己从 1-78 中输入 3 个不重复数字，最后点击牌背翻牌。"

    return prompt
