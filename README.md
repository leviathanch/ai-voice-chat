This is the script I'm using for talking to GPT3 on OpenAI

It requires an API key, which you should export in your bash environment:
    export OPENAI_API_KEY=<API KEY>

For getting the visual output execute:

    python3 ReVidia-Audio-Visualizer/ReVidiaGUI.py &

This will visualize the synthesized audio output on your default output device

Then execute
    python3 interface.py

You will have one button for starting to capture your voice, when you stop recording
your text will automatically be transcribed, sent to GPT3 and the response will be
synthesized into a voice and played.
