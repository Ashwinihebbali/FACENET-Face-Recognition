import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
from utils import detect_face, get_embedding, load_data

st.title("FACENET ⚡ Face Recognition System")

encodings, names = load_data()


# -------------------------------
# FACE RECOGNITION FUNCTION
# -------------------------------
def recognize(frame, debug=False):
    faces = detect_face(frame)

    if len(faces) == 0:
        return frame, "Not Detected", None

    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]
        emb = get_embedding(face)

        if len(encodings) == 0:
            label = "No Data"
            confidence = 0
        else:
            enc = np.array(encodings)
            distances = np.linalg.norm(enc - emb, axis=1)
            min_dist = np.min(distances)
            max_dist = np.max(distances)
            idx = np.argmin(distances)

            # ADJUSTED THRESHOLD for 10000-dimensional embeddings
            threshold = 50.0  # For 10000-dim vectors
            
            if min_dist < threshold:
                label = names[idx]
                confidence = round((1 - min_dist / threshold) * 100, 2)
            else:
                label = "Unknown Member"
                confidence = 0

            if debug:
                print(f"\n=== RECOGNITION DEBUG ===")
                print(f"Min distance: {min_dist:.4f}")
                print(f"Max distance: {max_dist:.4f}")
                print(f"Embedding size: {len(emb)}")
                print(f"Database size: {enc.shape}")
                print(f"Threshold: {threshold}")
                print(f"Top 5 distances: {sorted(distances)[:5]}")
                print(f"Matched person: {names[idx]} | Distance: {min_dist:.4f}")
                print(f"========================\n")

        # BOUNDING BOX
        color = (0, 255, 0) if label != "Unknown Member" else (0, 0, 255)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
        
        # TEXT
        text = f"{label}"
        cv2.putText(frame, text, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    return frame, label, confidence if len(faces) > 0 else None


# =================================
# UI OPTIONS
# =================================
option = st.radio("Select Option", ["Capture & Train", "Upload & Train", "Test", "View Database"])

# =================================
# VIEW DATABASE
# =================================
if option == "View Database":
    st.subheader("📊 Trained Faces Database")
    
    if not encodings:
        st.warning("No trained data available yet!")
    else:
        st.info(f"✅ Total Encodings: {len(encodings)}")
        st.info(f"✅ Total People: {len(set(names))}")
        
        # Show breakdown
        st.write("### People trained:")
        for person in sorted(set(names)):
            count = names.count(person)
            st.write(f"👤 **{person}**: {count} images")
        
        # Show images
        st.write("### Training Images:")
        data_path = "data/known_faces"
        if os.path.exists(data_path):
            for person in sorted(os.listdir(data_path)):
                person_path = os.path.join(data_path, person)
                if os.path.isdir(person_path):
                    st.write(f"**{person}:**")
                    cols = st.columns(5)
                    for idx, img_name in enumerate(sorted(os.listdir(person_path))):
                        if idx < 5:
                            img_path = os.path.join(person_path, img_name)
                            cols[idx].image(Image.open(img_path), width=100, caption=img_name)


# =================================
# CAPTURE & TRAIN
# =================================
if option == "Capture & Train":
    st.subheader("📸 Capture & Train New Face")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Enter Name").strip()
    with col2:
        num_images = st.slider("Number of images", 5, 30, 20)

    if st.button("Start Capture", key="capture_btn"):
        if not name:
            st.warning("⚠️ Enter name first")
        else:
            save_path = f"data/known_faces/{name}"
            os.makedirs(save_path, exist_ok=True)

            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                st.error("❌ Camera not accessible! Please check:")
                st.write("• Camera is connected")
                st.write("• Camera permissions are granted")
                st.write("• No other app is using the camera")
            else:
                count = 0
                progress_bar = st.progress(0)
                status_text = st.empty()
                frame_window = st.image([])
                
                st.info(f"📍 Position your face in center. Capturing {num_images} clear images...")
                st.info("💡 Tip: Move slightly between captures for better variety")

                while count < num_images:
                    ret, frame = cap.read()

                    if not ret:
                        st.error("Failed to grab frame!")
                        break

                    frame = cv2.flip(frame, 1)
                    frame_window.image(frame, channels="BGR", width=400)
                    
                    progress = count / num_images
                    progress_bar.progress(progress)

                    faces = detect_face(frame)

                    if len(faces) > 0:
                        (x, y, w, h) = faces[0]
                        face = frame[y:y+h, x:x+w]

                        cv2.imwrite(f"{save_path}/{count}.png", face)
                        status_text.write(f"✅ Captured {count+1}/{num_images}")
                        count += 1

                        import time
                        time.sleep(0.5)
                    else:
                        status_text.write(f"⏳ Waiting for face... ({count}/{num_images})")

                cap.release()

                progress_bar.progress(1.0)
                status_text.write("🔄 Training model...")
                
                os.system("python train.py")
                
                st.success(f"✅ Trained {num_images} images for {name}!")
                st.balloons()


# =================================
# UPLOAD & TRAIN
# =================================
elif option == "Upload & Train":
    st.subheader("📤 Upload Images & Train")
    
    name = st.text_input("Enter Name").strip()
    files = st.file_uploader("Upload Images (10+ recommended)", accept_multiple_files=True, type=["png", "jpg", "jpeg"])

    if st.button("Train Uploaded Images", key="upload_btn"):
        if not name:
            st.warning("⚠️ Enter name first")
        elif not files:
            st.warning("⚠️ Upload at least 5 images")
        else:
            save_path = f"data/known_faces/{name}"
            os.makedirs(save_path, exist_ok=True)

            progress_bar = st.progress(0)
            status_text = st.empty()

            for i, file in enumerate(files):
                try:
                    img = Image.open(file)
                    img.save(f"{save_path}/{i}.png")
                    
                    progress = (i + 1) / len(files)
                    progress_bar.progress(progress)
                    status_text.write(f"📤 Processing: {i+1}/{len(files)}")
                    
                except Exception as e:
                    st.error(f"Error with {file.name}: {e}")

            status_text.write("🔄 Training model...")
            os.system("python train.py")
            
            st.success(f"✅ Trained {len(files)} images for {name}!")
            st.balloons()


# =================================
# TEST (RECOGNITION)
# =================================
elif option == "Test":
    st.subheader("🧪 Test Face Recognition")
    
    mode = st.radio("Mode", ["Webcam", "Upload Image"])

    if mode == "Upload Image":
        file = st.file_uploader("Upload Image to Test", type=["png", "jpg", "jpeg"])

        if file:
            img = Image.open(file)
            frame = np.array(img)

            result_img, label, confidence = recognize(frame, debug=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.image(file, caption="Original Image", width=300)
            with col2:
                st.image(result_img, caption=f"Recognition Result", channels="BGR", width=300)
                
            st.divider()
            
            if label == "Unknown Member":
                st.warning(f"❓ **{label}** - Face not in database")
            elif label == "No Data":
                st.error("⚠️ No trained data. Please train faces first!")
            elif label == "Not Detected":
                st.error("⚠️ No face detected in image")
            else:
                st.success(f"✅ **{label}** recognized!")

    else:
        st.write("### 📹 Live Camera Feed")
        st.info("Real-time face recognition. Make sure to train faces first!")

        run = st.checkbox("Start Camera", key="webcam_check")
        FRAME_WINDOW = st.image([])
        status_text = st.empty()

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            st.error("❌ Camera not accessible!")
        else:
            while run:
                ret, frame = cap.read()
                
                if not ret:
                    st.error("Camera error!")
                    break

                frame = cv2.flip(frame, 1)
                result_img, label, confidence = recognize(frame)

                FRAME_WINDOW.image(result_img, channels="BGR")
                
                if label == "Not Detected":
                    status_text.write("⏳ No face detected")
                elif label == "No Data":
                    status_text.write("⚠️ No trained data")
                elif label == "Unknown Member":
                    status_text.write(f"❓ {label}")
                else:
                    status_text.write(f"✅ **{label}**")

            cap.release()


# =================================
# SIDEBAR
# =================================
st.sidebar.markdown("---")
st.sidebar.subheader("ℹ️ Information")
st.sidebar.write("""
**FACENET Face Recognition**

**Best Practices:**
- 15-20 images per person
- Vary angles & lighting
- Clear, frontal face photos
- Good camera quality

**Troubleshooting:**
- Low recognition? Add more images
- Poor lighting? Improve brightness
- Blurry images? Keep still longer
""")

st.sidebar.subheader("📊 Database")
if encodings:
    st.sidebar.success(f"✅ {len(encodings)} encodings")
    st.sidebar.info(f"👥 {len(set(names))} people")
else:
    st.sidebar.warning("No data yet")