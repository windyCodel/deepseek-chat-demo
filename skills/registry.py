from . import bazi, daily_fortune, date_selection, dream, naming, tarot


SKILL_MODULES = [daily_fortune, tarot, bazi, dream, date_selection, naming]
SKILLS = {module.SKILL["id"]: module.SKILL for module in SKILL_MODULES}

COMMON_SKILL_FLOW_PROMPT = """
通用技能执行规则：
1. 先判断当前对话是在收集信息、正式分析，还是用户对上一轮结果继续追问。
2. 信息不足时，只问下一步最关键的 1 个问题；不要一次列清单，不要先输出大段说明。
3. 如果用户消息或系统补充里已经明确写出“已确认的信息”“已经收齐的信息”“不要再次询问这些信息”，必须直接分析，不要重复索要同一项信息。
4. 正式分析时先给核心判断，再给依据和建议；每个自然标签后直接写内容，不要使用 Markdown 星号、下划线或夸张标题。
5. 追问上一轮结果时，默认沿用前文信息和当前技能语境，不要要求用户重新开始流程。
6. 所有结论都用“倾向”“可能”“可以参考”“更适合”表达，不能说成绝对事实、保证或预言。
7. 用户问“准不准”“会不会一定发生”“能不能保证”时，先说明不能保证，再把回答转成可观察信号和现实行动建议。
8. 用户没有要求详细时，正式分析默认控制在 4 到 6 个自然标签内；追问默认 2 到 4 句话，不重新输出完整报告。
9. 如果用户请求越过安全边界、隐私边界或专业边界，先简短说明不能这样判断，再提供安全的替代分析方向。
10. 安全边界优先于技能流程。用户请求借助玄学、仪式、咒语、符咒、法术、降头、蛊术、八字、塔罗、解梦、择日等方式伤害、控制、恐吓、报复、操纵他人，拒绝提供方法、话术、步骤或具体仪式；转为保护自己、放下执念、建立边界、平复情绪。
11. 涉及彩票、赌博、博彩、盘口、下注、赌运、中奖号码、必中号码、稳赢比分、稳赚套利，不提供投注指令、号码、盘口建议或保证收益；如果只是娱乐讨论，只能给不确定性分析和预算风险提醒。
12. 涉及医疗、心理诊断、用药、疾病吉凶、生死判断、法律诉讼、合同风险、投资理财、贷款债务、违法规避、诈骗、黑客、武器、爆炸物、毒品、隐私密钥、未成年人性内容或现实人身危险，停止对应玄学分析，按安全替代方向回应。
13. 输出前自检：是否重复问了已提供的信息；是否用了绝对化词；是否制造恐惧；是否给了医疗、法律、金融、心理治疗承诺；是否帮助伤害、控制、赌博下注、违法规避、泄露隐私；是否允许用户偏好覆盖安全边界；是否误用了其他技能术语。
"""


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
            ["八字", "四柱", "命理", "大运", "流年", "排盘", "合婚", "五行喜忌"],
        ),
        (
            "tarot",
            ["塔罗", "抽牌", "牌阵", "复合", "暧昧", "对方想法", "对方态度", "他怎么想", "她怎么想", "三张牌"],
        ),
        (
            "daily_fortune",
            ["每日运势", "今日运势", "今天运势", "明日运势", "本周运势", "星座运势", "生肖运势", "幸运色", "幸运数字"],
        ),
        (
            "dream",
            ["解梦", "周公解梦", "梦见", "梦到", "做梦", "噩梦", "梦境", "反复做梦", "掉牙", "被追"],
        ),
        (
            "date_selection",
            ["择日", "黄历", "老黄历", "黄道吉日", "吉日", "良辰", "搬家", "入宅", "开业", "签约", "领证", "结婚日子"],
        ),
        (
            "naming",
            ["起名", "取名", "名字", "姓名", "改名", "宝宝名", "公司名", "店名", "品牌名", "商标名", "艺名"],
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

    prompt = skill["prompt"].strip() + "\n\n" + COMMON_SKILL_FLOW_PROMPT.strip()

    if skill["id"] == "tarot":
        if tarot_cards:
            prompt += tarot.build_tarot_context(tarot_cards)
        elif any("抽牌结果" in (message.get("content") or "") for message in messages):
            prompt += "\n\n当前对话里已有塔罗抽牌结果。用户后续追问时，请基于前文牌面继续解释，不要要求重新抽牌。"
        else:
            prompt += "\n\n当前还没有抽牌结果。请引导用户先写下问题，再选择系统随机抽牌或自己从 1-78 中输入 3 个不重复数字，最后点击牌背翻牌。"

    return prompt
