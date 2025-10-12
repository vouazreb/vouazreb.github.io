import bibtexparser
from bibtexparser.customization import convert_to_unicode

# Input/output
bib_file = "assets/bibliography/papers.bib"
output_md = "content/papers.md"

# Load the .bib file
with open(bib_file, "r", encoding="utf-8") as f:
    bib_database = bibtexparser.load(f)

# Sort entries by year descending
entries = sorted(
    bib_database.entries, key=lambda e: int(e.get("year", 0)), reverse=True
)

md_lines = ["+++\ntitle = \"Papers\"\ntemplate = \"page.html\"\n+++"]

for entry in entries:
    # Title
    md_lines.append("<div class=\"bib_entry\">")
    title = entry.get("title", "").replace("{", "").replace("}", "")
    md_lines.append(f"<h3 class=\"title\">{title}</h3>\n")

    # Authors
    authors = entry.get("author", "").replace("\n", " ")
    md_lines.append(f" <div class=\"authors\">{authors}</div>\n")

    # Journal info
    journal = entry.get("journal", "")
    volume = entry.get("volume", "")
    pages = entry.get("pages", "")
    year = entry.get("year", "")
    journal_info = ", ".join(filter(None, [journal, volume, pages, year]))

    # If no journal, check for preprint
    if not journal:
        journal_info = entry.get("number", "")


    # Link (DOI preferred, fallback to URL)
    doi = entry.get("doi")
    url = entry.get("url")
    link = doi and f"https://doi.org/{doi}" or url or ""

    # Markdown link
    if link:
        md_lines.append(f"<div class=\"journal\"><a href=\"{link}\">{journal_info}</a></div>\n")
    else:
        md_lines.append(f"<div class=\"journal\"><a>{journal_info}</a></div>\n")

    # Add spacing between entries
    md_lines.append("</div>\n")

# Write Markdown file
with open(output_md, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))
