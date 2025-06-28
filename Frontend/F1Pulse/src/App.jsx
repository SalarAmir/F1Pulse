// src/App.jsx
import React, { useState } from "react";
import { motion } from "framer-motion";

// Driver-Team mappings for 2024 season with experience data
const driverTeamMap = {
  "Max Verstappen": { team: "Red Bull Racing", teamEncoded: 0, experience: 10 },
  "Sergio Perez": { team: "Red Bull Racing", teamEncoded: 0, experience: 13 },
  "Lewis Hamilton": { team: "Mercedes", teamEncoded: 1, experience: 17 },
  "George Russell": { team: "Mercedes", teamEncoded: 1, experience: 3 },
  "Charles Leclerc": { team: "Ferrari", teamEncoded: 2, experience: 6 },
  "Carlos Sainz": { team: "Ferrari", teamEncoded: 2, experience: 9 },
  "Lando Norris": { team: "McLaren", teamEncoded: 3, experience: 5 },
  "Oscar Piastri": { team: "McLaren", teamEncoded: 3, experience: 1 },
  "Fernando Alonso": { team: "Aston Martin", teamEncoded: 4, experience: 22 },
  "Lance Stroll": { team: "Aston Martin", teamEncoded: 4, experience: 7 },
  "Esteban Ocon": { team: "Alpine", teamEncoded: 5, experience: 7 },
  "Pierre Gasly": { team: "Alpine", teamEncoded: 5, experience: 6 },
  "Nico Hulkenberg": { team: "Haas", teamEncoded: 6, experience: 8 },
  "Kevin Magnussen": { team: "Haas", teamEncoded: 6, experience: 8 },
  "Daniel Ricciardo": { team: "RB", teamEncoded: 7, experience: 13 },
  "Yuki Tsunoda": { team: "RB", teamEncoded: 7, experience: 3 },
  "Alex Albon": { team: "Williams", teamEncoded: 8, experience: 4 },
  "Logan Sargeant": { team: "Williams", teamEncoded: 8, experience: 1 },
  "Valtteri Bottas": { team: "Kick Sauber", teamEncoded: 9, experience: 11 },
  "Zhou Guanyu": { team: "Kick Sauber", teamEncoded: 9, experience: 2 },
};

const races = [
  "Bahrain Grand Prix",
  "Saudi Arabian Grand Prix", 
  "Australian Grand Prix",
  "Japanese Grand Prix",
  "Chinese Grand Prix",
  "Miami Grand Prix",
  "Emilia Romagna Grand Prix",
  "Monaco Grand Prix",
  "Canadian Grand Prix",
  "Spanish Grand Prix",
  "Austrian Grand Prix",
  "British Grand Prix",
  "Hungarian Grand Prix",
  "Belgian Grand Prix",
  "Dutch Grand Prix",
  "Italian Grand Prix",
  "Azerbaijan Grand Prix",
  "Singapore Grand Prix",
  "United States Grand Prix",
  "Mexican Grand Prix",
  "Brazilian Grand Prix",
  "Las Vegas Grand Prix",
  "Qatar Grand Prix",
  "Abu Dhabi Grand Prix"
];

const seasons = [2021, 2022, 2023, 2024, 2025];

