import re

# ---------------------------
# Regex Patterns
# ---------------------------

EMAIL_REGEX = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

MOBILE_REGEX = re.compile(
    r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b"
)

PAN_REGEX = re.compile(
    r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
)

AADHAR_REGEX = re.compile(
    r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"
)

IFSC_REGEX = re.compile(
    r"\b[A-Z]{4}0[A-Z0-9]{6}\b"
)

CARD_REGEX = re.compile(
    r"\b(?:\d[ -]*?){13,16}\b"
)

UPI_REGEX = re.compile(
    r"\b[\w.-]+@[a-zA-Z]+\b"
)

# ---------------------------
# Registry Mapping
# ---------------------------

FIELD_MASK_RULES = {
    "email": "EMAIL",
    "mobile": "MOBILE",
    "phone": "MOBILE",
    "pan": "PAN",
    "aadhar": "AADHAR",
    "aadhaar": "AADHAR",
    "ifsc": "IFSC",
    "card_number": "CARD",
    "upi": "UPI"
}