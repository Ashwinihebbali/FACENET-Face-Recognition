import cv2
import numpy as np
import pickle
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load face cascade classifier
cascade_path = "models/haarcascade_frontalface_default.xml"

if not os.path.exists(cascade_path):
    logger.error(f"Cascade file not found at {cascade_path}")
    face_cascade = None
else:
    face_cascade = cv2.CascadeClassifier(cascade_path)
    if face_cascade.empty():
        logger.error(f"Failed to load cascade classifier from {cascade_path}")
        face_cascade = None


def detect_face(image):
    """
    Detect faces in an image using Haar Cascade classifier.
    """
    if image is None:
        logger.warning("Received None image for face detection")
        return np.array([])
    
    if face_cascade is None:
        logger.error("Cascade classifier not loaded")
        return np.array([])
    
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        return faces
    except Exception as e:
        logger.error(f"Error in face detection: {e}")
        return np.array([])


def get_embedding(face):
    """
    Generate embedding (feature vector) from a face image.
    Generates 10000-dimensional vector.
    """
    if face is None or face.size == 0:
        logger.warning("Received invalid face image for embedding")
        return np.zeros((10000,))
    
    try:
        # Ensure face is in BGR format
        if len(face.shape) != 3 or face.shape[2] != 3:
            logger.warning("Face image is not BGR format, converting...")
            face = cv2.cvtColor(face, cv2.COLOR_GRAY2BGR)
        
        # Resize to standard size
        face_resized = cv2.resize(face, (100, 100))
        gray = cv2.cvtColor(face_resized, cv2.COLOR_BGR2GRAY)
        
        # Extract multiple features
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        
        gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        magnitude, angle = cv2.cartToPolar(gx, gy)
        magnitude = cv2.normalize(magnitude, magnitude).flatten()
        
        pixels = gray.flatten() / 255.0
        
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        laplacian = cv2.normalize(laplacian, laplacian).flatten()
        
        gray_small = cv2.resize(gray, (50, 50))
        pixels_small = gray_small.flatten() / 255.0
        
        # Combine features to 10000 dimensions
        embedding = np.concatenate([
            hist[:1000],
            magnitude[:2000],
            pixels[:3000],
            laplacian[:2000],
            pixels_small[:1000],
            np.ones(1000) * np.std(pixels)
        ])
        
        if len(embedding) < 10000:
            embedding = np.pad(embedding, (0, 10000 - len(embedding)), mode='constant')
        else:
            embedding = embedding[:10000]
        
        # Normalize
        embedding = embedding / (np.linalg.norm(embedding) + 1e-6)
        
        return embedding
        
    except Exception as e:
        logger.error(f"Error in embedding generation: {e}")
        return np.zeros((10000,))


def convert_old_encoding_to_new(old_encoding):
    """
    Convert old 30000-dimensional encoding to new 10000-dimensional format.
    Uses dimensionality reduction via averaging.
    """
    if len(old_encoding) != 30000:
        return old_encoding  # Return as-is if not old format
    
    # Reshape 30000 -> 10000 by taking every 3rd element or averaging
    new_encoding = np.zeros(10000)
    
    # Simple method: take every 3rd element
    for i in range(10000):
        if i * 3 < len(old_encoding):
            new_encoding[i] = old_encoding[i * 3]
    
    # Normalize
    new_encoding = new_encoding / (np.linalg.norm(new_encoding) + 1e-6)
    
    return new_encoding


def save_data(encodings, names):
    """
    Save face encodings and names to pickle file.
    """
    if not encodings or not names:
        logger.warning("No data to save")
        return False
    
    if len(encodings) != len(names):
        logger.error("Mismatch: number of encodings != number of names")
        return False
    
    try:
        with open("encodings.pkl", "wb") as f:
            pickle.dump((encodings, names), f)
        logger.info(f"Successfully saved {len(encodings)} encodings")
        return True
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        return False


def load_data():
    """
    Load face encodings and names from pickle file.
    Automatically converts old 30000-dim encodings to new 10000-dim format.
    """
    if not os.path.exists("encodings.pkl"):
        logger.info("No encodings.pkl file found. Starting with empty database.")
        return [], []

    try:
        with open("encodings.pkl", "rb") as f:
            encodings, names = pickle.load(f)
        
        # Check if encodings are old format (30000-dim) and convert
        if len(encodings) > 0:
            first_encoding = np.array(encodings[0])
            if len(first_encoding) == 30000:
                logger.info("🔄 Detected old encoding format (30000-dim). Converting to new format (10000-dim)...")
                encodings = [convert_old_encoding_to_new(np.array(enc)) for enc in encodings]
                
                # Save converted encodings
                try:
                    with open("encodings.pkl", "wb") as f:
                        pickle.dump((encodings, names), f)
                    logger.info("✅ Encodings converted and saved successfully!")
                except Exception as e:
                    logger.warning(f"Could not save converted encodings: {e}")
        
        logger.info(f"✅ Successfully loaded {len(encodings)} encodings for {len(set(names))} people")
        return encodings, names
        
    except pickle.UnpicklingError as e:
        logger.error(f"Error unpickling data: {e}")
        return [], []
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return [], []