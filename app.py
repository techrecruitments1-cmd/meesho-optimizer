import streamlit as st
from PIL import Image, ImageOps
from rembg import remove
import io

st.set_page_config(page_title="Meesho Image Optimizer", layout="centered")

st.title("📦 Meesho 'Low Shipping' Optimizer")
st.info("This tool resizes your product to 65% of the frame to help qualify for lower shipping rates.")

uploaded_file = st.file_uploader("Upload Product Photo", type=["jpg", "jpeg", "png"])

if uploaded_file:
    input_image = Image.open(uploaded_file)
    
    if st.button("Generate Optimized Image"):
        with st.spinner('Removing background and resizing...'):
            # Remove Background
            no_bg = remove(input_image)
            
            # Create 1000x1000 White Canvas
            canvas = Image.new("RGB", (1000, 1000), (255, 255, 255))
            
            # Resize product to 650px (The "Small Product" Trick)
            no_bg.thumbnail((650, 650))
            
            # Center on canvas
            off_x = (1000 - no_bg.size[0]) // 2
            off_y = (1000 - no_bg.size[1]) // 2
            
            if no_bg.mode == 'RGBA':
                canvas.paste(no_bg, (off_x, off_y), no_bg)
            else:
                canvas.paste(no_bg, (off_x, off_y))
            
            st.image(canvas, caption="Optimized for Meesho")
            
            # Download Button
            buf = io.BytesIO()
            canvas.save(buf, format="JPEG", quality=95)
            st.download_button("Download Image", buf.getvalue(), "meesho_pro.jpg", "image/jpeg")
