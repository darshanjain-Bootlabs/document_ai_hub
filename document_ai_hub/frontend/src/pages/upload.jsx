import { useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [fileDomain, setFileDomain] = useState("general");
  const [status, setStatus] = useState("");
  const navigate = useNavigate();

  const upload_file = async (e) => {
    e.preventDefault();
    if (!file) {
      setStatus("Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("file_domain", fileDomain);
    try {
      setStatus("Uploading...");
      const token =
        localStorage.getItem("access_token") || localStorage.getItem("token");
      const headers = {};
      if (token) headers.Authorization = `Bearer ${token}`;

      const response = await api.post("/upload/upload", formData, {
        params: { file_domain: fileDomain },
        headers,
      });

      console.log("upload response:", response);
      setStatus(
        `Uploaded successfully. Chunks: ${response.data?.chunks_created ?? "unknown"}`,
      );
      navigate("/chat");
    } catch (error) {
      setStatus("Error uploading file.");
    }
  };

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white shadow-xl rounded-2xl p-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">
          Upload Document
        </h2>
        <p className="text-gray-500 mb-6">
          Upload a document to index it into the system.
        </p>

        <form onSubmit={upload_file} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">
              File Domain
            </label>
            <input
              type="text"
              value={fileDomain}
              onChange={(e) => setFileDomain(e.target.value)}
              placeholder="e.g. healthcare, academic"
              required
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none transition"
            />
          </div>

          <div className="border-2 border-dashed border-gray-300 rounded-xl p-6 text-center hover:border-blue-500 transition">
            <input
              type="file"
              onChange={(e) => setFile(e.target.files[0])}
              required
              className="block mx-auto text-sm text-gray-600"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2.5 rounded-lg hover:bg-blue-700 transition font-medium"
          >
            Upload
          </button>
        </form>

        {status && (
          <div
            className={`mt-6 p-3 rounded-lg text-sm ${
              status.includes("Error")
                ? "bg-red-100 text-red-600"
                : status.includes("Uploading")
                  ? "bg-yellow-100 text-yellow-700"
                  : "bg-green-100 text-green-700"
            }`}
          >
            {status}
          </div>
        )}
      </div>
    </div>
  );
}
