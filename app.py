# ============================================================================
#  📺 YOUTUBE TO STUDY NOTES - AI-Powered Note Generator
# ============================================================================
#  Author: Asad Naeem
#  Description: Convert YouTube videos into comprehensive study notes + HTML
#  Features: Multi-language support, MAP-REDUCE processing, Visual HTML export
# ============================================================================

import streamlit as st
import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()


# ============================================================================
#                       🤖 LLM SETUP (ALL FREE!)
# ============================================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def get_groq_llm():
    """Groq LLM - Llama 3.3 70B (FREE & FAST)"""
    if not GROQ_API_KEY:
        st.error("⚠️ GROQ_API_KEY not found in .env file!")
        return None
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        max_tokens=2000,
    )


def get_deepseek_llm():
    """OpenRouter - DeepSeek (FREE) - Best for notes"""
    if not OPENROUTER_API_KEY:
        st.error("⚠️ OPENROUTER_API_KEY not found in .env file!")
        return None
    return ChatOpenAI(
        model="tngtech/deepseek-r1t-chimera:free",
        openai_api_key=OPENROUTER_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.3,
        max_tokens=4000,
    )


def get_trinity_llm():
    """OpenRouter - Trinity (FREE) - Best for HTML generation"""
    if not OPENROUTER_API_KEY:
        st.error("⚠️ OPENROUTER_API_KEY not found in .env file!")
        return None
    return ChatOpenAI(
        model="arcee-ai/trinity-large-preview:free",
        openai_api_key=OPENROUTER_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.7,
        max_tokens=2000,
    )


# ============================================================================
#                       📺 YOUTUBE TRANSCRIPT
# ============================================================================

# Supported languages
LANGUAGE_OPTIONS = {
    "English": "en",
    "Hindi": "hi",
    "Urdu": "ur",
    "Spanish": "es",
    "Turkish": "tr",
    "Arabic": "ar",
    "French": "fr",
    "German": "de",
    "Auto (Any Available)": "auto"
}


def extract_video_id(user_input: str) -> str:
    """Extract YouTube video ID from URL or return as-is."""
    if "youtube.com/watch?v=" in user_input:
        return user_input.split("watch?v=")[1].split("&")[0]
    elif "youtu.be/" in user_input:
        return user_input.split("youtu.be/")[1].split("?")[0]
    return user_input.strip()


def get_youtube_transcript(video_id: str, language_code: str = "en") -> dict:
    """Fetch transcript from a YouTube video."""
    try:
        api = YouTubeTranscriptApi()

        try:
            if language_code == "auto":
                transcript_list = api.fetch(video_id)
                language = "auto"
            else:
                transcript_list = api.fetch(video_id, languages=[language_code])
                language = language_code
        except Exception:
            transcript_list = api.fetch(video_id)
            language = "auto (fallback)"

        if not transcript_list:
            return {"success": False, "transcript": None, "language": None, "error": "No transcript available"}

        transcript = " ".join(segment.text for segment in transcript_list)
        return {"success": True, "transcript": transcript, "language": language, "error": None}

    except TranscriptsDisabled:
        return {"success": False, "transcript": None, "language": None, "error": "Captions are disabled for this video"}
    except Exception as e:
        return {"success": False, "transcript": None, "language": None, "error": str(e)}


# ============================================================================
#                       📝 TEXT PROCESSING
# ============================================================================

def split_transcript_into_chunks(transcript: str, chunk_size: int = 2000, chunk_overlap: int = 200) -> list:
    """Split transcript into manageable chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return text_splitter.split_text(transcript)


# ============================================================================
#                       🗺️ MAP PHASE - Extract Notes from Chunks
# ============================================================================

def create_map_prompt():
    """Create prompt for extracting notes from each chunk."""
    template = """You are an expert educational content creator. Create clear, comprehensive notes from this video transcript chunk.

**IMPORTANT: Always write notes in ENGLISH, even if transcript is in another language.**

**Your Task:**
1. Extract ALL key concepts and topics
2. KEEP all explanations from the transcript
3. Add simple examples where helpful
4. Organize with headings and bullet points
5. Translate non-English content to English

**Rules:**
- DON'T summarize - include full explanations
- DON'T skip details
- DO use clear structure (headings, bullets)
- DO explain technical terms simply
- ALWAYS output in English

