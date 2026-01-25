# Permissions and Groups Setup (bookshelf)

## Custom Permissions
Defined in `CustomUser` model:
- can_view
- can_create
- can_edit
- can_delete

## Groups
- **Editors**: can_view, can_create, can_edit
- **Viewers**: can_view
- **Admins**: all permissions

## Usage
Views are protected using `@permission_required`.  
Assign users to groups via Django Admin or programmatically.  
Test by logging in as different users and verifying access control.

# HTTPS and Secure Redirects in Django

## Django Settings
- `SECURE_SSL_REDIRECT = True` → forces HTTPS
- `SECURE_HSTS_SECONDS = 31536000` → 1 year HSTS policy
- `SECURE_HSTS_INCLUDE_SUBDOMAINS = True` → applies to subdomains
- `SECURE_HSTS_PRELOAD = True` → allows preload list inclusion
- `SESSION_COOKIE_SECURE = True` → session cookies only over HTTPS
- `CSRF_COOKIE_SECURE = True` → CSRF cookies only over HTTPS
- `X_FRAME_OPTIONS = "DENY"` → prevents clickjacking
- `SECURE_CONTENT_TYPE_NOSNIFF = True` → prevents MIME sniffing
- `SECURE_BROWSER_XSS_FILTER = True` → enables browser XSS protection

## Deployment
- Configured Nginx/Apache to redirect HTTP → HTTPS
- Installed SSL/TLS certificates
- Enforced modern TLS protocols and ciphers

## Security Review
- All traffic is encrypted via HTTPS
- Cookies are secure and not sent over HTTP
- Headers protect against XSS, clickjacking, and MIME sniffing
- Potential improvement: add Content Security Policy (CSP) for stricter script/style control