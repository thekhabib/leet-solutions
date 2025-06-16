import os
import re
from collections import defaultdict, Counter
from pathlib import Path

# Mapping difficulty folder to label
DIFFICULTY_MAP = {
    'Easy': '<span style="color:teal">Easy</span>',
    'Medium': '<span style="color:orange">Medium</span>',
    'Hard': '<span style="color:red">Hard</span>'
}

def extract_primary_complexity(line: str) -> str:
    """Extract the first complexity expression like 'O(n)' from a line."""
    return line.split(",")[0].strip() if "," in line else line.strip()

def extract_metadata(filepath: str) -> dict | None:
    """Extract structured metadata from the docstring in a problem solution file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Try double quotes
    docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
    # If not found, try single quotes
    if not docstring_match:
        docstring_match = re.search(r"'''(.*?)'''", content, re.DOTALL)

    if not docstring_match:
        print(f"⚠️ Docstring not found in: {filepath}")
        return None

    lines = [line.strip() for line in docstring_match.group(1).strip().splitlines() if line.strip()]
    if not lines:
        print(f"⚠️ Empty docstring in: {filepath}")
        return None

    # 1. Title
    title_line = lines[0]
    match = re.match(r'(\d+)\.\s+(.*)', title_line)
    if not match:
        print(f"⚠️ Title format invalid in: {filepath}")
        return None
    number = int(match.group(1))
    title = match.group(2)

    # 2. URL
    url_line = next((l for l in lines if l.lower().startswith("url:")), None)
    if not url_line:
        print(f"⚠️ URL not found in: {filepath}")
        return None
    url = url_line.split(":", 1)[1].strip()

    # 3. Tags
    tags_line = next((l for l in lines if l.lower().startswith("tags:")), "")
    tags_clean = re.sub(r"tags?:", "", tags_line, flags=re.IGNORECASE)
    tags = [f'`{tag.strip()}`' for tag in tags_clean.split(",") if tag.strip()]

    # 4. Complexities
    time_line = next((l for l in lines if l.lower().startswith("time")), "")
    space_line = next((l for l in lines if l.lower().startswith("space")), "")
    time = extract_primary_complexity(time_line.split(":", 1)[1]) if ':' in time_line else 'N/A'
    space = extract_primary_complexity(space_line.split(":", 1)[1]) if ':' in space_line else 'N/A'

    return {
        'number': number,
        'title': title,
        'url': url,
        'filepath': filepath,
        'difficulty': Path(filepath).parts[0],
        'time': time,
        'space': space,
        'tags': tags,
    }

def collect_problems() -> list:
    """Collect all problems and their metadata from Easy/Medium/Hard folders."""
    problem_list = []
    for difficulty in DIFFICULTY_MAP.keys():
        folder = Path(difficulty)
        if not folder.exists():
            continue
        for file in folder.glob("*.py"):
            meta = extract_metadata(str(file))
            if meta:
                problem_list.append(meta)
    return sorted(problem_list, key=lambda x: x['number'])

def generate_stats(problem_list):
    counts = Counter(p['difficulty'] for p in problem_list)
    total = len(problem_list)
    easy = counts.get('Easy', 0)
    medium = counts.get('Medium', 0)
    hard = counts.get('Hard', 0)
    return f"**Total Problems: {total}** &nbsp;&nbsp; 🟢 `{easy}` &nbsp;&nbsp; 🟡 `{medium}` &nbsp;&nbsp; 🔴 `{hard}`"

def generate_table(problem_list):
    # Sort by difficulty first, then by problem number
    difficulty_order = {'Easy': 0, 'Medium': 1, 'Hard': 2}
    sorted_problems = sorted(
        problem_list,
        key=lambda x: (difficulty_order.get(x['difficulty'], 99), x['number'])
    )

    header = "| # | Title | Difficulty | Code | Time | Memory | Topics |"
    sep = "|:---:|:--------|:------------:|:--------:|:------:|:--------:|:----------|"
    rows = [header, sep]

    for p in sorted_problems:
        title_md = f"[{p['title']}]({p['url']})"
        path = f"{p['difficulty']}/{Path(p['filepath']).name}"
        solution_md = f"[View]({path})"
        difficulty_md = DIFFICULTY_MAP.get(p['difficulty'], p['difficulty'])
        tags_md = ', '.join(p['tags']) if p['tags'] else ''

        row = f"| {p['number']} | {title_md} | {difficulty_md} | {solution_md} | `{p['time']}` | `{p['space']}` | {tags_md} |"
        rows.append(row)

    return '\n'.join(rows)

def update_readme(problem_list):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    stats = generate_stats(problem_list)
    table = generate_table(problem_list)
    new_block = f"{stats}\n\n{table}"

    updated = re.sub(
        r'<!-- PROBLEM_TABLE_START -->(.*?)<!-- PROBLEM_TABLE_END -->',
        f'<!-- PROBLEM_TABLE_START -->\n{new_block}\n<!-- PROBLEM_TABLE_END -->',
        content,
        flags=re.DOTALL
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"✅ README.md updated with {len(problem_list)} problems.")

if __name__ == "__main__":
    problems = collect_problems()
    update_readme(problems)
