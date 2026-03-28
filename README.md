# Polish Parliament Speech Processing

A data pipeline for collecting, cleaning, and structuring speeches from the Polish Parliament (Sejm) for further NLP analysis.

It advantages from the Sejm website database structure to obtain clean, structured speeches grouped by speaker via URL iterations and raw HTML processing.

### Fuctionality
- Extracts speeches and speaker names from HTML
- Removes irrelevant entries (non-MP speeches)
- Cleans text:
   - removes HTML tags
   - removes interruptions and annotations
   - removes extra whitespace and formatting artifacts
   - normalization of punctuation
- Groups speeches by speaker

### Pipeline stages

1. Download data (from official sources)

	`python data_download.py`

2. Process data (clean and normalize text)

	`python data_processing.py`

3. Analyze / export (prepare structured datasets)

	`python data_analysis.py`
