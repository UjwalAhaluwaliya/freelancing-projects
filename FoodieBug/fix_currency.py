import os, glob

count = 0
for p in glob.glob('app/templates/**/*.html', recursive=True):
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    if '$' in content:
        content = content.replace('$', '₹')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Updated {p}")
print(f"Total files updated: {count}")
