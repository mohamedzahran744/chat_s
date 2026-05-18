"""
components/file_handler.py — File upload, extraction, context building
"""
import io

TEXT_EXTENSIONS = (
    ".txt", ".md", ".py", ".cpp", ".c", ".h", ".js", ".ts",
    ".java", ".json", ".csv", ".xml", ".html", ".css", ".sql",
    ".yaml", ".yml", ".rs", ".go", ".kt",
)
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".webp")

IMAGE_MEDIA_TYPES = {
    ".png":  "image/png",
    ".jpg":  "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif":  "image/gif",
    ".webp": "image/webp",
}


def extract_text_from_file(uploaded_file) -> tuple[str, str]:
    name = uploaded_file.name.lower()
    raw  = uploaded_file.read()

    if any(name.endswith(ext) for ext in TEXT_EXTENSIONS):
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("latin-1", errors="replace")
        return text[:8000], "📄 Text / Code File"

    if name.endswith(".pdf"):
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(io.BytesIO(raw))
            pages  = []
            for i, page in enumerate(reader.pages):
                if i >= 50:
                    break
                pages.append(page.extract_text() or "")
            return "\n".join(pages)[:8000], "📕 PDF"
        except Exception as e:
            return f"[PDF ERROR] {e}", "📕 PDF"

    if name.endswith(".docx"):
        try:
            from docx import Document
            doc  = Document(io.BytesIO(raw))
            text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
            return text[:8000], "📝 Word Document"
        except Exception as e:
            return f"[DOCX ERROR] {e}", "📝 Word Document"

    if any(name.endswith(ext) for ext in IMAGE_EXTENSIONS):
        # Return raw bytes + media type for vision analysis
        ext = "." + name.rsplit(".", 1)[-1]
        media_type = IMAGE_MEDIA_TYPES.get(ext, "image/jpeg")
        return "__IMAGE__", f"🖼️ Image ({media_type})", raw, media_type

    return f"[UNSUPPORTED]: {name}", "📎 File"


def build_file_context(extracted_text: str, file_label: str, filename: str) -> str:
    if extracted_text == "__IMAGE__":
        return f"[IMAGE_FOR_VISION] Sama uploaded '{filename}' for visual analysis."
    if not extracted_text.strip():
        return f"Sama uploaded '{filename}' but it has no readable content."
    return (
        f"Sama uploaded a {file_label} named '{filename}'.\n"
        f"Content:\n```\n{extracted_text}\n```\n"
        "Analyze this content and help Sama understand it in your warm, cute style."
    )
