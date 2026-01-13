"""
算命先生 AI Agent - 重构版
核心理念：算命先生从命理书中【选择】判词，而不是【生成】判词
"""
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class DestinyState(Enum):
    """命运状态机 - 用户的心理状态"""
    HESITATING = "hesitating"  # 犹豫
    ALREADY_DECIDED = "already_decided"  # 已有答案
    UNWILLING = "unwilling"  # 不甘心
    MIDNIGHT_ESCAPE = "midnight_escape"  # 深夜逃避
    SELF_DECEPTION = "self_deception"  # 自欺
    FIRST_TIME = "first_time"  # 第一次算
    REPEATED = "repeated"  # 反复算
    EMPTY_HEART = "empty_heart"  # 空虚无问
    SEEKING_CONFIRMATION = "seeking_confirmation"  # 寻求确认


class InputFeatures:
    """输入特征（非语义！）"""
    
    def __init__(
        self,
        is_empty: bool,
        char_length: int,
        has_question_mark: bool,
        hour: int,
        attempt_count: int
    ):
        self.is_empty = is_empty
        self.char_length = char_length
        self.has_question_mark = has_question_mark
        self.hour = hour
        self.attempt_count = attempt_count
        
        # 派生特征
        self.is_midnight = 23 <= hour or hour < 5
        self.is_dawn = 5 <= hour < 7
        self.is_worktime = 9 <= hour < 18
        self.length_category = self._categorize_length()
    
    def _categorize_length(self) -> str:
        """字符长度分类"""
        if self.char_length == 0:
            return "empty"
        elif self.char_length <= 5:
            return "very_short"
        elif self.char_length <= 15:
            return "short"
        elif self.char_length <= 30:
            return "medium"
        else:
            return "long"
    
    @classmethod
    def from_input(cls, question: str, history_count: int = 0) -> 'InputFeatures':
        """
        从用户输入提取特征
        
        Args:
            question: 用户输入
            history_count: 历史算命次数
            
        Returns:
            特征对象
        """
        is_empty = len(question.strip()) == 0
        char_length = len(question.strip())
        has_question_mark = "?" in question or "？" in question
        hour = datetime.now().hour
        
        features = cls(
            is_empty=is_empty,
            char_length=char_length,
            has_question_mark=has_question_mark,
            hour=hour,
            attempt_count=history_count + 1
        )
        
        logger.info(f"Extracted features: {features.to_dict()}")
        return features
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_empty": self.is_empty,
            "char_length": self.char_length,
            "has_question_mark": self.has_question_mark,
            "hour": self.hour,
            "attempt_count": self.attempt_count,
            "is_midnight": self.is_midnight,
            "is_dawn": self.is_dawn,
            "length_category": self.length_category
        }


def determine_state(features: InputFeatures) -> DestinyState:
    """
    命运状态机 - 根据特征判断用户状态
    
    这是纯规则判断，不涉及语义理解
    """
    # 空输入
    if features.is_empty:
        if features.attempt_count == 1:
            return DestinyState.EMPTY_HEART
        else:
            return DestinyState.SELF_DECEPTION
    
    # 深夜 + 短输入
    if features.is_midnight and features.length_category in ["very_short", "short"]:
        if features.attempt_count > 1:
            return DestinyState.MIDNIGHT_ESCAPE
        else:
            return DestinyState.FIRST_TIME
    
    # 反复算
    if features.attempt_count >= 3:
        if features.has_question_mark:
            return DestinyState.UNWILLING
        else:
            return DestinyState.REPEATED
    
    # 有问号 + 中等长度
    if features.has_question_mark and features.length_category in ["medium", "long"]:
        if features.attempt_count > 1:
            return DestinyState.HESITATING
        else:
            return DestinyState.FIRST_TIME
    
    # 无问号 + 短输入
    if not features.has_question_mark and features.length_category in ["very_short", "short"]:
        if features.attempt_count > 1:
            return DestinyState.ALREADY_DECIDED
        else:
            return DestinyState.SEEKING_CONFIRMATION
    
    # 长输入
    if features.length_category == "long":
        return DestinyState.HESITATING
    
    # 默认：第一次算
    return DestinyState.FIRST_TIME


