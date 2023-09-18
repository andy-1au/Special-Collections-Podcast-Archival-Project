from dataclasses import dataclass


@dataclass(slots=True)
class PodcastData:
    parent_object: str
    cmodel: str
    object_location: str
    label: str
    title: str
    creator: str
    contributors: str
    type: str
    genre: str
    genre_uri: str
    date_created: str
    year: str
    season: str
    date_captured: str
    publisher: str
    language_code: str
    language_text: str
    format: str
    format_uri: str
    file_format: str
    dimensions: str
    digital_origin: str
    description_abstract: str
    subject_topic: str
    website: str
    rights: str
    volume_number: str
    issue_number: str
