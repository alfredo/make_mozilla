from django.shortcuts import get_object_or_404, render
from make_mozilla.pages import models


def serve(request, path):
    page = get_object_or_404(models.Page, real_path=path.strip('/'))
    return render(request, 'pages/page.html', {'page': page})