class VerdictPool:
    """固定判词池 - "命理书"中的判词"""
    
    # 判词母句库（中文）
    VERDICTS_ZH = {
        DestinyState.HESITATING: [
            "犹豫时机已过，拖延的后果由你承担",
            "左右为难是因为答案早已明了，只是不愿承认",
            "你的迟疑会让机会从指缝溜走，两手空空",
            "选择困难症的代价是：两边都会失去",
            "纠结越久，结局越糟",
        ],
        DestinyState.ALREADY_DECIDED: [
            "你心里早有答案，只是想要一个赞同而已",
            "决定早已做出，何必装作犹豫",
            "你不是在问我，你是在说服自己",
            "明知故问的人，往往会为固执买单",
            "既然已经决定了，何必浪费我的时间",
        ],
        DestinyState.UNWILLING: [
            "不甘心的后果是：更不甘心",
            "反复确认不会改变结局，只会延长痛苦",
            "执念越深，陷得越深",
            "你越是不信，现实越会证明给你看",
            "算第三次的人，是在寻求谎言",
        ],
        DestinyState.MIDNIGHT_ESCAPE: [
            "深夜不睡来算命，逃避解决不了问题",
            "凌晨的焦虑会在天亮后加倍奉还",
            "失眠算命的人，白天会后悔",
            "深夜的决定，往往是错误的",
            "黑夜给了你黑色的眼睛，你却用它来逃避",
        ],
        DestinyState.SELF_DECEPTION: [
            "连问题都问不出口，说明你已经知道答案了",
            "空白的问题，暴露的是空虚的心",
            "无话可说时，沉默比谎言更诚实",
            "你不是没有问题，是不敢面对问题",
            "什么都不说，说明你什么都知道",
        ],
        DestinyState.FIRST_TIME: [
            "初问天机，答案会比你想象的更残酷",
            "第一次算命的人，往往承受不住真相",
            "你来得太晚了，时机已经过去",
            "新手的运气不会站在你这边",
            "第一卦就是定局，别想着重来",
        ],
        DestinyState.REPEATED: [
            "反复问同一件事，只能得到更糟的答案",
            "第N次算命的人，是在等待奇迹，但奇迹不会来",
            "重复提问不会改变命运，只会浪费时间",
            "你已经问过了，答案不会因为你的执着而改变",
            "算得越多，越证明你已经输了",
        ],
        DestinyState.EMPTY_HEART: [
            "空无一物的心，得到的也是空无一物",
            "连问题都没有的人，不配得到答案",
            "虚空问虚空，得到的只有虚空",
            "无问即无答，这就是你的命",
            "什么都不想说，那就什么都别得到",
        ],
        DestinyState.SEEKING_CONFIRMATION: [
            "寻求确认的人，最终会被现实否定",
            "你的笃定会在三天内崩塌",
            "确认是虚假的安全感，现实会给你真相",
            "斩钉截铁的人，往往会栽在细节上",
            "你想要的确认，恰恰是你的软肋",
        ],
    }
    
    # 判词母句库（英文）
    VERDICTS_EN = {
        DestinyState.HESITATING: [
            "The moment for hesitation has passed, you'll bear the consequences of delay",
            "You struggle because the answer is clear, you just refuse to admit it",
            "Your indecision will let opportunity slip through your fingers",
            "The price of being torn is losing both sides",
            "The longer you dwell, the worse the outcome",
        ],
        DestinyState.ALREADY_DECIDED: [
            "You already know the answer, you just want approval",
            "The decision is made, why pretend to hesitate",
            "You're not asking me, you're convincing yourself",
            "Those who ask knowingly often pay for their stubbornness",
            "Since you've decided, why waste my time",
        ],
        DestinyState.UNWILLING: [
            "The consequence of unwillingness is: more unwillingness",
            "Repeated confirmation won't change the ending, only prolong the pain",
            "The deeper the obsession, the deeper you sink",
            "The more you disbelieve, the more reality will prove you wrong",
            "Those who ask a third time are seeking lies",
        ],
        DestinyState.MIDNIGHT_ESCAPE: [
            "Seeking fortune at midnight won't solve your problems",
            "Pre-dawn anxiety will return doubled in daylight",
            "Those who divine while sleepless will regret it by day",
            "Midnight decisions are often wrong",
            "Night gave you dark eyes, yet you use them to escape",
        ],
        DestinyState.SELF_DECEPTION: [
            "Can't even voice the question means you already know the answer",
            "Empty questions expose an empty heart",
            "When speechless, silence is more honest than lies",
            "You don't lack questions, you fear facing them",
            "Saying nothing means you know everything",
        ],
        DestinyState.FIRST_TIME: [
            "First time asking fate, the answer will be crueler than you imagine",
            "First-timers often can't bear the truth",
            "You came too late, the moment has passed",
            "Beginner's luck won't be on your side",
            "The first reading is final, don't think of retrying",
        ],
        DestinyState.REPEATED: [
            "Asking repeatedly only gets worse answers",
            "Those who ask N times are waiting for miracles, but miracles won't come",
            "Repeated questions won't change fate, only waste time",
            "You've asked before, persistence won't change the answer",
            "The more you ask, the more you prove you've lost",
        ],
        DestinyState.EMPTY_HEART: [
            "An empty heart receives only emptiness",
            "Those without questions don't deserve answers",
            "Void asks void, void is all you get",
            "No question means no answer, that's your fate",
            "If you won't speak, you'll get nothing",
        ],
        DestinyState.SEEKING_CONFIRMATION: [
            "Those seeking confirmation will be denied by reality",
            "Your certainty will crumble within three days",
            "Confirmation is false security, reality will show the truth",
            "The resolute often stumble on details",
            "The confirmation you seek is exactly your weakness",
        ],
    }
    
    @staticmethod
    def get_verdicts(state: DestinyState, language: str = 'zh') -> List[str]:
        """获取指定状态的判词列表"""
        if language == 'zh':
            return VerdictPool.VERDICTS_ZH.get(state, VerdictPool.VERDICTS_ZH[DestinyState.FIRST_TIME])
        else:
            return VerdictPool.VERDICTS_EN.get(state, VerdictPool.VERDICTS_EN[DestinyState.FIRST_TIME])


