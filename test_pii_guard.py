from pii_engine import mask_text


samples = [
    "Processing KYC for PAN ABCDE1234F",
    "Customer mobile is 9876543210",
    "Aadhar number is 1111-2222-3333",
    "Email is john@gmail.com",
    (
        'User "Vikas Merchant" transferred money to '
        '"Aadhar Housing Fin" for invoice 987654321012 using sambabu@oksbi'
    ),
]


for sample in samples:
    print()
    print("INPUT :", sample)
    print("OUTPUT:", mask_text(sample))