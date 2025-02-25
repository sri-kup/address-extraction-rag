## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Python 3.13 or higher.
- You have a working internet connection to download necessary NLP models and libraries.

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/sri-kup/address-extraction-rag.git
    cd address-extraction-rag
    ```

2. **Set up a virtual environment:**
    ```sh
    python3.13 -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Place your PDF files in the `Files/` directory.**

2. **Run the main script:**
    ```sh
    python main.py
    ```

   This script will process all PDF files in the `Files/` directory and extract information

## Configuration

### Environment Variables

You can configure the project by setting the following environment variables:

- `GROQ_API_KEY`: "your-api-key"