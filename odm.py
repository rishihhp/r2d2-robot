import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import cv2
import numpy as np
from typing import List, Dict
import io
import warnings
import logging

# Suppress warnings and configure logging
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('absl').setLevel(logging.ERROR)

# Load environment variables
load_dotenv()

class GeminiVisionAnalyzer:
    def __init__(self, api_key: str):
        """Initialize the Gemini Vision Analyzer with your API key."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def capture_and_analyze(self) -> Dict[str, tuple]:
        """
        Capture an image from webcam and analyze it for objects.
        
        Returns:
            Dictionary with detected objects and their displacement from the center
        """
        cap = None
        try:
            # Initialize webcam with specific properties
            cap = cv2.VideoCapture(0)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            
            if not cap.isOpened():
                raise Exception("Could not open webcam")

            print("Press SPACE to capture image (or ESC to quit)...")
            
            while True:
                # Read frame from webcam
                ret, frame = cap.read()
                if not ret:
                    raise Exception("Could not read frame")

                # Display the frame
                cv2.imshow('Webcam (Press SPACE to capture, ESC to quit)', frame)

                # Wait for key press
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESC key
                    return {}
                elif key == 32:  # SPACE key
                    break  # Capture frame and continue

            # Convert frame to PIL Image
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            
            # Image dimensions
            img_height, img_width, _ = frame.shape
            center_x, center_y = img_width // 2, img_height // 2

            # Create the prompt for object detection
            prompt = """Please analyze this image and provide a list of all visible objects.
                       Return only the objects, one per line, without any additional text or numbers.
                       Be specific but concise."""
            
            # Generate response from Gemini
            response = self.model.generate_content([prompt, pil_image])
            
            # Extract objects from the response
            seen = set()
            objects = []
            for obj in response.text.split('\n'):
                obj = obj.strip()
                if obj and obj not in seen:
                    seen.add(obj)
                    objects.append(obj)

            # Compute displacement for each object using OpenCV
            displacement_dict = self.get_object_positions(frame, objects, center_x, center_y)

            return displacement_dict
        
        except Exception as e:
            print(f"Error capturing/analyzing image: {str(e)}")
            return {}
        
        finally:
            # Ensure webcam is released
            if cap is not None:
                cap.release()
            cv2.destroyAllWindows()

    def get_object_positions(self, frame, objects, center_x, center_y) -> Dict[str, tuple]:
        """
        Detects object positions and calculates displacement.
        
        Args:
            frame (numpy array): The captured image.
            objects (list): List of detected objects.
            center_x (int): X-coordinate of the image center.
            center_y (int): Y-coordinate of the image center.
        
        Returns:
            dict: A dictionary mapping objects to (dx, dy) displacement.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        object_positions = {}

        for i, contour in enumerate(contours[:len(objects)]):  # Map detected contours to objects
            M = cv2.moments(contour)
            if M["m00"] != 0:
                obj_x = int(M["m10"] / M["m00"])
                obj_y = int(M["m01"] / M["m00"])
                dx, dy = obj_x - center_x, obj_y - center_y
                object_positions[objects[i]] = (dx, dy)

        return object_positions

def main():
    # Get API key from environment
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Please set the GOOGLE_API_KEY environment variable")
    
    analyzer = GeminiVisionAnalyzer(api_key)
    detected_objects = analyzer.capture_and_analyze()

    if detected_objects:
        print("\nObject Displacement from Center (0,0):")
        for obj, (dx, dy) in detected_objects.items():
            print(f"{obj}: ({dx}, {dy})")

if __name__ == "__main__":
    # Suppress GRPC warning
    os.environ['GRPC_ENABLE_FORK_SUPPORT'] = '0'
    
    main()
