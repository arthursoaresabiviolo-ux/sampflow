from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. List of public URLs (which the user CAN access without logging in)
        public_urls = [
            reverse('login'),
            reverse('forgot_password'),
        ]

        # 2. Ensures that the tested URL always ends with '/'.
        path = request.path_info if request.path_info.endswith('/') else f"{request.path_info}/"

        # 3. Allow access to static and media files in the development environment and internal admin/API routes
        is_public_path = path in public_urls or path.startswith('/static/')

        # 4. Check if the user is NOT authenticated and trying to access a private page
        if not request.user.is_authenticated and not is_public_path:
            # Redirect to login including the destination page (next)
            login_url = reverse('login')
            return redirect(f"{login_url}?next={request.path}")

        response = self.get_response(request)
        return response