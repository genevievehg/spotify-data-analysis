# Spotify Listening Data Pipeline

An ETL/ELT data engineering project for extracting, transforming and analysing my personal Spotify listening history.

The project combines Spotify listening-history data with metadata retrieved from the Spotify Web API, then transforms the data into a structured format suitable for analysis.

## Project Goals

The aim of this project is to build a small end-to-end data pipeline that demonstrates:

* Extracting data from files and the Spotify Web API
* Working with semi-structured JSON data
* Cleaning and transforming data with Python and Pandas
* Handling API rate limits and caching
* Designing relational data structures
* Storing data in Parquet format
* Building reproducible data-processing workflows
* Testing data transformation and extraction functions

## Data Pipeline

The pipeline broadly follows:

```text
Spotify Listening History
          │
          ▼
      Extraction
          │
          ├──────────────► Spotify Web API
          │                       │
          │                       ▼
          │                Track / Artist Metadata
          │                       │
          ▼                       ▼
       Raw Data ─────────► Cached API Data
                                  │
                                  ▼
                            Transformation
                                  │
                                  ▼
                         Structured Data
                                  │
                                  ▼
                              Analysis
```

## Data Sources

### Spotify Listening History

Spotify provides a user's listening history as JSON data. The raw history contains information such as:

* Track name
* Artist name
* Album name
* Track URI
* Timestamp
* Listening duration
* Platform
* Country
* Playback information

The raw data is retained separately from transformed data so that the transformations can be reproduced.

### Spotify Web API

The Spotify Web API is used to enrich the listening history with additional metadata.

Examples include:

* Track metadata
* Artist metadata
* Album metadata
* Artist URIs

API responses are cached locally to avoid repeatedly requesting the same information.

## Technologies

* **Python**
* **Pandas**
* **PyArrow / Parquet**
* **Spotify Web API**
* **Spotipy**
* **pytest**
* **Git / GitHub**

## Project Structure

```text
spotify-data-pipeline/
│
├── data/
│   ├── raw/
│   │   ├── spotify_history/
│   │   └── spotify_api/
│   │
│   ├── reference/
│   │
│   └── processed/
│
├── logs/
│
├── src/
│   ├── extract/
│   ├── transform/
│   ├── load/
│   └── utils/
│
├── tests/
│
├── .gitignore
├── requirements.txt
└── README.md
```

The exact structure may evolve as the project develops.

## API Extraction

The project uses `Spotipy` to interact with the Spotify Web API.

Authentication uses Spotify's PKCE flow, with credentials stored outside the repository.

API responses are cached locally so that metadata does not need to be requested again for tracks that have already been processed.

For example, track metadata is stored in:

```text
data/raw/spotify_api/cached_track_metadata.parquet
```

The extraction process also saves progress periodically rather than waiting until the entire dataset has been processed.

This makes the pipeline more resilient to interruptions and API limitations.

## Handling API Rate Limits

Spotify API requests are subject to rate limits.

The pipeline therefore:

* Caches previously retrieved metadata
* Avoids requesting duplicate track URIs
* Processes tracks in batches
* Saves extraction progress periodically
* Records extraction activity in log files
* Handles API rate-limit responses rather than repeatedly retrying requests

This is particularly important when processing a large listening history.

## Limiting API Requests

To reduce the number of Spotify API calls, the pipeline only retrieves additional API metadata for tracks that meet the project's analysis requirements. In particular, it prioritises the user's most frequently played tracks rather than requesting metadata for every track in the listening history.

This reduces unnecessary API requests and helps minimise the impact of Spotify's rate limits while still providing sufficient data for analysis.

The listening history itself is retained in full, so limiting API enrichment does not remove the underlying listening records.

## Transformation

The transformation stage converts the raw API and listening-history data into cleaner, structured datasets.

Transformations include:

* Selecting relevant fields
* Renaming columns
* Converting data types
* Handling missing values
* Extracting nested values from API responses
* Converting timestamps into useful date/time fields
* Removing duplicate records
* Creating relationships between tracks, albums and artists

The data is stored in Parquet to provide a compact, columnar format that is convenient for analytical workloads.

## Data Model

The project is being designed around a relational/analytical model rather than keeping all Spotify information in a single denormalised table.

Potential entities include:

```text
                ┌─────────────┐
                │   Artists   │
                └──────┬──────┘
                       │
                       │
                ┌──────▼──────┐
                │    Track    │
                └──────┬──────┘
                       │
                ┌──────▼──────┐
                │    Album    │
                └─────────────┘

                       ▲
                       │
                ┌──────┴──────┐
                │   Listening │
                │    Events   │
                └─────────────┘
```

A separate artist-track relationship can be used because a track may have multiple artists.

## Testing

The project uses `pytest` to test individual pipeline components.

Tests cover areas such as:

* Extracting Spotify data
* Processing API responses
* Handling missing values
* Filtering unique Spotify URIs
* Transforming API results into DataFrames
* Handling different API response structures

The aim is to test the transformation logic independently from the live Spotify API wherever possible.

## Logging

Pipeline activity is recorded using Python's `logging` module.

Logs are stored in:

```text
logs/
```

Logging is used to record information such as:

* Extraction progress
* Number of records processed
* API requests
* Errors
* Rate-limit responses
* Pipeline failures

## Setup

Clone the repository:

```bash
git clone <repository-url>
cd spotify-data-pipeline
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Spotify API credentials

Create a Spotify Developer application and configure the required credentials.

Store credentials as environment variables rather than committing them to the repository.

For example:

```text
SPOTIFY_CLIENT_ID=...
SPOTIFY_CLIENT_SECRET=...
```

The required Spotify redirect URI should also be configured for the application.

## Running the Pipeline

The pipeline is currently being developed incrementally, with extraction, transformation and loading components being built and tested separately.

A typical workflow is:

```text
1. Load Spotify listening history
2. Identify unique tracks
3. Extract metadata from the Spotify API
4. Cache API responses
5. Transform raw data
6. Save structured datasets as Parquet
7. Analyse the resulting data
```

## Future Improvements

Possible next steps include:

* [ ] Complete the transformation pipeline
* [ ] Build the final dimensional data model
* [ ] Add additional Spotify API metadata
* [ ] Load transformed data into PostgreSQL
* [ ] Automate the pipeline
* [ ] Add more comprehensive unit tests
* [ ] Improve API error and rate-limit handling
* [ ] Add data-quality checks
* [ ] Create analytical queries and visualisations
* [ ] Containerise the pipeline
* [ ] Deploy the pipeline to AWS

## What I'm Learning

This project is being used to develop practical experience with:

* API-based data ingestion
* ETL/ELT pipeline design
* Data modelling
* Data transformation
* Data quality
* Caching
* API rate limiting
* Parquet and columnar data
* Python testing
* Logging and error handling
* Building reproducible data pipelines

## Status

**In development**

The extraction and API caching components are currently being developed, with transformation, modelling and analysis being added incrementally.
