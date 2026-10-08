import streamlit as st
import numpy as np
from PIL import Image
from copy import deepcopy
import os

# Page configuration
st.set_page_config(page_title="SVD Image Restoration", page_icon="🖼️", layout="wide")

st.title("Truncated SVD Image Restoration 🖼️✨")
st.markdown("This interactive application restores damaged images (scratches, folds) using Truncated Singular Value Decomposition (SVD).")

# Sidebar for hyperparameters
st.sidebar.header("⚙️ Hyperparameters")
k = st.sidebar.slider("Retained Singular Values (k)", min_value=10, max_value=200, value=50, step=5)
max_iter = st.sidebar.slider("Maximum Iterations", min_value=10, max_value=300, value=100, step=10)
epsilon = st.sidebar.number_input("Convergence Tolerance (epsilon)", min_value=1e-6, max_value=1e-2, value=1e-4, format="%.1e")

# Core mathematical function: Truncated SVD
def svd_truncated(A, k):
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    S[k:] = 0
    return U @ np.diag(S) @ Vt

# Iterative function to process a single channel (Grayscale or RGB component)
def process_channel(channel, mask, k, max_iter, epsilon):
    restored = deepcopy(channel)
    for i in range(max_iter):
        Ak = svd_truncated(restored, k)
        new_channel = channel * (1 - mask) + Ak * mask
        diff = np.linalg.norm(restored - new_channel, ord='fro')
        restored = new_channel
        if diff < epsilon:
            break
            
    # Calculate Frobenius norm only on the masked area
    diff_mask = mask * (restored - channel)
    local_norm = np.linalg.norm(diff_mask, ord='fro')
    return restored, local_norm, i + 1

# Input selection (Built-in examples vs File Upload)
st.subheader("📥 Input Data")
data_source = st.radio(
    "Choose an image source:",
    ("Use built-in example (Color Horse)", "Use built-in example (Grayscale Horse)", "Upload my own images")
)

img_pil = None
mask_pil = None

if data_source == "Use built-in example (Color Horse)":
    if os.path.exists("cheval-abime2.png") and os.path.exists("cheval-abime2-mask.png"):
        img_pil = Image.open("cheval-abime2.png")
        mask_pil = Image.open("cheval-abime2-mask.png").convert('L')
    else:
        st.error("⚠️ Default images not found! Make sure 'cheval-abime2.png' and 'cheval-abime2-mask.png' are in the same folder as this script.")
elif data_source == "Use built-in example (Grayscale Horse)":
    if os.path.exists("cheval-abime2-nb.png") and os.path.exists("cheval-abime2-mask.png"):
        img_pil = Image.open("cheval-abime2-nb.png")
        mask_pil = Image.open("cheval-abime2-mask.png").convert('L')
    else:
        st.error("⚠️ Default images not found! Make sure 'cheval-abime2-nb.png' and 'cheval-abime2-mask.png' are in the same folder as this script.")
else:
    col1, col2 = st.columns(2)
    with col1:
        img_file = st.file_uploader("Upload damaged image (PNG, JPG)", type=['png', 'jpg', 'jpeg'])
    with col2:
        mask_file = st.file_uploader("Upload binary mask (areas to restore in white)", type=['png', 'jpg', 'jpeg'])
    
    if img_file and mask_file:
        img_pil = Image.open(img_file)
        mask_pil = Image.open(mask_file).convert('L')

if img_pil and mask_pil:
    # Convert to normalized numpy arrays [0, 1]
    img_np = np.array(img_pil) / 255.0
    mask_np = np.array(mask_pil) / 255.0
    
    # Strict binarization of the mask
    mask_np = (mask_np > 0.5).astype(float)
    
    st.write("---")
    st.write("### 🔍 Input Preview")
    c1, c2 = st.columns(2)
    c1.image(img_np, caption="Original Damaged Image", use_container_width=True)
    c2.image(mask_np, caption="Alteration Mask", use_container_width=True)
    
    # Execution button
    if st.button("🚀 Run Restoration", type="primary"):
        # Auto-detect: Grayscale (2D) or Color (3D)
        is_color = len(img_np.shape) == 3
        
        with st.spinner("Restoring image... (Computing linear algebra via SVD)"):
            if is_color:
                restored_channels = []
                norms = []
                iters_list = []
                
                # Process each channel (R, G, B) independently
                for c in range(3):
                    restored_c, norm_c, iters = process_channel(img_np[:, :, c], mask_np, k, max_iter, epsilon)
                    restored_channels.append(restored_c)
                    norms.append(norm_c)
                    iters_list.append(iters)
                    
                # Reconstruct the final image
                img_restored = np.stack(restored_channels, axis=2)
                img_restored = np.clip(img_restored, 0, 1) # Safeguard for display
                
                st.success("✅ Restoration complete!")
                
                st.write("### ✨ Final Result")
                st.image(img_restored, caption="Restored Color Image", use_container_width=True)
                
                st.write("### 📊 Convergence Metrics (Frobenius Norm)")
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Global Average", f"{np.mean(norms):.4f}")
                m2.metric("Red Channel (R)", f"{norms[0]:.4f}")
                m3.metric("Green Channel (G)", f"{norms[1]:.4f}")
                m4.metric("Blue Channel (B)", f"{norms[2]:.4f}")
                
            else:
                # Grayscale image
                img_restored, norm, iters = process_channel(img_np, mask_np, k, max_iter, epsilon)
                img_restored = np.clip(img_restored, 0, 1)
                
                st.success(f"✅ Restoration complete in {iters} iterations!")
                
                st.write("### ✨ Final Result")
                st.image(img_restored, caption="Restored Grayscale Image", use_container_width=True, clamp=True)
                
                st.write("### 📊 Convergence Metric")
                st.metric("Frobenius Norm (Masked Area)", f"{norm:.4f}")