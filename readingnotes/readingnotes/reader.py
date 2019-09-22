import codecs
import datetime
import re
import yaml

from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from jinja2 import Environment, FileSystemLoader
from slugify import slugify

from .utils import copy


THEME_PATH = Path(__file__).parent / "theme"


@dataclass
class Note:
    note: str
    tags: List[str] = field(default_factory=list)
    author: str = ""


@dataclass
class Reading:
    title: str
    author: str
    read_on: datetime.datetime
    notes: List[Note]
    tags: list = field(default_factory=list)
    subtitle: str = ""
    url: str = ""
    isbn: str = ""
    cover: str = ""

    @staticmethod
    def load_from_yaml(filename):
        parsed = yaml.safe_load(filename.read_text())
        return Reading(**parsed)

    @property
    def slug(self):
        return slugify(self.title)

    @property
    def image_url(self):
        if self.cover:
            return self.cover
        if self.isbn:
            return f"http://covers.openlibrary.org/b/isbn/{{ self.isbn }}-L.jpg"
        return False


class Context:
    def __init__(self, readings):
        self.readings = readings
        self.tags = defaultdict(list)
        self.notes = []

    def build(self):
        self.postprocess_readings()
        self.build_tags()

    def postprocess_readings(self):
        for reading in self.readings:
            for note in reading.notes:
                if "tags" not in note:
                    note["tags"] = []
                note["tags"].extend(reading.tags)
                note["reading"] = reading

    def build_notes(self):
        for reading in self.readings:
            self.notes.extend(reading.notes)

    def build_tags(self):
        for reading in self.readings:
            for note in reading.notes:
                for tag in note["tags"]:
                    self.tags[tag].append(note)


class WebsiteGenerator:
    def __init__(self, output_path, theme_path, context):
        self.output_path = Path(output_path)
        self.theme_path = Path(theme_path)
        self.context = context

        template_path = self.theme_path / "templates"
        self._env = Environment(loader=FileSystemLoader(template_path.as_posix()))

    def generate_website(self):
        self.create_paths(
            self.output_path,
            self.output_path / "readings",
            self.output_path / "assets",
            self.output_path / "tags",
        )

        self.copy_assets()

        self.render_template("index.html", "index.html", readings=self.context.readings)

        # Readings
        for reading in self.context.readings:
            self.render_template(
                "reading.html", f"readings/{reading.slug}.html", reading=reading
            )

        # Tags
        for tag, notes in self.context.tags.items():
            self.render_template("tag.html", f"tags/{tag}.html", tag=tag, notes=notes)

    def copy_assets(self):
        copy(
            self.theme_path / "assets",
            self.output_path / "assets"
        )

    def render_template(self, tpl_name, filename, **options):
        template = self._env.get_template(tpl_name)
        output = template.render(**options)
        
        output_path = self.output_path / filename
        output_path.write_text(output, "utf-8")

    def create_paths(self, *paths):
        def _create_path(path):
            if not path.exists():
                path.mkdir(parents=True)

        list(map(_create_path, paths))


def process(path=".", output="output"):
    readings = list(map(Reading.load_from_yaml, Path(path).glob("notes-*.yaml")))
    ctx = Context(readings)
    ctx.build()

    generator = WebsiteGenerator(output, THEME_PATH, ctx)
    generator.generate_website()
