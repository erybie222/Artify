# 🎨 Artify – Neural Style Transfer Web App

**Artify** is a deep learning-powered web application that transforms your photos into artistic masterpieces by applying the style of famous paintings such as _Starry Night_ or _La Muse_. It uses neural style transfer with a pretrained VGG19 model to merge content and style images.

---

## 🧠 How it works

Artify leverages the [Neural Style Transfer](https://arxiv.org/abs/1508.06576) technique using a pretrained **VGG19** network from PyTorch. The algorithm minimizes a loss that blends:

- **Content loss**: how much the result resembles the original photo
- **Style loss**: how much the result reflects the texture of the selected painting

---

## 📦 Tech Stack

- Python + PyTorch
- Streamlit (frontend)
- TorchVision
- PIL (Pillow)

---

## 💻 Run locally

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/Artify.git
cd Artify
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
python -m streamlit run app.py
```
