import re


# --------------------------------------------- Experience duration ---------------------------------------------

def is_experience_duration(line):
    return bool(
        re.search(r"\d+\syear[s]?( \d+\smonth[s]?)?|\d+\smonth[s]?", line)
    )

def get_experience_duration_string(line):
    match = re.search(
        r"\d+\syear[s]?( \d+\smonth[s]?)?|\d+\smonth[s]?", line
    )
    return match.group(0) if match else ""

def parse_experience_duration(line):
    match = re.search(
        r"(?P<years>\d+)\syear[s]?( (?P<months>\d+)\smonth[s]?)?|(?P<only_months>\d+)\smonth[s]?",
        line
    )
    return match.groupdict() if match else ""




# --------------------------------------------- Experience timeline ---------------------------------------------


def is_experience_timeline(line):
    return bool(
        re.search(
            r"([A-Za-z]+\s\d{4})\s*-\s*(Present|[A-Za-z]+\s\d{4})\s*\(\d+\s(year|month)s?( \d+\smonth[s]?)?\)",
            line,
        )
    )


def parse_experience_timeline(line):
    match = re.search(
        r"(?P<start>[A-Za-z]+\s\d{4})\s*-\s*(?P<end>Present|[A-Za-z]+\s\d{4})\s*\((?P<duration>[\d\sA-Za-z]+)\)",
        line,
    )
    if match:
        return match.groupdict()
    return ""


def get_experience_timeline_string(line):
    match = re.search(
        r"[A-Za-z]+\s\d{4}\s*-\s*(Present|[A-Za-z]+\s\d{4})\s*\([\d\sA-Za-z]+\)", line
    )
    if match:
        return match.group(0)
    return ""


# --------------------------------------------- Education timeline ---------------------------------------------



def is_education_timeline(text):
    return bool(re.search(r"\((?:[A-Za-z]+\s)?\d{4}\s*-\s*(?:[A-Za-z]+\s)?\d{4}\)", text))

def parse_education_timeline(text):
    match = re.search(r"(?P<from>(?:[A-Za-z]+\s)?\d{4})\s*-\s*(?P<to>(?:[A-Za-z]+\s)?\d{4})", text)
    return match.groupdict() if match else ""

def get_education_timeline_string(text):
    matches = re.findall(r"\((?:[A-Za-z]+\s)?\d{4}\s*-\s*(?:[A-Za-z]+\s)?\d{4}\)", text)
    return matches[-1] if matches else ""
