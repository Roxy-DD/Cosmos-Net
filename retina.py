import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np

class Retina:
    """
    The Eye of Cosmos-Net.
    
    It uses a pre-trained CNN (MobileNetV2) to extract high-level semantic features 
    from raw visual input. It does NOT classify; it only 'sees' and describes.
    
    Philosophy: The Eye is rigid (evolutionarily pre-determined), 
    while the Brain (Cosmos-Net) is plastic (fluid memory).
    """
    def __init__(self):
        print("👁️ Awakening the Retina (MobileNetV2)...")
        # Load pre-trained MobileNetV2
        # We use the 'default' weights (ImageNet)
        weights = models.MobileNet_V2_Weights.DEFAULT
        self.model = models.mobilenet_v2(weights=weights)
        
        # Remove the classification head (classifier)
        # We only want the features (1280-dim vector from the last average pooling)
        self.model.classifier = nn.Identity()
        
        self.model.eval() # Set to evaluation mode (no dropout, etc.)
        
        # Define the biological preprocessing (standard ImageNet normalization)
        self.preprocess = weights.transforms()

    def perceive(self, image: Image.Image) -> np.ndarray:
        """
        Input: PIL Image
        Output: Normalized Semantic Vector (numpy array)
        """
        # 1. Biological Adaptation (Convert to RGB if grayscale, resize, normalize)
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        with torch.no_grad():
            # 2. Transduction (Image -> Tensor)
            img_tensor = self.preprocess(image).unsqueeze(0) # Add batch dim
            
            # 3. Neural Encoding (Forward pass)
            # MobileNetV2 features end with a GlobalAvgPool + Classifier.
            # Since we replaced classifier with Identity, we might get the flat vector 
            # or the pool output depending on pytorch version structure.
            # Let's be safe and extract features explicitly if needed, 
            # but usually modifying classifier is enough for MobileNetV2.
            features = self.model(img_tensor)
            
            # 4. Signal Flattening
            vec = features.squeeze().numpy()
            
            # 5. Semantic Normalization (L2 Norm)
            # Makes it ready for Cosine Similarity (Gravity)
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
                
        return vec

if __name__ == "__main__":
    # Test the eye
    print("Testing Retina...")
    eye = Retina()
    
    # Create a dummy visual stimulus (Random noise)
    dummy_img = Image.fromarray(np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8))
    
    vector = eye.perceive(dummy_img)
    print(f"✅ Visual Signal Received.")
    print(f"Shape: {vector.shape} (Should be 1280 for MobileNetV2)")
    print(f"Norm: {np.linalg.norm(vector):.4f} (Should be 1.0)")
