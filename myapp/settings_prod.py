from .settings_base import *

DEBUG = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = config('SMTP_EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('SMTP_EMAIL_PORT', 587)
EMAIL_HOST_USER = config('SMTP_EMAIL_USER')
EMAIL_HOST_PASSWORD = config('SMTP_EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default="webmaster@example.com") 


# Auto-reconnect on startup
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
# Production settings 
CELERY_BROKER_URL= config("CELERY_BROKER_REDIS_URL", default="redis://localhost:6379")
CELERY_RESULT_BACKEND= config("CELERY_BROKER_REDIS_URL", default="redis://localhost:6379")
CELERY_TASK_ALWAYS_EAGER = False  # Tasks run asynchronously
CELERYD_POOL = 'prefork'  # Default pool for production (can handle concurrency)

# Optionally, configure Celery Beat (task scheduler) in production
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'




# Enforce HTTPS connections
SECURE_SSL_REDIRECT = True  # Redirect all HTTP traffic to HTTPS
SECURE_HSTS_SECONDS = 31536000  # Enable HSTS for one year (recommended)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Apply HSTS to subdomains
SECURE_HSTS_PRELOAD = True  # Allow browser preload list (optional)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# Prevent MIME-type sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True  

# Prevent clickjacking attacks
X_FRAME_OPTIONS = "DENY"  # Options: DENY, SAMEORIGIN

# Enable browser XSS protection
SECURE_BROWSER_XSS_FILTER = True  

# Referrer Policy
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"  

# Permissions Policy (limits access to browser features)
PERMISSIONS_POLICY = {
    "geolocation": "self",
    "microphone": "none",
    "camera": "none",
    "fullscreen": "self",
    }

 





# Allow scripts and styles only from the same origin and specific sources
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "cdnjs.cloudflare.com", "'unsafe-inline'")  # Allow inline scripts cautiously
CSP_STYLE_SRC = ("'self'", "fonts.googleapis.com", "'unsafe-inline'")  # Allow inline styles cautiously
CSP_IMG_SRC = ("'self'", "data:", "cdn.example.com")  # Allow images from your domain and CDNs
CSP_FONT_SRC = ("'self'", "fonts.gstatic.com")
CSP_CONNECT_SRC = ("'self'", "api.example.com")  # Allow AJAX/WS connections to this domain
CSP_FRAME_SRC = ("'none'",)  # Disallow embedding in iframes
CSP_OBJECT_SRC = ("'none'",)  # Disallow Flash and other embedded objects
CSP_MEDIA_SRC = ("'self'",)


# Allow Alpine.js & HTMX if using them
CSP_SCRIPT_SRC += ("'unsafe-eval'",)  # Required for Alpine.js dynamic features
CSP_REPORT_URI = "/csp-report/"  # Endpoint to capture CSP violation reports
