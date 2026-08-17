#!/usr/bin/env python3
"""Repeatable integrity checks for the novel project.

This tool checks project wiring and preservation boundaries. It does not decide
literary quality, Canon truth, or whether a prose passage should be rewritten.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def chapter_numbers(directory: Path) -> list[int]:
    numbers = []
    for path in directory.glob("*.md"):
        match = re.match(r"^(\d{2})-", path.name)
        if match:
            numbers.append(int(match.group(1)))
    return sorted(numbers)


def chapter_stems(directory: Path) -> set[str]:
    return {
        path.stem
        for path in directory.glob("*.md")
        if re.match(r"^\d{2}-", path.name)
    }


def check_source_archive() -> None:
    expected = {
        "01-原始资料/共享会话原文/v1-Story-Bible-原始版.md": "1ba41891ad25948d99d1b4244af5bdc7821d6b101f35d34ec0fa16a32eb8b1e1",
        "01-原始资料/共享会话原文/v2-Story-Bible-爽感强化版.md": "e340d4fd36a2840dc905ac788c5cea6babb50a0604e995b0d9b7d525791ed7b4",
        "01-原始资料/共享会话原文/v3-情绪人物暗伤版.md": "645955674a393621e5c549f130edf2eed244816a01ea4faab22507b49df211d6",
        "01-原始资料/共享会话原文/v4-反转伏笔导演表.md": "b9e516a626203e12a176bcdc9f8ad84c5251deda835acabd7e6285cd0cfd0f23",
        "01-原始资料/共享会话原文/v5-六人核心人物圣经.md": "e0a64b2ef6e94337f36d49ee6e9eff9d89d716687d5474d998c4537553e4e1d5",
        "01-原始资料/共享会话原文/v6-篇章调度与关系架构.md": "0902967f2c5d8c362e21514bceeb51b21f6332fa7006bd2e9fd810986cb366c9",
        "01-原始资料/共享会话原文/v7-第一卷36章导演卡.md": "7c0993ef4a22172145fe87ebca3676935f08632510b2c24cb3da9850f6c7f7b8",
        "01-原始资料/共享会话原文/共享页面-原始HTML-2026-08-17.html": "a31c3e9d5dddbf39e147dce61dfe5154c368c60c23884466272fe91c79bfcf3b",
    }
    for relative, expected_hash in expected.items():
        path = ROOT / relative
        if not path.is_file():
            fail(f"missing source archive: {relative}")
            continue
        actual = sha256(path)
        if actual != expected_hash:
            fail(f"source hash changed: {relative} ({actual})")


def check_required_entries() -> None:
    required = [
        "02-Canon/CANON-唯一真源-v1.0.md",
        "02-Canon/Canon-Change记录.md",
        "02-Canon/权威层级.md",
        "03-结构化设定/人物圣经-v5.md",
        "03-结构化设定/技术概念总登记表.md",
        "04-第一卷设计/第一卷总控.md",
        "05-正文/第一卷/README.md",
        "06-审校/第一卷/第一卷-可持续生产基线.md",
        "06-审校/第一卷/第一卷-当前维护队列.md",
    ]
    for relative in required:
        if not (ROOT / relative).exists():
            fail(f"missing required project entry: {relative}")

    canon_files = sorted((ROOT / "02-Canon").glob("CANON-*.md"))
    if canon_files != [ROOT / "02-Canon/CANON-唯一真源-v1.0.md"]:
        names = ", ".join(path.name for path in canon_files) or "none"
        fail(f"formal Canon entry is not unique: {names}")


def check_chapter_ranges() -> None:
    volumes = [
        ("第一卷设计", ROOT / "04-第一卷设计/章节卡", 1, 36),
        ("第一卷正文", ROOT / "05-正文/第一卷", 1, 36),
        ("第二卷设计", ROOT / "04-第二卷设计/章节卡", 37, 72),
        ("第二卷正文", ROOT / "05-正文/第二卷", 37, 72),
        ("第三卷设计", ROOT / "04-第三卷设计/章节卡", 73, 87),
        ("第三卷正文", ROOT / "05-正文/第三卷", 73, 87),
    ]
    for label, directory, first, last in volumes:
        actual = chapter_numbers(directory)
        expected = list(range(first, last + 1))
        if actual != expected:
            fail(f"chapter range mismatch: {label}: expected {expected}, got {actual}")


def check_chapter_closures() -> None:
    volumes = [
        ("第一卷", ROOT / "04-第一卷设计/章节卡", ROOT / "05-正文/第一卷", ROOT / "06-审校/第一卷", 1, 36),
        ("第二卷", ROOT / "04-第二卷设计/章节卡", ROOT / "05-正文/第二卷", ROOT / "06-审校/第二卷", 37, 72),
        ("第三卷", ROOT / "04-第三卷设计/章节卡", ROOT / "05-正文/第三卷", ROOT / "06-审校/第三卷", 73, 87),
    ]
    for label, cards, prose, audits, first, last in volumes:
        expected_numbers = set(range(first, last + 1))
        card_stems = chapter_stems(cards)
        prose_stems = chapter_stems(prose)
        if card_stems != prose_stems:
            missing_prose = sorted(card_stems - prose_stems)
            missing_cards = sorted(prose_stems - card_stems)
            fail(f"chapter card/prose mismatch: {label}: missing prose={missing_prose}, missing cards={missing_cards}")
        audit_numbers = set(chapter_numbers(audits))
        if audit_numbers != expected_numbers:
            fail(f"chapter audit coverage mismatch: {label}: expected {sorted(expected_numbers)}, got {sorted(audit_numbers)}")


def check_markdown_links() -> None:
    link_pattern = re.compile(r"\]\((<[^>]+>|[^)]+)\)")
    relative_links = 0
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for raw in link_pattern.findall(text):
            target = raw[1:-1] if raw.startswith("<") and raw.endswith(">") else raw
            target = target.split("#", 1)[0].split("?", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            relative_links += 1
            target_path = (path.parent / unquote(target)).resolve()
            if not target_path.exists():
                fail(f"broken Markdown link: {path.relative_to(ROOT)} -> {target}")
    print(f"markdown_files={len(list(ROOT.rglob('*.md')))} relative_links={relative_links}")


def check_first_volume_technical_boundaries() -> None:
    prose_files = sorted((ROOT / "05-正文/第一卷").glob("[0-9][0-9]-*.md"))
    forbidden = ["OpenCV", "API", "ROI", "Mask", "Hough", "Morphology", "Alpha", "Channel", "Layer"]
    for path in prose_files:
        text = path.read_text(encoding="utf-8")
        for term in forbidden:
            if re.search(rf"(?<!\w){re.escape(term)}(?!\w)", text):
                fail(f"forbidden first-volume formal term: {path.name}: {term}")
        if "沈砚" in text or re.search(r"Zero\s*=\s*Alpha", text):
            fail(f"first-volume identity leakage: {path.name}")

    first_occurrence = {
        "Edge": 5,
        "Canny": 6,
        "Contour": 18,
        "Inside": 35,
        "Outside": 35,
        "Mat": 36,
        "View": 36,
    }
    for term, minimum in first_occurrence.items():
        found = []
        for path in prose_files:
            if re.search(rf"(?<!\w){re.escape(term)}(?!\w)", path.read_text(encoding="utf-8")):
                found.append(int(path.name[:2]))
        if found and min(found) < minimum:
            fail(f"formal term appears too early: {term} in chapter {min(found)}; expected >= {minimum}")


def main() -> int:
    check_source_archive()
    check_required_entries()
    check_chapter_ranges()
    check_chapter_closures()
    check_markdown_links()
    check_first_volume_technical_boundaries()
    if ERRORS:
        print(f"FAIL: {len(ERRORS)} issue(s)")
        for error in ERRORS:
            print(f"- {error}")
        return 1
    print("PASS: source archive, project entries, chapter ranges, Markdown links, and first-volume technical boundaries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
