"""
LLM服务 - 使用LiteLLM作为多服务接入层
"""
import asyncio
import logging
import os
from typing import Optional, Dict
from litellm import acompletion
import litellm

logger = logging.getLogger(__name__)

# 配置litellm日志级别
litellm.set_verbose = False


class LLMService:
    """LLM服务类 - 使用LiteLLM统一接口"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.provider = config.get('provider', 'openai')
        self.api_key = config.get('api_key')
        self.base_url = config.get('base_url')
        self.model = config.get('model', 'gpt-4')
        self.max_context_tokens = config.get('max_context_tokens', 128000)
        self.default_model = config.get('default_model', self.model)
        self.fallback_model = config.get('fallback_model', self.model)
        self.temperature = config.get('temperature', 0.7)
        self.max_tokens = config.get('max_tokens', 300)
        
        # 设置环境变量供LiteLLM使用
        if self.api_key:
            os.environ['OPENAI_API_KEY'] = self.api_key
            logger.info(f"LLM API key configured for provider: {self.provider}")
        
        if self.base_url:
            os.environ['OPENAI_API_BASE'] = self.base_url
            logger.info(f"LLM base URL configured: {self.base_url}")
        
        # 预设的备用答案
        self.fallback_responses = {
            'zh': [
                '时机未到，继续等待。',
                '答案在你心中，自己寻找。',
                '改变想法，重新选择。',
                '命运之轮暂时停转。',
                '你已经知道答案了，只是不愿承认。'
            ],
            'en': [
                'The time is not right, keep waiting.',
                'The answer is in your heart, seek it yourself.',
                'Change your mind, choose again.',
                'The wheel of destiny is temporarily stopped.',
                'You already know the answer, just unwilling to admit it.'
            ]
        }
    
    async def generate(self, prompt: str, language: str = 'zh', model: Optional[str] = None) -> str:
        """
        生成文本
        
        Args:
            prompt: 提示词
            language: 语言（'zh' 或 'en'）
            model: 指定模型，如果不指定则使用默认模型
            
        Returns:
            生成的文本
        """
        model_to_use = model or self.default_model
        
        try:
            logger.info(f"Generating with model: {model_to_use}, language: {language}")
            
            # 准备调用参数
            call_params = {
                "model": model_to_use,
                "messages": [{
                    "role": "user",
                    "content": prompt
                }],
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "timeout": 30.0  # 30秒超时
            }
            
            # 如果配置了自定义base_url，添加api_base参数
            if self.base_url:
                call_params["api_base"] = self.base_url
            
            # 使用litellm进行异步调用
            response = await acompletion(**call_params)
            
            # 提取生成的文本
            result = response.choices[0].message.content.strip()
            
            logger.info(f"LLM generation successful: {len(result)} chars")
            return result
            
        except Exception as e:
            logger.error(f"LLM generation failed with {model_to_use}: {str(e)}")
            
            # 如果主模型失败，尝试使用备用模型
            if model_to_use != self.fallback_model:
                try:
                    logger.info(f"Trying fallback model: {self.fallback_model}")
                    
                    fallback_params = {
                        "model": self.fallback_model,
                        "messages": [{
                            "role": "user",
                            "content": prompt
                        }],
                        "temperature": self.temperature,
                        "max_tokens": self.max_tokens,
                        "timeout": 30.0
                    }
                    
                    if self.base_url:
                        fallback_params["api_base"] = self.base_url
                    
                    response = await acompletion(**fallback_params)
                    
                    result = response.choices[0].message.content.strip()
                    logger.info(f"Fallback generation successful: {len(result)} chars")
                    return result
                    
                except Exception as fallback_error:
                    logger.error(f"Fallback model also failed: {str(fallback_error)}")
            
            # 最后使用预设答案
            return self._get_fallback_response(language)
    
    def _get_fallback_response(self, language: str) -> str:
        """获取备用答案"""
        import random
        responses = self.fallback_responses.get(language, self.fallback_responses['zh'])
        response = random.choice(responses)
        logger.info(f"Using fallback response: {response}")
        return response
    
    async def test_connection(self, model: Optional[str] = None) -> Dict:
        """
        测试LLM连接
        
        Args:
            model: 要测试的模型
            
        Returns:
            测试结果
        """
        model_to_test = model or self.default_model
        
        try:
            test_params = {
                "model": model_to_test,
                "messages": [{
                    "role": "user",
                    "content": "Hello"
                }],
                "max_tokens": 10,
                "timeout": 10.0
            }
            
            if self.base_url:
                test_params["api_base"] = self.base_url
            
            response = await acompletion(**test_params)
            
            return {
                "success": True,
                "model": model_to_test,
                "message": "Connection successful"
            }
            
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return {
                "success": False,
                "model": model_to_test,
                "error": str(e)
            }


# 创建全局实例
llm_service: Optional[LLMService] = None


def init_llm_service(config: Dict) -> LLMService:
    """初始化LLM服务"""
    global llm_service
    llm_service = LLMService(config)
    return llm_service


def get_llm_service() -> LLMService:
    """获取LLM服务实例"""
    if llm_service is None:
        raise RuntimeError("LLM service not initialized")
    return llm_service
