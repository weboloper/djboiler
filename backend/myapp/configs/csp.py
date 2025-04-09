from csp.constants import SELF

CONTENT_SECURITY_POLICY = {
    "EXCLUDE_URL_PREFIXES": ["/admin"],
    "DIRECTIVES": {
        "default-src": [SELF],
        "script-src": [
            SELF,
            "cdnjs.cloudflare.com",
            "https://accounts.google.com",
            "https://apis.google.com",
            "https://www.gstatic.com",
            "http://code.jquery.com",
            "https://*.s3.amazonaws.com",
            "'unsafe-inline'",  # Allow inline scripts, cautiously
            "'unsafe-eval'",    # Required for Alpine.js dynamic features
        ],
        "style-src": [
            SELF,
            "fonts.googleapis.com",
            "cdnjs.cloudflare.com",
            "https://accounts.google.com/gsi/style",
            "https://*.s3.amazonaws.com",
            "'unsafe-inline'",  # Allow inline styles cautiously
        ],
        "img-src": [
            SELF,
            "data:",
            "https://*.s3.amazonaws.com",
            "https://www.gstatic.com",  # Allow images from your domain and Google
        ],
        "font-src": [
            SELF,
            "fonts.gstatic.com",
            "https://fonts.gstatic.com",
            "cdnjs.cloudflare.com",
        ],
        "connect-src": [
            SELF,
            "https://csp.withgoogle.com",  # Allow Google sign-in API sources
            "https://accounts.google.com",
            "https://accounts.google.com/gsi/",
            "https://apis.google.com",
        ],
        "frame-src": [
            SELF,
            "https://accounts.google.com/gsi/",  # Disallow embedding in iframes
        ],
        "object-src": [
            SELF,
            "https://accounts.google.com/gsi/",  # Disallow Flash and other embedded objects
        ],
        "media-src": [SELF],
    },
}
