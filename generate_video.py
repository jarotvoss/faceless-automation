import asyncio
import os
import edge_tts
from moviepy.editor import TextClip, AudioFileClip, ColorClip, CompositeVideoClip

# Configuration
TEXT_SCRIPT = (
    "Stop spending hours editing videos. "
    "Here is how you can run a fully automated content machine "
    "straight from an iPad without ever showing your face!"
)
VOICE = "en-US-AriaNeural"  # Natural-sounding free Edge-TTS voice
OUTPUT_AUDIO = "voiceover.mp3"
OUTPUT_VIDEO = "output_short.mp4"

async def generate_audio():
    print("Generating voiceover with Edge-TTS...")
    communicate = edge_tts.Communicate(TEXT_SCRIPT, VOICE)
    await communicate.save(OUTPUT_AUDIO)

def build_video():
    print("Compiling video with MoviePy...")
    # Load audio to get exact duration
    audio = AudioFileClip(OUTPUT_AUDIO)
    duration = audio.duration

    # Create a simple background (Vertical 1080x1920 for Shorts/Reels)
    bg = ColorClip(size=(1080, 1920), color=(15, 15, 25), duration=duration)

    # Add text overlay (ensure ImageMagick or standard caption text is configured)
    txt_clip = (
        TextClip(
            TEXT_SCRIPT,
            fontsize=60,
            color='white',
            size=(900, None),
            method='caption',
            align='center'
        )
        .set_duration(duration)
        .set_position('center')
    )

    # Combine background, text, and audio
    video = CompositeVideoClip([bg, txt_clip]).set_audio(audio)
    
    # Write output file (lightweight encoding for GitHub Actions runners)
    video.write_videofile(
        OUTPUT_VIDEO,
        fps=24,
        codec='libx264',
        audio_codec='aac',
        preset='ultrafast'
    )
    print(f"Successfully generated video: {OUTPUT_VIDEO}")

if __name__ == "__main__":
    asyncio.run(generate_audio())
    build_video()
