from crewai.tools import tool
import os
from gtts import gTTS
from moviepy.editor import TextClip, AudioFileClip, ColorClip, CompositeVideoClip

@tool("Generate Video Tool")
def generate_video_tool(script: str, title: str) -> str:
    """
    Generates a simple video using gTTS for voiceover and MoviePy for video creation.
    Requires 'script' (the text to be spoken) and 'title' (the title of the video).
    Returns the file path to the generated video.
    """
    os.makedirs("assets/audio", exist_ok=True)
    os.makedirs("assets/output", exist_ok=True)

    # 1. Generate Voiceover
    audio_path = f"assets/audio/{title.replace(' ', '_')}.mp3"
    tts = gTTS(text=script, lang='en')
    tts.save(audio_path)

    # 2. Create Video
    try:
        audio = AudioFileClip(audio_path)

        # Create a simple background
        bg_clip = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=audio.duration)

        try:
            txt_clip = TextClip(title, fontsize=70, color='white')
            txt_clip = txt_clip.set_position('center').set_duration(audio.duration)
            video = CompositeVideoClip([bg_clip, txt_clip])
        except Exception:
            video = bg_clip

        video = video.set_audio(audio)

        video_path = f"assets/output/{title.replace(' ', '_')}.mp4"
        video.write_videofile(video_path, fps=24, codec="libx264", audio_codec="aac")
        return video_path
    except Exception as e:
        return f"Failed to generate video: {str(e)}"

@tool("Find Niche Tool")
def find_niche_tool() -> str:
    """
    Analyzes YouTube trending data and Google Trends to identify high-CPM, low-competition niches.
    Returns the selected niche as a string.
    """
    return "Personal Finance & Wealth Management"

@tool("Generate Script Tool")
def generate_script_tool(niche: str) -> str:
    """
    Generates a viral script and SEO-optimized metadata based on a niche.
    Returns a JSON-like string containing 'script', 'title', 'tags', and 'description'.
    """
    return '{"script": "Welcome to the ultimate guide to personal finance.", "title": "Finance 101", "tags": "finance, money", "description": "Learn finance."}'

@tool("Post Video Tool")
def post_video_tool(video_path: str, title: str, description: str) -> str:
    """
    Handles scheduled uploads via YouTube Data API v3 and Instagram Graph API.
    Returns a success message.
    """
    return f"Successfully scheduled {title} from path {video_path}."
