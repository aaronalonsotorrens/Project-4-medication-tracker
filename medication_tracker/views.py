from django.shortcuts import render

def error_404_view(request, exception):
    return render(request, 'errors/404.html', status=404)

def error_500_view(request):
    return render(request, 'errors/500.html', status=500)

def error_403_view(request, exception):
    return render(request, 'errors/403.html', status=403)

def error_405_view(request, exception):
    return render(request, 'errors/405.html', status=405)