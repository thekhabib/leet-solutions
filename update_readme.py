import os
import re
from pathlib import Path

# Mapping difficulty folder to label
DIFFICULTY_MAP = {
    'Easy': '🟢 Easy',
    'Medium': '🟡 Medium',
    'Hard': '🔴 Hard'
}

# Extract metadata from each solution file
def extract_metadata(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    docstring = re.search(r'"""(.*?)"""', content, re.DOTALL)
    if not docstring:
        return None

    lines = docstring.group(1).strip().splitlines()
    if not lines:
        return None

    # Problem info
    title_line = lines[0].strip()
    match = re.match(r'(\d+)\.\s+(.*)', title_line)
    if not match:
        return None

    number = int(match.group(1))
    title = match.group(2)

    # Tags
    tags_line = next((l for l in lines if l.startswith("#tag")), '')
    tags = [tag.strip() for tag in tags_line.replace("#tag:", "").split(',') if tag.strip()]

    # Time and space complexity
    time = next((l.split(':')[1].strip() for l in lines if l.lower().startswith('time')), 'N/A')
    space = next((l.split(':')[1].strip() for l in lines if l.lower().startswith('space')), 'N/A')

    return {
        'number': number,
        'title': title,
        'slug': title.lower().replace(' ', '-'),
        'filepath': filepath,
        'difficulty': Path(filepath).parts[0],
        'time': time,
        'space': space,
        'tags': tags
    }

# Find all problems
def collect_problems():
    problems = []
    for difficulty in ['Easy', 'Medium', 'Hard']:
        folder = Path(difficulty)
        if not folder.exists():
            continue
        for file in folder.glob("*.py"):
            meta = extract_metadata(str(file))
            if meta:
                problems.append(meta)
    return sorted(problems, key=lambda x: x['number'])

# Generate markdown table for problem list
def generate_table(problems):
    header = "| # | Title | Difficulty | Solution | Time | Memory | Tags |"
    sep =     "|--:|:------|:-----------|:---------|:-----:|:------:|:-----|"
    rows = [header, sep]

    for p in problems:
        link = f"https://leetcode.com/problems/{p['slug']}/"
        title_md = f"[{p['title']}]({link})"
        path = f"{p['difficulty']}/{str(Path(p['filepath']).name)}"
        solution_md = f"[View]({path})"
        tags_md = ', '.join(p['tags'])
        rows.append(f"| {p['number']} | {title_md} | {p['difficulty']} | {solution_md} | {p['time']} | {p['space']} | {tags_md} |")

    return '\n'.join(rows)

# Inject generated table into README
def update_readme(problems):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    table_md = generate_table(problems)
    new_content = re.sub(
        r'(## \ud83d\udcc8 Problem List\n\n)(.*?)(\n\n##)',
        f"\\1{table_md}\\3",
        content,
        flags=re.DOTALL
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    problems = collect_problems()
    update_readme(problems)
    print("✅ README.md updated with", len(problems), "problems.")
