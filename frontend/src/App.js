import React, { useState } from 'react';
import TextInput from './components/TextInput';
import ResponseBubble from './components/ResponseBubble';
import AvatarSelector from './components/AvatarSelector';

const App = () => {
  const [response, setResponse] = useState(null);
  const [selectedPersona, setSelectedPersona] = useState('default');

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-4">
      <h1 className="text-3xl font-bold mb-4">Ghofrane’s AI Portfolio Agent</h1>
      <AvatarSelector setSelectedPersona={setSelectedPersona} />
      <TextInput setResponse={setResponse} selectedPersona={selectedPersona} />
      {response && <ResponseBubble response={response} />}
    </div>
  );
};

export default App;