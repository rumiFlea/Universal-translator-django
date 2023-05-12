from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import SpeechToTextForm
from faster_whisper import WhisperModel
import whisper
import os, shutil
import torch
import subprocess

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(os.path.dirname(FILE_DIR), "outputs")

def download_all_files():
        shutil.make_archive("outputs", "txt", OUTPUT_DIR)

class SpeechToTextView(FormView):
    template_name = 'index.html'
    form_class = SpeechToTextForm
    success_url = reverse_lazy('process_audio')

    def form_valid(self, form):
        audio_file = form.cleaned_data['audio']
        model = whisper.load_model("base")

        file_path = "/tmp/" + audio_file.name
        with open(file_path, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)

        

        model_size = "base"

        model = WhisperModel(model_size, device="cpu", compute_type="int8")

        segments, info = model.transcribe(file_path, beam_size=5, task="translate")
        text = ''
        for segment in segments:
            #text.append(segment.text)
            text = text + segment.text


        # run whisper command with arguments
        # command = ["whisper", f"{audio}", "--language", "Japanese", "--task", "translate"]
        # process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # # capture output and errors
        # output, error = process.communicate()

        # context = output.decode()

        context = self.get_context_data()
        context['language'] = info[0]
        context['text'] = text
        # TODO: save the text to a file

        return self.render_to_response(context)
