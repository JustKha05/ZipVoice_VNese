import sys
import subprocess
import tempfile
from pathlib import Path

import streamlit as st


def run_zipvoice(prompt_file, prompt_text, text_to_gen, model_name="zipvoice"):
    """
    Gọi lệnh:
    python -m zipvoice.bin.infer_zipvoice ...
    và in ra log nếu có lỗi.
    """
    # Lưu file audio upload thành file tạm
    suffix = Path(prompt_file.name).suffix or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
        f.write(prompt_file.read())
        prompt_path = f.name

    out_path = Path("result_streamlit.wav")

    cmd = [
        sys.executable,
        "-m",
        "zipvoice.bin.infer_zipvoice",
        "--model-name",
        model_name,
        "--prompt-wav",
        prompt_path,
        "--prompt-text",
        prompt_text,
        "--text",
        text_to_gen,
        "--res-wav-path",
        str(out_path),
    ]

    st.markdown("### 🔧 Lệnh đang chạy")
    st.code(" ".join(cmd))

    # ❗ Không dùng check=True, và capture stdout/stderr
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    st.markdown("### 📤 STDOUT (output của script)")
    st.code(result.stdout or "(trống)")

    st.markdown("### 📕 STDERR (lỗi chi tiết, nếu có)")
    st.code(result.stderr or "(trống)")

    if result.returncode != 0:
        st.error(f"Lệnh infer bị lỗi (exit code = {result.returncode}). Xem STDERR ở trên.")
        return None

    if not out_path.exists():
        st.error("Không tìm thấy file kết quả result_streamlit.wav.")
        return None

    audio_bytes = out_path.read_bytes()
    return audio_bytes



def main():
    st.set_page_config(page_title="ZipVoice VNese demo", page_icon="🎙️")
    st.title("🎙️ ZipVoice VNese – Zero-shot TTS")
    st.write(
        "Upload **prompt audio** + nhập **prompt text** và **text cần đọc** "
        "→ ZipVoice sẽ sinh ra file audio mới."
    )

    # Sidebar chọn model
    with st.sidebar:
        st.header("Cấu hình")
        model_name = st.selectbox(
            "Chọn model",
            ["zipvoice"],
            index=0,
            help="Chọn model muốn dùng",
        )

    # Input chính
    prompt_file = st.file_uploader(
        "Prompt audio (giọng mẫu) – nên dùng .wav", type=["wav", "flac", "mp3"]
    )

    prompt_text = st.text_area(
        "Prompt text (nội dung của file prompt audio)",
        value="Xin chào, tôi là giọng nói mẫu.",
        height=70,
    )

    text_to_gen = st.text_area(
        "Text muốn generate",
        value="Đây là câu nói được sinh ra bằng ZipVoice.",
        height=120,
    )

    if st.button("🚀 Generate audio"):
        if prompt_file is None:
            st.error("Bạn cần upload **prompt audio** trước.")
            return
        if not text_to_gen.strip():
            st.error("Text muốn generate đang trống.")
            return

        with st.spinner("Đang tổng hợp giọng nói..."):
            audio_bytes = run_zipvoice(
                prompt_file=prompt_file,
                prompt_text=prompt_text,
                text_to_gen=text_to_gen,
                model_name=model_name,
            )
        
        if audio_bytes is None:
            return

        st.success("✅ Đã generate xong!")
        st.audio(audio_bytes, format="audio/wav")


if __name__ == "__main__":
    main()
