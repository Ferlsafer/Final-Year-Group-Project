from django.shortcuts import render,  redirect

import sys

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import SymptomHistory

def home(request):
       return render(request, 'home.html')

@login_required
def symptom_history(request):
    history = SymptomHistory.objects.filter(user=request.user).order_by('-analyzed_at')
    return render(request, 'history.html', {'history': history})


# Load the tokenizer and model from Hugging Face
model_name = "emilyalsentzer/Bio_ClinicalBERT"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

@csrf_exempt
def analyze(request):
    if request.method == 'POST':
        try:
            # Parse the JSON request body
            data = json.loads(request.body)
            symptoms = data.get('symptoms', '')

            # Tokenize the input symptoms
            inputs = tokenizer(symptoms, return_tensors="pt")

            # Perform inference
            with torch.no_grad():
                outputs = model(**inputs)

            # Get the predicted class
            logits = outputs.logits
            predicted_class = torch.argmax(logits, dim=1).item()

            # Map predicted class to conditions and medications (example mapping)
            conditions = {0: "Condition A", 1: "Condition B"}
            medications = {0: "Medication A", 1: "Medication B"}

            # Prepare the response
            response = {
                "condition": conditions.get(predicted_class, "Unknown"),
                "medication": medications.get(predicted_class, "Unknown")
            }

            return JsonResponse(response)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('symptom_history')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})