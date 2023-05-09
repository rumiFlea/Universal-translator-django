from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from .views import SpeechToTextView

urlpatterns = [
    path('process_audio/', SpeechToTextView.as_view(), name='process_audio'),
    re_path(r'^$', lambda request: redirect('process_audio/', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)