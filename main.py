import spacy
from spacy_layout import spaCyLayout
from rich.console import Console
from rich.markdown import Markdown
from rich import print
from spacy.tokens import Span
import re
from typing import List

custom_headings = [
    "Contact", "Top Skills", "Languages", "Certifications",
    "Summary", "Experience", "Education"
]
nlp = spacy.load("en_core_web_sm")
layout = spaCyLayout(nlp)

Span.set_extension("linkedin_label", default=None, force=True)
Span.set_extension("linkedin_heading", default=None, force=True)

doc = layout("./data/Ceren Kaya2.pdf")

def is_timeline(line):
    return bool(re.search(
        r'([A-Za-z]+\s\d{4})\s*-\s*(Present|[A-Za-z]+\s\d{4})\s*\(\d+\s(year|month)s?( \d+\smonth[s]?)?\)', 
        line
    ))

def extract_timeline(line):
    match = re.search(
        r'(?P<start>[A-Za-z]+\s\d{4})\s*-\s*(?P<end>Present|[A-Za-z]+\s\d{4})\s*\((?P<duration>[\d\sA-Za-z]+)\)',
        line
    )
    if match:
        return match.groupdict()
    return None

def get_timeline_string(line):
    match = re.search(r'[A-Za-z]+\s\d{4}\s*-\s*(Present|[A-Za-z]+\s\d{4})\s*\([\d\sA-Za-z]+\)', line)
    if match:
        return match.group(0)
    return None

def is_total_duration(line):
    return bool(re.fullmatch(r'\d+\syear[s]?( \d+\smonth[s]?)?|\d+\smonth[s]?', line.strip()))

social_domains = ["linkedin.com", "github.com", "medium.com", "kaggle.com", "twitter.com"]

def is_valid_url(token)->bool:
    return token.like_url or any(domain in token.text for domain in social_domains)

def is_location(span:Span):
    gpe = [] # countries, cities, states
    loc = [] # non gpe locations, mountain ranges, bodies of water
    
    doc = nlp(span.text)
    for ent in doc.ents:
        if (ent.label_ == 'GPE'):
            gpe.append(ent.text)
        elif (ent.label_ == 'LOC'):
            loc.append(ent.text)
    if len(gpe)>0 or len(loc)>0:
        return True
    return False

section_headers = set([
    "contact", "top skills", "languages", "certifications",
    "summary", "experience", "education", "honors-awards"
])

current_heading = ""
spans=doc.spans["layout"]
new_span_phase1:List[Span]=[]

for i, span in enumerate(spans):
    current_heading_updated =False
    span._.linkedin_label = span.label_
    span._.linkedin_heading = span._.heading
    
    # ----------------------------------- [ Custom Heading Initialization Logic ] -----------------------------------
    if span.text.strip().lower() in section_headers:
        span._.linkedin_label =  "section_header" 
        current_heading = span.text.strip().lower()
        current_heading_updated =True
        
    elif int(span._.layout.x) == 223 and int(span._.layout.y) == 46:
        span._.linkedin_label =  "section_header"
        current_heading = "userInfo"
        current_heading_updated =True
    
    # Predined Headings
    if current_heading: 
        span._.linkedin_heading = current_heading 
    
    # ----------------------------------- [ Custom label Initialization Logic ] -----------------------------------
    if span._.linkedin_heading == "experience":
        if is_timeline(span.text):
            span._.linkedin_label = "timeline"
            
        elif is_total_duration(span.text):
            span._.linkedin_label = "duration"

    # ----------------------------------- [ Print Statements ] -----------------------------------
    if current_heading_updated:
        print(span._.linkedin_heading)
        
    print(
        f"Label: [bold green]{span._.linkedin_label}[/] "
        f"Section: [bold cyan]{span._.linkedin_heading}[/] "
        f"Text: [yellow]{span.text}[/] "
    )
    new_span_phase1.append(span)
    

# Timeline cleanup Phase
new_span_phase2: List[Span] = []

for span in new_span_phase1:
    if span._.linkedin_label == "timeline":
        text = get_timeline_string(span.text)
        new_spans = [t.strip() for t in span.text.split(text) if t]

        if len(new_spans) == 0:
            # timeline only
            timeline_start = span.text.find(text)
            timeline_span = span.doc.char_span(span.start_char + timeline_start, span.start_char + timeline_start + len(text), alignment_mode="expand")
            if timeline_span:
                new_span_phase2[-1]._.linkedin_label = "jobrole"
                timeline_span._.linkedin_label = "timeline"
                timeline_span._.linkedin_heading = span._.linkedin_heading
                new_span_phase2.append(timeline_span)

        elif len(new_spans) == 1:
            # jobrole
            job_start = span.text.find(new_spans[0])
            job_span = span.doc.char_span(span.start_char + job_start, span.start_char + job_start + len(new_spans[0]), alignment_mode="expand")
            if job_span:
                job_span._.linkedin_label = "jobrole"
                job_span._.linkedin_heading = span._.linkedin_heading
                new_span_phase2.append(job_span)

            # timeline
            timeline_start = span.text.find(text)
            timeline_span = span.doc.char_span(span.start_char + timeline_start, span.start_char + timeline_start + len(text), alignment_mode="expand")
            if timeline_span:
                timeline_span._.linkedin_label = "timeline"
                timeline_span._.linkedin_heading = span._.linkedin_heading
                new_span_phase2.append(timeline_span)

        elif len(new_spans) == 2:
            # jobrole
            job_start = span.text.find(new_spans[0])
            job_span = span.doc.char_span(span.start_char + job_start, span.start_char + job_start + len(new_spans[0]), alignment_mode="expand")
            if job_span:
                job_span._.linkedin_label = "jobrole"
                job_span._.linkedin_heading = span._.linkedin_heading
                new_span_phase2.append(job_span)

            # timeline
            timeline_start = span.text.find(text)
            timeline_span = span.doc.char_span(span.start_char + timeline_start, span.start_char + timeline_start + len(text), alignment_mode="expand")
            if timeline_span:
                timeline_span._.linkedin_label = "timeline"
                timeline_span._.linkedin_heading = span._.linkedin_heading
                new_span_phase2.append(timeline_span)
    else:
        new_span_phase2.append(span)



for span in new_span_phase2:
    print(
        f"Label: [bold green]{span._.linkedin_label}[/] "
        f"Section: [bold cyan]{span._.linkedin_heading}[/] "
        f"Text: [yellow]{span.text}[/] "
    )


# Timeline cleanup Phase
new_span_phase3: List[Span] = []

for i, span in enumerate(new_span_phase2):
    if span._.linkedin_heading in ["userInfo","experience"]:
        if new_span_phase2[i-1]._.linkedin_label == "timeline":
            if is_location(span):
                span._.linkedin_label = "location"
        elif span._.linkedin_heading == "userInfo":
            if is_location(span):
                span._.linkedin_label = "location"

    new_span_phase3.append(span)