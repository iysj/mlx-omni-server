from pathlib import Path

from f5_tts_mlx.generate import generate

from ..schemas.tts_schema import TTSRequest


class F5Model():

    def __init__(self):
        pass

    def generate_audio(self, request: TTSRequest, output_path):
        generate(
            model_name=request.model,
            generation_text=request.input,
            speed=request.speed,
            output_path=output_path,
        )


class TTSService:
    model: F5Model

    def __init__(self):
        self.model = F5Model()
        # 直接指定本地音频文件路径
        self.sample_audio_path = Path("sample.wav")

    async def generate_speech(
        self,
        request: TTSRequest,
    ) -> bytes:
        """
        Generate speech from text.

        Returns:
            bytes: The generated audio content
        """

        try:
            self.model.generate_audio(request=request, output_path=self.sample_audio_path)
            with open(self.sample_audio_path, 'rb') as audio_file:
                audio_content = audio_file.read()
            self.sample_audio_path.unlink(missing_ok=True)
            return audio_content
        except Exception as e:
            raise Exception(f"Error reading audio file: {str(e)}")
