from myapp.settings import USE_SSL
if USE_SSL:
    # Enable SSL-related settings
    SECURE_SSL_REDIRECT = True  # Force all HTTP traffic to HTTPS
    SECURE_HSTS_SECONDS = 31536000  # Enable HSTS for one year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Apply to subdomains
    SECURE_HSTS_PRELOAD = True  # Allow preload
else:
    # Disable SSL-related settings if not using SSL
    SECURE_SSL_REDIRECT = False  # No SSL redirect
    SECURE_HSTS_SECONDS = 0  # Disable HSTS

# Secure cookie and XSS-related settings (can be True for both)
SESSION_COOKIE_SECURE = True  # Cookies are secure in both cases
CSRF_COOKIE_SECURE = True  # CSRF cookies are secure in both cases
SECURE_CONTENT_TYPE_NOSNIFF = True  # MIME sniffing protection
X_FRAME_OPTIONS = "SAMEORIGIN"  # Allow iframes from the same origin
SECURE_BROWSER_XSS_FILTER = True  # Enable XSS protection

# Referrer Policy
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"  

# Permissions Policy (limits access to browser features)
PERMISSIONS_POLICY = {
    "geolocation": "self",
    "microphone": "none",
    "camera": "none",
    "fullscreen": "self",
    }
