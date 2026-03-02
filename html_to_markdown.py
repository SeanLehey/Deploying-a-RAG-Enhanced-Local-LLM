import re
from pathlib import Path
from markdownify import markdownify as md
from bs4 import BeautifulSoup

source_dir = Path(r"C:\Users\Temporary\Documents\RAGProject\godot-docs-html-stable")
output_dir = Path(r"C:\Users\Temporary\Documents\RAGProject\CleanedData")

output_dir.mkdir(parents=True, exist_ok=True)

html_files = list(source_dir.rglob("*.html"))
total = len(html_files)

for i, html_file in enumerate(html_files, start=1):
    html_content = html_file.read_text(encoding="utf-8", errors="ignore")

    soup = BeautifulSoup(html_content, "html.parser")

    main = soup.find("div", {"role": "main"})

    if main is None:
        print(f"WARNING {i} of {total} - no main content found, skipping: {html_file.name}")
        continue

    # Remove heading anchor links
    for tag in main.find_all("a", class_="headerlink"):
        tag.decompose()

    # Remove inline permalink emoji anchors (🔗)
    for tag in main.find_all("a"):
        if tag.get_text().strip() == "🔗":
            tag.decompose()

    # Remove footer (prev/next navigation and copyright)
    for tag in main.find_all("footer"):
        tag.decompose()

    # In language switcher blocks, remove all non-GDScript panels and tab buttons
    for tabs in main.find_all("div", class_="sphinx-tabs"):
        for panel in tabs.find_all("div", class_="sphinx-tabs-panel"):
            if not panel.find("div", class_="highlight-gdscript"):
                panel.decompose()
        for button in tabs.find_all("button", class_="sphinx-tabs-tab"):
            button.decompose()

    markdown_content = md(str(main), heading_style="ATX")

    # Remove image references
    markdown_content = re.sub(r'!\[.*?\]\(.*?\)\n?', '', markdown_content)

    output_file = output_dir / html_file.with_suffix(".md").name
    output_file.write_text(markdown_content, encoding="utf-8")
    print(f"Converting {i} of {total}: {html_file.name}")


print("Done!")