def select_verdict(
    state: DestinyState,
    features: InputFeatures,
    language: str = 'zh'
) -> str:
    """
    判词选择器 - 从判词池中选择最合适的母句
    
    根据状态和特征，从判词池中选择最合适的一条
    使用简单的规则选择，不涉及语义理解
    """
    verdicts = VerdictPool.get_verdicts(state, language)
    
    # 根据特征选择索引
    # 这里使用简单的哈希策略，确保相同特征得到相同判词
    index = (
        features.attempt_count * 7 +
        features.char_length * 3 +
        features.hour * 5 +
        (1 if features.has_question_mark else 0) * 11
    ) % len(verdicts)
    
    selected = verdicts[index]
    logger.info(f"Selected verdict from pool: state={state.value}, index={index}")
    
    return selected


class LLMPerturbation:
    """LLM 微扰模块 - 被阉割的 LLM，只能改语气和节奏"""
    
    def __init__(self, llm_service):
        self.llm_service = llm_service
    
    async def perturb(
        self,
        mother_verdict: str,
        features: InputFeatures,
        language: str = 'zh'
    ) -> str:
        """
        对母句进行微扰
        
        Args:
            mother_verdict: 从判词池选出的母句
            features: 输入特征
            language: 语言
            
        Returns:
            微扰后的判词
        """
        # 构建严格限制的提示词
        if language == 'zh':
            prompt = f"""你是语言润色助手。给定一个判词母句，你只能调整语气和节奏。

【严格禁止】
1. 添加任何新信息
2. 添加建议或解释
3. 改变原句的核心含义
4. 使用温柔或安慰性语气
5. 添加形容词或副词（除非为了语气）

【允许操作】
1. 调整语序
2. 改变停顿节奏（逗号、句号位置）
3. 调整强硬或柔和的程度
4. 使用同义替换（不改变含义）

母句：{mother_verdict}

时间：{features.hour}点
尝试次数：{features.attempt_count}次
输入长度：{features.char_length}字

请根据时间和次数调整语气强度，输出调整后的判词（仅一句话）："""
        else:
            prompt = f"""You are a language polisher. Given a verdict, you can only adjust tone and rhythm.

【STRICTLY FORBIDDEN】
1. Add any new information
2. Add advice or explanation
3. Change core meaning
4. Use gentle or comforting tone
5. Add adjectives or adverbs (unless for tone)

【ALLOWED OPERATIONS】
1. Adjust word order
2. Change pause rhythm (comma, period position)
3. Adjust harshness or softness level
4. Use synonyms (without changing meaning)

Mother verdict: {mother_verdict}

Time: {features.hour}:00
Attempt count: {features.attempt_count}
Input length: {features.char_length} chars

Adjust tone based on time and count, output adjusted verdict (one sentence only):"""
        
        try:
            # 调用 LLM，但设置很低的 temperature 避免太大变化
            result = await self.llm_service.generate(
                prompt=prompt,
                language=language,
                temperature=0.3,  # 低温度，减少随机性
                max_tokens=100  # 限制长度
            )
            
            # 清理结果，确保只有一句话
            result = result.strip()
            if '\n' in result:
                result = result.split('\n')[0]
            
            logger.info(f"Perturbed verdict: '{mother_verdict}' -> '{result}'")
            return result
            
        except Exception as e:
            logger.error(f"LLM perturbation error: {e}, fallback to mother verdict")
            # 如果 LLM 出错，直接返回母句
            return mother_verdict


