from transformers import pipeline

def summarize_text(long_text, max_length_, min_length_):

    summarizer = pipeline(
        task="summarization",
        model="sshleifer/distilbart-cnn-12-6",
        revision="main"
    )

    summary = summarizer(long_text, max_length=max_length_, min_length=min_length_, do_sample=False)
    return summary[0]['summary_text']