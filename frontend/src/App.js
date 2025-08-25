// App.js
import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";
import {
  Card,
  CardContent,
} from "./components/ui/card";
import {
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  TableHeader,
} from "./components/ui/table";
import { Pie, Line } from "react-chartjs-2";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "./components/ui/tabs";

import {
  Chart as ChartJS,
  ArcElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend,
  PointElement,
} from "chart.js";

ChartJS.register(ArcElement, CategoryScale, LinearScale, Title, Tooltip, Legend, PointElement);

const API_URL = "http://localhost:5000/api";

const AuthPage = ({ setAuthenticated }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleAuth = async () => {
    const endpoint = isLogin ? "login" : "signup";
    setError("");
    try {
      await axios.post(`${API_URL}/${endpoint}`, { username, password }, { withCredentials: true });
      setAuthenticated(true);
    } catch (err) {
      setError(err.response?.data?.message || `${isLogin ? "Login" : "Signup"} failed. Please try again.`);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-blue-100 to-purple-100 p-4">
      <Card className="w-full max-w-md p-8 shadow-xl animate-fadeIn">
        <CardContent>
          <h2 className="text-3xl font-bold mb-6 text-center text-gray-800">{isLogin ? "Login" : "Signup"}</h2>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="border border-gray-300 rounded-lg w-full mb-4 p-3 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="border border-gray-300 rounded-lg w-full mb-4 p-3 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
          />
          {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
          <button
            onClick={handleAuth}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg px-4 py-3 w-full mb-3 transition"
          >
            {isLogin ? "Login" : "Signup"}
          </button>
          <button
            onClick={() => setIsLogin(!isLogin)}
            className="text-sm text-blue-600 hover:underline text-center w-full"
          >
            {isLogin ? "Don't have an account? Signup" : "Already have an account? Login"}
          </button>
        </CardContent>
      </Card>
    </div>
  );
};

const ThreatDashboard = ({ setAuthenticated }) => {
  const [logs, setLogs] = useState([]);
  const [devices, setDevices] = useState([]);
  const [deviceId, setDeviceId] = useState("");
  const [loading, setLoading] = useState(true);

  const fetchLogs = async () => {
    try {
      const res = await axios.get(`${API_URL}/logs`, { withCredentials: true });
      setLogs(res.data);
    } catch (error) {
      console.error("Error fetching logs:", error);
      if (error.response?.status === 401) setAuthenticated(false);
    }
  };

  const fetchDevices = async () => {
    try {
      const res = await axios.get(`${API_URL}/devices`, { withCredentials: true });
      setDevices(res.data);
    } catch (error) {
      console.error("Error fetching devices:", error);
    }
  };

  const registerDevice = async () => {
    if (!deviceId.trim()) return;
    try {
      await axios.post(`${API_URL}/devices`, { device_id: deviceId }, { withCredentials: true });
      setDeviceId("");
      fetchDevices();
    } catch (error) {
      console.error("Error registering device:", error);
    }
  };

  const removeDevice = async (id) => {
    try {
      await axios.delete(`${API_URL}/devices/${id}`, { withCredentials: true });
      fetchDevices();
    } catch (error) {
      console.error("Error removing device:", error);
    }
  };

  const handleLogout = async () => {
    try {
      await axios.post(`${API_URL}/logout`, {}, { withCredentials: true });
      setAuthenticated(false);
    } catch (error) {
      console.error("Error during logout:", error);
    }
  };

  useEffect(() => {
    fetchLogs();
    fetchDevices();
    const logsInterval = setInterval(fetchLogs, 5000);
    return () => clearInterval(logsInterval);
  }, []);

  const threatCounts = logs.reduce((acc, log) => {
    const type = log.prediction_label;
    acc[type] = (acc[type] || 0) + 1;
    return acc;
  }, {});

  const lineData = {
    labels: logs.map((log) => new Date(log.timestamp).toLocaleTimeString()),
    datasets: [
      {
        label: "Packet Rate",
        data: logs.map((log) => log.packet_rate || 0),
        fill: false,
        borderColor: "#3b82f6",
        tension: 0.3,
      },
    ],
  };

  const pieData = {
    labels: Object.keys(threatCounts),
    datasets: [
      {
        data: Object.values(threatCounts),
        backgroundColor: ["#ef4444", "#f59e0b", "#10b981", "#3b82f6", "#8b5cf6"],
      },
    ],
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen space-y-6 animate-fadeInSlow">
      <div className="flex justify-end">
        <button
          onClick={handleLogout}
          className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg shadow transition"
        >
          Logout
        </button>
      </div>

      <h1 className="text-4xl font-extrabold text-gray-800 text-center mb-8">IoT Threat Detection Dashboard</h1>

      <Tabs defaultValue="overview">
        <TabsList className="flex justify-center gap-4 mb-6">
          <TabsTrigger value="overview" className="px-4 py-2 rounded-lg hover:bg-blue-100">Overview</TabsTrigger>
          <TabsTrigger value="logs" className="px-4 py-2 rounded-lg hover:bg-blue-100">Logs</TabsTrigger>
          <TabsTrigger value="devices" className="px-4 py-2 rounded-lg hover:bg-blue-100">Devices</TabsTrigger>
          <TabsTrigger value="insights" className="px-4 py-2 rounded-lg hover:bg-blue-100">Insights</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview">
          <Card className="shadow-md max-w-4xl mx-auto">
            <CardContent className="p-6 space-y-4">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">System Overview</h2>
              <p className="text-gray-700 leading-relaxed">
                This IoT Threat Detection System continuously monitors incoming traffic from IoT devices and identifies suspicious activity in real time.
              </p>
              <p className="text-gray-700 leading-relaxed">
                The system uses machine learning models to evaluate packet features like packet rate, entropy, and behavior patterns to classify them as threats or normal.
              </p>
              <p className="text-gray-700 leading-relaxed">
                Detected threats are logged for review under the Logs tab. The Devices tab allows for registration or removal of IoT devices. Insights include visual analytics to observe trends.
              </p>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Logs Tab */}
	<TabsContent value="logs">
	  <Card className="shadow-md">
	    <CardContent className="p-6">
	      <h2 className="text-2xl font-semibold mb-4 text-gray-700">Device Logs</h2>
	      <div className="overflow-auto">
		<table className="min-w-full text-sm text-left border-collapse">
		  <thead>
		    <tr className="bg-blue-100">
		      <th className="log-header">Device ID</th>
		      <th className="log-header">Status</th>
		      <th className="log-header">Packet Rate</th>
		      <th className="log-header">Threat Type</th>
		      <th className="log-header">Timestamp</th>
		    </tr>
		  </thead>
		  <tbody>
		    {logs.map((log, index) => (
		      <tr key={index} className="even:bg-white odd:bg-gray-50">
		        <td className="log-cell">{log.device_id}</td>
		        <td className="log-cell">{log.status}</td>
		        <td className="log-cell">{log.packet_rate}</td>
		        <td className={`log-cell font-semibold ${log.prediction_label !== "Normal" ? "text-red-600" : "text-green-600"}`}>
		          {log.prediction_label}
		        </td>
		        <td className="log-cell">{new Date(log.timestamp).toLocaleString()}</td>
		      </tr>
		    ))}
		  </tbody>
		</table>
	      </div>
	    </CardContent>
	  </Card>
	</TabsContent>


        {/* Devices Tab */}
        <TabsContent value="devices">
          <Card className="shadow-md">
            <CardContent className="p-6">
              <h2 className="text-2xl font-semibold mb-6 text-gray-700">Manage Devices</h2>
              <div className="flex gap-4 mb-6">
                <input
                  type="text"
                  placeholder="Enter Device ID"
                  value={deviceId}
                  onChange={(e) => setDeviceId(e.target.value)}
                  className="border border-gray-300 rounded-lg p-3 flex-1 focus:outline-none focus:ring-2 focus:ring-green-400 transition"
                />
                <button
                  onClick={registerDevice}
                  className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg transition"
                >
                  Register
                </button>
              </div>
              <ul className="divide-y divide-gray-200">
                {devices.map((dev, index) => (
                  <li key={index} className="flex justify-between items-center py-3">
                    <span className="text-gray-700">{dev.device_id}</span>
                    <button
                      onClick={() => removeDevice(dev.device_id)}
                      className="text-red-600 hover:text-red-800 transition"
                    >
                      Remove
                    </button>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </TabsContent>
        {/* Insights Tab */}
        <TabsContent value="insights">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card className="shadow-md">
              <CardContent className="p-6">
              <div className="chart-container">
                <h2 className="text-2xl font-semibold mb-4 text-gray-700">Threat Breakdown</h2>
                <div className="chart-container">
                  <Pie data={pieData} />
                </div>
              </div>
              </CardContent>
            </Card>
            <Card className="shadow-md">
              <CardContent className="p-6">
              <div className="chart-container1">
                <h2 className="text-2xl font-semibold mb-4 text-gray-700">Packet Rate Trend</h2>
                <div className="chart-container">
                  <Line data={lineData} />
                </div>
              </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

const App = () => {
  const [authenticated, setAuthenticated] = useState(false);

  return authenticated ? (
    <ThreatDashboard setAuthenticated={setAuthenticated} />
  ) : (
    <AuthPage setAuthenticated={setAuthenticated} />
  );
};

export default App;
