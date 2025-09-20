import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.title("🎬 VideoDit - Demo")

uploaded_file = st.file_uploader("Upload MP4", type=["mp4"])

if uploaded_file:
    if st.button("Upload to Backend"):
        files = {"file": (uploaded_file.name, uploaded_file, "video/mp4")}
        res = requests.post(f"{BACKEND_URL}/api/videos/upload", files=files)

        if res.ok:
            video_info = res.json()
            st.success("✅ Uploaded successfully!")
            st.json(video_info)
            video_id = video_info["id"]

            # Show uploaded video
            st.video(f"{BACKEND_URL}/media/{video_info['file_path'].split('/')[-1]}")

            # --- Trim video ---
            st.subheader("✂️ Trim Video")
            start = st.number_input("Start (sec)", 0)
            end = st.number_input("End (sec)", 10)
            if st.button("Trim Video"):
                res = requests.post(
                    f"{BACKEND_URL}/api/videos/trim",
                    params={"video_id": video_id, "start": start, "end": end},
                )
                if res.ok:
                    trim_info = res.json()
                    st.success("✅ Trimmed video!")
                    st.video(f"{BACKEND_URL}/media/{trim_info['filepath'].split('/')[-1]}")
                else:
                    st.error(res.text)

            # --- Text Overlay ---
            st.subheader("📝 Text Overlay")
            text = st.text_input("Overlay Text")
            if st.button("Add Text Overlay"):
                res = requests.post(
                    f"{BACKEND_URL}/api/videos/{video_id}/overlay/text",
                    params={"text": text},
                )
                if res.ok:
                    overlay_info = res.json()
                    st.success("✅ Overlay applied!")
                    st.video(f"{BACKEND_URL}/media/{overlay_info['filepath'].split('/')[-1]}")
                else:
                    st.error(res.text)

            # --- Watermark ---
            st.subheader("💧 Add Watermark")
            watermark_file = st.file_uploader("Upload Watermark (PNG)", type=["png"])
            if watermark_file and st.button("Add Watermark"):
                # Save watermark temporarily to send to backend
                files = {"file": (watermark_file.name, watermark_file, "image/png")}
                res = requests.post(
                    f"{BACKEND_URL}/api/videos/{video_id}/watermark",
                    files=files,
                )
                if res.ok:
                    wm_info = res.json()
                    st.success("✅ Watermark added!")
                    st.video(f"{BACKEND_URL}/media/{wm_info['filepath'].split('/')[-1]}")
                else:
                    st.error(res.text)

        else:
            st.error(f"❌ Error: {res.text}")
