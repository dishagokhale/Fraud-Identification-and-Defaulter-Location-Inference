//home.js


import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../css/Home.css";

function Home() {
  const [userId, setUserId] = useState("");
  const navigate = useNavigate();

  const handleSearch = () => {
    if (userId.trim()) {
      navigate(`/report/${userId}`);
    } else {
      alert("Enter Account ID");
    }
  };

  return (
    <div className="home-page">
      <div className="nav">FICOFORCE</div>
      <div className="center-box">
        <h1 className="title">DETECT, TRACK<br />SECURE</h1>
        <input
          type="text"
          placeholder="Enter Account ID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
        />
        <button onClick={handleSearch}>SEARCH</button>
      </div>
    </div>
  );
}

export default Home;