import { useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";
import DarkVeil from "/src/component/DarkVeil.jsx";
import TextType from "/src/component/TextType.jsx";

export default function Login() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const params = new URLSearchParams();
      params.append("username", username);
      params.append("password", password);

      const response = await api.post("/auth/login", params, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      const token = response.data.access_token;
      localStorage.setItem("access_token", token);

      const meResponse = await api.get("/auth/me", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const { username: userName, role } = meResponse.data;
      localStorage.setItem("username", userName);
      localStorage.setItem("role", role);
      if (role === "admin") {
        navigate("/upload");
      } else {
        navigate("/rag");
      }
    } catch (err) {
      setError("Invalid username or password");
    } finally {
      setLoading(false);
    }
  };

  // return (
  //   <div className="login-container">
  //     <h2>Login</h2>

  //     <form onSubmit={handleSubmit}>
  //       <div>
  //         <label>Username:</label>
  //         <input
  //           type="text"
  //           value={username}
  //           onChange={(e) => setUsername(e.target.value)}
  //           required
  //         />
  //       </div>

  //       <div>
  //         <label>Password:</label>
  //         <input
  //           type="password"
  //           value={password}
  //           onChange={(e) => setPassword(e.target.value)}
  //           required
  //         />
  //       </div>

  //       {error && <p className="error">{error}</p>}

  //       <button type="submit">Login</button>
  //     </form>
  //   </div>
  // );

  return (
    <div className="relative min-h-screen w-full flex flex-col md:flex-row overflow-hidden">
      <div className="fixed inset-0 z-0 pointer-events-none">
        <DarkVeil
          hueShift={0}
          noiseIntensity={0}
          scanlineIntensity={0}
          speed={1}
          scanlineFrequency={0}
          warpAmount={0}
        />
      </div>
      <div className="relative z-10 flex-1 flex flex-col items-center justify-center p-12 text-white">
        <div className="max-w-lg">
          <h1 className="text-5xl font-extrabold mb-6 tracking-tight">
            <TextType
              text={["Document AI Hub"]}
              typingSpeed={75}
              pauseDuration={1500}
              showCursor
              cursorCharacter="_"
              texts={[
                "Welcome to Document AI Hub! Your gateway to intelligent document management.",
              ]}
              deletingSpeed={80}
              variableSpeedEnabled={false}
              variableSpeedMin={60}
              variableSpeedMax={120}
              cursorBlinkDuration={0.5}
            />
          </h1>
          <p className="text-lg text-gray-300 leading-relaxed">
            Welcome to Document AI Hub! Your gateway to intelligent document
            management.
          </p>
        </div>
      </div>

      <div className="relative z-20 flex-1 flex items-center justify-center bg-white dark:bg-neutral-900 p-8 md:p-16">
        <div className="w-full max-w-md">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Welcome Back
          </h2>
          <p className="text-gray-500 mb-8">Please login to your account</p>

          {error && (
            <div className="bg-red-100 text-red-600 text-sm p-3 rounded-lg mb-4">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Username
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className="w-full px-4 py-3 text-gray-100 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-sm text-gray-100 font-medium text-gray-700 dark:text-gray-300 mb-1">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-lg text-white focus:ring-2 focus:ring-blue-500 focus:outline-none"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-all shadow-lg shadow-blue-500/30 disabled:opacity-50"
            >
              {loading ? "Logging in..." : "Login"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
