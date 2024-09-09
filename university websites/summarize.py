from transformers import pipeline

def summarize_text(long_text):

    summarizer = pipeline(
        task="summarization",
        model="sshleifer/distilbart-cnn-12-6",
        revision="main"
    )

    summary = summarizer(long_text, max_length=50, min_length=25, do_sample=False)
    return summary[0]['summary_text']