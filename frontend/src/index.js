// src/index.js
import React from "react";
import ReactDOM from "react-dom/client"; // Notice the use of 'react-dom/client' for React 18
import App from "./App";
import "./index.css";
import "./App.css";

// This is the correct approach for React 18
const root = ReactDOM.createRoot(document.getElementById("root")); // Create the root
root.render( // Use the 'render' method on the root object
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
