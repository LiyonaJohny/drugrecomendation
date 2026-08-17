from pathlib import Path
import re

root = Path(r'c:\Users\liyon\Personal\MCA\PROJECT\drug project (2)\drug project\drugrecomendation\drugrecomendationapp\templates')

# Pattern to match the entire news section
news_pattern = re.compile(
    r'<section class="news section-padding">.*?</section>\s*',
    re.DOTALL
)

replacement = "{% include 'news_section.html' %}\n\n        "

count = 0
for file in root.glob('*.html'):
    try:
        text = file.read_text(encoding='utf-8')
        new_text = news_pattern.sub(replacement, text)
        if new_text != text:
            file.write_text(new_text, encoding='utf-8')
            count += 1
            print(f'Updated {file.name}')
    except Exception as e:
        print(f'Error processing {file.name}: {e}')

print(f'\nTotal files updated: {count}')
