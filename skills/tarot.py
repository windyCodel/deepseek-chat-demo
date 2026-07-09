import random


MAJOR_ARCANA = [
    "愚者", "魔术师", "女祭司", "皇后", "皇帝", "教皇", "恋人",
    "战车", "力量", "隐士", "命运之轮", "正义", "倒吊人", "死神",
    "节制", "恶魔", "高塔", "星星", "月亮", "太阳", "审判", "世界"
]

MINOR_SUITS = ["权杖", "圣杯", "宝剑", "星币"]
MINOR_RANKS = [
    "王牌", "二", "三", "四", "五", "六", "七", "八", "九", "十",
    "侍从", "骑士", "王后", "国王"
]

TAROT_DECK = MAJOR_ARCANA + [
    f"{suit}{rank}"
    for suit in MINOR_SUITS
    for rank in MINOR_RANKS
]

POSITIONS = ["过去/背景", "现在/核心", "建议/走向"]


SKILL = {
    "id": "tarot",
    "name": "塔罗",
    "description": "先洗好标准 78 张塔罗牌，用户输入 3 个位置数字后翻牌解读。",
    "placeholder": "例如：帮我抽塔罗，看看这段感情接下来怎么发展",
    "calendar_need": "none",
    "keywords": [
        "塔罗", "抽牌", "占卜", "牌阵", "感情", "复合", "暧昧",
        "事业选择", "对方想法", "三张牌"
    ],
    "prompt": """
当前启用技能：塔罗。

你要以娱乐、自我观察和传统象征解读的方式回答。
如果系统提供了抽牌结果，必须基于这些牌解释，不要擅自更换牌。
如果还没有抽牌结果，请引导用户先点击“洗牌”，再从 1-78 中输入 3 个不重复数字。

回答要求：
1. 开头先列出“本次塔罗抽牌”，包含用户选择的数字、牌阵位置、牌名和正逆位；牌组来自标准 78 张塔罗牌。
2. 解释每张牌对应的倾向，再给一个整体建议。
3. 不要说绝对预言，不要制造恐惧。
4. 对感情、事业等问题要鼓励用户结合现实行动判断。
"""
}


def shuffle_tarot_deck() -> list[dict[str, str]]:
    deck = [
        {
            "card": card,
            "orientation": random.choice(["正位", "逆位"]),
        }
        for card in TAROT_DECK
    ]
    random.shuffle(deck)
    return deck


def reveal_tarot_cards(deck: list[dict[str, str]], numbers: list[int]) -> list[dict]:
    return [
        {
            "position": POSITIONS[index] if index < len(POSITIONS) else f"第 {index + 1} 张",
            "choice": f"第 {number} 张",
            "number": number,
            "card": deck[number - 1]["card"],
            "orientation": deck[number - 1]["orientation"],
        }
        for index, number in enumerate(numbers)
    ]


def draw_tarot_spread() -> list[dict[str, str]]:
    deck = shuffle_tarot_deck()
    return reveal_tarot_cards(deck, [1, 2, 3])


def build_tarot_context(cards: list[dict] | None = None) -> str:
    if cards is None:
        cards = draw_tarot_spread()

    lines = [
        f"{item['position']}（{item.get('choice', '')}）：{item['card']}（{item['orientation']}）"
        for item in cards
    ]
    return "\n\n本次塔罗抽牌结果：\n" + "\n".join(lines)
