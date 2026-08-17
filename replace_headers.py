from pathlib import Path
import re

root = Path(r'c:\Users\liyon\Personal\MCA\PROJECT\drug project (2)\drug project\drugrecomendation\drugrecomendationapp\templates')

# Pattern to match navbar sections (handles different navbar class names)
navbar_pattern = re.compile(
    r'<nav class="navbar navbar-expand-lg[^"]*">.*?</nav>',
    re.DOTALL
)

replacement = "{% include 'header.html' %}"

count = 0
for file in root.glob('*.html'):
    try:
        text = file.read_text(encoding='utf-8')
        new_text = navbar_pattern.sub(replacement, text)
        if new_text != text:
            file.write_text(new_text, encoding='utf-8')
            count += 1
            print(f'Updated {file.name}')
    except Exception as e:
        print(f'Error processing {file.name}: {e}')

print(f'\nTotal files updated: {count}')
