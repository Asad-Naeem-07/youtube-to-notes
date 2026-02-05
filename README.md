# 📺 YouTube to Study Notes

Convert any YouTube video into comprehensive study notes + visual HTML guide using AI.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![LangChain](https://img.shields.io/badge/LangChain-0.1+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 📺 **YouTube Support** - Paste any YouTube URL or video ID
- 🌐 **Multi-Language** - Supports 9 languages (English, Hindi, Urdu, Spanish, etc.)
- 🗺️ **MAP-REDUCE** - Smart processing that handles long videos
- 📝 **Comprehensive Notes** - Full explanations, not just summaries
- 🎨 **HTML Visual Guide** - Beautiful concept maps with CSS styling
- 🆓 **100% FREE** - Uses free LLM APIs (Groq, OpenRouter)

## 🎬 Demo

![App Screenshot](screenshot.png)

## 🛠️ How It Works

```
┌─────────────────────────────────────────────────────────────┐
│              📺 YouTube to Study Notes                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [YouTube URL] → [Fetch Transcript] → [Split into Chunks]   │
│                                              ↓              │
│                        ┌─────────────────────┴─────────┐    │
│                        │       MAP PHASE              │    │
│                        │  Process each chunk → Notes  │    │
│                        └─────────────────────┬─────────┘    │
│                                              ↓              │
│                        ┌─────────────────────┴─────────┐    │
│                        │      REDUCE PHASE            │    │
│                        │  Merge + Deduplicate Notes   │    │
│                        └─────────────────────┬─────────┘    │
│                                              ↓              │
│                    [Final Notes] → [Generate HTML]          │
│                                              ↓              │
│                         [Download .md or .html]             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/youtube-to-notes.git
cd youtube-to-notes
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up API keys
```bash
cp .env.example .env
# Edit .env and add your API keys
```

**Get FREE API Keys:**
- 🔑 [Groq Console](https://console.groq.com/keys) - Super fast, free tier
- 🔑 [OpenRouter](https://openrouter.ai/keys) - Free models available

### 5. Run the app
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser!

## 📖 How to Use

1. **Paste YouTube URL** - Any video with captions/subtitles
2. **Select Language** - Choose transcript language (English, Hindi, etc.)
3. **Extract Transcript** - Click to fetch the video transcript
4. **Generate Notes** - AI creates comprehensive study notes
5. **Download** - Get your notes as Markdown (.md) or HTML

## 🌐 Supported Languages

| Language | Code |
|----------|------|
| English | en |
| Hindi | hi |
| Urdu | ur |
| Spanish | es |
| Turkish | tr |
| Arabic | ar |
| French | fr |
| German | de |
| Auto | auto |

## 🤖 AI Models Used (All FREE!)

| Model | Purpose | Provider |
|-------|---------|----------|
| DeepSeek R1T | Note Generation | OpenRouter |
| Trinity | HTML Generation | OpenRouter |
| Llama 3.3 70B | Alternative | Groq |

## 📁 Project Structure

```
youtube-to-notes/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables
├── .gitignore          # Git ignore rules
├── LICENSE             # MIT License
└── README.md           # This file
```

## 🎯 MAP-REDUCE Explained

### Why MAP-REDUCE?

Long videos = Long transcripts = Too much for LLM context window

**Solution: Split & Conquer!**

1. **MAP Phase**: Split transcript into chunks, extract notes from EACH chunk
2. **REDUCE Phase**: Merge all chunk notes, remove duplicates, organize logically

**Result**: Comprehensive notes without losing information!

## 🤝 Contributing

Contributions welcome! Feel free to submit a Pull Request.

## 📝 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) - LLM Framework
- [Streamlit](https://streamlit.io/) - UI Framework
- [Groq](https://groq.com/) - Fast LLM Inference
- [OpenRouter](https://openrouter.ai/) - LLM API Gateway

---

⭐ **Star this repo if you found it helpful!**
