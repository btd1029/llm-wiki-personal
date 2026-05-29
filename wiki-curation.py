#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wiki-curation.py — Weekly auto-curation for llm-wiki-personal

Features:
  1. 関連記事の自動提案 (related articles via cosine similarity)
  2. 学習パス（基礎→応用）(learning path via topological sort)
  3. 必須前提知識の提案 (prerequisite suggestions)
  4. 応用分野の提案 (application domain suggestions)

Usage:
  python wiki-curation.py [--wiki-dir Wiki] [--cache wiki-curation-cache.json] [--dry-run]
"""

import os
import sys
import io
import json
import re
import math
import argparse
import logging
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Optional

import requests

# UTF-8 stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5"
EMBED_ENDPOINT = f"{OLLAMA_URL}/api/embeddings"

SKIP_FILES = {
    "BACKLINKS.md",
    "MAINTENANCE_LOG.md",
    "index.md",
    "NOTION_PRICING.md",
    "NOTION_VS_OBSIDIAN.md",
}

PREREQ_SECTION_RE = re.compile(
    r"##\s+前提となる知識\s*\n(.*?)(?=\n##|\Z)", re.DOTALL
)
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")

AUTO_CURATION_START = "<!-- AUTO-CURATION-START -->"
AUTO_CURATION_END = "<!-- AUTO-CURATION-END -->"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def cosine_similarity(a: list, b: list) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def get_embedding(text: str) -> Optional[list]:
    """Fetch embedding vector from Ollama."""
    try:
        resp = requests.post(
            EMBED_ENDPOINT,
            json={"model": OLLAMA_MODEL, "prompt": text},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("embedding")
    except requests.RequestException as e:
        log.error(f"Ollama embedding request failed: {e}")
        return None


def extract_prereqs(content: str) -> list:
    """前提となる知識 セクションから [[wikilinks]] を抽出する"""
    match = PREREQ_SECTION_RE.search(content)
    if not match:
        return []
    section_text = match.group(1)
    return WIKILINK_RE.findall(section_text)


def extract_title(content: str, fallback: str) -> str:
    """Extract first H1 heading, or use filename as fallback."""
    for line in content.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def should_skip(filename: str) -> bool:
    """Return True for system/meta files that should not be curated."""
    if filename in SKIP_FILES:
        return True
    # Skip files that are all-uppercase names (system docs)
    stem = Path(filename).stem
    if stem == stem.upper() and len(stem) > 2:
        return True
    return False


# ---------------------------------------------------------------------------
# Topological sort helpers
# ---------------------------------------------------------------------------

def topological_sort(graph: dict, start_nodes: list) -> list:
    """
    Return nodes reachable from start_nodes in topological order
    (most-basic / no-prereq first, start_nodes last).
    graph: article_name -> list of its prerequisites (article_names)
    """
    visited_order = []
    seen = set()
    temp = set()

    def visit(node: str):
        if node in temp:
            return  # cycle — skip
        if node in seen:
            return
        temp.add(node)
        for prereq in graph.get(node, []):
            visit(prereq)
        temp.discard(node)
        seen.add(node)
        visited_order.append(node)

    for node in start_nodes:
        visit(node)

    return visited_order  # leaves (most basic) come first


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------

def load_cache(cache_path: Path) -> dict:
    if cache_path.exists():
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            log.warning(f"Failed to load cache: {e}. Starting fresh.")
    return {}


def save_cache(cache: dict, cache_path: Path):
    try:
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        log.error(f"Failed to save cache: {e}")


# ---------------------------------------------------------------------------
# Core curation logic
# ---------------------------------------------------------------------------

class WikiCurator:
    def __init__(self, wiki_dir: Path, cache_path: Path, dry_run: bool = False):
        self.wiki_dir = wiki_dir
        self.cache_path = cache_path
        self.dry_run = dry_run

        # article_name (stem without .md) -> {path, content, title, prereqs, embedding}
        self.articles: dict = {}
        self.cache: dict = load_cache(cache_path)

    # ------------------------------------------------------------------
    def load_articles(self):
        log.info(f"Loading articles from {self.wiki_dir} ...")
        md_files = sorted(self.wiki_dir.glob("*.md"))
        loaded = 0
        skipped = 0
        for md_path in md_files:
            if should_skip(md_path.name):
                log.debug(f"  Skip: {md_path.name}")
                skipped += 1
                continue
            try:
                content = md_path.read_text(encoding="utf-8")
            except Exception as e:
                log.warning(f"  Cannot read {md_path.name}: {e}")
                skipped += 1
                continue

            stem = md_path.stem
            title = extract_title(content, stem)
            prereqs = extract_prereqs(content)

            self.articles[stem] = {
                "path": md_path,
                "content": content,
                "title": title,
                "prereqs": prereqs,  # list of wikilink names (may not exist as files)
                "embedding": None,
            }
            loaded += 1

        log.info(f"  Loaded {loaded} articles, skipped {skipped}.")

    # ------------------------------------------------------------------
    def build_embeddings(self):
        log.info("Building embeddings (using cache where possible) ...")
        total = len(self.articles)
        for i, (stem, art) in enumerate(self.articles.items(), 1):
            content = art["content"]
            # Cache key based on stem + content hash
            content_hash = str(hash(content))
            cache_key = f"{stem}::{content_hash}"

            if cache_key in self.cache:
                art["embedding"] = self.cache[cache_key]
                log.debug(f"  [{i}/{total}] Cache hit: {stem}")
            else:
                log.info(f"  [{i}/{total}] Embedding: {stem} ...")
                # Use title + first 2000 chars of content for embedding
                embed_text = f"{art['title']}\n\n{content[:2000]}"
                vec = get_embedding(embed_text)
                if vec:
                    art["embedding"] = vec
                    self.cache[cache_key] = vec
                else:
                    log.warning(f"  Failed to get embedding for {stem}")

        save_cache(self.cache, self.cache_path)
        log.info("  Embeddings done.")

    # ------------------------------------------------------------------
    def compute_similarities(self) -> dict:
        """For each article, compute sorted list of (other_stem, similarity)."""
        log.info("Computing pairwise cosine similarities ...")
        stems = [s for s, a in self.articles.items() if a["embedding"]]
        vecs = {s: self.articles[s]["embedding"] for s in stems}

        sims: dict = {}
        n = len(stems)
        for i, s1 in enumerate(stems):
            row = []
            for s2 in stems:
                if s1 == s2:
                    continue
                sim = cosine_similarity(vecs[s1], vecs[s2])
                row.append((s2, sim))
            row.sort(key=lambda x: x[1], reverse=True)
            sims[s1] = row
            if (i + 1) % 10 == 0 or (i + 1) == n:
                log.info(f"  {i+1}/{n} articles processed")

        return sims

    # ------------------------------------------------------------------
    def build_prereq_graph(self) -> dict:
        """
        Build graph: article_stem -> list of prerequisite article_stems.
        Only includes prereqs that actually exist as wiki articles.
        """
        # Build a lookup: title/stem variations -> canonical stem
        lookup: dict = {}
        for stem, art in self.articles.items():
            lookup[stem] = stem
            title_key = art["title"].strip()
            if title_key:
                lookup[title_key] = stem

        graph: dict = {}
        for stem, art in self.articles.items():
            resolved = []
            for prereq_name in art["prereqs"]:
                if prereq_name in lookup:
                    resolved.append(lookup[prereq_name])
                else:
                    # Try partial match
                    candidates = [
                        k for k in lookup
                        if prereq_name in k or k in prereq_name
                    ]
                    if candidates:
                        resolved.append(lookup[candidates[0]])
                    # else: external concept not in wiki — skip
            graph[stem] = resolved

        return graph

    # ------------------------------------------------------------------
    def curate_article(
        self,
        stem: str,
        sims: dict,
        prereq_graph: dict,
        reverse_prereq: dict,
    ) -> str:
        """Generate the AUTO-CURATION block for one article."""
        art = self.articles[stem]

        # ---- 1. 関連記事 ------------------------------------------------
        top_related = sims.get(stem, [])[:5]
        related_lines = []
        for other_stem, score in top_related:
            other_art = self.articles[other_stem]
            related_lines.append(
                f"- [[{other_art['title']}]] (類似度: {score:.2f})"
            )

        # ---- 2. 学習パス -----------------------------------------------
        # Topological sort of prereq subgraph reachable from this article
        learning_path = topological_sort(prereq_graph, [stem])
        # learning_path: most-basic first, this article last
        path_lines = []
        for i, node in enumerate(learning_path):
            node_art = self.articles.get(node)
            node_title = node_art["title"] if node_art else node
            marker = " ← 本記事" if node == stem else ""
            path_lines.append(f"{i+1}. [[{node_title}]]{marker}")

        # ---- 3. 必須前提知識の提案 -------------------------------------
        # Common prereqs among the top similar articles
        prereq_counter: dict = defaultdict(int)
        top_neighbors = [s for s, _ in sims.get(stem, [])[:5]]
        for neighbor in top_neighbors:
            for prereq in prereq_graph.get(neighbor, []):
                if prereq != stem:
                    prereq_counter[prereq] += 1

        existing_prereqs = set(prereq_graph.get(stem, []))

        suggested_prereqs = sorted(
            prereq_counter.items(), key=lambda x: x[1], reverse=True
        )
        prereq_lines = []
        for prereq_stem, count in suggested_prereqs[:5]:
            prereq_art = self.articles.get(prereq_stem)
            prereq_title = prereq_art["title"] if prereq_art else prereq_stem
            already = " ✓" if prereq_stem in existing_prereqs else ""
            prereq_lines.append(
                f"- [[{prereq_title}]] ({count}件の関連記事が参照){already}"
            )

        # ---- 4. 応用分野の提案 -----------------------------------------
        # Articles that list THIS article as a prerequisite (reverse prereq)
        applications_direct = reverse_prereq.get(stem, [])

        # Also: top similar articles that are not prerequisites of this article
        applications_similar = [
            s for s, _ in sims.get(stem, [])[:8]
            if s not in applications_direct and s not in existing_prereqs
        ][:3]

        app_lines = []
        for app_stem in applications_direct[:5]:
            app_art = self.articles.get(app_stem)
            app_title = app_art["title"] if app_art else app_stem
            app_lines.append(f"- [[{app_title}]] (この記事を前提知識として参照)")
        for app_stem in applications_similar:
            app_art = self.articles.get(app_stem)
            app_title = app_art["title"] if app_art else app_stem
            app_lines.append(f"- [[{app_title}]] (関連する応用分野)")

        # ---- Assemble block --------------------------------------------
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        lines = [
            AUTO_CURATION_START,
            f"<!-- 自動生成: {now} -->",
            "",
            "## \U0001f517 関連記事",
            "",
        ]
        if related_lines:
            lines.extend(related_lines)
        else:
            lines.append("*関連記事が見つかりませんでした*")

        lines += ["", "## \U0001f4da 学習パス", ""]
        if len(learning_path) > 1:
            lines.extend(path_lines)
        elif len(learning_path) == 1:
            lines.append(f"1. [[{art['title']}]] ← 本記事（前提知識なし）")
        else:
            lines.append("*学習パスを構築できませんでした*")

        lines += ["", "## \U0001f4cb 必須前提知識の提案", ""]
        if prereq_lines:
            lines.extend(prereq_lines)
        else:
            lines.append("*提案できる前提知識が見つかりませんでした*")

        lines += ["", "## \U0001f680 応用分野", ""]
        if app_lines:
            lines.extend(app_lines)
        else:
            lines.append("*応用分野が見つかりませんでした*")

        lines += ["", AUTO_CURATION_END]
        return "\n".join(lines)

    # ------------------------------------------------------------------
    def write_curation(self, stem: str, curation_block: str):
        """Append or replace the AUTO-CURATION section in the .md file."""
        art = self.articles[stem]
        content = art["content"]
        path: Path = art["path"]

        if AUTO_CURATION_START in content and AUTO_CURATION_END in content:
            # Replace existing block
            pattern = re.compile(
                re.escape(AUTO_CURATION_START) + r".*?" + re.escape(AUTO_CURATION_END),
                re.DOTALL,
            )
            new_content = pattern.sub(curation_block, content)
        else:
            # Strip trailing whitespace and append
            new_content = content.rstrip() + "\n\n" + curation_block + "\n"

        if self.dry_run:
            log.info(f"  [DRY RUN] Would write curation to {path.name}")
        else:
            path.write_text(new_content, encoding="utf-8")
            log.info(f"  Written: {path.name}")

    # ------------------------------------------------------------------
    def run(self):
        log.info("=== Wiki Auto-Curation Start ===")
        self.load_articles()

        if not self.articles:
            log.error("No articles found. Exiting.")
            return

        self.build_embeddings()

        sims = self.compute_similarities()
        prereq_graph = self.build_prereq_graph()

        # Build reverse prereq index: stem -> [articles that have stem as prereq]
        reverse_prereq: dict = defaultdict(list)
        for stem, prereqs in prereq_graph.items():
            for prereq in prereqs:
                reverse_prereq[prereq].append(stem)

        log.info("Generating and writing curation blocks ...")
        total = len(self.articles)
        for i, stem in enumerate(sorted(self.articles.keys()), 1):
            if self.articles[stem]["embedding"] is None:
                log.warning(f"  [{i}/{total}] Skipping (no embedding): {stem}")
                continue
            log.info(f"  [{i}/{total}] Curating: {stem}")
            try:
                block = self.curate_article(stem, sims, prereq_graph, reverse_prereq)
                self.write_curation(stem, block)
            except Exception as e:
                log.error(f"  Error curating {stem}: {e}", exc_info=True)

        log.info("=== Wiki Auto-Curation Complete ===")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Weekly wiki auto-curation using Ollama embeddings"
    )
    parser.add_argument(
        "--wiki-dir",
        default="Wiki",
        help="Path to the Wiki directory (default: Wiki)",
    )
    parser.add_argument(
        "--cache",
        default="wiki-curation-cache.json",
        help="Path to the embedding cache file (default: wiki-curation-cache.json)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and compute but do not write changes to .md files",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    wiki_dir = (
        Path(args.wiki_dir)
        if Path(args.wiki_dir).is_absolute()
        else script_dir / args.wiki_dir
    )
    cache_path = (
        Path(args.cache)
        if Path(args.cache).is_absolute()
        else script_dir / args.cache
    )

    if not wiki_dir.exists():
        log.error(f"Wiki directory not found: {wiki_dir}")
        sys.exit(1)

    curator = WikiCurator(wiki_dir=wiki_dir, cache_path=cache_path, dry_run=args.dry_run)
    curator.run()


if __name__ == "__main__":
    main()
