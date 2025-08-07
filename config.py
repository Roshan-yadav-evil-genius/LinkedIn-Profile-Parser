from enum import Enum


class LinkedInCategory(Enum):
    CONTACT = "contact"
    TOPSKILLS = "top_skills"
    LANGUAGES = "languages"
    CERTIFICATIONS = "certifications"
    USERINFO = "userInfo"
    SUMMARY = "summary"
    EXPERIENCE = "experience"
    EDUCATION = "education"
    HONORSAWARDS = "honors_awards"


class LinkedInLabels(Enum):
    TIMELINE = "timeline"
    DURATION = "duration"
    EDUCATION = "education"
    LOCATION = "location"
    JOBROLE = "jobrole"
    ORGANIZATION = "organization"
    NAME = "name"


SECTION_HEADERS = {header.value for header in LinkedInCategory}

SOCIAL_DOMAINS = [
    "linkedin.com",
    "github.com",
    "medium.com",
    "kaggle.com",
    "twitter.com",
]
