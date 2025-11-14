python -m zipvoice.bin.infer_zipvoice \
    --model-name zipvoice \
    --prompt-wav prompt.wav \
    --tokenizer espeak \
    --lang vi \
    --checkpoint-name iter-525000-avg-2.pt \
    --prompt-text "Bởi nó có nguồn gốc từ vùng nông thôn." \
    --text "Bất kì nơi nào có dấu chân của hắn, đều chất chứa nhiều nỗi đau" \
    --res-wav-path result.wav