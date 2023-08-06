import logging as _logging

logger = _logging.getLogger(__name__)
__stream_handler = _logging.StreamHandler()
__stream_handler.setFormatter(_logging.Formatter("%(levelname)s - %(message)s"))
logger.addHandler(__stream_handler)

from .voicerss import VoiceRSS
