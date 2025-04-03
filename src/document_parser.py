def extract_text_from_pdf(path: str) -> str:
    import fitz
    doc = fitz.open(path)
    return "\n".join(page.get_text() for page in doc)

def extract_text_from_csv(path: str) -> str:
    import pandas as pd
    df = pd.read_csv(path)
    return df.to_string(index=False)