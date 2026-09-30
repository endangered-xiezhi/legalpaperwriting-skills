# legal-thesis-skill-draft

法学论文研究与写作辅助 skill 草稿。

## 它从原 humanities-thesis-skill 改了什么

- 适用范围从人文社科论文改为法学论文、案例评析、开题报告和投稿修改。
- 方法论从文本细读、理论框架，改为规范解释、案例研究、法教义学、比较法、法政策和实证法学。
- 防幻觉规则加入法条、司法解释、裁判文书、案号、案例效力层级、文献页码的核验要求。
- 参考材料改为法学写作模板、法学文献综述、法条案例拆解、法学引注格式和人工审核清单。
- 自动审查脚本加入法学论文常见问题：模糊的“司法实践认为”、法条后缺解释、案例后缺规则归纳、比较法直接移植、政策判断脱离规范依据。

## 人工审核入口

重点看这些文件：

- `USAGE_HANDOFF.md`：给用户或其他 agent 的详细使用与交接说明。
- `SKILL.md`：主指令和整体工作流。
- `references/human-review-checklist.md`：交付前人工审核清单。
- `references/legal-methods.md`：方法论是否符合你的法学训练。
- `references/legal-writing-templates.md`：模板是否适合你的写作风格。
- `references/law-review-article-patterns.md`：根据“法学家文章”语料提炼出的核心期刊式写法。
- `references/legal-language-style.md`：标题、段首、论据、段尾、内部层次和整体文风规则。
- `references/local-corpus-style.md`：根据 `/Users/kansang/Downloads/论文库txt` 原文 TXT 提炼句子连接、段落递进和 AI 味用语清理规则。
- `references/article-corpus-study-notes.md`：20 篇样本文献提炼出的结构、结论形态、论证风格和语言风格。
- `references/terminology-bilingual.md`：术语是否需要补充具体部门法。
- `scripts/lib/review_rules.py`：自动检查规则是否过严、漏检或误报。

## 使用审查脚本

```bash
python scripts/review.py paper.md
```

脚本只能做形式化检查，不能判断论文观点是否真正成立。最终内容仍需人工审核、补充和取舍。
