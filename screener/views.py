from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import ResumeUploadForm
from .models import Prediction
from .ml_utils import classify_resume, extract_text_from_pdf

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('classify_resume')
    else:
        form = UserCreationForm()
    return render(request, 'screener/signup.html', {'form': form})

@login_required
def classify_resume_view(request):
    result = None
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume_file = form.cleaned_data.get('resume_file')
            resume_text = form.cleaned_data.get('resume_text')

            if resume_file:
                if resume_file.name.endswith('.pdf'):
                    text = extract_text_from_pdf(resume_file)
                else:
                    text = resume_file.read().decode('utf-8', errors='ignore')
            else:
                text = resume_text

            category, confidence = classify_resume(text)

            Prediction.objects.create(
                user=request.user,
                resume_snippet=text[:300],
                predicted_category=category,
                confidence=confidence
            )

            result = {'category': category, 'confidence': confidence}
    else:
        form = ResumeUploadForm()

    return render(request, 'screener/classify.html', {'form': form, 'result': result})

@login_required
def history_view(request):
    predictions = Prediction.objects.filter(user=request.user)
    return render(request, 'screener/history.html', {'predictions': predictions})