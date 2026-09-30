"""查询预处理

将用户的自然语言搜索词优化为更适合学术数据库检索的形式。
处理中英文混合、法学术语中英对照、常见缩写展开等。
"""
from __future__ import annotations
import re


# 常见法学术语中英文对照
_SCHOLAR_MAP: dict[str, str] = {
    "请求权基础": "basis of claim",
    "民事法律行为": "juristic act",
    "意思表示": "declaration of intent",
    "善意取得": "good-faith acquisition",
    "公司人格否认": "piercing the corporate veil",
    "法人人格否认": "disregard of corporate personality",
    "信义义务": "fiduciary duty",
    "忠实义务": "duty of loyalty",
    "勤勉义务": "duty of care",
    "注意义务": "duty of care",
    "过错责任": "fault-based liability",
    "无过错责任": "strict liability",
    "证明责任": "burden of proof",
    "比例原则": "principle of proportionality",
    "信赖保护": "legitimate expectations",
    "正当程序": "due process",
    "罪刑法定": "principle of legality",
    "裁判规则": "judicial rule",
    "比较法": "comparative law",
}

# 常见学术缩写展开
_ABBREV_MAP: dict[str, str] = {
    "民法典": "中华人民共和国民法典 Civil Code",
    "公司法": "中华人民共和国公司法 Company Law",
    "刑法": "中华人民共和国刑法 Criminal Law",
    "行政法": "administrative law",
}


def _extract_chinese(text: str) -> list[str]:
    """提取中文词汇（连续中文字符）"""
    return re.findall(r"[\u4e00-\u9fff]+", text)


def _extract_english(text: str) -> list[str]:
    """提取英文词汇"""
    return re.findall(r"[a-zA-ZÀ-ÿ]+(?:\s+[a-zA-ZÀ-ÿ]+)*", text)


def expand_query(query: str) -> dict[str, str]:
    """将用户查询展开为中英文两个版本

    输入：用户的自然语言查询
    输出：{
        "zh": "中文优化查询",
        "en": "英文优化查询",
        "original": "原始查询"
    }

    示例：
        "公司人格否认 裁判规则"
        → zh: "公司人格否认 裁判规则"
        → en: "piercing the corporate veil judicial rule"
    """
    query = query.strip()
    zh_parts: list[str] = []
    en_parts: list[str] = []

    # 提取中文部分
    chinese_words = _extract_chinese(query)
    for word in chinese_words:
        zh_parts.append(word)
        # 如果是法学术语，添加英文对照
        if word in _SCHOLAR_MAP:
            en_parts.append(_SCHOLAR_MAP[word])
        # 如果是常见缩写，展开
        if word in _ABBREV_MAP:
            expanded = _ABBREV_MAP[word]
            if expanded != word:
                # 提取展开词中的英文部分
                en_words = _extract_english(expanded)
                if en_words:
                    en_parts.extend(en_words)

    # 提取英文部分
    english_words = _extract_english(query)
    en_parts.extend(english_words)

    # 尝试翻译关键法律概念
    concept_map = {
        "合同": "contract",
        "侵权": "tort",
        "公司": "company corporation",
        "股东": "shareholder",
        "董事": "director",
        "出资": "capital contribution",
        "担保": "security guarantee",
        "破产": "bankruptcy",
        "行政": "administrative",
        "刑事": "criminal",
        "证据": "evidence",
        "裁判": "judgment adjudication",
        "案例": "case",
        "法教义学": "legal dogmatics",
    }
    for word in chinese_words:
        if word in concept_map and concept_map[word] not in " ".join(en_parts).lower():
            en_parts.append(concept_map[word])

    # 如果英文部分为空，使用原始查询
    if not en_parts:
        en_parts = [query]

    return {
        "zh": " ".join(zh_parts) if zh_parts else query,
        "en": " ".join(en_parts) if en_parts else query,
        "original": query,
    }


def suggest_queries(query: str) -> list[str]:
    """基于用户查询推荐多个搜索变体

    返回3-5个搜索建议，用于不同数据库。
    """
    expanded = expand_query(query)
    suggestions = [expanded["original"]]

    if expanded["zh"] != expanded["original"]:
        suggestions.append(expanded["zh"])
    if expanded["en"] != expanded["original"]:
        suggestions.append(expanded["en"])

    # 如果查询包含理论家名字，生成"理论家+研究对象"的组合
    chinese_words = _extract_chinese(query)
    scholars_found = [w for w in chinese_words if w in _SCHOLAR_MAP]
    non_scholars = [w for w in chinese_words if w not in _SCHOLAR_MAP]

    if scholars_found and non_scholars:
        # 英文版：理论家英文名+研究对象
        for scholar in scholars_found:
            en_name = _SCHOLAR_MAP[scholar]
            en_suggestion = f"{en_name} {' '.join(non_scholars)}"
            if en_suggestion not in suggestions:
                suggestions.append(en_suggestion)

    return suggestions[:5]
