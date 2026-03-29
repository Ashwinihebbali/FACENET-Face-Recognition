import os
import cv2
from utils import detect_face, get_embedding, save_data

data_path = "data/known_faces"

# Check if data directory exists
if not os.path.exists(data_path):
    print(f"Error: {data_path} directory not found!")
    exit()

encodings = []
names = []

# Iterate through each person folder
for person in os.listdir(data_path):
    person_path = os.path.join(data_path, person)
    
    # Skip if it's not a directory
    if not os.path.isdir(person_path):
        continue
    
    print(f"Processing {person}...")
    person_encodings = 0

    # Iterate through images in person's folder
    for img_name in os.listdir(person_path):
        img_path = os.path.join(person_path, img_name)
        
        # Skip if not an image file
        if not img_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            continue
        
        img = cv2.imread(img_path)
        
        # Check if image loaded successfully
        if img is None:
            print(f"Warning: Could not read image {img_path}")
            continue

        faces = detect_face(img)

        if len(faces) == 0:
            print(f"  No face found in {img_name}")
            continue

        for (x, y, w, h) in faces:
            face = img[y:y+h, x:x+w]
            emb = get_embedding(face)

            encodings.append(emb)
            names.append(person)
            person_encodings += 1

    print(f"  {person}: {person_encodings} encodings saved")

# Check if any data was collected
if len(encodings) == 0:
    print("Warning: No faces detected in any images!")
else:
    save_data(encodings, names)
    print(f"\n✅ Training Complete!")
    print(f"Total encodings: {len(encodings)}")
    print(f"Total people: {len(set(names))}")