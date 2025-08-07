
def is_education_provider(text: str) -> bool:
    keywords = [
        "school", "university", "college", "institute", "academy", 
        "faculty", "polytechnic", "kindergarten", "lyceum", "high school"
    ]
    text_lower = text.lower()
    return any(kw in text_lower for kw in keywords)
