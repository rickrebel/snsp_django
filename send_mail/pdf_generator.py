"""
Generador de constancias PDF a partir de un template y un JSON de asistentes.

Dependencias:
    pip install pypdf reportlab

Uso:
    generator = ConstanciaGenerator(
        template_path="template_snsp.pdf",
        json_path="asistentes.json",
        output_dir="media",
        font_regular_path="ruta/a/Patria-Regular.ttf",
        font_light_path="ruta/a/Patria-Light.ttf",
    )
    generator.generate_all()
"""

import json
import os
import re
import io
import unicodedata
from dataclasses import dataclass

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import Color


@dataclass
class Attendee:
    """Represents a single attendee from the JSON file."""
    id: int
    full_name: str
    role: str
    email: str
    state: str


class ConstanciaGenerator:
    """
    Generates personalized PDF constancias by overlaying attendee data
    on top of a PDF template.

    The template is expected to have blank space where the attendee's
    name and role should appear. This class creates a transparent overlay
    with the text positioned at the correct coordinates, then merges it
    with the template.

    Coordinates are calibrated for the SNSP constancia template (737 x 992 pts).
    """

    # --- Layout constants (in reportlab coords: origin = bottom-left) ---
    # These were extracted from the template using pdfplumber.
    # "Nombre Apellido" center: pdfplumber top=380.6, bottom=429.6 → reportlab baseline ≈ 572
    # "Cargo que ocupa" center:  pdfplumber top=443.9, bottom=473.9 → reportlab baseline ≈ 524
    NAME_Y = 572
    ROLE_Y = 524
    DESCRIPTION_Y = 464

    NAME_FONT_SIZE = 49
    ROLE_FONT_SIZE = 30
    DESCRIPTION_FONT_SIZE = 20

    MAX_TEXT_WIDTH = 600  # Max width in pts before auto-shrinking the font
    MIN_FONT_SIZE = 16   # Never shrink below this

    # Text color extracted from the template (dark gray/black used in original)
    # TEXT_COLOR = Color(0.20, 0.20, 0.20)
    TEXT_COLOR = Color(0x70 / 255, 0x72 / 255, 0x72 / 255)

    def __init__(
        self,
        doc_name: str,
        template_path: str,
        json_path: str,
        output_dir: str = "media",
        font_regular_path: str | None = None,
        font_light_path: str | None = None,
        font_description_path: str | None = None,
    ):
        self.template_path = template_path
        self.json_path = json_path
        self.output_dir = output_dir
        self.doc_name = doc_name

        # Read template once and keep page dimensions
        self.template_reader = PdfReader(self.template_path)
        page = self.template_reader.pages[0]
        self.page_width = float(page.mediabox.width)
        self.page_height = float(page.mediabox.height)
        self.center_x = self.page_width / 2

        # Register fonts
        self._register_fonts(
            font_regular_path, font_light_path, font_description_path
        )

    _DEJAVU = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

    def _register_font(
        self,
        font_path: str | None,
        font_name: str,
        fallback_name: str,
        fallback_path: str,
    ) -> str:
        """
        Register a single font with reportlab.
        Returns the registered font name (primary or fallback).
        """
        if font_path and os.path.isfile(font_path):
            pdfmetrics.registerFont(TTFont(font_name, font_path))
            return font_name

        if os.path.isfile(fallback_path):
            try:
                pdfmetrics.registerFont(TTFont(fallback_name, fallback_path))
            except Exception:
                pass  # Already registered
        print(
            f"⚠ {font_name} not found at '{font_path}'. "
            f"Using fallback: {fallback_name}."
        )
        return fallback_name

    def _register_fonts(
        self,
        regular_path: str | None,
        light_path: str | None,
        description_path: str | None,
    ) -> None:
        """Register the Patria font family with reportlab."""
        self.font_regular = self._register_font(
            regular_path, "PatriaRegular", "FallbackRegular", self._DEJAVU
        )
        self.font_light = self._register_font(
            light_path, "PatriaLight", "FallbackLight", self._DEJAVU
        )
        self.font_description = self._register_font(
            description_path, "NotoSans", "FallbackDescription", self._DEJAVU
        )

    # ------------------------------------------------------------------
    # Text helpers
    # ------------------------------------------------------------------

    @staticmethod
    def slugify(text: str) -> str:
        """
        Convert text to a filesystem-safe slug.
        Example: "Ilanatllely Yazmin Hernández" → "ilanatllely-yazmin-hernandez"
        """
        text = unicodedata.normalize("NFKD", text)
        text = text.encode("ascii", "ignore").decode("ascii")
        text = text.lower().strip()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[-\s]+", "-", text)
        return text.strip("-")

    def _fit_font_size(
        self,
        text: str,
        font_name: str,
        target_size: float,
    ) -> float:
        """
        Reduce font size if the text exceeds MAX_TEXT_WIDTH at the target size.
        Returns the largest font size that fits, down to MIN_FONT_SIZE.
        """
        size = target_size
        while size > self.MIN_FONT_SIZE:
            width = pdfmetrics.stringWidth(text, font_name, size)
            if width <= self.MAX_TEXT_WIDTH:
                return size
            size -= 1
        return self.MIN_FONT_SIZE

    # ------------------------------------------------------------------
    # Overlay creation
    # ------------------------------------------------------------------

    def _create_overlay(self, attendee: Attendee) -> io.BytesIO:
        """
        Create a single-page transparent PDF with the attendee's name and role
        positioned to match the template layout.
        """
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=(self.page_width, self.page_height))

        name = attendee.full_name.strip()
        role = attendee.role.strip()

        # --- Draw full_name ---
        name_size = self._fit_font_size(
            name, self.font_regular, self.NAME_FONT_SIZE)
        c.setFont(self.font_regular, name_size)
        c.setFillColor(self.TEXT_COLOR)
        c.drawCentredString(self.center_x, self.NAME_Y, name)

        # --- Draw role ---
        role_size = self._fit_font_size(
            role, self.font_light, self.ROLE_FONT_SIZE)

        # If the role font was reduced a lot, also lower the Y position slightly
        # to keep visual balance.
        role_y = self.ROLE_Y
        if role_size < self.ROLE_FONT_SIZE:
            role_y = self.ROLE_Y + (role_size - self.ROLE_FONT_SIZE) * 0.3

        c.setFont(self.font_light, role_size)
        c.drawCentredString(self.center_x, role_y, role)

        c.save()
        buffer.seek(0)
        return buffer

    # ------------------------------------------------------------------
    # PDF merging
    # ------------------------------------------------------------------

    def _merge_overlay(self, overlay_buffer: io.BytesIO) -> PdfWriter:
        """
        Merge the transparent overlay onto the template's first page.
        Returns a PdfWriter ready to be saved.
        """
        overlay_reader = PdfReader(overlay_buffer)
        writer = PdfWriter()

        # Clone the template page and merge overlay on top
        template_page = self.template_reader.pages[0]
        writer.add_page(template_page)
        writer.pages[0].merge_page(overlay_reader.pages[0])

        return writer

    # ------------------------------------------------------------------
    # File output
    # ------------------------------------------------------------------

    def _build_output_path(self, attendee: Attendee) -> str:
        """
        Build the output path: media/{state}/{slug-name}_{slug-role}.pdf
        Creates directories as needed.
        """

        state_folder = self.slugify(attendee.state)

        name_slug = self.slugify(attendee.full_name)
        filename = f"Constancia-{self.doc_name}-{name_slug}.pdf"

        dir_path = os.path.join(self.output_dir, state_folder)
        os.makedirs(dir_path, exist_ok=True)

        return os.path.join(dir_path, filename)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load_attendees(self) -> list[Attendee]:
        """Load and parse the JSON file into a list of Attendee objects."""
        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        attendees = []
        for item in data:
            attendees.append(
                Attendee(
                    id=item["id"],
                    full_name=item["full_name"],
                    role=item["role"],
                    email=item["email"],
                    state=item["state"],
                )
            )
        return attendees

    def generate_one(self, attendee: Attendee) -> str:
        """
        Generate a single constancia PDF for one attendee.
        Returns the output file path.
        """
        overlay = self._create_overlay(attendee)
        writer = self._merge_overlay(overlay)

        output_path = self._build_output_path(attendee)
        with open(output_path, "wb") as f:
            writer.write(f)

        return output_path

    def generate_all(self, limit: int = None) -> list[str]:
        """
        Generate constancias for every attendee in the JSON file.
        Returns a list of generated file paths.
        """
        attendees = self.load_attendees()
        generated = []
        if limit:
            attendees = attendees[:limit]

        for i, attendee in enumerate(attendees, start=1):
            path = self.generate_one(attendee)
            generated.append(path)
            if i % 10 == 0:
                print(f"[{i}/{len(attendees)}] ✓ {attendee.full_name.strip()} → {path}")

        print(f"\n✅ {len(generated)} constancias generadas en '{self.output_dir}/'")
        return generated


# --------------------------------------------------------------------------
# Punto de entrada para ejecución directa
# --------------------------------------------------------------------------
# if __name__ == "__main__":
#     generator = ConstanciaGenerator(
#         template_path="template_snsp.pdf",
#         json_path="asistentes.json",
#         output_dir="media",
#         # ⬇ Ajusta estas rutas a donde tengas los archivos .ttf de Patria
#         font_regular_path=r"C:\path\to\Patria-Regular.ttf",
#         font_light_path=r"C:\path\to\Patria-Light.ttf",
#     )
#     generator.generate_all(limit=1)