**Transcript Chunk:**
{chunk}

**Generated Notes (in English):**"""

    return PromptTemplate(input_variables=["chunk"], template=template)


def process_chunk_to_notes(chunk: str, prompt, llm) -> str:
    """Process a single chunk through the LLM."""
    chain = prompt | llm
    result = chain.invoke({"chunk": chunk})
    return result.content.strip()


def map_phase_extract_notes(chunks: list, prompt, llm) -> list:
    """MAP Phase: Extract notes from each chunk."""
    chunk_notes = []
    for i, chunk in enumerate(chunks):
        st.write(f"📝 Processing chunk {i+1}/{len(chunks)}...")
        notes = process_chunk_to_notes(chunk, prompt, llm)
        chunk_notes.append(notes)
    return chunk_notes


# ============================================================================
#                       🔄 REDUCE PHASE - Merge & Deduplicate
# ============================================================================

def create_reduce_prompt():
    """Create prompt for merging all chunk notes."""
    template = """You are an expert educational content organizer. Merge these notes from multiple video chunks into ONE comprehensive document.

**Your Task:**
1. Merge all chunk notes into ONE document
2. Remove duplicate concepts
3. Organize topics logically
4. Maintain ALL explanations and examples
5. Create smooth transitions

**Rules:**
- DON'T lose important information
- DO remove redundant explanations
- DO organize in learning-friendly order
- DO use markdown formatting
- DO create a table of contents

**All Chunk Notes:**
{all_notes}

**Final Merged Notes:**"""

    return PromptTemplate(input_variables=["all_notes"], template=template)


def reduce_phase_merge_notes(chunk_notes: list, llm) -> str:
    """REDUCE Phase: Merge all chunk notes into one clean document."""
    all_notes = "\n\n---CHUNK SEPARATOR---\n\n".join(chunk_notes)
    reduce_prompt = create_reduce_prompt()
    chain = reduce_prompt | llm
    result = chain.invoke({"all_notes": all_notes})
    return result.content.strip()


# ============================================================================
#                       🎨 HTML GENERATION
# ============================================================================

def create_html_prompt():
    """Create prompt for generating visual HTML page."""
    template = """Create a simple, clean HTML page showing a VISUAL OVERVIEW of these study notes.

**KEEP IT SIMPLE - Show main concepts as a visual diagram!**

**Structure:**
1. Title at top
2. Visual "concept map" with colored boxes and arrows
3. Brief bullet points under each concept

**CSS Rules:**
- Colored boxes (divs) for each concept
- Flexbox layout
- Arrows using → symbols
- Clean, readable fonts
- Mobile friendly

**Technical Rules:**
- NO external libraries
- ALL CSS in <style> tag
- Simple HTML only
- Colorful but simple

**Study Notes:**
{notes}

