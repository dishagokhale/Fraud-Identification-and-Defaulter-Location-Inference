//report.js


import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import "../css/Report.css";

function Report() {
  const { userId } = useParams();
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/generate-report/${userId}`);
        setReportData(response.data);
      } catch (error) {
        console.error(error);
        setReportData({ status: "Error fetching report", metrics: [] });
      } finally {
        setLoading(false);
      }
    };
    fetchReport();
  }, [userId]);

  // Clean and extract system prediction
  const cleanedMetrics = reportData?.metrics?.map(m => m.trim()) || [];
  const systemPredictionMetric = cleanedMetrics.find(m => m.toLowerCase().includes("system prediction"));
  const systemPrediction = systemPredictionMetric?.split(":")[1]?.trim();

  return (
  <div className="result-page">
    <div className="glow-wrapper">
      <div className="risk-report-container">
      {/* LEFT COLUMN: Title and Prediction */}
      <div className="left-strip">
        <h1 className="page-title">RISK REPORT</h1>
          {!loading && systemPrediction && (
          <div className="system-prediction-box">
            System Prediction: <strong>{systemPrediction}</strong>
            </div>
          )}
        </div>
        {/* RIGHT COLUMN: Metrics */}
        <div className="right-metrics">
          {loading ? (
            <p className="loading-text">Generating report...</p>
          ) : (
            <div className="risk-metrics-grid">
              {cleanedMetrics
              .filter(metric => !metric.toLowerCase().includes("system prediction"))
              .map((metric, index) => {
                  let riskClass = "metric-low";
                  const lower = metric.toLowerCase();
                  if (lower.includes("moderate") || lower.includes("old")) riskClass = "metric-moderate";
                  if (lower.includes("high") || lower.includes("defaulter") || lower.includes("very high")) riskClass = "metric-high";
                  const [title, ...rest] = metric.split(":");
                  const description = rest.join(":").trim();
                  return (
                    <div key={index} className={`metric-card ${riskClass}`}>
                      <div className="metric-title">{title}</div>
                      <div className="metric-value">{description}</div>
                    </div>
                  );
                })
              }
            </div>
          )}
        </div>
      </div>
    </div>
  </div>
);

}

export default Report;