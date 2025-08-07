export function useTTS(){
    const fetchAndPlayTTS = async (
        text: string,
        lang: string="en",
        voice: string="english_female") => {
        const response = await fetch(`http://127.0.0.1:8000/api/v1/tts/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                lang: lang,
                voice: voice,
            }),
        });
        if (!response.ok) {
            throw new Error(`TTS failed: ${response.statusText}`);
        }
        const blob = await response.blob();
        const audioUrl= URL.createObjectURL(blob);
        const audio = new Audio(audioUrl);
        audio.play();
        return audioUrl;
    }
    return { fetchAndPlayTTS };
}