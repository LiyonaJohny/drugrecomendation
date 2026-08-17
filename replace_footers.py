from pathlib import Path
import re

root = Path(r'c:\Users\liyon\Personal\MCA\PROJECT\drug project (2)\drug project\drugrecomendation\drugrecomendationapp\templates')

footer_pattern = re.compile(
    r'<footer class="site-footer section-padding">.*?</footer>',
    re.DOTALL
)

replacement = "{% include 'footer.html' %}"

count = 0
for file in root.glob('*.html'):
    text = file.read_text(encoding='utf-8')
    new_text = footer_pattern.sub(replacement, text)
    if new_text != text:
        file.write_text(new_text, encoding='utf-8')
        count += 1
        print(f'Updated {file.name}')

print(f'\nTotal files updated: {count}')
