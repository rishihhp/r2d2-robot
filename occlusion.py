import torch
import cv2
import numpy as np
import timm
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from torchvision import models

class DepthEstimator:
    def __init__(self, model_name='DPT_Large', device=None, verbose=True):
        """Initialize the depth estimation model."""
        self.verbose = verbose
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self._load_model(model_name)
        self.transform = self._get_transform()
        
    def _log(self, message):
        """Prints log messages if verbose mode is enabled."""
        if self.verbose:
            print(message)
        
    def _load_model(self, model_name):
        """Loads the MiDaS model."""
        self._log(f"Loading model: {model_name}...")
        model = torch.hub.load("intel-isl/MiDaS", model_name).to(self.device)
        model.eval()
        self._log("Model loaded successfully!")
        return model

    def _get_transform(self):
        """Returns the transformation required for the model."""
        return transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((384, 384)),  # Standard MiDaS input size
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def estimate_depth(self, image_path):
        """Estimates depth from a given image path."""
        self._log(f"Loading image: {image_path}")
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        self._log("Preprocessing image...")
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        self._log("Running inference...")
        with torch.no_grad():
            depth_map = self.model(input_tensor)
        
        self._log("Processing output...")
        depth_map = depth_map.squeeze().cpu().numpy()
        depth_map = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min())  # Normalize
        
        self._log("Depth estimation completed.")
        return depth_map

    def visualize_depth(self, depth_map):
        """Displays the depth map."""
        self._log("Displaying depth map...")
        plt.figure(figsize=(10, 5))
        plt.imshow(depth_map, cmap='inferno')
        plt.colorbar()
        plt.title("Depth Map")
        plt.axis("off")
        plt.show()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Depth Perception from a Single Image")
    parser.add_argument("image_path", type=str, help="Path to the input image")
    args = parser.parse_args()
    
    estimator = DepthEstimator()
    depth = estimator.estimate_depth(args.image_path)
    estimator.visualize_depth(depth)
