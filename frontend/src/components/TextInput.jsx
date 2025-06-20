import React, { useState } from 'react';
import axios from 'axios';

const TextInput = ({ setResponse, selectedPersona }) => {
  const [inputText, setInputText] = useState('');

  const handleSubmit = async () => {
    const res = await axios.post('http://localhost:5000/ask', {
      question: inputText,
      persona: selectedPersona,
    });
    setResponse(res.data);
  };

  return (
    <div className="p-4">
      <textarea
        className="w-full p-2 border rounded"
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="Posez une question..."
      />
      <button
        className="mt-2 px-4 py-2 bg-blue-500 text-white rounded"
        onClick={handleSubmit}
      >
        Envoyer
      </button>
    </div>
  );
};

export default TextInput;