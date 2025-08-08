import streamlit as st
import uuid
import os
from labeler import (
    set_extensions,
    label_linkedin_headers,
    label_timelines,
    label_locations,
    label_experience_jobroles,
    label_experience_organizations,
    label_education_organizations,
    get_dict_output,
)
import spacy
from spacy_layout import spaCyLayout
from rich.console import Console
from rich.markdown import Markdown
from rich import print, print_json
from spacy.tokens import Span
from typing import List
import json
from config import SECTION_HEADERS, LinkedInCategory, LinkedInLabels


SAVE_DIR = "uploaded_pdfs"
os.makedirs(SAVE_DIR, exist_ok=True)

nlp = spacy.load("en_core_web_sm")
layout = spaCyLayout(nlp)
# @st.cache_resource
# def load_nlp_pipeline():


set_extensions()


def pdf_to_json(file):
    # Generate unique filename
    file_id = str(uuid.uuid4())
    file_path = os.path.join(SAVE_DIR, f"{file_id}.pdf")

    # Save file
    with open(file_path, "wb") as f:
        f.write(file.read())

    doc = layout(file_path)

    spans = doc.spans["layout"]
    new_span_phase1:List[Span]=label_linkedin_headers(spans)
    new_span_phase2:List[Span]=label_timelines(new_span_phase1)
    new_span_phase3:List[Span]=label_locations(new_span_phase2,nlp)
    new_span_phase4:List[Span]=label_experience_jobroles(new_span_phase3)
    new_span_phase5:List[Span]=label_experience_organizations(new_span_phase4)
    new_span_phase6:List[Span]=label_education_organizations(new_span_phase5,nlp)

    parsed_data = get_dict_output(new_span_phase6)
    return parsed_data


st.title("LinkedIn Profile PDF Parser")

uploaded_file = st.file_uploader("Upload LinkedIn PDF", type="pdf")

if uploaded_file:
    result = pdf_to_json(uploaded_file)
    st.subheader("Parsed JSON")
    st.json(result)
