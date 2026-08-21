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
REPO_ROOT = ROOT.parent
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
        "01-原始资料/共享会话-完整转录.md": "617e0dd058b0bca3347574f9dfd7f7dbc6824a472dd5a3414ec625dd9e837283",
        "01-原始资料/原始对话核对回复.md": "60ce5d32d950363f66f674f7d91a36c5dbdd07c4243b587e04bfaddee5c1a1c4",
        "01-原始资料/缺失与恢复状态/v1-v4-资料状态.md": "d5cf55949ee58bd420955d03ccff6d8db8e3df9bc8776b75fe42cde62efa2851",
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
        "01-原始资料/README.md",
        "02-Canon/README.md",
        "02-Canon/CANON-唯一真源-v1.0.md",
        "02-Canon/Canon-Change记录.md",
        "02-Canon/权威层级.md",
        "03-结构化设定/README.md",
        "03-结构化设定/人物圣经-v5.md",
        "03-结构化设定/技术概念总登记表.md",
        "04-第一卷设计/README.md",
        "04-第一卷设计/第一卷总控.md",
        "05-正文/README.md",
        "05-正文/第一卷/README.md",
        "06-审校/README.md",
        "06-审校/第一卷/第一卷-可持续生产基线.md",
        "06-审校/第一卷/第一卷-当前维护队列.md",
        "06-审校/第一卷/外部阅读反馈/README.md",
        "06-审校/第一卷/外部阅读反馈/第一卷-外部审核包.md",
        "06-审校/第一卷/外部阅读反馈/模板.md",
        "06-审校/第一卷/第一卷-人物弧与关系回归.md",
        "06-审校/第一卷/第一卷-章节推进链回归.md",
    ]
    for relative in required:
        if not (ROOT / relative).exists():
            fail(f"missing required project entry: {relative}")

    canon_files = sorted((ROOT / "02-Canon").glob("CANON-*.md"))
    if canon_files != [ROOT / "02-Canon/CANON-唯一真源-v1.0.md"]:
        names = ", ".join(path.name for path in canon_files) or "none"
        fail(f"formal Canon entry is not unique: {names}")


def check_cold_start_entries() -> None:
    """Protect the minimal human/AI entry layer at the repository root."""

    entries = ["README.md", "AGENTS.md", "STATUS.md", "CANON.md"]
    for name in entries:
        if not (REPO_ROOT / name).is_file():
            fail(f"missing repository cold-start entry: {name}")

    checks = {
        "README.md": ["STATUS.md", "AGENTS.md", "CANON.md", "凡存在者-项目/05-正文/"],
        "AGENTS.md": ["Cold start", "权威层级.md", "validate_project.py"],
        "STATUS.md": ["Current phase:", "Current volume:", "Current target:", "Next action:"],
        "CANON.md": ["not a second Canon", "CANON-唯一真源-v1.0.md", "Core invariants"],
    }
    for name, phrases in checks.items():
        path = REPO_ROOT / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                fail(f"repository cold-start entry marker missing: {name}: {phrase}")


def check_current_production_target() -> None:
    """Treat root STATUS.md as the single machine-readable current-state source."""

    status_path = REPO_ROOT / "STATUS.md"
    if not status_path.is_file():
        fail("missing current-state source: STATUS.md")
        return

    status = status_path.read_text(encoding="utf-8")
    required_fields = ["Current phase:", "Current volume:", "Current target:", "Next action:"]
    for field in required_fields:
        if field not in status:
            fail(f"current-state field missing from STATUS.md: {field}")

    if "Volume I" not in status or "《白色边缘》" not in status:
        fail("STATUS.md does not identify Volume I / 《白色边缘》 as the current volume")
    if "evidence-triggered" not in status:
        fail("STATUS.md is missing the evidence-triggered maintenance boundary")

    queue = (ROOT / "06-审校/第一卷/第一卷-当前维护队列.md").read_text(encoding="utf-8")
    if "有证据触发的维护阶段" not in queue:
        fail("first-volume maintenance queue is missing evidence-triggered status")
    if "不虚构第37章" not in queue:
        fail("first-volume maintenance queue is missing no-chapter-37 guard")


