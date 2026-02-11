import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const navigate = useNavigate();

  const token = localStorage.getItem("access_token") || localStorage.getItem("token");
  const role = localStorage.getItem("role");

  if (!token) {
    navigate("/login");
    return null;
  }

  const logout = () => {
    localStorage.clear();
    navigate("/login");
  };
    return (
        <div style={{ maxWidth: "600px", margin: "60px auto", fontFamily: "Arial" }}>
        <h2>Document AI Dashboard</h2>

        <p>
            <strong>Role:</strong> {role}
        </p>

        <hr />

        {(role === "admin" || role === "researcher") && (
            <button
            style={{ width: "100%", padding: "12px", marginBottom: "10px" }}
            onClick={() => navigate("/upload")}
            >
            Upload Documents
            </button>
        )}

        <button
            style={{ width: "100%", padding: "12px", marginBottom: "10px" }}
            onClick={() => navigate("/chat")}
        >
            Ask Questions (RAG)
        </button>

        <hr />

        <button
            style={{
            width: "100%",
            padding: "10px",
            background: "crimson",
            color: "white",
            border: "none",
            }}
            onClick={logout}
        >
            Logout
        </button>
        </div>
    );
};

export default Dashboard;
