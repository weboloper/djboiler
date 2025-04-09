
# Allow scripts and styles only from the same origin and specific sources
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = (
    "'self'", 
    "cdnjs.cloudflare.com", 
    "https://accounts.google.com", 
    "https://apis.google.com", 
    "https://www.gstatic.com", 
    "http://code.jquery.com",
    # "http://stackpath.bootstrapcdn.com",
    "'unsafe-inline'",  # Allow inline scripts, cautiously
)
CSP_STYLE_SRC = (
    "'self'", 
    "fonts.googleapis.com", 
    "cdnjs.cloudflare.com", 
    # "http://stackpath.bootstrapcdn.com",
    "https://accounts.google.com/gsi/style", 
    "'unsafe-inline'",  # Allow inline styles cautiously
)
CSP_IMG_SRC = ("'self'", "data:", "https://www.gstatic.com")  # Allow images from your domain and Google
CSP_FONT_SRC = (
    "'self'", 
    "fonts.gstatic.com", 
    "https://fonts.gstatic.com", 
    "cdnjs.cloudflare.com", 
    # "https://stackpath.bootstrapcdn.com",
)
CSP_CONNECT_SRC = (
    "'self'",
    "https://csp.withgoogle.com",  # Allow Google sign-in API sources
    "https://accounts.google.com",
    "https://accounts.google.com/gsi/",
    "https://apis.google.com",
)
CSP_FRAME_SRC = ("'self'","https://accounts.google.com/gsi/")  # Disallow embedding in iframes
CSP_OBJECT_SRC = ("'self'", "https://accounts.google.com/gsi/")  # Disallow Flash and other embedded objects
CSP_MEDIA_SRC = ("'self'",)

# Allow Alpine.js & HTMX if using them
CSP_SCRIPT_SRC += ("'unsafe-eval'",)  # Required for Alpine.js dynamic features
# CSP_REPORT_URI = "/csp-report/"  # Endpoint to capture CSP violation reports