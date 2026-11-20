import re
from .db import connection

CATEGORY_KEYWORDS = {
    "preferences": ("دوست دارم", "ترجیح", "علاقه", "می‌خواهم", "میخوام", "prefer", "like"),
    "projects": ("پروژه", "نکروس", "ربات", "سایت", "برنامه", "project", "robot", "website"),
    "work": ("کار", "شغل", "وظیفه", "درآمد", "work", "job"),
    "learning": ("یاد بگیر", "آموزش", "درس", "برنامه‌نویسی", "یادگیری", "learn", "study"),
}

STOP_WORDS = {
    "و", "در", "به", "از", "که", "را", "با", "برای", "این", "آن", "یک",
    "می", "من", "تو", "است", "هست", "the", "and", "for", "with", "this",
    "that", "you", "are", "was", "have",
}

def _tokens(text: str):
    words = re.findall(r"[\wآ-ی]+", text.casefold())
    return {word for word in words if len(word) > 1 and word not in STOP_WORDS}

def _category(content: str):
    lowered = content.casefold()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            return category
    return "general"

def add_memory(content: str, category: str | None = None, importance: int = 3, tags: str = ""):
    content = content.strip()
    if not content:
        raise ValueError("Memory cannot be empty")
    if not 1 <= importance <= 5:
        raise ValueError("Importance must be between 1 and 5")
    category = (category or _category(content)).strip().lower()[:40]
    tags = tags.strip()[:300]
    with connection() as db:
        # Avoid storing the exact same fact repeatedly.
        existing = db.execute(
            "SELECT * FROM memories WHERE lower(trim(content)) = lower(trim(?)) ORDER BY id DESC LIMIT 1",
            (content,),
        ).fetchone()
        if existing:
            return dict(existing)
        cur = db.execute(
            "INSERT INTO memories(content, category, importance, tags) VALUES (?, ?, ?, ?)",
            (content, category, importance, tags),
        )
        return dict(db.execute("SELECT * FROM memories WHERE id=?", (cur.lastrowid,)).fetchone())

def list_memories(limit: int = 100):
    with connection() as db:
        rows = db.execute(
            "SELECT * FROM memories ORDER BY importance DESC, id DESC LIMIT ?",
            (max(1, min(limit, 200)),),
        )
        return [dict(row) for row in rows]

def search_memories(query: str, limit: int = 10):
    query = query.strip()
    if not query:
        raise ValueError("Search query cannot be empty")
    terms = _tokens(query)
    if not terms:
        raise ValueError("Search query must contain searchable words")

    with connection() as db:
        rows = db.execute("SELECT * FROM memories ORDER BY id DESC LIMIT 1000").fetchall()

    ranked = []
    for row in rows:
        item = dict(row)
        content = item["content"].casefold()
        content_terms = _tokens(content)
        overlap = terms & content_terms
        if not overlap:
            continue
        # Fully local relevance score: no network or AI provider required.
        score = (len(overlap) / len(terms)) * 10
        score += min(item.get("importance", 3), 5) * 0.35
        if query.casefold() in content:
            score += 3
        if item.get("category") and item["category"] in query.casefold():
            score += 1
        item["relevance"] = round(score, 2)
        ranked.append(item)

    ranked.sort(key=lambda item: (item["relevance"], item["id"]), reverse=True)
    return ranked[:max(1, min(limit, 50))]
