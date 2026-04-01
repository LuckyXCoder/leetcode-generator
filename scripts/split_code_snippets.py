"""
临时脚本：从 codeSnippets JSON 中拆解出各语言代码列

用法：python scripts/split_code_snippets.py
"""
import csv
import json
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "题目详情.csv")

LANG_MAP = {
    "java": "javaCode",
    "python3": "pythonCode",
    "cpp": "cppCode",
}


def main():
    rows = []
    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        for lang_col in LANG_MAP.values():
            if lang_col not in fieldnames:
                fieldnames.append(lang_col)
        for row in reader:
            snippets = json.loads(row.get("codeSnippets") or "[]")
            for slug, col in LANG_MAP.items():
                for s in snippets:
                    if s.get("langSlug") == slug:
                        row[col] = s["code"]
                        break
            rows.append(row)

    with open(CSV_PATH, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"完成！共处理 {len(rows)} 行，新增列: {', '.join(LANG_MAP.values())}")


if __name__ == "__main__":
    main()
