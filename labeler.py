from spacy.tokens import Span
from typing import List
from utils._regex import (
    get_education_timeline_string,
    is_education_timeline,
    is_experience_timeline,
    is_experience_duration,
    get_experience_timeline_string,
    get_experience_duration_string,
)
from utils._spacy import is_location
from utils._rule import is_education_provider
from spacy.language import Language
from config import SECTION_HEADERS, LinkedInCategory, LinkedInLabels


def set_extensions():
    Span.set_extension("linkedin_label", default=None, force=True)
    Span.set_extension("linkedin_category", default=None, force=True)


def set_experience_timeline(spans: List[Span]) -> List[Span]:
    updated_spans: List[Span] = []

    for i, span in enumerate(spans):
        if span._.linkedin_category != LinkedInCategory.EXPERIENCE.value:
            updated_spans.append(span)
            continue

        if is_experience_timeline(span.text):
            timeline_text = get_experience_timeline_string(span.text)
            parts = [t.strip() for t in span.text.split(timeline_text) if t]

            timeline_start = span.text.find(timeline_text)
            timeline_span = span.doc.char_span(
                span.start_char + timeline_start,
                span.start_char + timeline_start + len(timeline_text),
                alignment_mode="expand",
            )

            if len(parts) == 0 and timeline_span:
                timeline_span._.linkedin_label = LinkedInLabels.TIMELINE.value
                timeline_span._.linkedin_category = span._.linkedin_category
                updated_spans.append(timeline_span)
            elif len(parts) == 1 and timeline_span:
                befor_span_start = span.text.find(parts[0])
                befor_span_span = span.doc.char_span(
                    span.start_char + befor_span_start,
                    span.start_char + befor_span_start + len(parts[0]),
                    alignment_mode="expand",
                )

                if befor_span_span:
                    befor_span_span._.linkedin_label = span.label_
                    befor_span_span._.linkedin_category = span._.linkedin_category
                    updated_spans.append(befor_span_span)

                # timeline span after creation of span of prefix string
                timeline_span._.linkedin_label = LinkedInLabels.TIMELINE.value
                timeline_span._.linkedin_category = span._.linkedin_category
                updated_spans.append(timeline_span)

            elif len(parts) == 2 and timeline_span:
                befor_span_start = span.text.find(parts[0])
                befor_span_span = span.doc.char_span(
                    span.start_char + befor_span_start,
                    span.start_char + befor_span_start + len(parts[0]),
                    alignment_mode="expand",
                )

                if befor_span_span:
                    befor_span_span._.linkedin_label = span.label_
                    befor_span_span._.linkedin_category = span._.linkedin_category
                    updated_spans.append(befor_span_span)

                # timeline span after creation of span of prefix string
                timeline_span._.linkedin_label = LinkedInLabels.TIMELINE.value
                timeline_span._.linkedin_category = span._.linkedin_category
                updated_spans.append(timeline_span)

                # span after creation of timeline span of suffix string
                after_span_start = span.text.find(parts[1])
                after_span_span = span.doc.char_span(
                    span.start_char + after_span_start,
                    span.start_char + after_span_start + len(parts[1]),
                    alignment_mode="expand",
                )

                if after_span_span:
                    after_span_span._.linkedin_label = span.label_
                    after_span_span._.linkedin_category = span._.linkedin_category
                    updated_spans.append(after_span_span)

        elif is_experience_duration(span.text):
            # span._.linkedin_label = LinkedInLabels.DURATION.value
            duration_text = get_experience_duration_string(span.text)
            parts = [t.strip() for t in span.text.split(duration_text) if t]
            duration_start = span.text.find(duration_text)
            duration_span = span.doc.char_span(
                span.start_char + duration_start,
                span.start_char + duration_start + len(duration_text),
                alignment_mode="expand",
            )

            if len(parts) == 0 and duration_span:
                duration_span._.linkedin_label = LinkedInLabels.DURATION.value
                duration_span._.linkedin_category = span._.linkedin_category
                updated_spans.append(duration_span)
            elif len(parts) == 1 and duration_span:
                befor_span_start = span.text.find(parts[0])
                befor_span_span = span.doc.char_span(
                    span.start_char + befor_span_start,
                    span.start_char + befor_span_start + len(parts[0]),
                    alignment_mode="expand",
                )

                if befor_span_span:
                    befor_span_span._.linkedin_label = span.label_
                    befor_span_span._.linkedin_category = span._.linkedin_category
                    updated_spans.append(befor_span_span)

                # duration span after creation of span of prefix string
                duration_span._.linkedin_label = LinkedInLabels.DURATION.value
                duration_span._.linkedin_category = span._.linkedin_category
                updated_spans.append(duration_span)

            elif len(parts) == 2 and duration_span:
                befor_span_start = span.text.find(parts[0])
                befor_span_span = span.doc.char_span(
                    span.start_char + befor_span_start,
                    span.start_char + befor_span_start + len(parts[0]),
                    alignment_mode="expand",
                )

                if befor_span_span:
                    befor_span_span._.linkedin_label = span.label_
                    befor_span_span._.linkedin_category = span._.linkedin_category
                    updated_spans.append(befor_span_span)

                # duration span after creation of span of prefix string
                duration_span._.linkedin_label = LinkedInLabels.DURATION.value
                duration_span._.linkedin_category = span._.linkedin_category
                updated_spans.append(duration_span)

                # span after creation of duration span of suffix string
                after_span_start = span.text.find(parts[1])
                after_span_span = span.doc.char_span(
                    span.start_char + after_span_start,
                    span.start_char + after_span_start + len(parts[1]),
                    alignment_mode="expand",
                )

                if after_span_span:
                    after_span_span._.linkedin_label = span.label_
                    after_span_span._.linkedin_category = span._.linkedin_category
                    updated_spans.append(after_span_span)
        else:
            updated_spans.append(span)
    return updated_spans