**Output HTML (start with <!DOCTYPE html>):**"""

    return PromptTemplate(input_variables=["notes"], template=template)


def generate_html_page(notes: str, llm) -> str:
    """Generate visual HTML page from notes."""
    html_prompt = create_html_prompt()
    chain = html_prompt | llm
    result = chain.invoke({"notes": notes})
    html_content = result.content

    # Clean up markdown code blocks if present
    if "```html" in html_content:
        html_content = html_content.split("```html")[1].split("```")[0]
    elif "```" in html_content:
        html_content = html_content.split("```")[1].split("```")[0]

    return html_content.strip()


# ============================================================================
#                       🎯 MAIN APP
# ============================================================================

def main():
    st.set_page_config(
        page_title="YouTube to Study Notes",
        page_icon="📺",
        layout="centered"
    )

    st.title("📺 YouTube to Study Notes")
    st.caption("Convert any YouTube video into comprehensive study notes + HTML visual guide!")

    # Initialize session state
    if "transcript" not in st.session_state:
        st.session_state.transcript = None
    if "chunks" not in st.session_state:
        st.session_state.chunks = None
    if "language" not in st.session_state:
        st.session_state.language = None
    if "combined_notes" not in st.session_state:
        st.session_state.combined_notes = None
    if "html_content" not in st.session_state:
        st.session_state.html_content = None
    if "ready_for_html" not in st.session_state:
        st.session_state.ready_for_html = False

    # Initialize LLMs
    llm_notes = get_deepseek_llm()  # For note generation
    llm_html = get_trinity_llm()    # For HTML generation

    # =========================================================================
    # STEP 1: YouTube URL Input
    # =========================================================================
    
    st.subheader("1️⃣ Enter YouTube Video")
    
    youtube_input = st.text_input(
        "🔗 YouTube URL or Video ID",
        placeholder="https://www.youtube.com/watch?v=..."
    )

    selected_language = st.selectbox(
        "🌐 Transcript Language",
        options=list(LANGUAGE_OPTIONS.keys()),
        index=0,
        help="Choose the language. Falls back to any available if not found."
    )

    if st.button("📥 Extract Transcript", type="primary"):
        if not youtube_input.strip():
            st.warning("Please enter a YouTube URL or video ID.")
            st.stop()

        with st.status("📥 Fetching transcript...", expanded=True) as status:
            video_id = extract_video_id(youtube_input)
            language_code = LANGUAGE_OPTIONS[selected_language]
            st.write(f"🔹 Video ID: `{video_id}`")
            st.write(f"🌐 Language: `{selected_language}`")

            result = get_youtube_transcript(video_id, language_code)

            if not result["success"]:
                st.error(f"❌ {result['error']}")
                status.update(label="Failed", state="error")
                st.stop()

            st.session_state.transcript = result["transcript"]
            st.session_state.language = result["language"]
            st.session_state.chunks = split_transcript_into_chunks(result["transcript"])
            
            status.update(label="✅ Transcript extracted!", state="complete")

    # =========================================================================
    # STEP 2: Show Transcript & Generate Notes
    # =========================================================================
    
    if st.session_state.transcript:
        st.divider()
        st.subheader("2️⃣ Transcript Ready")
        
        st.success(f"✅ {len(st.session_state.transcript)} characters | {len(st.session_state.chunks)} chunks")

        with st.expander("📄 View Full Transcript"):
            st.text(st.session_state.transcript)

        st.divider()
        st.subheader("3️⃣ Generate Study Notes")

        if st.button("🎓 Generate Notes", type="primary"):
            with st.status("🧠 Generating notes...", expanded=True) as status:
                st.write("⚙️ Using DeepSeek AI...")
                map_prompt = create_map_prompt()

                # MAP Phase
                st.write(f"🗺️ MAP: Processing {len(st.session_state.chunks)} chunks...")
                chunk_notes = map_phase_extract_notes(st.session_state.chunks, map_prompt, llm_notes)
                st.write(f"✅ Extracted from {len(chunk_notes)} chunks")

                # REDUCE Phase
                st.write("🔄 REDUCE: Merging & deduplicating...")
                final_notes = reduce_phase_merge_notes(chunk_notes, llm_notes)
                st.write("✅ Notes merged!")

                st.session_state.combined_notes = final_notes
                st.session_state.ready_for_html = True
                status.update(label="✅ Notes generated!", state="complete")

    # =========================================================================
    # STEP 3: Show Notes & Download
    # =========================================================================
    
    if st.session_state.combined_notes:
        st.divider()
        st.subheader("📚 Your Study Notes")
        st.markdown(st.session_state.combined_notes)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "⬇️ Download Notes (.md)",
                st.session_state.combined_notes,
                file_name="study_notes.md",
                mime="text/markdown"
            )

        with col2:
            if st.button("🎨 Generate HTML Visual"):
                with st.status("🎨 Creating HTML...", expanded=True) as html_status:
                    st.write("⚙️ Using Trinity AI...")
                    html_content = generate_html_page(st.session_state.combined_notes, llm_html)
                    st.session_state.html_content = html_content
                    html_status.update(label="✅ HTML ready!", state="complete")

    # =========================================================================
    # STEP 4: Show HTML Preview & Download
    # =========================================================================
    
    if st.session_state.html_content:
        st.divider()
        st.subheader("🎨 HTML Visual Guide")

        with st.expander("👀 Preview"):
            st.components.v1.html(st.session_state.html_content, height=600, scrolling=True)

        st.download_button(
            "⬇️ Download HTML",
            st.session_state.html_content,
            file_name="study_notes.html",
            mime="text/html",
            type="primary"
        )


if __name__ == "__main__":
    main()
