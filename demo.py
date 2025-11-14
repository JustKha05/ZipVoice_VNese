import sys
import subprocess
import tempfile
from pathlib import Path

import streamlit as st


def run_zipvoice(prompt_file, prompt_text, text_to_gen, model_name="zipvoice"):
    """
    Gọi lệnh:
    python -m zipvoice.bin.infer_zipvoice \
        --model-name ... \
        --prompt-wav ... \
        --prompt-text ... \
        --text ... \
        --res-wav-path ...
    rồi đọc file wav ra để phát trên web.
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

    # Cho dễ debug nếu lỗi
    st.text("🔧 Đang chạy lệnh:")
    st.code(" ".join(cmd))

    # Chạy infer
    subprocess.run(cmd, check=True)

    # Đọc lại file audio vừa sinh ra
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

        st.success("✅ Đã generate xong!")
        st.audio(audio_bytes, format="audio/wav")


if __name__ == "__main__":
    main()
