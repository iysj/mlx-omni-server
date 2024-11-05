from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import Optional
from ..models.tts import TTSRequest, AudioFormat
from ..services.tts_service import TTSService
import io

router = APIRouter(tags=["text-to-speech"])

@router.post("/audio/speech")
@router.post("/v1/audio/speech")
async def create_speech(request: TTSRequest):
    """
    Generate audio from input text.

    Returns:
        StreamingResponse: Audio file content in the requested format
    """
    tts_service = TTSService()

    try:
        audio_content = await tts_service.generate_speech(
            model=request.model,
            input_text=request.input,
            voice=request.voice,
            response_format=request.response_format,
            speed=request.speed
        )

        # Create content type mapping
        content_type_mapping = {
            AudioFormat.MP3: "audio/mpeg",
            AudioFormat.OPUS: "audio/opus",
            AudioFormat.AAC: "audio/aac",
            AudioFormat.FLAC: "audio/flac",
            AudioFormat.WAV: "audio/wav",
            AudioFormat.PCM: "audio/pcm",
        }

        # Create response
        return StreamingResponse(
            io.BytesIO(audio_content),
            media_type=content_type_mapping[request.response_format],
            headers={
                'Content-Disposition': f'attachment; filename="speech.{request.response_format.value}"'
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
