from fastapi import Request

def detect_language(request: Request) -> str:
    """Detect the user's preferred language from cookies or headers."""
    cookie_lang = request.cookies.get("lang")
    header_lang = request.headers.get("Accept-Language", "en")[:2]
    return cookie_lang if cookie_lang in ["en", "pl"] else header_lang if header_lang in ["en", "pl"] else "en" 