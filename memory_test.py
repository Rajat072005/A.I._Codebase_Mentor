import os
import psutil

process = psutil.Process(os.getpid())

def print_ram(step):
    print(f"{step:<35} | {process.memory_info().rss / 1024 / 1024:.1f} MB")

print_ram("Base Python RAM")

import flask
print_ram("After importing Flask")

import torch
print_ram("After importing PyTorch")

from sentence_transformers import SentenceTransformer
print_ram("After importing SentenceTransformers")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
print_ram("After loading MiniLM Model")

import sklearn
print_ram("After importing scikit-learn")

import joblib
classifier = joblib.load("classifier/models/intent_classifier.pkl")
print_ram("After loading Intent Classifier")

