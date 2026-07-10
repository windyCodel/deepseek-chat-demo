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

MAJOR_IMAGE_FILES = [
    "major_00_fool.jpg",
    "major_01_magician.jpg",
    "major_02_high_priestess.jpg",
    "major_03_empress.jpg",
    "major_04_emperor.jpg",
    "major_05_hierophant.jpg",
    "major_06_lovers.jpg",
    "major_07_chariot.jpg",
    "major_08_strength.jpg",
    "major_09_hermit.jpg",
    "major_10_wheel_of_fortune.jpg",
    "major_11_justice.jpg",
    "major_12_hanged_man.jpg",
    "major_13_death.jpg",
    "major_14_temperance.jpg",
    "major_15_devil.jpg",
    "major_16_tower.jpg",
    "major_17_star.jpg",
    "major_18_moon.jpg",
    "major_19_sun.jpg",
    "major_20_judgement.jpg",
    "major_21_world.jpg",
]

SUIT_IMAGE_PREFIXES = {
    "权杖": "wands",
    "圣杯": "cups",
    "宝剑": "swords",
    "星币": "pents",
}

TAROT_IMAGE_FILES = MAJOR_IMAGE_FILES + [
    f"{SUIT_IMAGE_PREFIXES[suit]}_{index + 1:02d}.jpg"
    for suit in MINOR_SUITS
    for index, _rank in enumerate(MINOR_RANKS)
]

CARD_IMAGE_PATHS = {
    card: f"/static/tarot/cards/{image_file}"
    for card, image_file in zip(TAROT_DECK, TAROT_IMAGE_FILES)
}

POSITIONS = ["过去/背景", "现在/核心", "建议/走向"]


SKILL = {
    "id": "tarot",
    "name": "塔罗",
    "description": "先洗好标准 78 张塔罗牌，用户输入 3 个位置数字并点击翻牌后解读。",
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
如果还没有抽牌结果，请引导用户先写下问题，点击“开始洗牌”，再从 1-78 中输入 3 个不重复数字并点击牌背翻牌。

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
            "image": CARD_IMAGE_PATHS[card],
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
            "image": deck[number - 1]["image"],
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
