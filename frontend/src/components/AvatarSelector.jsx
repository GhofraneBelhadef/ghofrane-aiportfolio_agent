function AvatarSelector({ setSelectedPersona }) {
  const personas = ['default', 'technical', 'creative'];

  return (
    <div className="mb-4">
      <label className="mr-2">Select Persona:</label>
      <select
        onChange={(e) => setSelectedPersona(e.target.value)}
        className="p-2 border rounded-md"
      >
        {personas.map((persona) => (
          <option key={persona} value={persona}>
            {persona.charAt(0).toUpperCase() + persona.slice(1)}
          </option>
        ))}
      </select>
    </div>
  );
}

export default AvatarSelector;