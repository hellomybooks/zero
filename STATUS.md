# 当前状态 / Project Status

这个文件只描述**现在**，不保存完整项目历史。历史由 Git、Issues、审校记录和原始资料层承担。

## Machine-readable current state

**Current phase:** Volume III ARC08 staged production
**Current volume:** Volume III — 《不存在的区域》
**Current target:** Continue ARC08 from Chapter 88 while preserving Volume I chapters 1–36 as a protected reviewed baseline with evidence-triggered maintenance only.
**Next action:** Submit the Chapter 89 checkpoint for external review; do not continue to Chapter 90 before review.
**Review blockers:** Boundary Form payoff remains a P2 publication-level observation; precision-splitting as a recurring solution pattern and character-specific language failure remain long-range review items.

## 项目规模

- 计划：7 卷 / 252 章 / 21 个主要篇章。
- 第一卷《白色边缘》：第 1—36 章已完成初稿与内部审校，目前处于可持续基线与外部阅读维护阶段。
- 第二卷《阈值之城》：第 37—72 章已保存为完整生产快照。
- 第三卷《不存在的区域》：第89章已形成创作 checkpoint，等待外部阶段审阅；第36章仍不触碰。
- 第四—七卷：已有宏观结构，章级生产尚未完成。

## 当前工作边界

当前优先级是第三卷 ARC08 的阶段性生产，同时保护第一卷质量、Canon 一致性和已审阅的可接管基线；不为制造进度而扩写。

对现有小说进行工作时：

1. 先读 [`AGENTS.md`](./AGENTS.md) 与 [`CANON.md`](./CANON.md)。
2. 只加载当前任务所需的最小上下文。
3. 第一卷修订必须由具体证据触发；没有外部反馈、Canon 冲突或连续性证据时，不主动重写。
4. 不为第一卷虚构“第37章”，也不把第二、第三卷快照反向写成第一卷真相。

## 当前可安全执行的工作

- 处理明确的外部阅读反馈；
- 修复已证实的 Canon / 正文冲突；
- 维护连续性、伏笔和角色状态；
- 改善仓库冷启动、验证器和导航，但不把架构迁移和正文重写混在同一修改中。

## 可选平行实验

[`CORE-SEED.md`](./CORE-SEED.md) 只用于从相同概念 DNA 生长**独立故事**。它不是继续当前小说所需的上下文，也不是当前生产目标。

结构修改后运行：

```bash
python3 凡存在者-项目/tools/validate_project.py
```
