import { Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/login";
import Upload from "./pages/upload";
import Chat from "./pages/chat";

import ProtectedRoute from "./components/ProtectedRoute";
import DashboardLayout from "./components/DashboardLayout";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />

      <Route element={<DashboardLayout />}>
        <Route
          path="/upload"
          element={
            <ProtectedRoute allowedRoles={["admin"]}>
              <Upload />
            </ProtectedRoute>
          }
        />

        <Route
          path="/rag"
          element={
            <ProtectedRoute
              allowedRoles={[
                "admin",
                "lawyer",
                "doctor",
                "business_user",
                "student",
                "bank_officer",
              ]}
            >
              <Chat />
            </ProtectedRoute>
          }
        />
      </Route>

      {/* Default route */}
      <Route path="/" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}

export default App;
