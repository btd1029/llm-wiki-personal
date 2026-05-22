#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Karpathy-style LLM Wiki Maintenance Script
Runs weekly to maintain wiki integrity and generate backlinks
"""

import os
import sys
import io
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class WikiMaintenance:
    def __init__(self, wiki_dir: str = "Wiki"):
        self.wiki_dir = Path(wiki_dir)
        self.log_file = self.wiki_dir / "MAINTENANCE_LOG.md"
        self.index_file = self.wiki_dir / "INDEX.md"
        self.backlinks_file = self.wiki_dir / "BACKLINKS.md"

        if not self.wiki_dir.exists():
            raise FileNotFoundError(f"Wiki directory not found: {wiki_dir}")

        self.pages = {}
        self.backlinks = defaultdict(set)
        self.links = defaultdict(set)
        self.stats = {
            "total_pages": 0,
            "total_links": 0,
            "orphan_pages": 0,
            "pages_with_backlinks": 0
        }

    def scan_wiki_pages(self) -> dict:
        """Scan all markdown files in wiki directory"""
        print("\n📖 Scanning wiki pages...")

        for md_file in self.wiki_dir.glob("*.md"):
            if md_file.name.startswith("MAINTENANCE") or md_file.name.startswith("INDEX") or md_file.name.startswith("BACKLINKS"):
                continue

            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract title from filename or first header
                title = md_file.stem
                if content.startswith("# "):
                    header_match = re.match(r"# (.+)", content.split('\n')[0])
                    if header_match:
                        title = header_match.group(1)

                self.pages[title] = {
                    "file": md_file.name,
                    "path": str(md_file),
                    "size": len(content),
                    "content": content,
                    "created": datetime.fromtimestamp(md_file.stat().st_ctime).strftime('%Y-%m-%d'),
                    "modified": datetime.fromtimestamp(md_file.stat().st_mtime).strftime('%Y-%m-%d'),
                }

                self.stats["total_pages"] += 1
                print(f"  ✓ {title} ({len(content)} bytes)")
            except Exception as e:
                print(f"  ✗ Error reading {md_file.name}: {e}")

        return self.pages

    def extract_links(self) -> dict:
        """Extract wikilinks [[page-name]] from all pages"""
        print("\n🔗 Extracting links...")

        link_pattern = re.compile(r'\[\[([^\]]+)\]\]')

        for page_title, page_data in self.pages.items():
            content = page_data["content"]
            found_links = link_pattern.findall(content)

            for linked_page in found_links:
                self.links[page_title].add(linked_page)
                self.backlinks[linked_page].add(page_title)
                self.stats["total_links"] += 1

        print(f"  ✓ Found {self.stats['total_links']} links")
        return self.links

    def find_orphan_pages(self) -> list:
        """Find pages with no inbound or outbound links"""
        print("\n🏜️  Finding orphan pages...")

        orphans = []
        for page_title, page_data in self.pages.items():
            inbound = len(self.backlinks.get(page_title, []))
            outbound = len(self.links.get(page_title, []))

            if inbound == 0 and outbound == 0:
                orphans.append({
                    "title": page_title,
                    "file": page_data["file"],
                    "size": page_data["size"]
                })

        self.stats["orphan_pages"] = len(orphans)

        if orphans:
            print(f"  ⚠️  Found {len(orphans)} orphan pages:")
            for orphan in orphans:
                print(f"     - {orphan['title']} ({orphan['size']} bytes)")
        else:
            print("  ✓ No orphan pages found")

        return orphans

    def generate_index(self) -> str:
        """Generate comprehensive wiki index"""
        print("\n📑 Generating index...")

        index_content = f"""# Wiki Index

**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Pages:** {self.stats['total_pages']}
**Total Links:** {self.stats['total_links']}
**Orphan Pages:** {self.stats['orphan_pages']}

---

## All Pages

| Page | File | Size | Links In | Links Out | Modified |
|------|------|------|----------|-----------|----------|
"""

        # Sort pages by title
        for page_title in sorted(self.pages.keys()):
            page = self.pages[page_title]
            inbound = len(self.backlinks.get(page_title, []))
            outbound = len(self.links.get(page_title, []))

            size_kb = page["size"] / 1024
            index_content += f"| {page_title} | {page['file']} | {size_kb:.1f}KB | {inbound} | {outbound} | {page['modified']} |\n"

        index_content += "\n---\n\n## Orphan Pages\n\n"

        orphans = self.find_orphan_pages()
        if orphans:
            for orphan in orphans:
                index_content += f"- **{orphan['title']}** - {orphan['file']} ({orphan['size']} bytes)\n"
            index_content += "\n> 💡 **Action:** Consider linking these pages or removing them if no longer needed.\n"
        else:
            index_content += "> ✅ No orphan pages - all pages are properly connected!\n"

        index_content += "\n---\n\n## Statistics\n\n"
        index_content += f"- Total Pages: {self.stats['total_pages']}\n"
        index_content += f"- Total Links: {self.stats['total_links']}\n"
        index_content += f"- Pages with Backlinks: {len([p for p in self.pages if self.backlinks.get(p)])}\n"

        return index_content

    def generate_backlinks(self) -> str:
        """Generate backlinks document"""
        print("\n🔙 Generating backlinks...")

        backlinks_content = f"""# Backlinks Map

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This document maps which pages link to which pages.

