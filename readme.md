# FACENET Face Recognition System

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-5C3EE8?style=flat-square&logo=opencv)](https://opencv.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](https://opensource.org/licenses/MIT)
[![Status: Active](https://img.shields.io/badge/Status-Active-success?style=flat-square)](https://github.com/yourusername/FACENET-Face-Recognition)

**Real-time face recognition system with webcam capture, model training, and instant recognition powered by Streamlit and OpenCV.**

### 🎯 Core Features
- 📸 **Webcam Capture** - Auto-detect and capture face images
- 📤 **Batch Upload** - Train with existing image collections
- 🧪 **Real-time Testing** - Test with webcam or upload
- 📊 **Database Viewer** - Monitor trained faces

</td>
<td width="50%">

### 🚀 Advanced Capabilities
- ✅ Auto-face detection and capture
- 🎨 Color-coded recognition feedback
- 📈 Real-time confidence scoring
- 💾 Persistent face database
- 🔄 Auto-encoding conversion
- ⚠️ Comprehensive error handling

</td>
</tr>
</table>

---

## 🚀 Quick Start

Get up and running in 5 minutes!

### Prerequisites
- Python 3.8+
- Webcam (for capture feature)
- 500MB disk space

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/FACENET-Face-Recognition.git
cd FACENET-Face-Recognition

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On macOS/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download Haar Cascade Classifier
mkdir models
# Download from: https://github.com/opencv/opencv/raw/master/data/haarcascades/haarcascade_frontalface_default.xml
# Save to: models/haarcascade_frontalface_default.xml

# Run the application
streamlit run app.py
```

Open your browser at `http://localhost:8501` 🎉

---

## 📖 Usage

### 1. Capture & Train

Train the system with your face in real-time:

```
1. Select "Capture & Train"
2. Enter your name
3. Click "Start Capture"
4. Position face in center (app auto-captures 20 images)
5. Wait for training to complete
```

**Best Practices:**
- ✅ Use good lighting (natural light preferred)
- ✅ Capture from different angles
- ✅ Keep face clear and centered
- ✅ Use 15-20 images minimum

### 2. Upload & Train

Use existing images to train:

```
1. Select "Upload & Train"
2. Enter your name
3. Upload 5-10 clear face images
4. Click "Train"
5. System trains automatically
```

**Supported Formats:** PNG, JPG, JPEG

### 3. Test Recognition

Test face recognition in two modes:

**Webcam Mode:**
```
1. Select "Test" → "Webcam"
2. Click "Start Camera"
3. Real-time face recognition begins
4. Uncheck to stop
```

**Upload Mode:**
```
1. Select "Test" → "Upload Image"
2. Upload a photo
3. System identifies the face
4. Shows confidence score
```

### 4. View Database

Monitor your trained faces:

```
1. Select "View Database"
2. See total encodings and people count
3. View per-person statistics
4. See thumbnail previews
```

---

## 📁 Project Structure

```
FACENET-Face-Recognition/
├── README.md                              # This file
├── LICENSE                                # MIT License
├── requirements.txt                       # Python dependencies
├── .gitignore                             # Git ignore rules
│
├── app.py                                 # Main Streamlit application
├── train.py                               # Model training script
├── utils.py                               # Utility functions
│
├── models/
│   └── haarcascade_frontalface_default.xml   # Face detector
│
├── data/
│   └── known_faces/                       # Training images (auto-created)
│       ├── Person1/
│       └── Person2/
│
└── encodings.pkl                          # Face database (auto-created)
```

---

## 🧠 How It Works

### 1. **Face Detection**
Uses Haar Cascade Classifier to detect face regions in images/video frames

### 2. **Embedding Generation**
Extracts 10,000-dimensional feature vectors combining:
- Histogram-based features
- Gradient-based features (HOG-like)
- Direct pixel values
- Edge detection features
- Multi-scale features

### 3. **Face Recognition**
Compares embeddings using Euclidean distance:
- Distance < 50.0 → **Recognized** ✅
- Distance ≥ 50.0 → **Unknown** ❌

### 4. **Database Storage**
Face encodings stored in `encodings.pkl` with:
- Automatic format conversion
- Backward compatibility
- Fast serialization

## 🎓 Learning Resources

This project demonstrates:

- **Computer Vision** - Face detection with Haar Cascades
- **Feature Extraction** - Embedding generation techniques
- **Distance-based Matching** - Euclidean distance recognition
- **Web Development** - Streamlit framework
- **Machine Learning Workflow** - Training → Inference
- **Python Best Practices** - Logging, error handling

---

## 📈 Future Enhancements

- [ ] Deep learning embeddings (FaceNet, VGGFace2)
- [ ] Multiple faces in single image
- [ ] Real-time face tracking
- [ ] Attendance system integration
- [ ] Database export/import
- [ ] Mobile app version
- [ ] Performance optimizations

---

## 📋 Requirements

```
streamlit==1.28.0
opencv-python==4.8.0.74
pillow==10.0.0
numpy==1.24.0
scikit-learn==1.3.0
```

Install all with:
```bash
pip install -r requirements.txt
```


## 💡 Use Cases

- 🎓 **Educational** - Learn computer vision and ML
- 🔒 **Security** - Access control systems
- 📸 **Photography** - Auto-tagging face images
- 👥 **Events** - Attendance tracking
- 🏢 **Organization** - Employee identification
