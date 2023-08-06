# swisscore-pyTTS
Easy to use python Text To Speech (TTS) library.

Currently supported API's:
* Voice RSS (api key needed)

***Note: More API's might beeing added in the future.***

## Installation
***Note: If you are on macOS or Linux you may have to use `pip3`.***
```
pip install git+https://github.com/SwissCorePy/swisscore-pyTTS/
```

## Quick Start
```python
import os
from pathlib import Path

# Import VoiceRSS API
from pytts import VoiceRSS

# To avoid writing your API key in source code, you can set it in an environment
# variable API_KEY, then read the variable in your Python code:
api_key = os.getenv("API_KEY")

# The text to turn into speech
text = "Hello. Thank you for downloading this package."

# Setup API instance with default values
tts = VoiceRSS(
    api_key,
    hl=VoiceRSS.hl.en_us,  # Set English (United States) as default
    v=VoiceRSS.v.en_us.John,  # Set John as default voice
    c=VoiceRSS.c.MP3,  # Set MP3 as default codec
    f=VoiceRSS.f.stereo_16khz_16bit,  # Set 16khz, 16bit, stereo as default
)

# The outupt file path
out = Path(__file__).parent / "test.mp3"

# Turn the text into a file
if file := tts.to_file(text, out):
    print(f"Success! Now you can do with {file.name} what you want.")
    pass

```

