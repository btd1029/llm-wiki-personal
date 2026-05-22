# Wiki Maintenance Setup - Karpathy Style

## ✅ Setup Complete!

You now have a fully automated **Karpathy-style Wiki maintenance system** that runs weekly.

---

## 📅 Schedule

| Item | Value |
|------|-------|
| **Task Name** | LLM-Wiki-Weekly-Maintenance |
| **Frequency** | Weekly |
| **Day** | Sunday |
| **Time** | 10:00 AM |
| **Status** | Ready (Active) |

---

## 🤖 What It Does

Every Sunday at 10:00 AM, the system automatically:

### 1. **INDEX.md Generation** 📑
Creates a comprehensive catalog of all wiki pages:
- Lists all pages with metadata (file size, links in/out)
- Shows orphan pages (pages with no connections)
- Provides statistics

**Location:** `Wiki/INDEX.md`

### 2. **BACKLINKS.md Generation** 🔙
Maps bidirectional links between pages:
- Shows which pages each article links to
- Shows which pages link back to each article
- Marks broken links with ✗

**Location:** `Wiki/BACKLINKS.md`

### 3. **Orphan Page Detection** 🏜️
Identifies pages that:
- Have no inbound links (nobody links to them)
- Have no outbound links (they don't link to anything)
- Suggests actions for these pages

### 4. **Maintenance Log** 📋
Records every maintenance run:
- Timestamp
- Statistics (page count, link count, orphan count)
- Duration
- Status (success/failure)

**Location:** `Wiki/MAINTENANCE_LOG.md`

---

## 📊 Current Wiki Stats

From the latest maintenance run:

```
Total Pages: 5
Total Links: 49
Orphan Pages: 0
Pages with Backlinks: 0
```

### Your Pages:
1. 18の文献が暴いた、努力と才能の不都合な事実【行動遺伝学×経済学】
2. Software Fundamentals Matter More Than Ever — Matt Pocock
3. なぜ港区女子はみんな同じ見た目なのか【進化心理学×行動経済学】
4. 無題のファイル
5. 男女の友情は、なぜ「成立する」のに永遠に疑われ続けるのか【言語哲学 × 進化心理学】

---

## 🔍 How to Use Generated Files

### INDEX.md
Read this to:
- See all pages at a glance
- Find orphan pages
- Check statistics
- Identify pages that might need updating

### BACKLINKS.md
Read this to:
- Understand which concepts connect
- Find missing wiki pages (marked with ✗)
- Plan new pages to create
- See the knowledge graph

### MAINTENANCE_LOG.md
Read this to:
- Track maintenance history
- Check when the wiki was last updated
- See how the wiki has grown over time

---

## 🛠️ Testing the Script

To run the maintenance script manually at any time:

```powershell
cd C:\Users\bitet\llm-wiki-personal
python wiki-maintenance.py
```

Expected output:
```
======================================================================
🚀 WIKI MAINTENANCE - Karpathy-style
======================================================================
...
✅ MAINTENANCE COMPLETE
======================================================================
```

---

## 📝 Next Steps

### 1. Review the Generated Files
- Read `Wiki/INDEX.md` to see your wiki structure
- Read `Wiki/BACKLINKS.md` to understand connections
- Check `Wiki/MAINTENANCE_LOG.md` for history

### 2. Link Your Pages
The system detected 49 links between your pages (marked with `[[page-name]]`).

Some links point to pages that don't exist yet (marked with ✗ in BACKLINKS.md).

Consider creating these pages:
- [[行動遺伝学]] (Behavioral Genetics)
- [[進化心理学]] (Evolutionary Psychology)
- [[機械学習]] (Machine Learning)
- [[ソフトウェア設計]] (Software Design)

### 3. Monitor Automatically
The maintenance runs every Sunday at 10:00 AM. Check the log file (`Wiki/MAINTENANCE_LOG.md`) to confirm it's running.

---

## ⚙️ How It Works Behind the Scenes

### Daily Flow:
```
8:00 AM   → simple-ingest.bat processes raw/*.md
           → personal-ingest.py generates wiki pages

20:00 PM  → simple-ingest.bat processes raw/*.md
           → personal-ingest.py generates wiki pages

Every Sunday 10:00 AM → wiki-maintenance.py runs
                        ├─ Scans all wiki pages
                        ├─ Extracts [[links]]
                        ├─ Generates INDEX.md
                        ├─ Generates BACKLINKS.md
                        └─ Logs the run
```

### Integration Points:

**personal-ingest.py** (Run daily at 8 AM & 8 PM)
```
raw/*.md → Read by Claude → Extract summary/concepts
         → Generate wiki pages
```

**wiki-maintenance.py** (Run weekly on Sunday)
```
Wiki/*.md → Scan all files → Extract all [[links]]
          → Analyze connections → Generate index
          → Map backlinks → Log results
```

---

## 🔧 Customization

### Change the Schedule

If you want maintenance to run at a different time, edit this file:
`register-weekly-maintenance.ps1`

Change this line:
```powershell
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At "10:00:00"
```

Examples:
```powershell
# Monday at 2:00 AM
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At "02:00:00"

# Every day at 11:00 PM
$trigger = New-ScheduledTaskTrigger -Daily -At "23:00:00"

# Every 4 days at 6:00 AM
$trigger = New-ScheduledTaskTrigger -Once -At "06:00:00" -RepetitionInterval (New-TimeSpan -Days 4) -RepetitionDuration (New-TimeSpan -Days 3650)
```

Then re-register:
```powershell
cd C:\Users\bitet\llm-wiki-personal
& '.\register-weekly-maintenance.ps1'
```

---

## 📚 Architecture Summary

You now have a **Karpathy-style LLM Wiki** with three layers:

```
Layer 1: RAW (你 curate, immutable)
  ├─ raw/articles/
  ├─ raw/papers/
  └─ raw/assets/

Layer 2: WIKI (LLM generates, you read)
  ├─ personal-ingest.py creates new pages daily
  ├─ Each article touches 10-15 pages
  └─ Pages are connected via [[links]]

Layer 3: MAINTENANCE (Automated weekly)
  ├─ wiki-maintenance.py scans connections
  ├─ Generates INDEX.md (what we have)
  ├─ Generates BACKLINKS.md (how it connects)
  └─ Appends to MAINTENANCE_LOG.md
```

---

## ✨ What's Happening

1. **Continuous Ingest** (8 AM, 8 PM daily)
   - New articles from `raw/` get processed
   - Claude generates wiki pages automatically
   - Related pages are updated

2. **Passive Maintenance** (Sunday 10 AM weekly)
   - All wiki files are scanned
   - Links are mapped and verified
   - Index is regenerated
   - Log is updated

3. **You Stay in Control**
   - You curate sources (put articles in `raw/`)
   - You read the wiki (browse in Obsidian)
   - You ask questions to the LLM
   - You decide what's important

---

## 🚀 You're All Set!

Your wiki is now ready for Karpathy-style knowledge management:

- ✅ Daily automatic ingestion at 8 AM & 8 PM
- ✅ Weekly maintenance every Sunday 10 AM
- ✅ Automatic index and backlink generation
- ✅ Full operation logging
- ✅ Ready for continuous learning

Keep adding articles to `raw/` and let the system grow your knowledge base automatically!

---

**Last Updated:** 2026-05-17
