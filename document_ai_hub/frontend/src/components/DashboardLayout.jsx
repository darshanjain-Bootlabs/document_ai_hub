import { Link, Outlet, useNavigate, useLocation } from "react-router-dom";
import TextType from "/src/component/TextType.jsx";
import { useEffect, useState } from "react";
import api from "../services/api";

export default function DashboardLayout() {
  const navigate = useNavigate();
  const location = useLocation();
  const [documents, setDocuments] = useState([]);
  const role = localStorage.getItem("role");
  const username = localStorage.getItem("username");

  useEffect(() => {
    const fetchDocuments = async () => {
      try {
        const res = await api.get("/upload/upload/docinfo", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });
        setDocuments(res.data.documents);
      } catch (err) {
        console.error("Failed to fetch documents");
        console.log(res.data);
      }
    };

    fetchDocuments();
  }, []);

  const logout = () => {
    localStorage.clear();
    navigate("/login");
  };

  return (
    <div className="min-h-screen flex bg-gray-100">
      {/* Sidebar */}
      <aside className="w-64 bg-white shadow-lg flex flex-col border-r">
        <div className="p-6 border-b">
          <h1 className="text-2xl font-bold text-gray-800 mb-2">
            Document AI Hub
          </h1>
          <TextType
            text={[
              "Empowering Your Document Intelligence",
              "Transforming Documents into Insights",
              "Unlocking the Power of Your Documents",
              "Your Gateway to Document AI",
            ]}
            typingSpeed={75}
            pauseDuration={1500}
            showCursor
            cursorCharacter="_"
            texts={[
              "Empowering Your Document Intelligence",
              "Transforming Documents into Insights",
              "Unlocking the Power of Your Documents",
              "Your Gateway to Document AI",
            ]}
            deletingSpeed={50}
            variableSpeedEnabled={false}
            variableSpeedMin={60}
            variableSpeedMax={120}
            cursorBlinkDuration={0.5}
          />
        </div>

        <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
          {role === "admin" && (
            <Link
              to="/upload"
              className={`block px-4 py-2 rounded-lg transition ${
                location.pathname === "/upload"
                  ? "bg-blue-600 text-white"
                  : "text-gray-700 hover:bg-gray-200"
              }`}
            >
              Upload
            </Link>
          )}

          <Link
            to="/rag"
            className={`block px-4 py-2 rounded-lg transition ${
              location.pathname.startsWith("/rag")
                ? "bg-blue-600 text-white"
                : "text-gray-700 hover:bg-gray-200"
            }`}
          >
            Chat
          </Link>

          {/* Divider */}
          <div className="mt-6 border-t pt-4">
            <h3 className="text-xs font-semibold text-gray-500 uppercase mb-3">
              Documents
            </h3>

            <div className="space-y-1 max-h-82 overflow-y-auto">
              {documents.length === 0 ? (
                <p className="text-sm text-gray-400 px-2">No documents found</p>
              ) : (
                documents.map((doc) => (
                  <Link
                    key={doc.id}
                    to={`/rag/${doc.id}`}
                    className={`block px-3 py-2 text-sm rounded-md truncate transition ${
                      location.pathname === `/rag/${doc.id}`
                        ? "bg-blue-100 text-blue-700"
                        : "text-gray-700 hover:bg-gray-200"
                    }`}
                    title={doc.document_name}
                  >
                    {doc.document_name}
                  </Link>
                ))
              )}
            </div>
          </div>
        </nav>

        <div className="p-4 border-t">
          <button
            onClick={logout}
            className="w-full bg-red-500 text-white py-2 rounded-lg hover:bg-red-600 transition"
          >
            Logout
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Top Navbar */}
        <header className="bg-white shadow-sm p-4 flex justify-between items-center">
          <div>
            <h2 className="text-lg font-semibold text-gray-800">
              {location.pathname === "/upload"
                ? "Upload Documents"
                : "RAG Chat"}
            </h2>
          </div>

          <div className="flex items-center gap-3">
            <span className="text-sm text-gray-600">{username}</span>
            <span className="px-3 py-1 text-xs bg-blue-100 text-blue-600 rounded-full capitalize">
              {role}
            </span>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 p-6 overflow-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
