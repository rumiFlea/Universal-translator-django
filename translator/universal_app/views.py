from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import SpeechToTextForm
import whisper
import torch
import subprocess

class SpeechToTextView(FormView):
    template_name = 'index.html'
    form_class = SpeechToTextForm
    success_url = reverse_lazy('process_audio')

    def form_valid(self, form):
        audio_file = form.cleaned_data['audio']
        model = whisper.load_model("medium")
        
        file_path = "/tmp/" + str(audio_file)
        with open(file_path, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)

        audio = whisper.load_audio(file_path)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        _, probs = model.detect_language(mel)
        language = max(probs, key=probs.get)

        # Run whisper command with arguments for translation
        command = ["whisper", file_path, "--language", language, "--task", "translate"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Capture output and errors
        output, error = process.communicate()
        english_text = output.decode()

        # Handle any errors
        if process.returncode != 0:
            print(f"Error: {error.decode()}")
            english_text = "An error occurred during translation."

        context = self.get_context_data()
        context['language'] = language
        context['text'] = english_text

        return self.render_to_response(context)
