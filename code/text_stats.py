"""统计 UTF-8 文本文件中的单词信息。"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


WORD_PATTERN = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*", re.UNICODE)


def count_words(text: str) -> Counter[str]:
    """返回文本中不区分大小写的单词频次。"""
    return Counter(word.casefold() for word in WORD_PATTERN.findall(text))


def five_most_common(word_counts: Counter[str]) -> list[tuple[str, int]]:
    """按出现次数降序返回最多五个单词，并稳定处理并列项。"""
    return sorted(word_counts.items(), key=lambda item: (-item[1], item[0]))[:5]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="统计文本文件中的单词信息")
    parser.add_argument("file", type=Path, help="要统计的 UTF-8 文本文件路径")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        text = args.file.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise SystemExit(f"无法读取文件 {args.file}: {error}") from error

    word_counts = count_words(text)
    top_five = five_most_common(word_counts)

    print(f"总单词数: {sum(word_counts.values())}")
    print(f"不同单词数量: {len(word_counts)}")
    print("出现次数最多的 5 个单词:")

    if not top_five:
        print("（文本中没有单词）")
        return

    for index, (word, count) in enumerate(top_five, start=1):
        print(f"{index}. {word}: {count}")


if __name__ == "__main__":
    main()
