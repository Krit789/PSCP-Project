'''Prevent Cross Site Scripting (XSS) with Bleach'''
import bleach

def md_cleaner(text: str) -> str:
    ALLOWED_TAGS = [
    "h1", "h2", "h3", "h4", "h5", "h6", "hr",
    "ul", "ol", "li", "p", "br",
    "pre", "code", "blockquote",
    "strong", "em", "a", "img", "b", "i",
    "table", "thead", "tbody", "tr", "th", "td",
    ]
    ALLOWED_ATTRIBUTES = {
        "h1": ["id"], "h2": ["id"], "h3": ["id"],  "h4": ["id"],
        "a": ["href", "title"],
        "img": ["src", "title", "alt"],
    }
    ALLOWED_PROTOCOLS = ["http", "https", "mailto"]
    cleaner = bleach.Cleaner(
                tags=ALLOWED_TAGS,
                attributes=ALLOWED_ATTRIBUTES,
                protocols=ALLOWED_PROTOCOLS)
    return cleaner.clean(text)