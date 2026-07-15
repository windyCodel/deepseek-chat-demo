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

        function renderServiceFallback() {
            const grid = document.getElementById("serviceGrid");
            const fallbackServices = [
                ["daily_fortune", "每日运势", "看看今日、明日或本周的节奏与提示。"],
                ["tarot", "塔罗占卜", "先写下问题，再抽三张牌进行解读。"],
                ["bazi", "八字分析", "围绕出生信息和关注方向逐步分析。"],
                ["date_selection", "择日", "为搬家、开业、签约等事项梳理时间。"],
                ["naming", "姓名分析", "分析已有名字，或一起寻找合适的名字。"],
                ["", "通用咨询", "还不确定方向时，从这里开始聊聊。"]
            ];
            grid.innerHTML = "";

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
            const lines = String(content || "").replace(/\r\n?/g, "\n").split("\n");
            const blocks = [];
            let listItems = [];

            function renderInline(value) {
                return escapeHtml(value).replace(/\*\*([^*\n][^*\n]*?)\*\*/g, "<strong>$1</strong>");
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
                "": ["最近有点迷茫", "想看感情", "想看事业"],
                daily_fortune: ["看今天运势", "看明日运势", "看本周运势"],
                tarot: ["感情走向", "工作选择", "对方想法"],
                bazi: ["看看事业", "看看感情", "看看财运"],
                date_selection: ["搬家择日", "开业择日", "签约择日"],
                naming: ["分析名字", "女孩起名", "店铺起名"]
            };
            text.textContent = welcomeMessages[skillId] || config.guideText;
            card.appendChild(text);

            const chips = document.createElement("div");
            chips.className = "prompt-chips";
            (quickPrompts[skillId] || config.examples.slice(0, 3)).forEach(function(example) {
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
                        messages: messages.slice(-12),
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

        document.getElementById("openPreferences").addEventListener("click", openPreferences);
        document.getElementById("backToServices").addEventListener("click", showServiceView);
        document.getElementById("clearChat").addEventListener("click", clearChat);
        document.getElementById("sendMessage").addEventListener("click", sendMessage);
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
