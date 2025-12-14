import torch
import torchvision
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import time

def load_mnist(limit=1000, train=True):
    """
    Downloads and provides a subset of MNIST data.
    train=True for training set, False for test set.
    """
    mode_str = "Training" if train else "Test"
    print(f"📚 Opening the Library (MNIST {mode_str} Set)...")
    transform = transforms.Compose([
        transforms.Resize((28, 28)), # Ensure size
        transforms.ToTensor(),       # [0,1] tensor
    ])
    
    # --- Hack: Add reliable mirrors for China/Network stability ---
    # The default yann.lecun.com is often unstable or blocked.
    new_mirrors = [
        'https://ossci-datasets.s3.amazonaws.com/mnist/',
        'http://yann.lecun.com/exdb/mnist/', 
        'https://storage.googleapis.com/cvdf-datasets/mnist/'
    ]
    torchvision.datasets.MNIST.mirrors = new_mirrors

    # Download to local folder
    dataset_obj = torchvision.datasets.MNIST(root='./data', train=train,
                                        download=True, transform=transform)
    
    # Create simple iterator
    dataset = []
    for i in range(min(limit, len(dataset_obj))):
        img_tensor, label = dataset_obj[i]
        # Convert back to PIL for consistency with Retina interface
        img_pil = transforms.ToPILImage()(img_tensor)
        dataset.append((img_pil, str(label))) # Ensure label is string
        
    return dataset

def evolve_in_dreams(brain, retina, dataset, progress_callback=None):
    """
    Batch evolution loop (Deep Sleep Mode).
    """
    count = 0
    total = len(dataset)
    new_stars = 0
    
    print(f"💤 Entering Deep Sleep. Processing {total} memories...")
    
    start_time = time.time()
    
    for image, label in dataset:
        try:
            # 1. Perceive via Retina
            # Note: We must ensure image is in correct format for Retina
            features = retina.perceive(image)
            
            # 2. Memorize
            # Unlike interactive mode, we trust the dataset labels here (Supervised Batch)
            # OR we could just "perceive" and only reinforce if confident?
            # For "Mass Evolution", we typically treat it as Ground Truth teaching.
            action = brain.memorize(features, label)
            
            if "New" in action:
                new_stars += 1
                
        except Exception as e:
            print(f"❌ Nightmare (Error): {e}")
        
        count += 1
        if progress_callback:
            progress_callback(count, total)
            
    duration = time.time() - start_time
    return f"Evolution Complete. Dreamed of {total} concepts in {duration:.2f}s. {new_stars} new stars created."

def evaluate_brain(brain, retina, dataset, progress_callback=None, self_reinforce=False):
    correct = 0
    total = len(dataset)
    start_time = time.time()
    reinforced_count = 0

    for i, (image, true_label) in enumerate(dataset):
        features = retina.perceive(image)
        star, gravity = brain.perceive(features)
        pred_label = star.label if star else "?"
        
        is_correct = str(pred_label) == str(true_label)
        
        if is_correct:
            correct += 1
            # Self-Reinforcement: If I am right, I become more confident.
            # This is "Test-Time Training" or "Confirmation Bias" in action.
            if self_reinforce:
                brain.memorize(features, true_label)
                reinforced_count += 1
        
        if progress_callback:
            progress_callback(i + 1, total)
            
    duration = time.time() - start_time
    accuracy = (correct / total) * 100 if total > 0 else 0
    
    msg = f"Exam Score: {correct}/{total} ({accuracy:.2f}%). Time: {duration:.2f}s"
    if self_reinforce:
        msg += f". Reinforced {reinforced_count} correct memories."
        
    return accuracy, msg
