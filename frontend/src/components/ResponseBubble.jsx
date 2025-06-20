function ResponseBubble({ response }) {
  return (
    <div className="mt-4 w-full max-w-md p-4 bg-white rounded-lg shadow-md">
      <p className="text-gray-800">{response}</p>
    </div>
  );
}

export default ResponseBubble;