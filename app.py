import streamlit as st
from models.style_transfer import style_transfer
from PIL import Image
import os
import uuid

# App title
st.title("🎨 Artify – Neural Style Transfer App")

st.markdown("""
Transform your photo into artwork in the style of Van Gogh, Picasso, and more!  
Upload a content image and choose a style below:
""")

# Upload content image
content_file = st.file_uploader("📤 Upload a content image", type=["jpg", "jpeg", "png"])

# Load style images
style_dir = "assets/style"
style_options = [f for f in os.listdir(style_dir) if f.endswith((".jpg", ".jpeg", ".png"))]
style_choice = st.selectbox("🎨 Choose a style image:", style_options)

# When both images are ready
if content_file and style_choice:
    content_img = Image.open(content_file)
    style_img_path = os.path.join(style_dir, style_choice)

    st.image(content_img, caption="🖼️ Content Image", use_container_width=True)
    st.image(style_img_path, caption="🎨 Style Image", use_container_width=True)

    if st.button("🔄 Stylize!"):
        with st.spinner("Processing... This may take a moment ⏳"):

            content_path = f"temp_{uuid.uuid4()}.jpg"
            if content_img.mode == 'RGBA':
                content_img = content_img.convert('RGB')

            content_img.save(content_path)

            print("🔄 Style transfer started...")
            output_img = style_transfer(content_path, style_img_path)
            print("✅ Style transfer completed.")

            st.success("Done!")
            st.image(output_img, caption="🖌️ Stylized Result", use_container_width=True)

            output_file = f"artify_result_{uuid.uuid4().hex[:8]}.jpg"
            output_img.save(output_file)

            with open(output_file, "rb") as f:
                btn = st.download_button(
                    label="📥 Download image",
                    data=f,
                    file_name="stylized.jpg",
                    mime="image/jpeg"
                )

            os.remove(content_path)
            os.remove(output_file)
