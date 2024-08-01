import os
from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.audio.fx.all import audio_fadein, audio_fadeout, audio_normalize
from moviepy.video.fx.all import speedx

# Directories
video_dir = "D:/mini projects/Video Generator/video"
audio_dir = "D:/mini projects/Video Generator/audio"
output_dir = "D:/mini projects/Video Generator/output"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

def process_video_and_audio(video_path, audio_path, output_path):
    try:
        videoclip = VideoFileClip(video_path)
        audioclip = AudioFileClip(audio_path)
        
        video_duration = videoclip.duration
        audio_duration = audioclip.duration

        # Remove original audio if it exists
        videoclip = videoclip.without_audio()

        # Adjust speed of audio and video based on their durations
        if video_duration < audio_duration:
            audioclip = audioclip.set_duration(video_duration).fx(audio_fadein, 0.1).fx(audio_fadeout, 0.1)
            audioclip = audioclip.fx(speedx, factor=audio_duration / video_duration)
        elif video_duration <= 15:
            videoclip = videoclip.set_duration(video_duration * 1.8).fx(speedx, factor=video_duration / (video_duration * 1.8))
            audioclip = audioclip.set_duration(video_duration * 1.8).fx(audio_fadein, 0.1).fx(audio_fadeout, 0.1)
        elif video_duration == audio_duration:
            videoclip = videoclip.set_duration(video_duration * 1.8).fx(speedx, factor=video_duration / (video_duration * 1.8))
            audioclip = audioclip.set_duration(video_duration * 1.8).fx(audio_fadein, 0.1).fx(audio_fadeout, 0.1)
        else:
            videoclip = videoclip.set_duration(audio_duration).fx(speedx, factor=video_duration / audio_duration)

        # Set the audio of the video to the adjusted audio file
        videoclip = videoclip.set_audio(audioclip)

        # Save the final video
        videoclip.write_videofile(output_path, codec="libx264", audio_codec="aac")

        # Close the clips to release resources
        videoclip.close()
        audioclip.close()
    except Exception as e:
        print(f"Error processing {video_path} and {audio_path}: {e}")

# Get sorted lists of video and audio files
video_files = sorted([f for f in os.listdir(video_dir) if f.endswith(('.mp4', '.avi', '.mov'))], key=lambda x: int(os.path.splitext(x)[0]))
audio_files = sorted([f for f in os.listdir(audio_dir) if f.endswith(('.mp3', '.wav', '.aac'))], key=lambda x: int(os.path.splitext(x)[0]))

# Process each video and audio pair
for video_file, audio_file in zip(video_files, audio_files):
    video_path = os.path.join(video_dir, video_file)
    audio_path = os.path.join(audio_dir, audio_file)
    output_path = os.path.join(output_dir, f"output_{video_file}")
    
    process_video_and_audio(video_path, audio_path, output_path)

print("Processing complete.")
