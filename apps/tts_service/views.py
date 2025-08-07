# Create your views here.
from .serializers import TTSRequestSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import tempfile
from django.http import FileResponse
from rest_framework.permissions import AllowAny

def fetch_tts_audio(text, language="en", voice="english_female"):
    url= "http://localhost:8002/tts/"
    payload = {
        "text": text,
        "language": language,
        "voice": voice
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Error fetching TTS audio: {response.status_code} {response.text}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching TTS audio: {e}")
    
class TTSAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = TTSRequestSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data['text']
            language = serializer.validated_data.get('language','en')
            voice = serializer.validated_data.get('voice','english_female')
            try:    
                audio = fetch_tts_audio(text, language, voice)
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                    temp_file.write(audio)
                    temp_file.flush()
                    temp_file.seek(0)
                    
                    temp_file_path = temp_file.name
                    response = FileResponse(open(temp_file_path, 'rb'), content_type='audio/wav')
                    response['Content-Disposition'] = 'attachment; filename="output.wav"'
                    return response
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)