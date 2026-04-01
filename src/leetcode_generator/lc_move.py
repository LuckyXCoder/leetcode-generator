"""
题目移动模块

将指定题号从 generated/{lang}/problems 目录复制到外部刷题目录。
支持批量复制，自动补零匹配目录名。
"""
import argparse
import os
import shutil

from env_utils import LANGUAGES, TARGET_DIR_MAP, _lang_problems_dir


def move_problem(number: str, lang: str) -> None:
    """
    将指定题号从 generated/{lang}/problems 复制到外部刷题目录

    Args:
        number: 题号（支持 1、001、0001 等格式）
        lang: 语言（java, python, cpp）
    """
    number = number.strip()
    padded = number.zfill(4)
    problems_dir = _lang_problems_dir(lang)

    matched = [
        d for d in os.listdir(problems_dir)
        if os.path.isdir(os.path.join(problems_dir, d)) and d.startswith(f"lc{padded}_")
    ]

    if not matched:
        print(f"  未找到题号 {number} 对应的目录")
        return

    if len(matched) > 1:
        print(f"  匹配到多个目录: {matched}")
        return

    dir_name = matched[0]
    src = os.path.join(problems_dir, dir_name)
    target_dir = TARGET_DIR_MAP.get(lang, "")
    if not target_dir:
        print(f"  [{number}] 未配置 LC_TARGET_DIR_{lang.upper()}，跳过")
        return
    dst = os.path.join(target_dir, dir_name)

    if os.path.exists(dst):
        print(f"  [{number}] {dir_name} - 目标目录已存在，跳过")
        return

    os.makedirs(target_dir, exist_ok=True)
    shutil.copytree(src, dst)
    print(f"  [{number}] {dir_name} -> {target_dir}/{dir_name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="将题目从 generated 目录复制到刷题目录")
    parser.add_argument("numbers", nargs="+", help="题号（支持 1、001、0001 等格式，可多选）")
    parser.add_argument("--lang", default=LANGUAGES[0] if LANGUAGES else "java",
                        choices=["java", "python", "cpp"], help="语言（默认: java）")
    args = parser.parse_args()

    problems_dir = _lang_problems_dir(args.lang)
    target_dir = TARGET_DIR_MAP.get(args.lang, "(未配置)")
    print(f"源目录: {problems_dir}")
    print(f"目标目录: {target_dir}")
    print(f"语言: {args.lang}")
    print(f"共 {len(args.numbers)} 题\n")

    for number in args.numbers:
        move_problem(number, args.lang)

    print("\n完成！")


if __name__ == "__main__":
    main()