def set_education_timeline(spans: List[Span]) -> List[Span]:
    updated_spans: List[Span] = []

    for i, span in enumerate(spans):
        if span._.linkedin_category != LinkedInCategory.EDUCATION.value:
            updated_spans.append(span)
            continue

        if is_education_timeline(span.text):
            timeline_text = get_education_timeline_string(span.text)
            parts = [
                t.strip().strip("·")
                for t in span.text.split(timeline_text)
                if t.strip().strip("·")
            ]

            timeline_start = span.text.find(timeline_text)
            timeline_span = span.doc.char_span(
                span.start_char + timeline_start,
                span.start_char + timeline_start + len(timeline_text),
                alignment_mode="expand",
            )

            if len(parts) == 0 and timeline_span:
                timeline_span._.linkedin_label = LinkedInLabels.TIMELINE.value
                timeline_span._.linkedin_category = span._.linkedin_category
                updated_spans.append(timeline_span)

            elif len(parts) == 1 and timeline_span:
                befor_span_start = span.text.find(parts[0])
                befor_span_span = span.doc.char_span(
                    span.start_char + befor_span_start,
                    span.start_char + befor_span_start + len(parts[0]),
                    alignment_mode="expand",
                )

                if befor_span_span:
                    befor_span_span._.linkedin_label = LinkedInLabels.EDUCATION.value
                    befor_span_span._.linkedin_category = span._.linkedin_category
                    updated_spans.append(befor_span_span)

                # timeline span after creation of span of prefix string
                timeline_span._.linkedin_label = LinkedInLabels.TIMELINE.value
                timeline_span._.linkedin_category = span._.linkedin_category
                updated_spans.append(timeline_span)

            elif len(parts) == 2 and timeline_span:
                befor_span_start = span.text.find(parts[0])
                befor_span_span = span.doc.char_span(
                    span.start_char + befor_span_start,
                    span.start_char + befor_span_start + len(parts[0]),
                    alignment_mode="expand",
                )

                if befor_span_span:
                    befor_span_span._.linkedin_label = LinkedInLabels.EDUCATION.value
                    befor_span_span._.linkedin_category = span._.linkedin_category
                    updated_spans.append(befor_span_span)

                # timeline span after creation of span of prefix string
                timeline_span._.linkedin_label = LinkedInLabels.TIMELINE.value
                timeline_span._.linkedin_category = span._.linkedin_category
                updated_spans.append(timeline_span)

                # span after creation of timeline span of suffix string
                after_span_start = span.text.find(parts[1])
                after_span_span = span.doc.char_span(
                    span.start_char + after_span_start,
                    span.start_char + after_span_start + len(parts[1]),
                    alignment_mode="expand",
                )

                if after_span_span:
                    after_span_span._.linkedin_label = span.label_
                    after_span_span._.linkedin_category = span._.linkedin_category
                    updated_spans.append(after_span_span)
        else:
            updated_spans.append(span)
    return updated_spans


