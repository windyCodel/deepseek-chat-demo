const skillConfigs = {
            "": {
                placeholder: "请输入你的问题，例如：我想看每日运势、八字、塔罗、择日或姓名分析",
                hint: "通用咨询：直接描述你的问题，我会尽量判断适合的方向。",
                serviceTitle: "自由聊聊",
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
        const PRIMARY_SERVICE_ORDER = ["daily_fortune", "tarot", "bazi", ""];
        const SECONDARY_SERVICE_ORDER = ["date_selection", "naming"];
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
        let dailyFortuneState = defaultDailyFortuneState();
        let baziFlowState = defaultBaziFlowState();
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

        function setTarotFlowState(nextState) {
            tarotFlowState = nextState;
            if (document.getElementById("userInput")) {
                updateUserInputPlaceholder();
            }
        }

        function restoreTarotState(state) {
            resetTarotFlowState();
            if (!state) {
                return;
            }

            setTarotFlowState(state.tarotFlowState || "idle");
            tarotShuffleId = state.tarotShuffleId || "";
            currentTarotCards = state.currentTarotCards || null;
            currentTarotQuestion = state.currentTarotQuestion || "";
            currentTarotNumbers = Array.isArray(state.currentTarotNumbers) ? state.currentTarotNumbers : [];
            currentTarotDrawMode = state.currentTarotDrawMode || "";
            currentTarotMethodCard = null;
            revealedTarotIndexes = Array.isArray(state.revealedTarotIndexes) ? state.revealedTarotIndexes : [];
            tarotReadingRequested = Boolean(state.tarotReadingRequested);
        }

        function defaultDailyFortuneState() {
            return { period: "today" };
        }

        function getDailyFortuneState() {
            return { period: dailyFortuneState.period || "today" };
        }

        function resetDailyFortuneState() {
            dailyFortuneState = defaultDailyFortuneState();
        }

        function restoreDailyFortuneState(state) {
            const allowedPeriods = ["today", "tomorrow", "week"];
            dailyFortuneState = {
                period: state && allowedPeriods.includes(state.period) ? state.period : "today"
            };
        }

        function updateDailyFortunePeriod(text) {
            if (/明天|明日/.test(text)) {
                dailyFortuneState.period = "tomorrow";
            } else if (/本周|这周|一周|本星期/.test(text)) {
                dailyFortuneState.period = "week";
            } else if (/今天|今日/.test(text)) {
                dailyFortuneState.period = "today";
            }
        }

        function buildDailyFortuneRequest(text) {
            const periodLabels = {
                today: "今天",
                tomorrow: "明天",
                week: "本周"
            };
            const period = periodLabels[dailyFortuneState.period] || "今天";
            return "当前每日运势的时间范围是“" + period + "”，请保持该时间范围回答。\n用户问题：" + text;
        }

        function defaultBaziFlowState() {
            return {
                stage: "intro",
                birthDate: "",
                birthTime: "",
                birthCity: "",
                gender: "",
                focus: ""
            };
        }

        function getBaziState() {
            return Object.assign({}, baziFlowState);
        }

        function resetBaziFlowState() {
            baziFlowState = defaultBaziFlowState();
            if (document.getElementById("userInput")) {
                updateUserInputPlaceholder();
            }
        }

        function restoreBaziState(state, hasLegacyConversation) {
            const defaults = defaultBaziFlowState();
            if (!state || typeof state !== "object") {
                baziFlowState = defaults;
                if (hasLegacyConversation) {
                    baziFlowState.stage = "done";
                }
                return;
            }

            const allowedStages = [
                "intro", "waiting_birth_date", "waiting_birth_time",
                "waiting_birth_city", "waiting_gender", "waiting_focus",
                "analyzing", "done"
            ];
            baziFlowState = {
                stage: allowedStages.includes(state.stage) ? state.stage : "intro",
                birthDate: String(state.birthDate || "").slice(0, 80),
                birthTime: String(state.birthTime || "").slice(0, 80),
                birthCity: String(state.birthCity || "").slice(0, 80),
                gender: String(state.gender || "").slice(0, 30),
                focus: String(state.focus || "").slice(0, 100)
            };
            if (baziFlowState.stage === "analyzing") {
                baziFlowState.stage = "waiting_focus";
            }
        }

        function setBaziFlowStage(stage) {
            baziFlowState.stage = stage;
            if (document.getElementById("userInput")) {
                updateUserInputPlaceholder();
            }
        }

        function removeTransientMessages(chatBox = document.getElementById("chatBox")) {
            if (!chatBox) {
                return;
            }
            chatBox.querySelectorAll(".thinking-message, .tarot-progress-message").forEach(function(message) {
                message.remove();
            });
        }

        function removeVisibleMarkdownMarkers(root) {
            if (!root) {
                return;
            }

            const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
            const textNodes = [];
            while (walker.nextNode()) {
                textNodes.push(walker.currentNode);
            }
            textNodes.forEach(function(node) {
                node.nodeValue = node.nodeValue
                    .replace(/\*+/g, "")
                    .replace(/_{2,}/g, "");
            });
        }

        function getPersistableChatHtml(chatBox) {
            if (!chatBox) {
                return "";
            }

            const snapshot = chatBox.cloneNode(true);
            removeTransientMessages(snapshot);
            return snapshot.innerHTML;
        }

        function persistCurrentSession() {
            const skillId = activeSkillId || "";
            const chatBox = document.getElementById("chatBox");
            const input = document.getElementById("userInput");

            chatSessions[skillId] = {
                messages: cloneMessages(messages),
                chatHtml: getPersistableChatHtml(chatBox),
                inputValue: input ? input.value : "",
                tarotState: getTarotState(),
                dailyFortuneState: getDailyFortuneState(),
                baziState: getBaziState(),
                updatedAt: new Date().toISOString()
            };
            saveStoredSessions();
        }

        function rehydrateChatInteractions() {
            document.querySelectorAll(".prompt-chip").forEach(function(chip) {
                chip.addEventListener("click", function() {
                    fillPrompt(chip.dataset.promptText || chip.textContent);
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
                        setTarotFlowState("waiting_question");
                        addMessage("assistant", "好的，请在下方输入新的塔罗问题。");
                        document.getElementById("userInput").focus();
                    }
                });
            });

            document.querySelectorAll(".tarot-flip-card:not(.flipped)").forEach(function(button) {
                const frontImage = button.querySelector(".tarot-card-front img");
                const position = button.querySelector(".tarot-flip-position");
                if (frontImage) {
                    frontImage.alt = "";
                    frontImage.setAttribute("aria-hidden", "true");
                }
                if (position) {
                    button.setAttribute("aria-label", position.textContent + "，点击翻牌");
                }
            });

            const tarotGrids = document.querySelectorAll(".tarot-flip-grid");
            const activeTarotGrid = tarotGrids.length ? tarotGrids[tarotGrids.length - 1] : null;
            if (!activeTarotGrid) {
                return;
            }

            activeTarotGrid.querySelectorAll(".tarot-flip-card").forEach(function(button) {
                const index = Number(button.dataset.tarotIndex);
                const item = currentTarotCards && currentTarotCards[index];
                updateTarotCardAccessibility(button, item, revealedTarotIndexes.includes(index));
                button.addEventListener("click", function() {
                    flipTarotCard(index, button);
                });
            });

        }

        function refreshRestoredGuideCard(skillId) {
            const chatBox = document.getElementById("chatBox");
            const guideCard = chatBox.querySelector(".guide-card");
            if (!guideCard) {
                return;
            }

            guideCard.replaceWith(createGuideCard(getSkillConfig(skillId), skillId));
        }

        function setHistoricalAnswerExpanded(message, expanded) {
            const toggle = message.querySelector(".history-answer-toggle");
            message.classList.toggle("history-answer-collapsed", !expanded);
            if (toggle) {
                toggle.textContent = expanded ? "收起历史回答" : "展开完整回答";
                toggle.setAttribute("aria-expanded", String(expanded));
            }
        }

        function refreshHistoricalAnswers() {
            const chatBox = document.getElementById("chatBox");
            const assistantMessages = Array.from(
                chatBox.querySelectorAll(".msg.assistant:not(.thinking-message)")
            );
            const latestAssistantMessage = assistantMessages.length
                ? assistantMessages[assistantMessages.length - 1]
                : null;

            assistantMessages.forEach(function(message) {
                message.classList.remove("history-answer", "history-answer-collapsed");
                message.querySelectorAll(".history-answer-toggle").forEach(function(toggle) {
                    toggle.remove();
                });

                const answer = message.querySelector(".assistant-text");
                const isLongAnswer = answer && answer.textContent.trim().length > 260;
                if (!isLongAnswer || message === latestAssistantMessage) {
                    return;
                }

                message.classList.add("history-answer");
                const toggle = document.createElement("button");
                toggle.type = "button";
                toggle.className = "history-answer-toggle";
                toggle.addEventListener("click", function() {
                    const expanded = toggle.getAttribute("aria-expanded") === "true";
                    setHistoricalAnswerExpanded(message, !expanded);
                    persistCurrentSession();
                });
                message.querySelector(".message-main").appendChild(toggle);
                setHistoricalAnswerExpanded(message, false);
            });
        }

        function scrollMessageToTop(message, behavior = "auto") {
            if (!message) {
                return;
            }

            const chatBox = document.getElementById("chatBox");
            window.requestAnimationFrame(function() {
                const targetTop = message.getBoundingClientRect().top
                    - chatBox.getBoundingClientRect().top
                    + chatBox.scrollTop
                    - 8;
                chatBox.scrollTo({
                    top: Math.max(0, targetTop),
                    behavior: behavior
                });
            });
        }

        function updateUserInputPlaceholder() {
            const input = document.getElementById("userInput");
            const config = getSkillConfig(activeSkillId);
            if (activeSkillId === "bazi") {
                const placeholders = {
                    intro: config.placeholder,
                    waiting_birth_date: "请输入出生日期，并说明公历或农历，例如：公历 2000 年 7 月 7 日",
                    waiting_birth_time: "请输入出生时间，例如：晚上 8 点；不清楚也可以直接说明",
                    waiting_birth_city: "请输入出生城市，例如：湖南长沙",
                    waiting_gender: "请输入性别；不方便提供也可以回复“跳过”",
                    waiting_focus: "最想关注什么？例如：事业、财运、感情或整体",
                    analyzing: "信息已收齐，筮渡正在整理八字参考",
                    done: "可以继续追问阶段趋势或某个具体方向"
                };
                input.placeholder = placeholders[baziFlowState.stage] || config.placeholder;
                return;
            }
            if (activeSkillId !== "tarot") {
                input.placeholder = config.placeholder;
                return;
            }

            if (tarotFlowState === "choosing_method") {
                input.placeholder = "请选择上方抽牌方式，或输入“系统抽牌 / 自己选牌”";
            } else if (tarotFlowState === "shuffling") {
                input.placeholder = "正在处理这次抽牌，请稍候";
            } else if (tarotFlowState === "waiting_numbers") {
                input.placeholder = "从 1-78 中输入 3 个不重复数字，例如：7、24、66";
            } else if (tarotFlowState === "waiting_reveal") {
                input.placeholder = "请先点击三张牌完成翻牌";
            } else if (tarotFlowState === "reading") {
                input.placeholder = "三张牌已翻开，筮渡正在整理解读";
            } else if (tarotFlowState === "done") {
                input.placeholder = "可以继续追问某张牌或整体建议，也可以输入新的塔罗问题";
            } else {
                input.placeholder = config.placeholder;
            }
        }

        function resetConversation(options = {}) {
            messages = initialMessages();
            document.getElementById("chatBox").innerHTML = "";
            document.getElementById("userInput").value = "";
            resetTarotFlowState();
            resetDailyFortuneState();
            resetBaziFlowState();

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
            removeTransientMessages(chatBox);
            chatBox.querySelectorAll(".assistant-text").forEach(function(bubble) {
                removeVisibleMarkdownMarkers(bubble);
            });
            input.value = session.inputValue || "";
            restoreTarotState(session.tarotState);
            restoreDailyFortuneState(session.dailyFortuneState);
            restoreBaziState(
                session.baziState,
                (skillId || "") === "bazi" && messages.length > 1
            );
            rehydrateChatInteractions();
            refreshRestoredGuideCard(skillId || "");
            refreshHistoricalAnswers();
            updateUserInputPlaceholder();

            const visibleMessages = Array.from(
                chatBox.querySelectorAll(".msg:not(.history-answer-collapsed):not(.thinking-message)")
            );
            const latestAssistantMessage = visibleMessages.slice().reverse().find(function(message) {
                return message.classList.contains("assistant");
            });
            const restoreTarget = latestAssistantMessage
                || (visibleMessages.length ? visibleMessages[visibleMessages.length - 1] : null);
            scrollMessageToTop(restoreTarget);
            persistCurrentSession();
            return Boolean(session.chatHtml);
        }

        function renderServiceCards() {
            const grid = document.getElementById("serviceGrid");
            const secondaryGrid = document.getElementById("secondaryServiceGrid");
            grid.innerHTML = "";
            secondaryGrid.innerHTML = "";

            PRIMARY_SERVICE_ORDER.forEach(function(skillId) {
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

            SECONDARY_SERVICE_ORDER.forEach(function(skillId) {
                const config = getSkillConfig(skillId);
                const card = document.createElement("button");
                card.type = "button";
                card.className = "secondary-service-card";
                card.addEventListener("click", function() {
                    enterChat(skillId);
                });

                const title = document.createElement("span");
                title.className = "secondary-service-title";
                title.textContent = config.serviceTitle;

                const desc = document.createElement("span");
                desc.className = "secondary-service-desc";
                desc.textContent = skillId === "date_selection"
                    ? "搬家、开业、签约等日期参考"
                    : "名字含义、风格与起名建议";

                card.appendChild(title);
                card.appendChild(desc);
                secondaryGrid.appendChild(card);
            });
        }

        function renderServiceFallback() {
            const grid = document.getElementById("serviceGrid");
            const secondaryGrid = document.getElementById("secondaryServiceGrid");
            const fallbackServices = [
                ["daily_fortune", "每日运势", "看看今日、明日或本周的节奏与提示。"],
                ["tarot", "塔罗占卜", "先写下问题，再抽三张牌进行解读。"],
                ["bazi", "八字分析", "围绕出生信息和关注方向逐步分析。"],
                ["", "自由聊聊", "还不确定方向时，从这里开始聊聊。"]
            ];
            const fallbackSecondaryServices = [
                ["date_selection", "择日", "搬家、开业、签约等日期参考"],
                ["naming", "姓名分析", "名字含义、风格与起名建议"]
            ];
            grid.innerHTML = "";
            secondaryGrid.innerHTML = "";

            fallbackServices.forEach(function(service) {
                const card = document.createElement("button");
                card.type = "button";
                card.className = "service-card";
                card.addEventListener("click", function() {
                    enterChat(service[0]);
                });

                const title = document.createElement("div");
                title.className = "service-card-title";
                title.textContent = service[1];
                const desc = document.createElement("div");
                desc.className = "service-card-desc";
                desc.textContent = service[2];

                card.appendChild(title);
                card.appendChild(desc);
                grid.appendChild(card);
            });

            fallbackSecondaryServices.forEach(function(service) {
                const card = document.createElement("button");
                card.type = "button";
                card.className = "secondary-service-card";
                card.addEventListener("click", function() {
                    enterChat(service[0]);
                });

                const title = document.createElement("span");
                title.className = "secondary-service-title";
                title.textContent = service[1];
                const desc = document.createElement("span");
                desc.className = "secondary-service-desc";
                desc.textContent = service[2];

                card.appendChild(title);
                card.appendChild(desc);
                secondaryGrid.appendChild(card);
            });
        }

        function showServiceView() {
            persistCurrentSession();
            document.body.classList.remove("chat-mode");
            document.getElementById("chatView").classList.remove("active");
            document.getElementById("serviceView").classList.add("active");
        }

        function showChatView() {
            document.body.classList.add("chat-mode");
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

            updateUserInputPlaceholder();
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

        function addMessage(role, content, options = {}) {
            if (role === "assistant") {
                removeTransientMessages();
            }
            const shell = createMessageShell(role);
            if (role === "assistant") {
                shell.bubble.classList.add("assistant-text");
                if (options.resultSkillId !== undefined) {
                    const resultClass = String(options.resultSkillId || "free").replace(/_/g, "-");
                    shell.bubble.classList.add("skill-result", "skill-result-" + resultClass);
                }
                shell.bubble.innerHTML = renderAssistantText(content);
            } else {
                shell.bubble.textContent = content;
            }

            shell.chatBox.appendChild(shell.message);
            refreshHistoricalAnswers();
            if (role === "assistant" && String(content).trim().length > 260) {
                scrollMessageToTop(shell.message, "smooth");
            } else {
                shell.chatBox.scrollTop = shell.chatBox.scrollHeight;
            }
            persistCurrentSession();
        }

        function setAssistantMessageContent(message, content) {
            const bubble = message ? message.querySelector(".assistant-text") : null;
            if (!bubble) {
                return;
            }

            if (String(content || "").trim()) {
                bubble.innerHTML = renderAssistantText(content);
            } else {
                bubble.innerHTML = '<p class="streaming-placeholder">正在连接 DeepSeek...</p>';
            }
        }

        function createStreamingAssistantMessage(resultSkillId) {
            removeTransientMessages();
            const shell = createMessageShell("assistant");
            shell.message.classList.add("streaming-message");
            shell.bubble.classList.add("assistant-text", "streaming-text");
            const resultClass = String(resultSkillId || "free").replace(/_/g, "-");
            shell.bubble.classList.add("skill-result", "skill-result-" + resultClass);
            setAssistantMessageContent(shell.message, "");
            shell.chatBox.appendChild(shell.message);
            shell.chatBox.scrollTop = shell.chatBox.scrollHeight;
            return shell;
        }

        function finalizeStreamingAssistantMessage(message, content) {
            if (!message) {
                return;
            }

            message.classList.remove("streaming-message");
            setAssistantMessageContent(message, content);
            refreshHistoricalAnswers();

            if (String(content).trim().length > 260) {
                scrollMessageToTop(message, "smooth");
            } else {
                document.getElementById("chatBox").scrollTop = document.getElementById("chatBox").scrollHeight;
            }
            persistCurrentSession();
        }

        async function readChatError(response) {
            const contentType = response.headers.get("Content-Type") || "";
            if (contentType.includes("application/json")) {
                try {
                    const data = await response.json();
                    return data.error || "请求失败";
                } catch (error) {
                    return "请求失败";
                }
            }

            const text = await response.text();
            return text || "请求失败";
        }

        async function requestChatStream(payload, resultSkillId) {
            const response = await fetch("/chat/stream", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error(await readChatError(response));
            }

            const skillId = response.headers.get("X-Skill-Id") || "";
            const shell = createStreamingAssistantMessage(resultSkillId || skillId);
            const decoder = new TextDecoder("utf-8");
            let reply = "";

            if (!response.body) {
                reply = await response.text();
                return {
                    reply: reply,
                    skillId: skillId,
                    message: shell.message
                };
            }

            const reader = response.body.getReader();
            try {
                while (true) {
                    const result = await reader.read();
                    if (result.done) {
                        break;
                    }

                    reply += decoder.decode(result.value, { stream: true });
                    setAssistantMessageContent(shell.message, reply);
                    shell.chatBox.scrollTop = shell.chatBox.scrollHeight;
                }
                reply += decoder.decode();
            } catch (error) {
                if (!reply.trim()) {
                    shell.message.remove();
                    throw error;
                }
                reply += "\n服务暂时不可用，请稍后再试。";
            }

            return {
                reply: reply,
                skillId: skillId,
                message: shell.message
            };
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
            const lines = String(content || "").replace(/\r\n?/g, "\n").split("\n");
            const blocks = [];
            let listItems = [];

            function renderInline(value) {
                return escapeHtml(value)
                    .replace(/\*{2}\s*([^*\n]+?)\s*\*{2}/g, "<strong>$1</strong>")
                    .replace(/_{2}\s*([^_\n]+?)\s*_{2}/g, "<strong>$1</strong>")
                    .replace(/\*+/g, "")
                    .replace(/_{2,}/g, "");
            }

            function flushList() {
                if (!listItems.length) {
                    return;
                }
                blocks.push('<ul class="assistant-list">' + listItems.map(function(item) {
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

                const heading = trimmed.match(/^#{1,3}\s+(.+)$/);
                const listItem = trimmed.match(/^(?:[-*•]|\d+[.)])\s+(.+)$/);
                const conclusion = trimmed.match(/^(结论|核心结论|今日重点|建议)[：:]\s*(.+)$/);
                const label = trimmed.match(/^([^：:]{1,16}[：:])\s*(.*)$/);
                if (heading) {
                    flushList();
                    blocks.push('<div class="assistant-heading">' + renderInline(heading[1]) + "</div>");
                } else if (listItem) {
                    listItems.push(listItem[1]);
                } else {
                    flushList();
                    if (conclusion) {
                        blocks.push(
                            '<div class="assistant-conclusion">'
                            + '<div class="assistant-conclusion-label">' + renderInline(conclusion[1]) + '</div>'
                            + '<p>' + renderInline(conclusion[2]) + '</p>'
                            + '</div>'
                        );
                    } else if (label) {
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
            refreshHistoricalAnswers();
            shell.chatBox.scrollTop = shell.chatBox.scrollHeight;
            persistCurrentSession();
        }

        function addThinkingMessage() {
            const shell = createMessageShell("assistant");
            shell.message.classList.add("thinking-message");
            shell.bubble.classList.add("thinking-bubble");
            shell.bubble.innerHTML = '<span>筮渡正在整理思路</span><span class="thinking-dots" aria-label="正在思考"><span></span><span></span><span></span></span>';
            shell.chatBox.appendChild(shell.message);
            shell.chatBox.scrollTop = shell.chatBox.scrollHeight;
            return shell.message;
        }

        function setPromptFillState(active) {
            const inputRow = document.querySelector(".input-row");
            const hint = document.getElementById("promptFillHint");
            if (!inputRow || !hint) {
                return;
            }

            inputRow.classList.toggle("prompt-filled", active);
            hint.hidden = !active;
        }

        function fillPrompt(text) {
            const input = document.getElementById("userInput");
            input.value = text;
            setPromptFillState(true);
            input.focus();
            input.setSelectionRange(text.length, text.length);
            persistCurrentSession();
        }

        function createGuideCard(config, skillId) {
            const card = document.createElement("div");
            card.className = "guide-card";
            card.dataset.skillId = skillId;

            const text = document.createElement("p");
            const zodiacName = getZodiacName(userPreferences.zodiac);
            const dailyGreeting = zodiacName
                ? "你好呀，今天想看看哪方面？我会结合你选择的" + zodiacName + "来陪你分析。"
                : "你好呀，今天想看看哪方面？我会陪你一步步分析。";
            const welcomeMessages = {
                "": "你好呀，今天想看看哪方面？你可以直接说说近况。",
                daily_fortune: dailyGreeting,
                tarot: "你好呀，先说说这次最想问的事，后面我们再一起抽牌。",
                bazi: "你好呀，今天更想看看事业、感情，还是整体状态？",
                date_selection: "你好呀，先告诉我准备做什么事，我陪你一起理清时间。",
                naming: "你好呀，想分析一个已有名字，还是一起想新名字？"
            };
            const quickPrompts = {
                "": [
                    { label: "最近有点迷茫", prompt: "我最近有些迷茫，不太确定下一步该往哪里走，可以陪我梳理一下现在最需要关注的事情吗？" },
                    { label: "想看感情", prompt: "我想聊聊最近的感情状态，可以帮我分析目前的关系，以及接下来适合怎么做吗？" },
                    { label: "想看事业", prompt: "我想梳理一下最近的事业发展，可以帮我分析目前的处境、可能的方向和下一步行动吗？" }
                ],
                daily_fortune: [
                    { label: "看今天运势", prompt: "我想看看今天的整体运势，请结合我选择的星座，分别说说工作、感情和需要注意的地方。" },
                    { label: "看明日运势", prompt: "我想提前看看明天的整体运势，请结合我选择的星座，说说适合做什么以及需要注意什么。" },
                    { label: "看本周运势", prompt: "我想看看本周的整体运势，请结合我选择的星座，分析工作、感情和生活节奏。" }
                ],
                tarot: [
                    { label: "感情走向", prompt: "我想看看未来三个月的感情走向，以及这段关系中我需要注意什么。" },
                    { label: "工作选择", prompt: "我最近正在考虑一项工作选择，想看看不同方向的潜在发展和需要注意的问题。" },
                    { label: "对方想法", prompt: "我想了解对方目前对这段关系可能抱有什么想法，以及我应该如何看待这段关系。" }
                ],
                bazi: [
                    { label: "看看事业", prompt: "我想通过八字看看自己的事业方向和发展特点，请告诉我需要提供哪些必要信息。" },
                    { label: "看看感情", prompt: "我想通过八字了解自己的感情特点和关系倾向，请告诉我需要提供哪些必要信息。" },
                    { label: "看看财运", prompt: "我想通过八字看看自己的财运特点和需要注意的方向，请告诉我需要提供哪些必要信息。" }
                ],
                date_selection: [
                    { label: "搬家择日", prompt: "我准备在近期搬家，请告诉我需要提供哪些信息，再帮我逐步选择合适的日期。" },
                    { label: "开业择日", prompt: "我准备为新店开业选择日期，请告诉我需要提供哪些信息，再帮我分析合适的时间。" },
                    { label: "签约择日", prompt: "我准备进行一次重要签约，请告诉我需要提供哪些信息，再帮我选择较合适的日期。" }
                ],
                naming: [
                    { label: "分析名字", prompt: "我想分析一个已有名字，请告诉我需要提供哪些基本信息，并从含义、读音和整体感觉上帮我看看。" },
                    { label: "女孩起名", prompt: "我想给女孩起名，请告诉我需要提供哪些基本信息，并帮我梳理喜欢的风格和方向。" },
                    { label: "店铺起名", prompt: "我想给店铺起名，请告诉我需要提供哪些基本信息，并结合行业和期望风格给出建议。" }
                ]
            };
            text.textContent = welcomeMessages[skillId] || config.guideText;
            card.appendChild(text);

            const chips = document.createElement("div");
            chips.className = "prompt-chips";
            const promptItems = quickPrompts[skillId]
                || config.examples.slice(0, 3).map(function(example) {
                    return { label: example, prompt: example };
                });
            promptItems.forEach(function(item) {
                const chip = document.createElement("button");
                chip.type = "button";
                chip.className = "prompt-chip";
                chip.textContent = item.label;
                chip.dataset.promptText = item.prompt;
                chip.addEventListener("click", function() {
                    fillPrompt(item.prompt);
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
                setTarotFlowState("waiting_question");
            } else if (skillId === "daily_fortune") {
                resetDailyFortuneState();
            } else if (skillId === "bazi") {
                resetBaziFlowState();
            }

            addRichAssistantNode(createGuideCard(config, skillId));

        }

        async function sendMessage(options = {}) {
            const input = document.getElementById("userInput");
            const text = options.text || input.value.trim();

            if (!text) {
                return false;
            }

            input.value = "";
            setPromptFillState(false);

            if (!options.bypassSkillFlow) {
                if (activeSkillId === "daily_fortune") {
                    updateDailyFortunePeriod(text);
                } else if (activeSkillId === "bazi") {
                    const handled = await handleBaziFlowInput(text);
                    if (handled) {
                        return true;
                    }
                } else if (activeSkillId === "tarot") {
                    const handled = await handleTarotFlowInput(text);
                    if (handled) {
                        return true;
                    }
                }
            }

            const requestText = activeSkillId === "daily_fortune" && !options.bypassSkillFlow
                ? buildDailyFortuneRequest(text)
                : text;
            messages.push({
                role: "user",
                content: requestText
            });

            if (options.showUser !== false) {
                addMessage("user", options.displayText || text);
            }
            const thinkingMessage = addThinkingMessage();
            const chatPayload = {
                messages: messages.slice(-12),
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                skill_id: activeSkillId || null,
                allow_skill_routing: false,
                tarot_cards: options.tarotCards || null,
                user_preferences: getChatPreferences()
            };

            try {
                const resultSkillId = options.resultSkillId !== undefined
                    ? options.resultSkillId
                    : activeSkillId;
                const data = await requestChatStream(chatPayload, resultSkillId);
                const reply = data.reply.trim() || "服务暂时不可用，请稍后再试。";

                if (data.skillId && activeSkillId && data.skillId !== activeSkillId) {
                    setSkill(data.skillId);
                }

                messages.push({
                    role: "assistant",
                    content: reply
                });

                finalizeStreamingAssistantMessage(data.message, reply);
                return true;

            } catch (error) {
                if (thinkingMessage.isConnected) {
                    thinkingMessage.remove();
                }
                addMessage("assistant", "请求异常：" + error);
                return false;
            }
        }

        function looksLikeBirthDate(text) {
            return /(?:公历|阳历|农历|阴历)|\d{4}\s*(?:年|[-/.])\s*\d{1,2}\s*(?:月|[-/.])\s*\d{1,2}/.test(text);
        }

        function isGeneralBaziQuestion(text) {
            return /(?:通用|今年|明年|\d{4}\s*年)/.test(text)
                && /(?:运势|趋势|流年|大方向)/.test(text);
        }

        function isBaziExplanationQuestion(text) {
            return /(?:什么是八字|八字是什么|八字.*什么意思|八字.*原理|八字准不准|八字靠谱吗)/.test(text);
        }

        function addBaziCollectionExchange(userText, assistantText) {
            messages.push({ role: "user", content: userText });
            addMessage("user", userText);
            messages.push({ role: "assistant", content: assistantText });
            addMessage("assistant", assistantText);
            persistCurrentSession();
        }

        function buildBaziAnalysisRequest() {
            return [
                "请根据以下已经确认的信息进行八字传统文化参考分析，不要再次询问这些信息。",
                "出生日期：" + baziFlowState.birthDate,
                "出生时间：" + baziFlowState.birthTime,
                "出生城市：" + baziFlowState.birthCity,
                "性别：" + baziFlowState.gender,
                "重点关注：" + baziFlowState.focus,
                "请依次给出：已用信息、基础参考、事业财运、感情人际、阶段趋势、行动建议。不要输出 Markdown 星号。"
            ].join("\n");
        }

        async function handleBaziFlowInput(text) {
            const stage = baziFlowState.stage;
            if (stage === "done") {
                return false;
            }

            if (stage === "intro" || stage === "waiting_birth_date") {
                if (stage === "intro" && isBaziExplanationQuestion(text)) {
                    return false;
                }
                if (stage === "intro" && isGeneralBaziQuestion(text)) {
                    setBaziFlowStage("done");
                    persistCurrentSession();
                    return false;
                }
                if (!looksLikeBirthDate(text)) {
                    setBaziFlowStage("waiting_birth_date");
                    addBaziCollectionExchange(
                        text,
                        "先告诉我你的出生日期，并说明是公历还是农历，例如“公历 2000 年 7 月 7 日”。"
                    );
                    return true;
                }
                baziFlowState.birthDate = text.slice(0, 80);
                setBaziFlowStage("waiting_birth_time");
                addBaziCollectionExchange(
                    text,
                    "接下来告诉我出生时间即可；如果不清楚具体时间，可以说大概时辰或“不清楚”。"
                );
                return true;
            }

            if (stage === "waiting_birth_time") {
                baziFlowState.birthTime = text.slice(0, 80);
                setBaziFlowStage("waiting_birth_city");
                addBaziCollectionExchange(text, "出生地写到城市即可，例如“湖南长沙”，不需要详细地址。");
                return true;
            }

            if (stage === "waiting_birth_city") {
                baziFlowState.birthCity = text.slice(0, 80);
                setBaziFlowStage("waiting_gender");
                addBaziCollectionExchange(text, "传统排盘还需要性别，请回复男、女；不方便提供也可以回复“跳过”。");
                return true;
            }

            if (stage === "waiting_gender") {
                if (!/男|女|跳过|不方便|其他/.test(text)) {
                    addBaziCollectionExchange(text, "请回复男、女；不方便提供也可以直接回复“跳过”。");
                    return true;
                }
                baziFlowState.gender = text.slice(0, 30);
                setBaziFlowStage("waiting_focus");
                addBaziCollectionExchange(text, "最后告诉我这次最想关注什么，例如事业、财运、感情或整体趋势。");
                return true;
            }

            if (stage === "waiting_focus") {
                baziFlowState.focus = text.slice(0, 100);
                setBaziFlowStage("analyzing");
                const succeeded = await sendMessage({
                    text: buildBaziAnalysisRequest(),
                    displayText: text,
                    bypassSkillFlow: true,
                    resultSkillId: "bazi"
                });
                setBaziFlowStage(succeeded ? "done" : "waiting_focus");
                persistCurrentSession();
                return true;
            }

            return false;
        }

        async function handleTarotFlowInput(text) {
            if (tarotFlowState === "idle") {
                setTarotFlowState("waiting_question");
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
            setTarotFlowState("idle");
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
            setTarotFlowState("choosing_method");
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

        function enableTarotInlineCard(card) {
            if (!card) {
                return;
            }
            card.querySelectorAll("input, button").forEach(function(element) {
                element.disabled = false;
            });
        }

        function completeTarotMethodCard(card, methodLabel) {
            if (!card) {
                return;
            }

            card.classList.add("tarot-inline-card-complete");
            const title = card.querySelector(".tarot-inline-title");
            const desc = card.querySelector("p");
            const actions = card.querySelector(".tarot-inline-actions");
            if (title) {
                title.textContent = "抽牌方式已确认";
            }
            if (desc) {
                desc.textContent = "已选择：" + methodLabel;
            }
            if (actions) {
                actions.remove();
            }
            currentTarotMethodCard = null;
        }

        function addTarotProgressMessage(text) {
            const shell = createMessageShell("assistant");
            shell.message.classList.add("tarot-progress-message");
            shell.bubble.classList.add("tarot-status-bubble");
            shell.bubble.textContent = text;
            shell.chatBox.appendChild(shell.message);
            shell.chatBox.scrollTop = shell.chatBox.scrollHeight;
            return shell.message;
        }

        function completeTarotProgressMessage(message, text) {
            if (!message || !message.isConnected) {
                return;
            }
            message.classList.remove("tarot-progress-message");
            message.classList.add("tarot-status-message");
            const bubble = message.querySelector(".bubble");
            if (bubble) {
                bubble.textContent = text;
            }
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
                setTarotFlowState("waiting_question");
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
                setTarotFlowState("waiting_question");
                addMessage("assistant", "请先写下本次塔罗想问的问题。");
                return;
            }

            if (showUserSelection) {
                addMessage("user", "系统随机抽牌");
            }

            const methodCard = sourceCard || currentTarotMethodCard;
            disableTarotInlineCard(methodCard);
            setTarotFlowState("shuffling");
            const progressMessage = addTarotProgressMessage("正在为这个问题重新洗牌，并随机抽出 3 张牌...");

            try {
                const response = await fetch("/tarot/random-draw", {
                    method: "POST"
                });
                const data = await response.json();

                if (!response.ok) {
                    enableTarotInlineCard(methodCard);
                    setTarotFlowState("choosing_method");
                    addMessage("assistant", data.error || "系统抽牌失败，请稍后再试。");
                    return;
                }

                currentTarotCards = data.cards;
                currentTarotNumbers = data.numbers;
                currentTarotDrawMode = "system";
                revealedTarotIndexes = [];
                tarotReadingRequested = false;
                tarotShuffleId = "";
                completeTarotMethodCard(methodCard, "系统随机抽牌");
                completeTarotProgressMessage(progressMessage, "已完成洗牌，系统随机抽出 3 张牌。");
                setTarotFlowState("waiting_reveal");
                addTarotRevealMessage();
            } catch (error) {
                enableTarotInlineCard(methodCard);
                setTarotFlowState("choosing_method");
                addMessage("assistant", "系统抽牌异常：" + error);
            }
        }

        async function startManualTarotDraw(sourceCard, showUserSelection) {
            if (!currentTarotQuestion) {
                setTarotFlowState("waiting_question");
                addMessage("assistant", "请先写下本次塔罗想问的问题。");
                return;
            }

            if (showUserSelection) {
                addMessage("user", "我自己选牌");
            }

            const methodCard = sourceCard || currentTarotMethodCard;
            disableTarotInlineCard(methodCard);
            setTarotFlowState("shuffling");
            const progressMessage = addTarotProgressMessage("正在为这次问题洗好 78 张牌...");

            try {
                const response = await fetch("/tarot/shuffle", {
                    method: "POST"
                });
                const data = await response.json();

                if (!response.ok) {
                    enableTarotInlineCard(methodCard);
                    setTarotFlowState("choosing_method");
                    addMessage("assistant", data.error || "洗牌失败，请稍后再试。");
                    return;
                }

                tarotShuffleId = data.shuffle_id;
                currentTarotDrawMode = "manual";
                completeTarotMethodCard(methodCard, "我自己选牌");
                completeTarotProgressMessage(progressMessage, "已完成洗牌，请选择 3 个数字。");
                setTarotFlowState("waiting_numbers");
                addTarotNumberPrompt();
            } catch (error) {
                enableTarotInlineCard(methodCard);
                setTarotFlowState("choosing_method");
                addMessage("assistant", "洗牌异常：" + error);
            }
        }

        function parseTarotNumbersFromText(text) {
            return text
                .split(/[,\s，、]+/)
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
                setTarotFlowState("waiting_question");
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
                setTarotFlowState("waiting_question");
                return;
            }

            if (showUserSelection) {
                addMessage("user", "我选择：" + numbers.join("、"));
            }

            const numberGrids = document.querySelectorAll(".tarot-number-grid");
            const latestNumberGrid = numberGrids.length ? numberGrids[numberGrids.length - 1] : null;
            const numberCard = sourceCard || (latestNumberGrid ? latestNumberGrid.closest(".tarot-inline-card") : null);
            disableTarotInlineCard(numberCard);
            setTarotFlowState("shuffling");
            const progressMessage = addTarotProgressMessage("已确认你的 3 个数字，正在从洗好的牌序中抽出对应牌面...");

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
                    enableTarotInlineCard(numberCard);
                    setTarotFlowState("waiting_numbers");
                    addMessage("assistant", data.error || "抽牌失败");
                    return;
                }

                currentTarotCards = data.cards;
                currentTarotNumbers = numbers;
                currentTarotDrawMode = "manual";
                revealedTarotIndexes = [];
                tarotReadingRequested = false;
                tarotShuffleId = "";
                completeTarotProgressMessage(progressMessage, "已按你选择的数字抽出 3 张牌。");
                setTarotFlowState("waiting_reveal");
                addTarotRevealMessage();
            } catch (error) {
                enableTarotInlineCard(numberCard);
                setTarotFlowState("waiting_numbers");
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
            frontImage.alt = "";
            frontImage.setAttribute("aria-hidden", "true");
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
            updateTarotCardAccessibility(button, item, false);
            return button;
        }

        function updateTarotCardAccessibility(button, item, revealed) {
            if (!button || !item) {
                return;
            }

            const frontImage = button.querySelector(".tarot-card-front img");
            if (revealed) {
                button.setAttribute("aria-label", item.position + "，" + item.card + "，" + item.orientation + "，已翻开，再次点击可放大查看");
                if (frontImage) {
                    frontImage.alt = item.card + " " + item.orientation;
                    frontImage.removeAttribute("aria-hidden");
                }
            } else {
                button.setAttribute("aria-label", item.position + "，" + item.choice + "，点击翻牌");
                if (frontImage) {
                    frontImage.alt = "";
                    frontImage.setAttribute("aria-hidden", "true");
                }
            }
        }

        function openTarotPreview(item) {
            if (!item) {
                return;
            }

            const preview = document.getElementById("tarotPreview");
            const image = document.getElementById("tarotPreviewImage");
            image.src = item.image;
            image.alt = item.card + " " + item.orientation;
            image.classList.toggle("reversed-card-image", item.orientation === "逆位");
            document.getElementById("tarotPreviewPosition").textContent = item.position + " · " + item.choice;
            document.getElementById("tarotPreviewName").textContent = item.card + "（" + item.orientation + "）";
            preview.hidden = false;
            preview.setAttribute("aria-hidden", "false");
            document.body.classList.add("tarot-preview-open");
            document.getElementById("tarotPreviewCloseButton").focus();
        }

        function closeTarotPreview() {
            const preview = document.getElementById("tarotPreview");
            if (preview.hidden) {
                return;
            }

            preview.hidden = true;
            preview.setAttribute("aria-hidden", "true");
            document.body.classList.remove("tarot-preview-open");
        }

        function flipTarotCard(index, button) {
            if (!currentTarotCards) {
                return;
            }

            const item = currentTarotCards[index];
            if (revealedTarotIndexes.includes(index)) {
                openTarotPreview(item);
                return;
            }
            if (tarotReadingRequested) {
                return;
            }

            revealedTarotIndexes.push(index);
            button.classList.add("flipped");
            button.querySelector(".tarot-flip-name").textContent = item.card + "（" + item.orientation + "）";
            updateTarotCardAccessibility(button, item, true);
            persistCurrentSession();

            if (revealedTarotIndexes.length === currentTarotCards.length && !tarotReadingRequested) {
                tarotReadingRequested = true;
                setTarotFlowState("reading");
                persistCurrentSession();
                requestTarotReading();
            }
        }

        async function requestTarotReading() {
            const cardSummary = currentTarotCards.map(function(item) {
                return item.position + "（" + item.choice + "）：" + item.card + "（" + item.orientation + "）";
            }).join("\n");
            const drawSummary = currentTarotDrawMode === "system"
                ? "系统从重新洗好的 78 张牌里随机抽到：" + currentTarotNumbers.join("、")
                : "我从洗好的 78 张牌里选择了：" + currentTarotNumbers.join("、");
            const userText = "我的塔罗问题：" + currentTarotQuestion
                + "\n" + drawSummary
                + "\n抽牌结果：\n" + cardSummary;

            await sendMessage({
                text: userText,
                showUser: false,
                tarotCards: currentTarotCards,
                bypassSkillFlow: true
            });

            setTarotFlowState("done");
            persistCurrentSession();
        }

        function clearChat() {
            resetConversation();
            showSkillGuide(activeSkillId);
            document.getElementById("userInput").focus();
        }

        document.getElementById("userInput").addEventListener("input", function() {
            setPromptFillState(false);
            persistCurrentSession();
        });

        document.getElementById("userInput").addEventListener("keydown", function(event) {
            if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        });

        document.getElementById("openPreferences").addEventListener("click", openPreferences);
        document.getElementById("backToServices").addEventListener("click", showServiceView);
        document.getElementById("clearChat").addEventListener("click", clearChat);
        document.getElementById("sendMessage").addEventListener("click", sendMessage);
        document.getElementById("closeTarotPreview").addEventListener("click", closeTarotPreview);
        document.getElementById("tarotPreviewCloseButton").addEventListener("click", closeTarotPreview);
        document.addEventListener("keydown", function(event) {
            if (event.key === "Escape") {
                closeTarotPreview();
            }
        });
        document.querySelectorAll("[data-static-skill-id]").forEach(function(card) {
            card.addEventListener("click", function() {
                enterChat(card.dataset.staticSkillId || "");
            });
        });

        function initializeApp() {
            try {
                renderServiceCards();
            } catch (error) {
                console.error("服务入口渲染失败，已使用备用入口。", error);
                renderServiceFallback();
            }

            try {
                renderPreferenceSummary();
            } catch (error) {
                console.error("偏好摘要渲染失败。", error);
            }

            document.getElementById("closePreferences").addEventListener("click", closePreferences);
            document.querySelector(".preference-backdrop").addEventListener("click", closePreferences);
            document.getElementById("savePreferences").addEventListener("click", savePreferences);
            document.getElementById("skipPreferences").addEventListener("click", skipPreferences);

            if (!userPreferences.setupComplete) {
                openPreferences();
            }
        }

        initializeApp();
