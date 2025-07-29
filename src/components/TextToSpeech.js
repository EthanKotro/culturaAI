// export function speak(text) {
//     const synth = window.SpeechSynthesis;
//     const utter = new SpeechSynthesisUtterance(text);

//     utter.lang = 'en-US';
//     synth.speak(utter);
// }


// src/components/TextToSpeech.js
import React, { useState } from "react";

export default function TextToSpeech() {
  const [text, setText] = useState("Hello! Welcome to our translation app.");

  const speak = () => {
    if ("speechSynthesis" in window) {
      const utter = new SpeechSynthesisUtterance(text);
      utter.lang = "en-US"; // Set your desired language code (e.g., 'sw-KE' for Swahili)
      window.speechSynthesis.speak(utter);
    } else {
      alert("Text-to-Speech is not supported in this browser.");
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto bg-white rounded shadow">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows="4"
        className="w-full border p-2 rounded mb-2"
      />
      <button
        onClick={speak}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        🔊 Speak
      </button>
    </div>
  );
}
