# AI IN ACTION Copilot

RAG chatbot cho chương trình AI Thực Chiến - Batch 02, VinUniversity.

## Project Structure

```
AI_IN_ACTION_Copilot/
├── data/
│   ├── raw_text/          # Text files extracted from slides
│   ├── processed/         # Chunks and manifest
│   └── vectorstore/       # ChromaDB vector database
├── src/
│   ├── dataset/           # Dataset ingestion pipeline
│   │   ├── text_loader.py
│   │   ├── text_cleaner.py
│   │   ├── chunker.py
│   │   ├── build_index.py
│   │   └── inspect_index.py
│   └── retriever.py       # Course content retriever
└── requirements.txt
```

## Build Knowledge Base

1. Put text files into `data/raw_text/`:
   ```
   data/raw_text/
   ├── day1.txt
   ├── day2.txt
   ├── day3.txt
   ├── day4.txt
   ├── day5.txt
   └── day6.txt
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the build pipeline:
   ```bash
   python -m src.dataset.build_index
   ```

4. Inspect the index:
   ```bash
   python -m src.dataset.inspect_index
   ```

## Pipeline

```
Text → Clean → Chunk → Embedding → ChromaDB
```

### Pipeline Steps

1. **Text Loader**: Read .txt files from `data/raw_text/`, extract metadata (day, source_file)
2. **Text Cleaner**: Normalize whitespace, preserve headings and Vietnamese text
3. **Chunker**: Split text into chunks (1200 chars with 200 chars overlap), detect sections
4. **Build Index**: Generate embeddings using `paraphrase-multilingual-MiniLM-L12-v2`, store in ChromaDB

## Usage

### Build Index

```bash
# Basic usage
python -m src.dataset.build_index

# Custom directory and rebuild
python -m src.dataset.build_index --raw-dir data/raw_text --rebuild
```

### Search Content

```python
from src.retriever import CourseRetriever

retriever = CourseRetriever()
results = retriever.search("Day 5 cần nộp gì?", top_k=4)

for result in results:
    print(f"Source: {result['source_file']}")
    print(f"Section: {result['section']}")
    print(f"Score: {result['score']:.4f}")
    print(f"Content: {result['content'][:200]}...")
```

### Inspect Index

```bash
python -m src.dataset.inspect_index
```

## Output Files

After building, you'll have:

- `data/processed/chunks.jsonl` - All text chunks with metadata
- `data/processed/manifest.json` - Index statistics
- `data/vectorstore/chroma/` - ChromaDB vector database

## Dependencies

- chromadb >= 0.4.0
- sentence-transformers >= 2.2.0
- python-dotenv >= 1.0.0

## Notes

- Vietnamese text is fully supported
- Idempotent: Running build_index multiple times won't create duplicates
- Use `--rebuild` flag to force rebuild the vector index
