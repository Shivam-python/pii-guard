# Hybrid PII Guard Engine (V1)

A lightweight, high-performance PII masking engine built using deterministic Regex strategies.

This is the V1 implementation focused on:

- Fast masking
- Zero ML overhead
- Structured JSON masking
- Recursive traversal
- Extensible strategy registry
- Simple integration

The NLP + Logging pipeline will be introduced in V2.

---

# Features

## Supported PII Types

- Email
- Mobile Number
- PAN
- Aadhaar
- IFSC
- Card Numbers
- UPI IDs

---

# Architecture

Current implementation uses:

```text
Input
  ↓
Strategy Registry
  ↓
Regex Strategy Execution
  ↓
Masked Output
```

No NLP models are used in V1.

---

# Project Structure

```text
project/
│
├── config.py
├── pii_engine.py
├── strategies.py
└── sample.py
```

---

# Installation

## 1. Clone Repository

```bash
git clone <repo_url>
cd <repo_name>
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Linux / Mac

```bash
source venv/bin/activate
```

### Windows

```bash
venv\\Scripts\\activate
```

---

## 3. Install Dependencies

```bash
pip install cachetools
```

Or:

```bash
pip install -r requirements.txt
```

---

# File Overview

## config.py

Contains:

- Regex patterns
- Field-to-strategy mappings

Example:

```python
FIELD_MASK_RULES = {
    "email": "EMAIL",
    "mobile": "MOBILE",
    "pan": "PAN",
}
```

---

## strategies.py

Contains masking strategies.

Current strategies:

- BaseStrategy
- RegexStrategy

Example:

```python
RegexStrategy(
    EMAIL_REGEX,
    "[REDACTED_EMAIL]"
)
```

---

## pii_engine.py

Core orchestration engine.

Responsibilities:

- Recursive JSON traversal
- Field-based routing
- Text masking
- LRU caching
- Public masking APIs

Main APIs:

```python
mask_pii()
mask_text()
mask_json()
```

---

## sample.py

Example usage and sample masking flows.

Run using:

```bash
python sample.py
```

---

# Usage

## Basic String Masking

```python
from pii_engine import mask_text

text = "Customer PAN is ABCDE1234F"

print(mask_text(text))
```

Output:

```text
Customer PAN is [REDACTED_PAN]
```

---

# Structured JSON Masking

```python
from pii_engine import mask_pii

payload = {
    "email": "john@gmail.com",
    "mobile": "9876543210",
    "pan": "ABCDE1234F",
}

print(mask_pii(payload))
```

Output:

```python
{
    "email": "[REDACTED_EMAIL]",
    "mobile": "[REDACTED_MOBILE]",
    "pan": "[REDACTED_PAN]",
}
```

---

# Recursive Nested Object Support

Nested dictionaries and lists are automatically traversed.

Example:

```python
payload = {
    "user": {
        "email": "john@gmail.com"
    },
    "transactions": [
        {
            "pan": "ABCDE1234F"
        }
    ]
}
```

---

# Extending the Engine

## Add New Regex Pattern

In `config.py`

```python
PASSPORT_REGEX = re.compile(
    r"\\b[A-Z][0-9]{7}\\b"
)
```

---

## Add Strategy Mapping

```python
FIELD_MASK_RULES = {
    "passport": "PASSPORT"
}
```

---

## Register Strategy

In `pii_engine.py`

```python
"PASSPORT": RegexStrategy(
    PASSPORT_REGEX,
    "[REDACTED_PASSPORT]"
)
```

---

# Caching

V1 includes LRU caching for repeated masking calls.

```python
@lru_cache(maxsize=10000)
```

Benefits:

- Reduces repeated regex execution
- Improves throughput
- Useful for repetitive logs/events

---

# Performance Characteristics

## Regex Complexity

Most regex operations are approximately:

```text
O(n)
```

where:

```text
n = input length
```

---

# Why Regex-Only in V1?

V1 intentionally avoids ML/NLP models because:

- Lower latency
- Simpler deployment
- CPU-friendly
- Easier debugging
- Deterministic behavior
- No GPU requirements

This makes it ideal for:

- APIs
- High-throughput systems
- Log pipelines
- Background workers

---

# Current Limitations

V1 does NOT reliably detect:

- Person names
- Addresses
- Contextual PII
- OCR ambiguity
- Semantic entities

Example:

```text
Payment received from Rahul Sharma
```

will NOT be masked in V1.

---

# Example Supported Inputs

## Email

```text
john@gmail.com
```

---

## PAN

```text
ABCDE1234F
```

---

## Aadhaar

```text
1111 2222 3333
```

---

## Mobile

```text
9876543210
```

---

## IFSC

```text
HDFC0001234
```

---

# Running Samples

```bash
python sample.py
```

Example output:

```text
INPUT : Processing PAN ABCDE1234F
OUTPUT: Processing PAN [REDACTED_PAN]
```

---

# TODO (V2)

Planned additions for next version:

## NLP / Semantic Detection

Integrate:

- HuggingFace transformers
- Piiranha PII model

for contextual masking.

Example:

```text
Payment from Rahul Sharma
```

---

## Hybrid Regex + NLP Strategy

Introduce:

```text
Regex First
    ↓
Ambiguity Detection
    ↓
NLP Verification
```

---

## Logging Pipeline

Add:

- QueueHandler
- QueueListener
- Async masking
- Context-aware decorators
- Scoped redaction
- Automatic logger interception

---

## FastAPI Middleware

Planned support for:

- Request masking
- Response masking
- Header masking
- Trace sanitization

---

## Partial Masking

Examples:

```text
XXXX-XXXX-XXXX-1111
```

instead of:

```text
[REDACTED_CARD]
```

---

## Distributed Cache

Potential Redis integration.

---

# Future Production Enhancements

Potential future additions:

- Kafka log pipeline
- OpenTelemetry integration
- Celery worker support
- Triton inference server
- GPU batching
- Multi-language entity detection

---

# License

MIT