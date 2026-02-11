import { useState } from "react";

const Chat = () => {
  const [question, setQuestion] = useState("");
  const [format, setFormat] = useState("markdown");
  const [docDomain, setDocDomain] = useState("");
  const [mode, setMode] = useState("general");

  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) {
      alert("Please enter a question");
      return;
    }

    if (!docDomain.trim()) {
      alert("Please enter document domain");
      return;
    }

    setLoading(true);
    setAnswer("");

    try {
      const token =
        localStorage.getItem("access_token") || localStorage.getItem("token");

      if (!token) {
        setAnswer("Not authenticated — please log in");
        return;
      }

      const headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      };

      const response = await fetch(
        `http://127.0.0.1:8000/rag/rag` +
          `?query=${encodeURIComponent(question)}` +
          `&response_format=${format}` +
          `&doc_domain=${docDomain}` +
          `&mode=${mode}`,
        {
          method: "POST",
          headers,
          body: JSON.stringify({}),
        },
      );

      if (response.status === 401) {
        localStorage.removeItem("access_token");
        setAnswer(
          "Unauthorized — token missing or expired. Please log in again.",
        );
        return;
      }

      if (!response.ok) {
        const text = await response.text();
        setAnswer(`Backend error ${response.status}: ${text}`);
        return;
      }

      const data = await response.json();
      setAnswer(data.answer || "No answer returned");
    } catch (error) {
      setAnswer("Error calling backend");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto flex flex-col h-[80vh]">
      <div className="bg-white shadow-md rounded-xl p-4 mb-4 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Document Domain
          </label>
          <input
            type="text"
            placeholder="e.g. legal, medical"
            value={docDomain}
            onChange={(e) => setDocDomain(e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Answer Format
          </label>
          <select
            value={format}
            onChange={(e) => setFormat(e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
          >
            <option value="plain">Plain Text</option>
            <option value="markdown">Markdown</option>
            <option value="table">Table</option>
            <option value="json">JSON</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Mode
          </label>
          <select
            value={mode}
            onChange={(e) => setMode(e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
          >
            <option value="general">General</option>
            <option value="strict">Strict (Docs Only)</option>
            <option value="summary">Summary</option>
          </select>
        </div>
      </div>

      <div className="flex-1 bg-white rounded-xl shadow-lg p-6 overflow-y-auto space-y-4">
        {question && (
          <div className="flex justify-end">
            <div className="bg-blue-600 text-white px-4 py-2 rounded-2xl max-w-lg">
              {question}
            </div>
          </div>
        )}

        {loading ? (
          <div className="flex justify-start">
            <div className="bg-gray-200 text-gray-700 px-4 py-2 rounded-2xl">
              Thinking...
            </div>
          </div>
        ) : (
          answer && (
            <div className="flex justify-start">
              <div className="bg-gray-100 text-gray-800 px-4 py-3 rounded-2xl max-w-lg whitespace-pre-wrap">
                {answer}
              </div>
            </div>
          )
        )}
      </div>

      <div className="mt-4 flex gap-3">
        <textarea
          rows={2}
          placeholder="Ask a question about your documents..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none resize-none"
        />

        <button
          onClick={askQuestion}
          disabled={loading}
          className="bg-blue-600 text-white px-6 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default Chat;

// import { useState } from "react";

// const Chat = () => {
//   const [question, setQuestion] = useState("");
//   const [format, setFormat] = useState("");
//   const [answer, setAnswer] = useState("");
//   const [loading, setLoading] = useState(false);

//   const askQuestion = async () => {
//     if (!question.trim()) {
//       alert("Please enter a question");
//       return;
//     }

//     setLoading(true);
//     setAnswer("");

//     try {
//       const response = await fetch(
//         `http://127.0.0.1:8000/rag/rag?query=${encodeURIComponent(
//           question
//         )}&response_format=${format}&top_k=3`,
//         {
//           method: "POST",
//         }
//       );

//       const data = await response.json();
//       setAnswer(data.answer || "No answer returned");
//     } catch (error) {
//       setAnswer("Error calling backend");
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div style={{ maxWidth: "800px", margin: "40px auto", fontFamily: "Arial" }}>
//       <h2>RAG Chat Interface</h2>

//       {/* Question Input */}
//       <textarea
//         rows={4}
//         style={{ width: "100%", padding: "10px" }}
//         placeholder="Ask a question about your documents..."
//         value={question}
//         onChange={(e) => setQuestion(e.target.value)}
//       />

//       {/* Format Selector */}
//       <div style={{ marginTop: "10px" }}>
//         <label><strong>Answer Format: </strong></label>
//         <select
//           value={format}
//           onChange={(e) => setFormat(e.target.value)}
//         >
//           <option value="plain">Plain Text</option>
//           <option value="markdown">Markdown</option>
//           <option value="table">Table</option>
//           <option value="json">JSON</option>
//         </select>
//       </div>

//       {/* Ask Button */}
//       <button
//         onClick={askQuestion}
//         style={{ marginTop: "15px", padding: "10px 20px" }}
//       >
//         Ask
//       </button>

//       {/* Answer Section */}
//       <div style={{ marginTop: "30px" }}>
//         <h3>Answer:</h3>

//         {loading ? (
//           <p>Thinking...</p>
//         ) : (
//           <pre
//             style={{
//               background: "#f4f4f4",
//               padding: "15px",
//               whiteSpace: "pre-wrap",
//             }}
//           >
//             {answer}
//           </pre>
//         )}
//       </div>
//     </div>
//   );
// };

// export default Chat;
