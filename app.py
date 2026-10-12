"""ReplyPal: paste a customer review, get an on-brand reply.

Setup:
    pip install streamlit groq
    export GROQ_API_KEY="your_key_here"   # Windows: set GROQ_API_KEY=your_key_here
Run:
    streamlit run review_reply.py
"""
import os
import streamlit as st
from groq import Groq

MODEL = "openai/gpt-oss-120b"  # open-weight; swap for any model on your Groq model list

client = Groq(api_key=os.environ["GROQ_API_KEY"])

st.title("ReplyPal")
st.caption("Reply to customer reviews in your own voice, powered by an open-weight model on Groq.")

business = st.text_input("Your business (one line)", "Small handmade candle shop")
tone = st.selectbox("Tone", ["Warm and friendly", "Professional", "Playful"])
review = st.text_area("Paste the customer review", height=150)

if st.button("Write reply") and review.strip():
    prompt = (
        f"You write replies to customer reviews for this business: {business}.\n"
        f"Tone: {tone}. Keep it under 80 words. Thank them, address their specific points, "
        f"and if the review is negative, apologize sincerely and offer a fix. No emojis unless playful.\n\n"
        f"Review:\n{review}"
    )
    with st.spinner("Writing..."):
        out = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
    st.subheader("Suggested reply")
    st.write(out.choices[0].message.content)