def label_timelines(spans: List[Span]) -> List[Span]:
    updated_spans1 = set_experience_timeline(spans)
    updated_spans = set_education_timeline(updated_spans1)
    return updated_spans


def label_locations(spans: List[Span], nlp: Language) -> List[Span]:
    updated_spans = []

    for i, span in enumerate(spans):
        is_user_or_experience = span._.linkedin_category in {"userInfo", "experience"}

        if is_user_or_experience:
            previous_label = spans[i - 1]._.linkedin_label if i > 0 else None
            if (
                previous_label == LinkedInLabels.TIMELINE.value
                or span._.linkedin_category == "userInfo"
            ) and is_location(span, nlp):
                span._.linkedin_label = "location"

        updated_spans.append(span)

    return updated_spans


def linkedin_header_to_category_value(text: str) -> str:
    return text.strip().lower().replace(" ", "_").replace("-", "_")


def label_linkedin_headers(spans: List[Span]) -> List[Span]:
    current_heading = ""
    labeled_spans: List[Span] = []

    for span in spans:
        section_category = linkedin_header_to_category_value(span.text)
        span._.linkedin_label = span.label_
        span._.linkedin_category = span._.heading

        if section_category in SECTION_HEADERS:
            current_heading = section_category
            span._.linkedin_label = "section_header"
        elif int(span._.layout.x) == 223 and int(span._.layout.y) == 46:
            current_heading = LinkedInCategory.USERINFO.value
            span._.linkedin_label = LinkedInLabels.NAME.value
        elif labeled_spans[-1]._.linkedin_label == LinkedInLabels.NAME.value:
            span._.linkedin_label = LinkedInLabels.JOBROLE.value

        if current_heading:
            span._.linkedin_category = current_heading

        labeled_spans.append(span)

    return labeled_spans


def label_experience_jobroles(spans: List[Span]) -> List[Span]:
    updated_spans: List[Span] = []

    for span in spans:
        if span._.linkedin_category == "experience":
            if span._.linkedin_label == LinkedInLabels.TIMELINE.value:
                updated_spans[-1]._.linkedin_label = "jobrole"

        updated_spans.append(span)

    return updated_spans


def label_experience_organizations(spans: List[Span]) -> List[Span]:
    updated_spans: List[Span] = []
    present_experience=True
    a=0
    for i, span in enumerate(spans):
        if span._.linkedin_category == "experience":
            a+=1
            if (
                span._.linkedin_label in (LinkedInLabels.DURATION.value, "jobrole")
                and updated_spans[-1]._.linkedin_label == "section_header"
            ):
                updated_spans[-1]._.linkedin_label = "organization"
            
            if present_experience and a==2:
                span._.linkedin_label = "organization"

        updated_spans.append(span)
    return updated_spans


def label_education_organizations(spans: List[Span], nlp: Language) -> List[Span]:
    updated_spans: List[Span] = []

    for i, span in enumerate(spans):
        if span._.linkedin_category == "education" and span._.linkedin_label not in [
            "education",
            LinkedInLabels.TIMELINE.value,
        ]:
            doc = nlp(span.text)
            if any(
                ent.label_ in {"ORG", "FAC"} for ent in doc.ents
            ) or is_education_provider(span.text):
                span._.linkedin_label = "organization"

        updated_spans.append(span)
    return updated_spans

def get_type_by_category():
    pass