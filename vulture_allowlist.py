# Vulture allowlist for Django project
# This file contains code that vulture should not report as dead code

# Django model fields that appear unused but are accessed via ORM
_.objects  # Django model manager
_.DoesNotExist  # Django model exception
_.MultipleObjectsReturned  # Django model exception

# Django admin
_.admin  # Django admin module imports

# Django URL patterns
_.urlpatterns  # Django URL configuration
_.app_name  # Django app namespace

# Django settings
_.DATABASES  # Django database configuration
_.INSTALLED_APPS  # Django installed applications
_.MIDDLEWARE  # Django middleware
_.ROOT_URLCONF  # Django root URL configuration
_.TEMPLATES  # Django template configuration
_.STATIC_URL  # Django static files URL
_.STATIC_ROOT  # Django static files root
_.MEDIA_URL  # Django media files URL
_.MEDIA_ROOT  # Django media files root

# Django management commands
_.handle  # Django management command method
_.add_arguments  # Django management command method

# Django migrations
_.dependencies  # Django migration dependencies
_.operations  # Django migration operations

# Django forms
_.clean  # Django form validation methods
_.save  # Django form save method

# Django views
_.get_context_data  # Django class-based view method
_.get_queryset  # Django class-based view method
_.get_object  # Django class-based view method

# Django tests
_.setUp  # Django test setup method
_.tearDown  # Django test teardown method