class FortuneAgent:
    """
    算命先生 AI Agent - 重构版
    
    核心理念：从"命理书"中选择判词，而不是生成判词
    """
    
    def __init__(self, llm_service):
        self.llm_service = llm_service
        self.memory: List[Dict[str, Any]] = []
        self.llm_perturbation = LLMPerturbation(llm_service)
    
    async def execute(
        self,
        question: str,
        language: str = 'zh',
        enable_reasoning: bool = False
    ) -> Dict[str, Any]:
        """
        执行完整的算命流程
        
        流程：
        1. 提取输入特征（非语义）
        2. 状态机判断用户状态
        3. 从判词池选择母句
        4. LLM 微扰（只改语气/节奏）
        5. 返回结果
        """
        try:
            # 1. 提取特征
            features = InputFeatures.from_input(
                question=question,
                history_count=len(self.memory)
            )
            
            # 2. 判断状态
            state = determine_state(features)
            logger.info(f"Determined state: {state.value}")
            
            # 3. 选择判词母句
            mother_verdict = select_verdict(
                state=state,
                features=features,
                language=language
            )
            
            # 4. LLM 微扰
            final_verdict = await self.llm_perturbation.perturb(
                mother_verdict=mother_verdict,
                features=features,
                language=language
            )
            
            # 5. 保存到记忆
            memory_entry = {
                "question": question,
                "result": final_verdict,
                "state": state.value,
                "mother_verdict": mother_verdict,
                "features": features.to_dict(),
                "timestamp": datetime.now().isoformat()
            }
            self.memory.append(memory_entry)
            
            # 6. 构建响应
            response = {
                "result": final_verdict,
                "state": state.value,
            }
            
            if enable_reasoning:
                response["reasoning"] = {
                    "features": features.to_dict(),
                    "state": state.value,
                    "mother_verdict": mother_verdict,
                    "perturbation": "applied"
                }
            
            return response
            
        except Exception as e:
            logger.error(f"Agent execution error: {str(e)}", exc_info=True)
            raise
    
    def get_memory(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取历史记忆"""
        return self.memory[-limit:]
    
    def clear_memory(self):
        """清空记忆"""
        self.memory = []
        logger.info("Agent memory cleared")


# 全局实例（单例）
_fortune_agent = None


def init_fortune_agent(llm_service) -> FortuneAgent:
    """初始化 Agent"""
    global _fortune_agent
    _fortune_agent = FortuneAgent(llm_service)
    logger.info("Fortune Agent initialized (Refactored Version)")
    return _fortune_agent


def get_fortune_agent() -> FortuneAgent:
    """获取 Agent 实例"""
    if _fortune_agent is None:
        raise RuntimeError("Fortune Agent not initialized. Call init_fortune_agent first.")
    return _fortune_agent