export default function App() {
  const [formData, setFormData] = useState({
    season: "",
    driver: "",
    race: "",
    customExperience: "", // For custom experience override
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Get team info when driver is selected
  const selectedDriverInfo = formData.driver ? driverTeamMap[formData.driver] : null;

  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPrediction(null);

    if (!selectedDriverInfo) {
      setError("Please select a valid driver");
      setLoading(false);
      return;
    }

    try {
      console.log("Making prediction request...");
      const res = await fetch("http://localhost:8080/api/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          season: Number(formData.season),
          team_encoded: selectedDriverInfo.teamEncoded,
          driver_name: formData.driver,
          race_name: formData.race,
          driver_experience: formData.customExperience ? 
            Number(formData.customExperience) : selectedDriverInfo.experience,
        }),
      });

      if (!res.ok) throw new Error("Failed to fetch prediction");

      const data = await res.json();
      console.log("Response from API:", data); // Debug log
      setPrediction(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-lg mx-auto mt-12 p-6 bg-white rounded-lg shadow-lg font-sans">
      <motion.h1
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-3xl font-bold mb-6 text-center text-blue-700"
      >
        🏎️ F1 Position Predictor
      </motion.h1>

      <form onSubmit={handleSubmit} className="flex flex-col gap-5">
        <select
          name="season"
          value={formData.season}
          onChange={handleChange}
          required
          className="p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
        >
          <option value="" disabled>
            Select Season
          </option>
          {seasons.map((season) => (
            <option key={season} value={season}>
              {season}
            </option>
          ))}
        </select>

        <select
          name="driver"
          value={formData.driver}
          onChange={handleChange}
          required
          className="p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
        >
          <option value="" disabled>
            Select Driver
          </option>
          {Object.keys(driverTeamMap).map((driver) => (
            <option key={driver} value={driver}>
              {driver}
            </option>
          ))}
        </select>

        {/* Show team and experience automatically based on driver selection */}
        {selectedDriverInfo && (
          <div className="p-3 bg-gray-100 rounded border space-y-2">
            <p><strong>Team:</strong> {selectedDriverInfo.team}</p>
            <p><strong>Experience:</strong> {selectedDriverInfo.experience} years</p>
          </div>
        )}

        <select
          name="race"
          value={formData.race}
          onChange={handleChange}
          required
          className="p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
        >
          <option value="" disabled>
            Select Race
          </option>
          {races.map((race) => (
            <option key={race} value={race}>
              {race}
            </option>
          ))}
        </select>

        {/* Optional: Custom Experience Override */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">
            Driver Experience (Optional Override)
          </label>
          <input
            type="number"
            name="customExperience"
            value={formData.customExperience}
            onChange={handleChange}
            min="1"
            max="25"
            placeholder={selectedDriverInfo ? `Default: ${selectedDriverInfo.experience} years` : "Years of experience"}
            className="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <p className="text-xs text-gray-500">
            Leave empty to use default experience for selected driver
          </p>
        </div>

        <motion.button
          type="submit"
          disabled={loading}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className={`p-3 font-semibold rounded text-white ${
            loading ? "bg-gray-400 cursor-not-allowed" : "bg-blue-600"
          }`}
        >
          {loading ? "Predicting..." : "🏁 Predict Position"}
        </motion.button>
      </form>

      {error && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mt-4 text-red-600 font-medium"
        >
          Error: {error}
        </motion.p>
      )}

      {prediction && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mt-6 p-4 bg-blue-50 rounded shadow"
        >
          <h2 className="text-xl font-semibold mb-2 text-blue-700">
            🏁 Position Prediction Results
          </h2>
          
          {/* Main Prediction */}
          <div className="bg-white p-4 rounded border-l-4 border-blue-500 mb-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-lg">
                  <strong>🎯 Predicted Position:</strong>
                </p>
                <span className="text-4xl font-bold text-blue-600">
                  P{prediction.predicted_position || prediction.predictedPosition}
                </span>
              </div>
              <div className="text-right">
                <p className="text-sm text-gray-600">Confidence</p>
                <span className="text-2xl font-bold text-green-600">
                  {((prediction.prediction_confidence || prediction.predictionConfidence || 0) * 100).toFixed(1)}%
                </span>
              </div>
            </div>
          </div>

          {/* Race Details */}
          <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
            <div>
              <p><strong>Season:</strong> {formData.season}</p>
              <p><strong>Driver:</strong> {formData.driver}</p>
            </div>
            <div>
              <p><strong>Team:</strong> {selectedDriverInfo?.team}</p>
              <p><strong>Experience:</strong> {formData.customExperience || selectedDriverInfo?.experience} years</p>
            </div>
          </div>

          {/* Race Name */}
          <div className="mb-4 p-2 bg-gray-50 rounded">
            <p className="text-center"><strong>📍 Race:</strong> {formData.race}</p>
          </div>

          {/* Historical Data Section */}
          {prediction.is_historical && prediction.historical_result && (
            <div className="bg-yellow-50 p-4 rounded border-l-4 border-yellow-500 mb-4">
              <h3 className="font-semibold text-yellow-700 mb-2">📊 Historical Result</h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p><strong>Actual Position:</strong> P{prediction.historical_result.position || "N/A"}</p>
                  <p><strong>Actual Points:</strong> {prediction.historical_result.points?.toFixed(2) || "N/A"}</p>
                </div>
                <div>
                  <p><strong>Driver:</strong> {prediction.historical_result.driver || "N/A"}</p>
                  <p><strong>Team:</strong> {prediction.historical_result.team || "N/A"}</p>
                </div>
              </div>
              
              {/* Position Prediction vs Reality Comparison */}
              {prediction.historical_result.position && (
                <div className="mt-3 p-3 bg-white rounded border">
                  <h4 className="font-semibold text-gray-700 mb-2">⚡ Position Accuracy</h4>
                  {(() => {
                    const predicted = prediction.predicted_position || prediction.predictedPosition || 20;
                    const actual = prediction.historical_result.position;
                    const difference = Math.abs(predicted - actual);
                    const isExact = difference === 0;
                    const isClose = difference <= 2;
                    
                    return (
                      <div className="text-sm">
                        <p><strong>Predicted:</strong> P{predicted}</p>
                        <p><strong>Actual:</strong> P{actual}</p>
                        <p><strong>Difference:</strong> {difference} position{difference !== 1 ? 's' : ''}</p>
                        <p><strong>Accuracy:</strong> 
                          <span className={`ml-1 font-bold ${isExact ? 'text-green-600' : isClose ? 'text-yellow-600' : 'text-red-600'}`}>
                            {isExact ? '🎯 Exact Match!' : isClose ? '🟡 Close!' : '🔴 Off target'}
                          </span>
                        </p>
                      </div>
                    );
                  })()}
                </div>
              )}
            </div>
          )}

          {/* Future Prediction Notice */}
          {!prediction.is_historical && (
            <div className="bg-green-50 p-4 rounded border-l-4 border-green-500 mb-4">
              <h3 className="font-semibold text-green-700 mb-2">🔮 Future Prediction</h3>
              <p className="text-sm text-green-600">
                This is a prediction for a future season. Historical data not available for comparison.
              </p>
            </div>
          )}
          
          {/* Position context and confidence interpretation */}
          <div className="mt-4 p-3 bg-white rounded border-l-4 border-blue-500">
            <h3 className="font-semibold text-gray-700 mb-2">🏁 Understanding the Prediction:</h3>
            <div className="text-sm text-gray-600 space-y-2">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p><strong>Confidence Level:</strong></p>
                  <p className="text-xs">
                    {(() => {
                      const conf = (prediction.prediction_confidence || prediction.predictionConfidence || 0) * 100;
                      if (conf >= 80) return "🟢 Very High (80%+)";
                      if (conf >= 60) return "🟡 High (60-80%)";
                      if (conf >= 40) return "🟠 Medium (40-60%)";
                      return "🔴 Low (<40%)";
                    })()}
                  </p>
                </div>
                <div>
                  <p><strong>Position Range:</strong></p>
                  <p className="text-xs">Positions 1-20 (1st to 20th place)</p>
                </div>
              </div>
              
              <div className="mt-3 pt-3 border-t border-gray-200">
                <p className="font-medium">🏆 F1 Points by Position:</p>
                <div className="grid grid-cols-2 gap-2 mt-1 text-xs">
                  <div>
                    <p>🥇 P1: 25 pts | 🥈 P2: 18 pts | 🥉 P3: 15 pts</p>
                    <p>P4: 12 pts | P5: 10 pts | P6: 8 pts</p>
                  </div>
                  <div>
                    <p>P7: 6 pts | P8: 4 pts | P9: 2 pts | P10: 1 pt</p>
                    <p>P11-P20: 0 points</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
}
