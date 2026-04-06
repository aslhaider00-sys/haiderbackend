from django.shortcuts import render
from .models import Post
# from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms
from .serializer import PostSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny

# Create your views here.
# @login_required(login_url="/users/login/")
def posts_list(request):
    posts = Post.objects.all()  .order_by('-date')                #dic post and its data parang key value
    return render(request, 'posts/posts_list.html', {'posts': posts})

def posts_page(request, slug):
    # return HttpResponse(slug)
    post = Post.objects.get(slug=slug)             #dic post and its data parang key value
    return render(request, 'posts/post_page.html', {'post': post })

#check if this function runs if the user is login if not redirect to login url
@login_required(login_url="/users/login/")
def posts_new(request):
    if request.method == 'POST':
        form = forms.CreatePost(request.POST, request.FILES)
        if form.is_valid():
            newpost = form.save(commit=False)
            newpost.author = request.user
            newpost.save()
    else:
        form = forms.CreatePost()
    return render(request, 'posts/posts_new.html', {'form': form })

@api_view(['GET'])
def demonstration_api(request):
    posts = Post.objects.all().order_by('title')
    serializer = PostSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)

import base64
import json
import numpy as np
import cv2
import os
import math
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier

# Path Settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "Model/keras_model.h5")
LABELS_PATH = os.path.join(BASE_DIR, "Model/labels.txt")


classifier = Classifier(MODEL_PATH, LABELS_PATH)
with open(LABELS_PATH, "r") as f:
    labels = [line.strip() for line in f]


# Hand detector
detector = HandDetector(maxHands=1)

# Image settings
OFFSET = 20
IMG_SIZE = 300

@csrf_exempt
def predict_gesture(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    try:
        body = json.loads(request.body)
        img_data = body.get("image")

        if not img_data:
            return JsonResponse({"error": "No image provided"}, status=400)

        # Decode base64 to OpenCV image
        nparr = np.frombuffer(base64.b64decode(img_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Flip for front camera consistency
        img = cv2.flip(img, 1)
        hands, _ = detector.findHands(img)

        if not hands:
            return JsonResponse({"gesture": "", "error": "No hands detected"})

        # Get hand bounding box
        hand = hands[0]
        x, y, w, h = hand['bbox']

        # Create White Background
        imgWhite = np.ones((IMG_SIZE, IMG_SIZE, 3), np.uint8) * 255
        
        # Crop logic with offset
        y1, y2 = max(0, y - OFFSET), min(img.shape[0], y + h + OFFSET)
        x1, x2 = max(0, x - OFFSET), min(img.shape[1], x + w + OFFSET)
        imgCrop = img[y1:y2, x1:x2]

        if imgCrop.size == 0:
            return JsonResponse({"gesture": "", "error": "Invalid crop size"})

        # Resize and Center logic
        aspectRatio = h / w

        if aspectRatio > 1:
            k = IMG_SIZE / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, IMG_SIZE))
            wGap = math.ceil((IMG_SIZE - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
        else:
            k = IMG_SIZE / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (IMG_SIZE, hCal))
            hGap = math.ceil((IMG_SIZE - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize

        # Prediction
        prediction, index = classifier.getPrediction(imgWhite, draw=False)
        predicted_label = labels[index].split()[-1]
# raw_label = labels[index]       # e.g. "0 A"
# predicted_label = raw_label.split()[-1]  # "A"

        return JsonResponse({
            "gesture": predicted_label
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)