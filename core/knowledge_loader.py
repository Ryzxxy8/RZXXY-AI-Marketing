from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"

CORE_FILES = [
    "jareds-takes.md",
]

TASK_FILES = {
    "email": ["marketing-email.md", "marketing-copywriting.md"],
    "ads": ["marketing-fb-ads.md", "marketing-copywriting.md"],
    "lead_magnet": ["marketing-lead-magnets.md", "marketing-copywriting.md"],
    "content": ["marketing-content.md", "marketing-copywriting.md"],
    "analytics": ["marketing-analytics.md"],
    "sales_letter": ["marketing-sales-letter.md", "marketing-copywriting.md"],
    "copywriting": ["marketing-copywriting.md"],
    "strategy": ["the-fundamentals.md"],
}

KEYWORDS = {
    "email": ["email", "အီးမေးလ်", "စာပို့"],
    "ads": ["facebook ads", "facebook ad", "ကြော်ငြာ", "ads"],
    "lead_magnet": ["lead magnet", "opt-in", "lead", "စာရင်းသွင်း"],
    "content": ["content", "အကြောင်းအရာ", "post", "video"],
    "analytics": ["analytics", "metric", "baseline", "data", "ကိန်းဂဏန်း"],
    "sales_letter": ["sales letter", "sales page", "အရောင်းစာ"],
    "strategy": ["strategy", "funnel", "စီမံချက်", "မဟာဗျူဟာ"],
    "copywriting": ["copywriting", "headline", "စာသား", "ရေးပေး"],
}


def detect_tasks(task):
    text = task.lower()
    matched = []

    for category, keywords in KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            matched.append(category)

    return matched or ["copywriting"]


def load_knowledge(task):
    categories = detect_tasks(task)
    selected_files = list(CORE_FILES)

    for category in categories:
        if category == "strategy":
            selected_files.extend(TASK_FILES["strategy"])
        selected_files.extend(
            file for file in TASK_FILES.get(category, [])
            if file not in selected_files
        )

    loaded = []

    for filename in selected_files:
        path = KNOWLEDGE_DIR / filename

        if not path.is_file():
            raise FileNotFoundError(
                "Knowledge file not found: {}".format(filename)
            )

        loaded.append(
            "\n\n# SOURCE: {}\n\n{}".format(
                filename, path.read_text(encoding="utf-8")
            )
        )

    return categories, "\n".join(loaded)


if __name__ == "__main__":
    import sys

    task = " ".join(sys.argv[1:]).strip()

    if not task:
        print("Usage: python3 core/knowledge_loader.py <marketing task>")
        sys.exit(1)

    categories, knowledge = load_knowledge(task)

    print("Detected tasks:", ", ".join(categories))
    print("Knowledge files loaded:")

    for section in knowledge.split("# SOURCE: ")[1:]:
        print("-", section.splitlines()[0])

    print("Total knowledge characters:", len(knowledge))
