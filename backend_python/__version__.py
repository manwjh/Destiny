"""
版本信息 | Version Information
《算一卦/Destiny》- Calculate a Fortune/Destiny
"""

__version__ = "0.1.0"
__version_info__ = (0, 1, 0)

# 版本元信息 | Version Metadata
VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_PATCH = 0

# 版本标签 | Version Tag
VERSION_TAG = "v0.1.0"

# 发布日期 | Release Date
RELEASE_DATE = "2026-01-13"

# 项目信息 | Project Information
PROJECT_NAME = "Destiny"
PROJECT_NAME_CN = "算一卦"
PROJECT_DESCRIPTION = "A fun fortune-telling software - An oracle that doesn't comfort you, just gives results"
PROJECT_DESCRIPTION_CN = "一个好玩的算命软件 - 不安慰你，只给结果的算卦器"

# API版本 | API Version
API_VERSION = "v1"

def get_version():
    """获取版本字符串 | Get version string"""
    return __version__

def get_version_info():
    """获取版本信息元组 | Get version info tuple"""
    return __version_info__

def get_full_version():
    """获取完整版本信息 | Get full version information"""
    return {
        "version": __version__,
        "version_tag": VERSION_TAG,
        "release_date": RELEASE_DATE,
        "project_name": PROJECT_NAME,
        "project_name_cn": PROJECT_NAME_CN,
        "api_version": API_VERSION,
        "description": PROJECT_DESCRIPTION,
        "description_cn": PROJECT_DESCRIPTION_CN,
    }
