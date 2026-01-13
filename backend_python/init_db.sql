-- 《算一卦/Destiny》数据库初始化脚本
-- Database Initialization Script for Destiny

-- 设置时区
SET timezone = 'UTC';

-- 用户会话表
CREATE TABLE IF NOT EXISTS user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id VARCHAR(255),
    question TEXT NOT NULL,
    language VARCHAR(2) NOT NULL CHECK (language IN ('zh', 'en')),
    result TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_agent TEXT,
    ip_hash VARCHAR(64),
    response_time INTEGER NOT NULL CHECK (response_time > 0)
);

-- 用户会话表索引
CREATE INDEX IF NOT EXISTS idx_sessions_timestamp ON user_sessions (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_sessions_client ON user_sessions (client_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_sessions_language ON user_sessions (language, timestamp DESC);

-- 提示词模板表
CREATE TABLE IF NOT EXISTS prompt_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    language VARCHAR(2) NOT NULL CHECK (language IN ('zh', 'en')),
    template_type VARCHAR(50) NOT NULL CHECK (template_type IN ('base', 'night', 'special')),
    template_content TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 提示词模板表索引
CREATE INDEX IF NOT EXISTS idx_templates_active ON prompt_templates (language, template_type, is_active);
CREATE INDEX IF NOT EXISTS idx_templates_name ON prompt_templates (name, version);

-- 插入默认提示词模板（中文）
INSERT INTO prompt_templates (name, language, template_type, template_content, version, is_active) 
VALUES
('base_zh', 'zh', 'base', 
'你是一个冷酷的命运判官。用户向你询问命运，你需要给出简短、直接、有力的判决。
规则：
1. 不要安慰用户，不要给建议
2. 直接揭示结果和后果
3. 语气冷静、客观、不留情面
4. 回答控制在50-100字以内
5. 不要使用"可能"、"也许"等模糊词汇

用户问题：{question}

你的判决：', 1, true),

('night_zh', 'zh', 'night', 
'深夜时分，你是洞察人心的命运之眼。用户在黑暗中向你寻求答案，你要用最锋利的真相回应。
规则：
1. 揭示隐藏的真相，不留情面
2. 语气深邃、直接
3. 50-100字以内
4. 直指核心，不绕弯子

用户问题：{question}

你的判决：', 1, true);

-- 插入默认提示词模板（英文）
INSERT INTO prompt_templates (name, language, template_type, template_content, version, is_active) 
VALUES
('base_en', 'en', 'base', 
'You are a cold and direct fortune judge. Users ask you about their destiny, and you give short, direct, and powerful verdicts.
Rules:
1. No comfort, no advice
2. Reveal results and consequences directly
3. Tone: calm, objective, ruthless
4. Answer within 50-100 words
5. No vague words like "maybe", "perhaps"

User question: {question}

Your verdict:', 1, true),

('night_en', 'en', 'night', 
'In the dead of night, you are the eye of destiny that sees through hearts. Users seek answers from you in darkness, and you respond with the sharpest truth.
Rules:
1. Reveal hidden truths without mercy
2. Tone: profound, direct
3. Within 50-100 words
4. Cut to the core, no detours

User question: {question}

Your verdict:', 1, true);

-- 统计视图：每日请求统计
CREATE OR REPLACE VIEW daily_stats AS
SELECT 
    DATE(timestamp) as date,
    language,
    COUNT(*) as total_requests,
    AVG(response_time)::INTEGER as avg_response_time,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY response_time)::INTEGER as median_response_time,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY response_time)::INTEGER as p95_response_time
FROM user_sessions
GROUP BY DATE(timestamp), language
ORDER BY date DESC, language;

-- 创建完成消息
DO $$
BEGIN
    RAISE NOTICE '==============================================';
    RAISE NOTICE '数据库初始化完成 | Database initialized';
    RAISE NOTICE '==============================================';
    RAISE NOTICE '表创建完成 | Tables created:';
    RAISE NOTICE '  - user_sessions (用户会话)';
    RAISE NOTICE '  - prompt_templates (提示词模板)';
    RAISE NOTICE '索引创建完成 | Indexes created';
    RAISE NOTICE '默认数据插入完成 | Default data inserted';
    RAISE NOTICE '视图创建完成 | Views created:';
    RAISE NOTICE '  - daily_stats (每日统计)';
    RAISE NOTICE '==============================================';
END $$;
