"""
The Voice RSS Text-to-Speech (TTS) API allows conversion of textual content to speech easier than ever. 

Website: https://www.voicerss.org/
"""


from pathlib import Path
from typing import Any, Optional

import requests

from .. import logger
from . import formats
from . import languages
from . import codecs
from . import voices


class VoiceRSS:
    """
    The Voice RSS Text-to-Speech (TTS) API
    """

    URL = "http://api.voicerss.org/"
    """the url of this api"""

    hl = languages
    """summary of all languages this api supports"""

    v = voices
    """summary of all voices of the selected language this api supports"""

    c = codecs
    """summary of all codecs this api supports"""

    f = formats
    """summary of all formats this api supports"""

    def __init__(
        self,
        api_key: str,
        hl: str,
        v: Optional[str] = None,
        r: Optional[int] = None,
        c: Optional[str] = None,
        f: Optional[str] = None,
        ssml: Optional[bool] = None,
        b64: Optional[bool] = None,
    ) -> None:
        """
        You can set default values to use for all

        :param api_key: Required. The API key. Get your own API key here https://www.voicerss.org/login.aspx
        :param hl: Required. The textual content language.
            Allows values: see Languages.
        :param v: Required. The speech voice.
            Allows values: see Voices.
            Default value: depends on a language.
        :param r: Optional. The speech rate (speed).
            Allows values: from -10 (slowest speed) up to 10 (fastest speed).
            Default value: 0 (normal speed).
        :param c: Optional. The speech audio codec.
            Allows values: see Audio Codecs.
            Default value: WAV.
        :param f: Optional. The speech audio formats.
            Allows values: see Audio Formats.
            Default value: 8khz_8bit_mono.
        :param ssml: Optional. The SSML textual content format (see SSML documentation).
            Allows values: true and false.
            Default value: false.
        :param b64: Optional. Defines output as a Base64 string format (for an internet browser playing).
            Allows values: true and false.
            Default value: false.
        """
        self.api_key = api_key
        self.lang = hl
        self.voice = v
        self.rate = r
        self.codec = c
        self.format = f
        self.ssml = ssml
        self.b64 = b64

    def _request(self, **params: Any) -> bytes | None:
        params["key"] = self.api_key
        r = requests.request("POST", self.URL, params=params)
        data = r.content
        if data.startswith(b"ERROR: "):
            logger.error(
                f"A request to the {self.__class__.__name__} API was unsuccessful: {data.decode()}"
            )
            return

        return data

    def to_file(
        self,
        src: str,
        out: Path | str,
        hl: Optional[str] = None,
        v: Optional[str] = None,
        r: Optional[int] = None,
        c: Optional[str] = None,
        f: Optional[str] = None,
        *,
        ssml: Optional[bool] = None,
        b64: Optional[bool] = None,
    ) -> Path | None:
        """
        :param src: The textual content for converting to speech (length limited by 100KB).
        :param out: The path to save the result to.
            If the file exists, it will be overwritten.
            Note: The file must match the codec.
        :param hl: Mandatory. The textual content language.
            Allows values: see Languages.
        :param v: Optional. The speech voice.
            Allows values: see Voices.
            Default value: depends on a language.
        :param r: Optional. The speech rate (speed).
            Allows values: from -10 (slowest speed) up to 10 (fastest speed).
            Default value: 0 (normal speed).
        :param c: Optional. The speech audio codec.
            Allows values: see Audio Codecs.
            Default value: WAV.
        :param f: Optional. The speech audio formats.
            Allows values: see Audio Formats.
            Default value: 8khz_8bit_mono.
        :param ssml: Optional. The SSML textual content format (see SSML documentation).
            Allows values: true and false.
            Default value: false.
        :param b64: Optional. Defines output as a Base64 string format (for an internet browser playing).
            Allows values: true and false.
            Default value: false.
        :return: The result file as bytes
        """
        if isinstance(out, str):
            out = Path(out)

        if not out.parent.exists():
            logger.error(f"'{str(out.parent)}' not found!")
            return

        if out.exists():
            logger.warn(f"'{out.name}' already exists. It will be overwritten!")

        if content := self.to_bytes(src, hl, v, r, c, f, ssml=ssml, b64=b64):
            with out.open("wb") as _out:
                _out.write(content)

            return out

    def to_bytes(
        self,
        src: str,
        hl: Optional[str] = None,
        v: Optional[str] = None,
        r: Optional[int] = None,
        c: Optional[str] = None,
        f: Optional[str] = None,
        *,
        ssml: Optional[bool] = None,
        b64: Optional[bool] = None,
    ) -> bytes | None:
        """
        :param src: The textual content for converting to speech (length limited by 100KB).
        :param hl: Mandatory. The textual content language.
            Allows values: see Languages.
        :param v: Optional. The speech voice.
            Allows values: see Voices.
            Default value: depends on a language.
        :param r: Optional. The speech rate (speed).
            Allows values: from -10 (slowest speed) up to 10 (fastest speed).
            Default value: 0 (normal speed).
        :param c: Optional. The speech audio codec.
            Allows values: see Audio Codecs.
            Default value: WAV.
        :param f: Optional. The speech audio formats.
            Allows values: see Audio Formats.
            Default value: 8khz_8bit_mono.
        :param ssml: Optional. The SSML textual content format (see SSML documentation).
            Allows values: true and false.
            Default value: false.
        :param b64: Optional. Defines output as a Base64 string format (for an internet browser playing).
            Allows values: true and false.
            Default value: false.
        :return: The result file as bytes
        """

        return self._request(
            src=src,
            hl=hl or self.lang,
            v=v or self.voice,
            r=r or self.rate,
            c=c or self.codec,
            f=f or self.format,
            ssml=ssml or self.ssml,
            b64=b64 or self.b64,
        )