def check_external_review_boundary() -> None:
    """Protect the reviewer handoff without judging literary quality."""

    kit = ROOT / "06-审校/第一卷/外部阅读反馈/第一卷-外部审核包.md"
    entry = ROOT / "06-审校/第一卷/外部阅读反馈/README.md"
    template = ROOT / "06-审校/第一卷/外部阅读反馈/模板.md"
    kit_text = kit.read_text(encoding="utf-8")
    entry_text = entry.read_text(encoding="utf-8")
    template_text = template.read_text(encoding="utf-8")

    kit_phrases = [
        "只读第1—36章正文",
        "不需要打开维护队列",
        "第1—36章正文直达清单",
        "无剧透简介",
    ]
    for phrase in kit_phrases:
        if phrase not in kit_text:
            fail(f"external review kit marker missing: {phrase}")

    entry_phrases = [
        "第一卷外部审核包",
        "首次阅读不需要打开维护队列",
        "作者侧复核",
    ]
    for phrase in entry_phrases:
        if phrase not in entry_text:
            fail(f"external review entry marker missing: {phrase}")

    template_fields = [
        "我实际观察到的内容",
        "我的推测",
        "我的评价",
        "阅读行为",
        "影响范围",
        "严重度理由",
        "是否建议修改",
    ]
    for field in template_fields:
        if field not in template_text:
            fail(f"external review template field missing: {field}")

    if "### 事实、推测与评价必须分开" not in template_text:
        fail("external review template is missing the fact/speculation/evaluation heading")
    issue_header = next(
        (line for line in template_text.splitlines() if line.startswith("|") and "章节 / 场景" in line),
        "",
    )
    for column in ["类型", "严重度", "证据或短引", "我的建议"]:
        if column not in issue_header:
            fail(f"external review template issue table is missing column: {column}")

    def section_between(text: str, heading: str) -> str:
        pattern = rf"(?ms)^### {re.escape(heading)}\s*$([\s\S]*?)(?=^### |\Z)"
        match = re.search(pattern, text)
        if not match:
            fail(f"external review kit section missing: {heading}")
            return ""
        return match.group(1)

    def linked_paths(text: str, base: Path) -> list[Path | None]:
        link_pattern = re.compile(r"\]\((<[^>]+>|[^)]+)\)")
        paths: list[Path | None] = []
        for raw in link_pattern.findall(text):
            target = raw[1:-1] if raw.startswith("<") and raw.endswith(">") else raw
            target = target.split("#", 1)[0].split("?", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                paths.append(None)
                continue
            paths.append((base / unquote(target)).resolve())
        return paths

    prose_directory = ROOT / "05-正文/第一卷"
    prose_files = sorted(prose_directory.glob("[0-9][0-9]-*.md"))
    expected_prose = [path.resolve() for path in prose_files]

    synopsis = re.search(
        r"(?ms)^<!-- synopsis:start -->\s*(.*?)\s*^<!-- synopsis:end -->$",
        kit_text,
    )
    if not synopsis:
        fail("external review kit is missing a bounded synopsis block")
    else:
        synopsis_text = synopsis.group(1)
        for phrase in ["软件工程师", "魔法异世界", "无法看清"]:
            if phrase not in synopsis_text:
                fail(f"external review synopsis is missing safe premise marker: {phrase}")
        spoiler_terms = [
            "OpenCV",
            "Canny",
            "Alpha",
            "Copy",
            "Mat",
            "View",
            "世界原图",
            "观察者",
            "谁定义计算规则",
        ]
        for term in spoiler_terms:
            if re.search(rf"(?<!\w){re.escape(term)}(?!\w)", synopsis_text):
                fail(f"external review synopsis contains protected spoiler term: {term}")

    first_read = section_between(kit_text, "第一次阅读：只读正文")
    first_read_forbidden = [
        ROOT / "02-Canon",
        ROOT / "03-结构化设定",
        ROOT / "04-第一卷设计",
        ROOT / "05-正文/第二卷",
        ROOT / "05-正文/第三卷",
    ]
    feedback_root = (ROOT / "06-审校/第一卷/外部阅读反馈").resolve()
    for target in linked_paths(first_read, kit.parent):
        if target is None:
            continue
        if any(target == forbidden or forbidden in target.parents for forbidden in first_read_forbidden):
            fail(f"first-reading section links to author-side or later-volume material: {target.relative_to(ROOT)}")
        if ROOT / "06-审校" in target.parents and feedback_root not in target.parents:
            fail(f"first-reading section links outside the feedback handoff: {target.relative_to(ROOT)}")

    direct_list = section_between(kit_text, "第1—36章正文直达清单")
    direct_targets = linked_paths(direct_list, kit.parent)
    if len(direct_targets) != len(expected_prose):
        fail(
            "external review direct prose list must contain exactly "
            f"{len(expected_prose)} links, got {len(direct_targets)}"
        )
    elif direct_targets != expected_prose:
        fail("external review direct prose list is not exactly ordered from chapter 1 through chapter 36")

    # Keep the broader check as a safety net for accidental deletion outside the
    # designated ordered list, while the exact list check above protects order
    # and volume boundaries.
    link_pattern = re.compile(r"\]\((<[^>]+>|[^)]+)\)")
    linked_targets = set()
    for raw in link_pattern.findall(kit_text):
        target = raw[1:-1] if raw.startswith("<") and raw.endswith(">") else raw
        target = target.split("#", 1)[0].split("?", 1)[0]
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        linked_targets.add((kit.parent / unquote(target)).resolve())

    for path in sorted(prose_directory.glob("[0-9][0-9]-*.md")):
        if path.resolve() not in linked_targets:
            fail(f"external review kit missing direct prose link: {path.name}")


def check_chapter_ranges() -> None:
    volumes = [
        ("第一卷设计", ROOT / "04-第一卷设计/章节卡", 1, 36),
        ("第一卷正文", ROOT / "05-正文/第一卷", 1, 36),
        ("第二卷设计", ROOT / "04-第二卷设计/章节卡", 37, 72),
        ("第二卷正文", ROOT / "05-正文/第二卷", 37, 72),
        ("第三卷设计", ROOT / "04-第三卷设计/章节卡", 73, 88),
        ("第三卷正文", ROOT / "05-正文/第三卷", 73, 88),
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
        ("第三卷", ROOT / "04-第三卷设计/章节卡", ROOT / "05-正文/第三卷", ROOT / "06-审校/第三卷", 73, 88),
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
    markdown_paths = list(ROOT.rglob("*.md")) + list(REPO_ROOT.glob("*.md"))
    for path in markdown_paths:
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
    print(f"markdown_files={len(markdown_paths)} relative_links={relative_links}")


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
    check_cold_start_entries()
    check_current_production_target()
    check_chapter_ranges()
    check_chapter_closures()
    check_markdown_links()
    check_external_review_boundary()
    check_first_volume_technical_boundaries()
    if ERRORS:
        print(f"FAIL: {len(ERRORS)} issue(s)")
        for error in ERRORS:
            print(f"- {error}")
        return 1
    print("PASS: source archive, cold-start entries, current status, project wiring, chapter ranges, Markdown links, and first-volume technical boundaries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
