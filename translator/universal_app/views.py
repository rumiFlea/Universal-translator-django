from django.urls import reverse_lazy
from .forms import SpeechToTextForm
import whisper
import torch

class SpeechToTextView(FormView):
    template_name = 'index.html'
    form_class = SpeechToTextForm
    success_url = reverse_lazy('process_audio')

    def form_valid(self, form):
        audio_file = form.cleaned_data['audio']
        model = whisper.load_model("base")

        file_path = "/tmp/" + str(audio_file)
        with open(file_path, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)

        audio = whisper.load_audio(file_path)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        _, probs = model.detect_language(mel)
        language = max(probs, key=probs.get)

        options = whisper.DecodingOptions(fp16=False)
        result = whisper.decode(model, mel, options)

        context = self.get_context_data()
        context['language'] = language
        context['text'] = result.text

        return self.render_to_response(context)