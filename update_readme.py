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

    # Link to the problem
    link_line = next((l for l in lines if l.lower().startswith("url:")), None)
    if not link_line:
        return None
    url = link_line.split(":", 1)[1].strip()

    # Tags
    tags_line = next((l for l in lines if l.lower().startswith("#tag")), '')
    tags_line = re.sub(r"#tags?:", "", tags_line, flags=re.IGNORECASE)
    tags = [tag.strip() for tag in tags_line.split(',') if tag.strip()]

    # Time and space complexity
    time = next((l.split(':')[1].strip() for l in lines if l.lower().startswith('time')), 'N/A')
    space = next((l.split(':')[1].strip() for l in lines if l.lower().startswith('space')), 'N/A')

    return {
        'number': number,
        'title': title,
        'url': url,
        'filepath': filepath,
        'difficulty': Path(filepath).parts[0],
        'time': time,
        'space': space,
        'tags': tags
    }

# Find all problems
def collect_problems():
    problem_list = []
    for difficulty in ['Easy', 'Medium', 'Hard']:
        folder = Path(difficulty)
        if not folder.exists():
            continue
        for file in folder.glob("*.py"):
            meta = extract_metadata(str(file))
            if meta:
                problem_list.append(meta)
    return sorted(problem_list, key=lambda x: x['number'])

# Generate markdown table for problem list
def generate_table(problem_list):
    header = "| # | Title | Difficulty | Solution | Time | Memory | Tags |"
    sep = "|---:|:-----------|:------------|:----------|:------:|:-------:|:-----------|"
    rows = [header, sep]

    for p in problem_list:
        title_md = f"[{p['title']}]({p['url']})"
        path = f"{p['difficulty']}/{Path(p['filepath']).name}"
        solution_md = f"[View]({path})"

        # Map difficulty to label
        difficulty_md = DIFFICULTY_MAP.get(p['difficulty'], p['difficulty'])

        # Tags in backtick markdown format
        tags_md = ', '.join(f"`{tag}`" for tag in p['tags'])

        rows.append(
            f"| {p['number']} | {title_md} | {difficulty_md} | {solution_md} | {p['time']} | {p['space']} | {tags_md} |"
        )

    return '\n'.join(rows)

# Inject generated table into README
def update_readme(problem_list):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    table_md = generate_table(problem_list)

    # Jadvalni <!-- PROBLEM_TABLE_START --> va <!-- PROBLEM_TABLE_END --> orasiga joylashtirish
    new_content = re.sub(
        r'<!-- PROBLEM_TABLE_START -->(.*?)<!-- PROBLEM_TABLE_END -->',
        f'<!-- PROBLEM_TABLE_START -->\n{table_md}\n<!-- PROBLEM_TABLE_END -->',
        content,
        flags=re.DOTALL
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    problems = collect_problems()
    update_readme(problems)
    print("✅ README.md updated with", len(problems), "problems.")
