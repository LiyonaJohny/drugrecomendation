from pathlib import Path

root = Path(r"c:\Users\liyon\Personal\MCA\PROJECT\drug project (2)\drug project\drugrecomendation")

replacements = [
    ('Crispy Kitchen - Bootstrap 5 HTML Template', 'Liyona Johny | Drug Recommendation'),
    ('Crispy Kitchen', 'Liyona Johny'),
    ('Tooplate 2129 Crispy Kitchen', 'Liyona Johny | Health & Medication Portal'),
    ('https://www.tooplate.com/view/2129-crispy-kitchen', 'https://www.liyonajohny.com'),
    ('Copyright © 2022 Crispy Kitchen Co., Ltd.', 'Copyright © 2024 Liyona Johny'),
    ('Design: <a rel="nofollow" href="https://www.tooplate.com/" target="_blank">Tooplate</a>', 'Design: Liyona Johny'),
    ('Design: <a rel="nofollow" href="https://www.tooplate.com/" target="_blank">Tooplate</a></p>', 'Design: Liyona Johny</p>'),
    ('121 Einstein Loop N, Bronx, NY 10475, United States', '1810 Crossroads vista drive, 27606, United States'),
    ('https://goo.gl/maps/wZVGLA7q64uC1s886', 'https://www.google.com/maps/search/?api=1&query=1810+Crossroads+Vista+Drive+27606+United+States'),
    ('News &amp; Events', 'Medication &amp; Health News &amp; Events'),
    ('News & Events', 'Medication & Health News & Events'),
    ('Healthy Lifestyle and happy living tips', 'Medication safety and healthy living tips'),
    ('How to make a healthy meal', 'How to use medicines safely'),
    ('Is Coconut good for you?', 'Are supplements right for you?'),
    ('Salmon Steak Noodle', 'Medication adherence essentials'),
    ('Making a healthy salad', 'Supporting long-term health with daily routines'),
    ('Tooplate Soup', 'Medication Guide'),
    ('Premium Steak', 'Vitality Support'),
    ('Seafood Set', 'Wellness Pack'),
    ('Burger Set', 'Recovery Care'),
    ('Healthy Soup', 'Balanced Health Plan'),
    ('Drug Recommender', 'Liyona Johny'),
    ('Drug Recommendation', 'Liyona Johny'),
    ('Drug recommendation', 'Liyona Johny'),
    ('#<link href="/static/css/tooplate-crispy-kitchen.css" rel="stylesheet">', '<link href="/static/css/tooplate-crispy-kitchen.css" rel="stylesheet">'),
]

count = 0
for path in list(root.rglob('*.html')) + list(root.rglob('*.css')):
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        continue
    new_text = text
    for old, new in replacements:
        new_text = new_text.replace(old, new)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        count += 1

print(f'Updated {count} files with the Liyona Johny branding and health/medication content.')
