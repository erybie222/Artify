import streamlit as st
from models.style_transfer import style_transfer
from PIL import Image
import os
import uuid

# Tytuł aplikacji
st.title("🎨 Artify – Neural Style Transfer App")

st.markdown("""
Zamień swoje zdjęcie w obraz w stylu Van Gogha, Picassa i innych!  
Wgraj zdjęcie i wybierz styl poniżej:
""")


content_file = st.file_uploader("📤 Wgraj obraz treści (content)", type=["jpg", "jpeg", "png"])


style_dir = "assets/style"
style_options = [f for f in os.listdir(style_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
style_choice = st.selectbox("🎨 Wybierz styl:", style_options)


if content_file and style_choice:
    content_img = Image.open(content_file)
    style_img_path = os.path.join(style_dir, style_choice)

    st.image(content_img, caption="🖼️ Obraz treści", use_container_width=True)
    st.image(style_img_path, caption="🎨 Obraz stylu", use_container_width=True)

    if st.button("🔄 Stylizuj!"):
        with st.spinner("Przetwarzanie... może chwilę potrwać ⏳"):

            content_path = f"temp_{uuid.uuid4()}.jpg"
            if content_img.mode == 'RGBA':
                content_img = content_img.convert('RGB')

            content_img.save(content_path)

            print("🔄 Stylizacja start...")
            output_img = style_transfer(content_path, style_img_path)
            print("✅ Stylizacja zakończona.")


            st.success("Gotowe!")
            st.image(output_img, caption="🖌️ Wynik", use_container_width=True)


            output_file = f"artify_result_{uuid.uuid4().hex[:8]}.jpg"
            output_img.save(output_file)

            with open(output_file, "rb") as f:
                btn = st.download_button(
                    label="📥 Pobierz obraz",
                    data=f,
                    file_name="stylized.jpg",
                    mime="image/jpeg"
                )


            os.remove(content_path)
            os.remove(output_file)