---

## Backlink Map

"""

        for page_title in sorted(self.pages.keys()):
            inbound = self.backlinks.get(page_title, set())
            outbound = self.links.get(page_title, set())

            if inbound or outbound:
                backlinks_content += f"\n### {page_title}\n\n"

                if outbound:
                    backlinks_content += f"**Links to:**\n"
                    for link in sorted(outbound):
                        exists = "✓" if link in self.pages else "✗"
                        backlinks_content += f"- {exists} [[{link}]]\n"

                if inbound:
                    backlinks_content += f"\n**Linked from:**\n"
                    for link in sorted(inbound):
                        backlinks_content += f"- {link}\n"

        return backlinks_content

    def append_log(self, status: str, details: dict):
        """Append entry to maintenance log"""
        print("\n📋 Updating maintenance log...")

        log_entry = f"""
## [{datetime.now().strftime('%Y-%m-%d %H:%M')}] Maintenance Run - {status}

**Summary:**
- Total Pages: {self.stats['total_pages']}
- Total Links: {self.stats['total_links']}
- Orphan Pages: {self.stats['orphan_pages']}
- Pages with Backlinks: {len([p for p in self.pages if self.backlinks.get(p)])}

**Details:**
- Index: {'Generated' if details.get('index_generated') else 'Skipped'}
- Backlinks Map: {'Generated' if details.get('backlinks_generated') else 'Skipped'}
- Scan Time: {details.get('duration', 'N/A')}

---
"""

        # Read existing log or create new
        if self.log_file.exists():
            with open(self.log_file, 'r', encoding='utf-8') as f:
                existing = f.read()
            log_content = existing + log_entry
        else:
            log_content = f"# Wiki Maintenance Log\n\n{log_entry}"

        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(log_content)

        print(f"  ✓ Log updated: {self.log_file}")

    def run(self):
        """Run full maintenance cycle"""
        print("\n" + "="*70)
        print("🚀 WIKI MAINTENANCE - Karpathy-style")
        print("="*70)

        start_time = datetime.now()

        try:
            # 1. Scan all pages
            self.scan_wiki_pages()

            # 2. Extract links
            self.extract_links()

            # 3. Find orphans
            orphans = self.find_orphan_pages()

            # 4. Generate index
            index = self.generate_index()
            with open(self.index_file, 'w', encoding='utf-8') as f:
                f.write(index)
            print(f"  ✓ Index saved: {self.index_file}")

            # 5. Generate backlinks
            backlinks = self.generate_backlinks()
            with open(self.backlinks_file, 'w', encoding='utf-8') as f:
                f.write(backlinks)
            print(f"  ✓ Backlinks saved: {self.backlinks_file}")

            # 6. Update log
            duration = (datetime.now() - start_time).total_seconds()
            self.append_log("✅ SUCCESS", {
                "index_generated": True,
                "backlinks_generated": True,
                "duration": f"{duration:.2f}s"
            })

            # Print summary
            print("\n" + "="*70)
            print("✅ MAINTENANCE COMPLETE")
            print("="*70)
            print(f"\n📊 Summary:")
            print(f"  • Total Pages: {self.stats['total_pages']}")
            print(f"  • Total Links: {self.stats['total_links']}")
            print(f"  • Orphan Pages: {self.stats['orphan_pages']}")
            print(f"  • Duration: {duration:.2f} seconds")
            print(f"\n📄 Generated:")
            print(f"  • {self.index_file.name}")
            print(f"  • {self.backlinks_file.name}")
            print(f"  • {self.log_file.name}")
            print("\n")

            return 0

        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            self.append_log("❌ FAILED", {"error": str(e)})
            return 1

def main():
    wiki_dir = Path("Wiki")

    if not wiki_dir.exists():
        print(f"❌ Wiki directory not found: {wiki_dir}")
        return 1

    maintenance = WikiMaintenance(str(wiki_dir))
    return maintenance.run()

if __name__ == "__main__":
    sys.exit(main())
