"""
路径配置集中管理模块

所有路径均支持通过环境变量覆盖，开箱即用。
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# 加载项目根目录的 .env
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(_PROJECT_ROOT / ".env")

PROJECT_ROOT = str(_PROJECT_ROOT)

OUTPUT_DIR = os.getenv("LC_OUTPUT_DIR", os.path.join(PROJECT_ROOT, "data"))
GENERATED_DIR = os.getenv("LC_GENERATED_DIR", os.path.join(PROJECT_ROOT, "generated"))
DETAIL_CSV = os.getenv("LC_DETAIL_CSV", os.path.join(OUTPUT_DIR, "题目详情.csv"))

# 语言配置
LANGUAGES = [lang.strip() for lang in os.getenv("LC_LANGUAGES", "java").split(",") if lang.strip()]

# 题型子目录名
TYPE_SUBDIRS = ["problems", "LCP", "LCR", "LCS", "interview"]

# 生成目录按语言划分：generated/leetcode/{lang}/leetcode/problems/ ...
def _lang_generated_dir(lang: str) -> str:
    return os.path.join(GENERATED_DIR, lang)

def _lang_problems_dir(lang: str) -> str:
    return os.path.join(GENERATED_DIR, lang, "leetcode", "problems")

# 各语言题型目录映射
def get_type_dir_map(lang: str) -> dict[str, str]:
    base = os.path.join(_lang_generated_dir(lang), "leetcode")
    return {
        "problems": os.path.join(base, "problems"),
        "LCP": os.path.join(base, "LCP"),
        "LCR": os.path.join(base, "LCR"),
        "LCS": os.path.join(base, "LCS"),
        "面试题": os.path.join(base, "interview"),
    }

# 各语言的外部刷题目标目录
TARGET_DIR_MAP = {
    "java": os.getenv("LC_TARGET_DIR_JAVA", ""),
    "python": os.getenv("LC_TARGET_DIR_PYTHON", ""),
    "cpp": os.getenv("LC_TARGET_DIR_CPP", ""),
}
