"""
Curated FAQ knowledge base for the chatbot.

Each entry contains:
- question: canonical version used for similarity scoring
- answer: authoritative response returned to the user
- keywords: extra lexical cues that should boost similarity
"""

FAQ_DATA = [
    {
        "question": "What services does your company provide?",
        "answer": "We deliver 24x7 AI-powered customer assistance, onboarding guidance, and self-help resources tailored to your account.",
        "keywords": ["services", "provide", "offer", "capabilities"],
    },
    {
        "question": "Who are you and what is this chatbot?",
        "answer": "I'm an AI assistant built with Python, Flask, and Hugging Face's DialoGPT as part of the Codec Technologies internship assignment.",
        "keywords": ["who", "yourself", "introduce", "about you", "who are you"],
    },
    {
        "question": "What can you do?",
        "answer": "I can chat with you, answer the curated FAQs, and log every conversation in SQLite so the Codec Technologies team can review them later.",
        "keywords": ["what can you do", "capabilities", "features", "help me with"],
    },
    {
        "question": "Tell me more about Codec Technologies.",
        "answer": "Codec Technologies mentors interns on real-world AI workflows. This chatbot project demonstrates how to combine Flask, DialoGPT, and SQLite into a production-style prototype.",
        "keywords": ["codec", "codec technologies", "about codec", "internship"],
    },
    {
        "question": "How can I reset my password?",
        "answer": "You can reset your password from the login screen by selecting “Forgot password,” entering your registered email, and following the verification link we send.",
        "keywords": ["password", "reset", "forgot", "recover"],
    },
    {
        "question": "What is your refund policy?",
        "answer": "We offer a no-questions-asked refund within the first 30 days. Reach out to support with your order ID so we can process it immediately.",
        "keywords": ["refund", "return", "money back"],
    },
    {
        "question": "How do I contact support?",
        "answer": "You can chat with us here or email support@yourcompany.com anytime. For urgent issues, call +1-800-000-0000 and we will escalate it instantly.",
        "keywords": ["contact", "support", "helpdesk", "email", "phone"],
    },
    {
        "question": "What are your support hours?",
        "answer": "Our virtual agents are online around the clock, and human specialists are available Monday through Friday, 9 AM to 9 PM local time.",
        "keywords": ["hours", "availability", "open", "time"],
    },
    {
        "question": "Where can I track my order?",
        "answer": "Open your dashboard, go to Orders, and click “Track shipment.” The status updates in real time using the carrier scan data.",
        "keywords": ["track", "order", "shipping", "status"],
    },
    {
        "question": "Do you offer custom plans or pricing?",
        "answer": "Yes, we design custom plans for teams of every size. Share your goals and usage estimates, and we’ll send a tailored quote within one business day.",
        "keywords": ["pricing", "cost", "custom", "plan", "quote"],
    },
    {
        "question": "How do I get started or create an account?",
        "answer": "Sign up with your work email, verify the confirmation link, and the onboarding checklist will walk you through the initial setup in less than five minutes.",
        "keywords": ["start", "signup", "account", "create"],
    },
    {
        "question": "Can the platform integrate with other tools?",
        "answer": "Absolutely. We support native integrations with Slack, Teams, Salesforce, and Zapier, plus webhooks for anything else.",
        "keywords": ["integration", "tools", "connect", "api"],
    },
    {
        "question": "How do I report a technical issue?",
        "answer": "Send us the error details plus the steps to reproduce it, and our reliability team will take over right away.",
        "keywords": ["issue", "bug", "error", "problem"],
    },
]

