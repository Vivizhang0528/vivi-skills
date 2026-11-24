# Vivi Skills

可复用的学术 presentation 制作规范，记录 Vivi 偏好的叙述逻辑、证据呈现和简洁视觉。

目前包含 **[Vivi 学术 PPT](vivi-academic-ppt/SKILL.md)**（`vivi-academic-ppt`），适用于课程 pre、研究汇报、现有 Google Slides / PowerPoint 的结构调整与视觉优化。

## 怎样调用

在能够读取本仓库文件、并加载 [AGENTS.md](AGENTS.md) 的项目中，直接说：

> 调用 Vivi 学术 PPT，先阅读我的 outline、研究设计和现有 PPT，再优化叙述结构与视觉。

也可以说：

> 沿用上次学术 PPT 的审美，重点检查案例对照、结论和引用。

在支持已安装 skills 的环境中，可使用 `$vivi-academic-ppt`。**保存在 GitHub 不等于已全局安装**；新环境需先导入完整 skill 文件夹，或显式提供 SKILL.md 及配套资源。

## 11 条核心规则

1. **简洁封面**：研究题目、必要信息、合适配图。
2. **第二页 Contents**：明确 Part 数量、结构和顺序。
3. **Part 扉页**：每部分之前有扉页，仅放编号、短标题和可选单图。
4. **统一标题**：主标题字号一致，标题与内容小标题加粗；结构标签小而浅。
5. **对比用表格框**：品牌、案例或条件采用清晰、有边框的并列比较。
6. **当前页标来源**：引用、他人图文和论文在该页底部注明出处。
7. **结论先亮答案**：Conclusion 的第一张内容页直接给核心结论和关键数据，对应 RQ。
8. **Limitation 独立**：研究局限单独一页。
9. **References 独立**：参考文献单独呈现，Q&A 另页。
10. **保留 Appendix**：完整证据、补充统计、编码和图源可查，版面简洁。
11. **流程进度条**：正文按 Part 页数分段并逐页推进，附录独立计算。

## 叙述与视觉偏好

- 按“现实背景 → 研究缺口 → RQ → 框架与方法 → 结果和案例 → 回答 RQ → 讨论与局限”展开；不要以收集量或文献篇数代替研究动机。
- 案例是主体，理论和论文依据放下方；中文社媒语料采用中文原文与简短英文翻译配合。
- 默认四个 Part，按课程 rubric 和实际内容调整，不机械套固定页数。
- 使用统一无衬线字体、灰蓝与暖白、加粗标题和细横线；纸纹轻且只用于原有色块，Appendix 保持纯色。
- 独立品牌标签可使用可追溯的标准 Logo；正文与原始引文中的品牌名称保留可编辑文字。
- 为出处、页码和进度条预留空间；保持截图比例，不让页脚与内容重叠。
- 核对数据、分母、时段、来源和推断边界，不编造结果、文献或受众效果。
- 用户当前要求和课程 rubric 优先于默认审美。

## 文件说明

| 文件 | 用途 |
| --- | --- |
| [AGENTS.md](AGENTS.md) | 项目内的调用入口 |
| [SKILL.md](vivi-academic-ppt/SKILL.md) | 主流程与核心规则 |
| [openai.yaml](vivi-academic-ppt/agents/openai.yaml) | Skill 名称和调用提示 |
| [visual-system.md](vivi-academic-ppt/references/visual-system.md) | 字体、颜色、页面分区和版式 |
| [story-and-evidence.md](vivi-academic-ppt/references/story-and-evidence.md) | 研究叙述、案例与证据边界 |
| [quality-checklist.md](vivi-academic-ppt/references/quality-checklist.md) | 交付前的结构、学术和视觉自查 |
| [progress_plan.py](vivi-academic-ppt/scripts/progress_plan.py) | 根据最终页序生成进度布局计划 |

## 进度条辅助脚本

脚本只使用 Python 标准库，读取包含实际页 ID、角色与 Part 的 JSON 计划：

```bash
python vivi-academic-ppt/scripts/progress_plan.py plan.json --output progress.json
```

输入示例：

```json
{
  "slides": [
    {"id": "cover", "role": "cover"},
    {"id": "contents", "role": "contents"},
    {"id": "part1", "role": "part", "part": "1"},
    {"id": "background", "role": "content", "part": "1"},
    {"id": "references", "role": "references"},
    {"id": "qa", "role": "qa"},
    {"id": "appendix_a", "role": "appendix"}
  ]
}
```

示例 ID 只用于说明；编辑线上文件时必须使用已验证的实际页 ID。脚本输出分段、圆点位置和链接目标，不会自动修改 PPT，也不能代替引用核验和逐页视觉检查。

## 已完成的验证

- Skill 格式与调用元数据校验。
- 33 页情境下的 Part 权重、正文进度、附录进度与几何边界测试。
- 重复页 ID、缺失 Part 等错误输入检查。
- 使用另一份研究草稿进行独立结构试用。

每次制作仍须依据当次材料核对事实、渲染全部页面并检查最终版本。
