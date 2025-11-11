from django.http import HttpResponse
from django.core.management import call_command
from django.contrib.auth.decorators import user_passes_test

def is_superuser(user):
    return user.is_superuser

def create_temp_superuser_view(request):
    try:
        # It's better to capture the output from the command
        from io import StringIO
        out = StringIO()
        call_command('create_temp_superuser', stdout=out)
        response_message = out.getvalue().replace('\n', '<br>')
        return HttpResponse(f"Command output:<br><pre>{response_message}</pre>")
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)
