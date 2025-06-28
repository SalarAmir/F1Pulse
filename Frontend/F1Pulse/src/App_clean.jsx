// src/App.jsx
import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import './App.css';

// Driver-Team mappings for 2024 season with experience data and images
const driverTeamMap = {
  "Max Verstappen": { 
    team: "Red Bull Racing", 
    teamEncoded: 0, 
    experience: 10,
    image: "https://www.formula1.com/content/dam/fom-website/drivers/M/MAXVER01_Max_Verstappen/maxver01.png.transform/1col/image.png",
    flag: "🇳🇱",
    number: "1"
  },
  "Sergio Perez": { 
    team: "Red Bull Racing", 
    teamEncoded: 0, 
    experience: 13,
    image: "https://www.formula1.com/content/dam/fom-website/drivers/S/SERPER01_Sergio_Perez/serper01.png.transform/1col/image.png",
    flag: "🇲🇽",
    number: "11"
  },
  "Lewis Hamilton": { 
    team: "Mercedes", 
    teamEncoded: 1, 
    experience: 17,
    image: "https://www.formula1.com/content/dam/fom-website/drivers/L/LEWHAM01_Lewis_Hamilton/lewham01.png.transform/1col/image.png",
    flag: "🇬🇧",
    number: "44"
  },
  "George Russell": { 
    team: "Mercedes", 
    teamEncoded: 1, 
    experience: 3,
    image: "https://www.formula1.com/content/dam/fom-website/drivers/G/GEORUS01_George_Russell/georus01.png.transform/1col/image.png",
    flag: "🇬🇧",
    number: "63"
  },
  "Charles Leclerc": { 
    team: "Ferrari", 
    teamEncoded: 2, 
    experience: 6,
    image: "https://www.formula1.com/content/dam/fom-website/drivers/C/CHALEC01_Charles_Leclerc/chalec01.png.transform/1col/image.png",
    flag: "🇲🇨",
    number: "16"
  },
  "Carlos Sainz": { 
    team: "Ferrari", 
    teamEncoded: 2, 
    experience: 9,
    image: "https://www.formula1.com/content/dam/fom-website/drivers/C/CARSAI01_Carlos_Sainz/carsai01.png.transform/1col/image.png",
    flag: "🇪🇸",
    number: "55"
  },
  "Lando Norris": { 
    team: "McLaren", 
    teamEncoded: 3, 
    experience: 5,
    image: "https://www.formula1.com/content/dam/fom-website/drivers/L/LANNOR01_Lando_Norris/lannor01.png.transform/1col/image.png",
    flag: "🇬🇧",
    number: "4"
  },
  "Oscar Piastri": { 
    team: "McLaren", 
    teamEncoded: 3, 
    experience: 1,
    image: "https://www.formula1.com/content/dam/fom-website/drivers/O/OSCPIA01_Oscar_Piastri/oscpia01.png.transform/1col/image.png",
    flag: "🇦🇺",
    number: "81"
  },
  "Fernando Alonso": { 
    team: "Aston Martin", 
    teamEncoded: 4, 
    experience: 22,
    image: "https://www.formula1.com/content/dam/fom-website/drivers/F/FERALO01_Fernando_Alonso/feralo01.png.transform/1col/image.png",
    flag: "🇪🇸",
    number: "14"
  },
  "Lance Stroll": { 
    team: "Aston Martin", 
    teamEncoded: 4, 
    experience: 7,
    image: "https://www.formula1.com/content/dam/fom-website/drivers/L/LANSTR01_Lance_Stroll/lanstr01.png.transform/1col/image.png",
    flag: "🇨🇦",
    number: "18"
  },
  "Esteban Ocon": { 
    team: "Alpine", 
    teamEncoded: 5, 
    experience: 7,
    image: "https://www.formula1.com/content/dam/fom-website/drivers/E/ESTOCO01_Esteban_Ocon/estoco01.png.transform/1col/image.png",
    flag: "🇫🇷",
    number: "31"
  },
  "Pierre Gasly": { 
    team: "Alpine", 
    teamEncoded: 5, 
    experience: 6,
    image: "https://www.formula1.com/content/dam/fom-website/drivers/P/PIEGAS01_Pierre_Gasly/piegas01.png.transform/1col/image.png",
    flag: "🇫🇷",
    number: "10"
  },
  "Nico Hulkenberg": { 
    team: "Haas", 
    teamEncoded: 6, 
    experience: 8,
    image: "https://www.formula1.com/content/dam/fom-website/drivers/N/NICHUL01_Nico_Hulkenberg/nichul01.png.transform/1col/image.png",
    flag: "🇩🇪",
    number: "27"
  },
  "Kevin Magnussen": { 
    team: "Haas", 
    teamEncoded: 6, 
    experience: 8,
    image: "https://www.formula1.com/content/dam/fom-website/drivers/K/KEVMAG01_Kevin_Magnussen/kevmag01.png.transform/1col/image.png",
    flag: "🇩🇰",
    number: "20"
  },
  "Daniel Ricciardo": { 
    team: "RB", 
    teamEncoded: 7, 
    experience: 13,
    image: "https://www.formula1.com/content/dam/fom-website/drivers/D/DANRIC01_Daniel_Ricciardo/danric01.png.transform/1col/image.png",
    flag: "🇦🇺",
    number: "3"
  },
  "Yuki Tsunoda": { 
    team: "RB", 
    teamEncoded: 7, 
    experience: 3,
    image: "https://www.formula1.com/content/dam/fom-website/drivers/Y/YUKTSU01_Yuki_Tsunoda/yuktsu01.png.transform/1col/image.png",
    flag: "🇯🇵",
    number: "22"
  },
  "Alex Albon": { 
    team: "Williams", 
    teamEncoded: 8, 
    experience: 4,
    image: "https://www.formula1.com/content/dam/fom-website/drivers/A/ALEALB01_Alexander_Albon/alealb01.png.transform/1col/image.png",
    flag: "🇹🇭",
    number: "23"
  },
  "Logan Sargeant": { 
    team: "Williams", 
    teamEncoded: 8, 
    experience: 1,
    image: "https://www.formula1.com/content/dam/fom-website/drivers/L/LOGSAR01_Logan_Sargeant/logsar01.png.transform/1col/image.png",
    flag: "🇺🇸",
    number: "2"
  },
  "Valtteri Bottas": { 
    team: "Kick Sauber", 
    teamEncoded: 9, 
    experience: 11,
    image: "https://www.formula1.com/content/dam/fom-website/drivers/V/VALBOT01_Valtteri_Bottas/valbot01.png.transform/1col/image.png",
    flag: "🇫🇮",
    number: "77"
  },
  "Zhou Guanyu": { 
    team: "Kick Sauber", 
    teamEncoded: 9, 
    experience: 2,
    image: "https://www.formula1.com/content/dam/fom-website/drivers/G/GUAZHO01_Guanyu_Zhou/guazho01.png.transform/1col/image.png",
    flag: "🇨🇳",
    number: "24"
  },
};

const races = [
  {
    name: "Bahrain Grand Prix",
    circuit: "Bahrain International Circuit",
    image: "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Bahrain_Circuit.png.transform/7col/image.png",
    flag: "🇧🇭",
    laps: 57
  },
  {
    name: "Saudi Arabian Grand Prix",
    circuit: "Jeddah Corniche Circuit", 
    image: "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Saudi_Arabia_Circuit.png.transform/7col/image.png",
    flag: "🇸🇦",
    laps: 50
  },
  {
    name: "Australian Grand Prix",
    circuit: "Albert Park Circuit",
    image: "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Australia_Circuit.png.transform/7col/image.png",
    flag: "🇦🇺",
    laps: 58
  },
  {
    name: "Japanese Grand Prix",
    circuit: "Suzuka International Racing Course",
    image: "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Japan_Circuit.png.transform/7col/image.png",
    flag: "🇯🇵",
    laps: 53
  },
  {
    name: "Chinese Grand Prix",
    circuit: "Shanghai International Circuit",
    image: "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/China_Circuit.png.transform/7col/image.png",
    flag: "🇨🇳",
    laps: 56
  },
  {
    name: "Miami Grand Prix",
    circuit: "Miami International Autodrome",
    image: "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Miami_Circuit.png.transform/7col/image.png",
    flag: "🇺🇸",
    laps: 57
  },
  {
    name: "Emilia Romagna Grand Prix",
    circuit: "Autodromo Enzo e Dino Ferrari",
    image: "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Emilia_Romagna_Circuit.png.transform/7col/image.png",
    flag: "🇮🇹",
    laps: 63
  },
  {
    name: "Monaco Grand Prix",
    circuit: "Circuit de Monaco",
    image: "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Monaco_Circuit.png.transform/7col/image.png",
    flag: "🇲🇨",
    laps: 78
  },
  {
    name: "Canadian Grand Prix",
    circuit: "Circuit Gilles Villeneuve",
    image: "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Canada_Circuit.png.transform/7col/image.png",
    flag: "🇨🇦",
    laps: 70
  },
  {
    name: "Spanish Grand Prix",
    circuit: "Circuit de Barcelona-Catalunya",
    image: "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Spain_Circuit.png.transform/7col/image.png",
    flag: "🇪🇸",
    laps: 66
  },
  {
    name: "Austrian Grand Prix",
    circuit: "Red Bull Ring",
    image: "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Austria_Circuit.png.transform/7col/image.png",
    flag: "🇦🇹",
    laps: 71
  },
  {
    name: "British Grand Prix",
    circuit: "Silverstone Circuit",
    image: "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Great_Britain_Circuit.png.transform/7col/image.png",
    flag: "🇬🇧",
    laps: 52
  },
  {
    name: "Hungarian Grand Prix",
    circuit: "Hungaroring",
    image: "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Hungary_Circuit.png.transform/7col/image.png",
    flag: "🇭🇺",
    laps: 70
  },
  {
    name: "Belgian Grand Prix",
    circuit: "Circuit de Spa-Francorchamps",
    image: "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Belgium_Circuit.png.transform/7col/image.png",
    flag: "🇧🇪",
    laps: 44
  },
  {
    name: "Dutch Grand Prix",
    circuit: "Circuit Zandvoort",
    image: "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Netherlands_Circuit.png.transform/7col/image.png",
    flag: "🇳🇱",
    laps: 72
  },
  {
    name: "Italian Grand Prix",
    circuit: "Autodromo Nazionale Monza",
    image: "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Italy_Circuit.png.transform/7col/image.png",
    flag: "🇮🇹",
    laps: 53
  },
  {
    name: "Azerbaijan Grand Prix",
    circuit: "Baku City Circuit",
    image: "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Azerbaijan_Circuit.png.transform/7col/image.png",
    flag: "🇦🇿",
    laps: 51
  },
  {
    name: "Singapore Grand Prix",
    circuit: "Marina Bay Street Circuit",
    image: "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Singapore_Circuit.png.transform/7col/image.png",
    flag: "🇸🇬",
    laps: 61
  },
  {
    name: "United States Grand Prix",
    circuit: "Circuit of the Americas",
    image: "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/USA_Circuit.png.transform/7col/image.png",
    flag: "🇺🇸",
    laps: 56
  },
  {
    name: "Mexican Grand Prix",
    circuit: "Autodromo Hermanos Rodriguez",
    image: "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Mexico_Circuit.png.transform/7col/image.png",
    flag: "🇲🇽",
    laps: 71
  },
  {
    name: "Brazilian Grand Prix",
    circuit: "Autodromo Jose Carlos Pace",
    image: "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Brazil_Circuit.png.transform/7col/image.png",
    flag: "🇧🇷",
    laps: 71
  },
  {
    name: "Las Vegas Grand Prix",
    circuit: "Las Vegas Strip Circuit",
    image: "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Las_Vegas_Circuit.png.transform/7col/image.png",
    flag: "🇺🇸",
    laps: 50
  },
  {
    name: "Qatar Grand Prix",
    circuit: "Lusail International Circuit",
    image: "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Qatar_Circuit.png.transform/7col/image.png",
    flag: "🇶🇦",
    laps: 57
  },
  {
    name: "Abu Dhabi Grand Prix",
    circuit: "Yas Marina Circuit",
    image: "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Abu_Dhabi_Circuit.png.transform/7col/image.png",
    flag: "🇦🇪",
    laps: 58
  }
];

const seasons = [2021, 2022, 2023, 2024, 2025];

export default function App() {
  const [formData, setFormData] = useState({
    season: "",
    driver: "",
    race: "",
    customExperience: "",
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentStep, setCurrentStep] = useState(1);
  const [showDriverGrid, setShowDriverGrid] = useState(false);
  const [showRaceGrid, setShowRaceGrid] = useState(false);

  const selectedDriverInfo = formData.driver ? driverTeamMap[formData.driver] : null;
  const selectedRaceInfo = formData.race ? races.find(r => r.name === formData.race) : null;

  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleDriverSelect = (driverName) => {
    setFormData((prev) => ({ ...prev, driver: driverName }));
    setShowDriverGrid(false);
    setCurrentStep(3);
  };

  const handleRaceSelect = (raceName) => {
    setFormData((prev) => ({ ...prev, race: raceName }));
    setShowRaceGrid(false);
    setCurrentStep(4);
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
      const res = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
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
      setPrediction(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getTeamColor = (teamEncoded) => {
    const colors = {
      0: '#3B82F6', 1: '#6B7280', 2: '#DC2626', 3: '#F97316', 4: '#16A34A',
      5: '#EC4899', 6: '#EF4444', 7: '#60A5FA', 8: '#1E40AF', 9: '#22C55E'
    };
    return colors[teamEncoded] || '#6B7280';
  };

  return (
    <div className="app-container">
      {/* Header */}
      <motion.div 
        className="header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <h1>🏎️ F1 PULSE</h1>
        <p>Advanced Position Prediction System</p>
        
        <div className="progress-container">
          {[1, 2, 3, 4].map((step) => (
            <div
              key={step}
              className={`progress-dot ${currentStep >= step ? 'active' : ''}`}
            />
          ))}
        </div>
        
        <div className="progress-labels">
          {['Season', 'Driver', 'Circuit', 'Predict'].map((label, idx) => (
            <span key={label} className={currentStep >= idx + 1 ? 'active' : ''}>
              {label}
            </span>
          ))}
        </div>
      </motion.div>

      {/* Main Content */}
      <div className="main-content">
        {/* Form Section */}
        <motion.div 
          className="card"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6 }}
        >
          <form onSubmit={handleSubmit} className="form-section">
            
            {/* Step 1: Season Selection */}
            <div>
              <div className="step-header">
                <span className="step-number">1</span>
                <h3 className="step-title">Select Season</h3>
              </div>
              <div className="season-grid">
                {seasons.map((season) => (
                  <button
                    key={season}
                    type="button"
                    onClick={() => {
                      setFormData(prev => ({ ...prev, season }));
                      setCurrentStep(2);
                    }}
                    className={`season-button ${formData.season === season ? 'selected' : ''}`}
                  >
                    <div className="season-year">{season}</div>
                    <div className="season-type">
                      {season === 2025 ? '🔮 Future' : '📊 Historical'}
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Step 2: Driver Selection */}
            {currentStep >= 2 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              >
                <div className="step-header">
                  <span className="step-number">2</span>
                  <h3 className="step-title">Select Driver</h3>
                </div>
                
                {!showDriverGrid ? (
                  <div 
                    className="selection-placeholder"
                    onClick={() => setShowDriverGrid(true)}
                  >
                    {selectedDriverInfo ? (
                      <div className="selection-content">
                        <img 
                          src={selectedDriverInfo.image} 
                          alt={formData.driver}
                          className="driver-avatar"
                          onError={(e) => {
                            e.target.src = `https://via.placeholder.com/64x64/FF6B6B/FFFFFF?text=${selectedDriverInfo.flag}`;
                          }}
                        />
                        <div className="selection-info">
                          <h3>{formData.driver}</h3>
                          <p>{selectedDriverInfo.team} • {selectedDriverInfo.flag} #{selectedDriverInfo.number}</p>
                        </div>
                      </div>
                    ) : (
                      <div className="selection-info">
                        <h3>Choose Your Driver</h3>
                        <p>Click to view all drivers</p>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="grid-container">
                    <div className="driver-grid">
                      {Object.entries(driverTeamMap).map(([driverName, info]) => (
                        <div
                          key={driverName}
                          className="driver-card"
                          onClick={() => handleDriverSelect(driverName)}
                          style={{ borderColor: getTeamColor(info.teamEncoded) }}
                        >
                          <div className="driver-number">#{info.number}</div>
                          <img 
                            src={info.image} 
                            alt={driverName}
                            className="driver-image"
                            onError={(e) => {
                              e.target.src = `https://via.placeholder.com/100x100/FF6B6B/FFFFFF?text=${info.flag}`;
                            }}
                          />
                          <div className="driver-name">{driverName.split(' ')[1]}</div>
                          <div className="driver-info">{info.flag} • {info.experience}y exp</div>
                          <span 
                            className="team-badge"
                            style={{ backgroundColor: getTeamColor(info.teamEncoded) }}
                          >
                            {info.team.split(' ')[0]}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            )}

            {/* Step 3: Circuit Selection */}
            {currentStep >= 3 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              >
                <div className="step-header">
                  <span className="step-number">3</span>
                  <h3 className="step-title">Select Circuit</h3>
                </div>
                
                {!showRaceGrid ? (
                  <div 
                    className="selection-placeholder"
                    onClick={() => setShowRaceGrid(true)}
                  >
                    {selectedRaceInfo ? (
                      <div className="selection-info">
                        <h3>{selectedRaceInfo.name}</h3>
                        <p>{selectedRaceInfo.circuit} • {selectedRaceInfo.laps} Laps</p>
                      </div>
                    ) : (
                      <div className="selection-info">
                        <h3>Choose Circuit</h3>
                        <p>Click to view all circuits</p>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="grid-container">
                    <div className="circuit-grid">
                      {races.map((race) => (
                        <div
                          key={race.name}
                          className="circuit-card"
                          onClick={() => handleRaceSelect(race.name)}
                        >
                          <div className="circuit-image-container">
                            <img 
                              src={race.image} 
                              alt={race.circuit}
                              className="circuit-image"
                              onError={(e) => {
                                e.target.src = "https://via.placeholder.com/400x200/FF6B6B/FFFFFF?text=Circuit+Map";
                              }}
                            />
                            <div className="circuit-overlay">
                              <span>{race.flag}</span>
                            </div>
                          </div>
                          <div className="circuit-name">{race.name}</div>
                          <div className="circuit-location">{race.circuit}</div>
                          <div className="circuit-badges">
                            <span className="circuit-badge">{race.laps} Laps</span>
                            <span className="circuit-badge">{race.flag}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            )}

            {/* Step 4: Final Settings & Submit */}
            {currentStep >= 4 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              >
                <div className="step-header">
                  <span className="step-number">4</span>
                  <h3 className="step-title">Final Settings</h3>
                </div>
                
                {selectedDriverInfo && (
                  <div className="submit-section">
                    <div className="driver-summary">
                      <img 
                        src={selectedDriverInfo.image} 
                        alt={formData.driver}
                        className="driver-avatar"
                      />
                      <div className="driver-details">
                        <h4>{formData.driver}</h4>
                        <p>{selectedDriverInfo.team}</p>
                        <p>Default: {selectedDriverInfo.experience} years experience</p>
                      </div>
                    </div>
                    
                    <div className="input-group">
                      <label className="input-label">
                        Override Driver Experience (Optional)
                      </label>
                      <input
                        type="number"
                        name="customExperience"
                        value={formData.customExperience}
                        onChange={handleChange}
                        min="1"
                        max="25"
                        placeholder={`Default: ${selectedDriverInfo.experience} years`}
                        className="input-field"
                      />
                      <p className="input-help">
                        Leave empty to use default experience for selected driver
                      </p>
                    </div>
                  </div>
                )}

                <button
                  type="submit"
                  disabled={loading || !formData.season || !formData.driver || !formData.race}
                  className="btn btn-primary w-full"
                >
                  {loading ? (
                    <>
                      <span className="loading-icon">🏎️</span>
                      Predicting Position...
                    </>
                  ) : (
                    "🏁 PREDICT FINISHING POSITION"
                  )}
                </button>
              </motion.div>
            )}
          </form>
        </motion.div>

        {/* Results Section */}
        <motion.div 
          className="results-section"
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          {/* Error Display */}
          {error && (
            <motion.div 
              className="card error-card"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
            >
              <div className="error-content">
                <span className="error-icon">⚠️</span>
                <div>
                  <h3 className="error-title">Prediction Failed</h3>
                  <p className="error-message">{error}</p>
                </div>
              </div>
            </motion.div>
          )}

          {/* Loading State */}
          {loading && (
            <motion.div 
              className="card loading-card"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
            >
              <div className="loading-icon">🏎️</div>
              <h3>Analyzing Race Data</h3>
              <p>AI is processing your prediction...</p>
            </div>
          )}

          {/* Prediction Results */}
          {prediction && (
            <motion.div 
              className="card"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              <div className="text-center mb-4">
                <h2>🏁 Position Prediction</h2>
                <p>AI-Powered F1 Race Analysis</p>
              </div>
              
              <div className="prediction-card">
                <div className="prediction-header">Predicted Finishing Position</div>
                <div className="prediction-position">
                  P{prediction.predicted_position || prediction.predictedPosition}
                </div>
                <div className="prediction-confidence">
                  {((prediction.prediction_confidence || prediction.predictionConfidence || 0) * 100).toFixed(1)}% Confidence
                </div>
              </div>

              <div className="info-grid">
                <div className="info-card">
                  <h4>
                    <span>👨‍🏎️</span>
                    Driver Analysis
                  </h4>
                  {selectedDriverInfo && (
                    <>
                      <div className="driver-summary">
                        <img 
                          src={selectedDriverInfo.image} 
                          alt={formData.driver}
                          className="driver-avatar"
                        />
                        <div className="driver-details">
                          <h4>{formData.driver}</h4>
                          <p>{selectedDriverInfo.team}</p>
                          <p>{selectedDriverInfo.flag} #{selectedDriverInfo.number}</p>
                        </div>
                      </div>
                      <p><strong>Experience:</strong> {formData.customExperience || selectedDriverInfo.experience} years</p>
                      <p><strong>Season:</strong> {formData.season}</p>
                    </>
                  )}
                </div>

                <div className="info-card">
                  <h4>
                    <span>🏁</span>
                    Circuit Analysis
                  </h4>
                  {selectedRaceInfo && (
                    <>
                      <p><strong>{selectedRaceInfo.name}</strong></p>
                      <p>{selectedRaceInfo.circuit}</p>
                      <p><strong>Total Laps:</strong> {selectedRaceInfo.laps}</p>
                      <p><strong>Country:</strong> {selectedRaceInfo.flag}</p>
                    </>
                  )}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-4 mt-4">
                <button
                  onClick={() => {
                    setFormData({season: "", driver: "", race: "", customExperience: ""});
                    setPrediction(null);
                    setCurrentStep(1);
                    setShowDriverGrid(false);
                    setShowRaceGrid(false);
                  }}
                  className="btn btn-secondary flex-1"
                >
                  🔄 New Prediction
                </button>
                <button
                  onClick={() => {
                    navigator.clipboard.writeText(`F1 Pulse Prediction: ${formData.driver} at ${formData.race} ${formData.season} - Predicted Position: P${prediction.predicted_position || prediction.predictedPosition} (${((prediction.prediction_confidence || prediction.predictionConfidence || 0) * 100).toFixed(1)}% confidence)`);
                    alert("Prediction copied to clipboard!");
                  }}
                  className="btn btn-outline flex-1"
                >
                  📋 Share Result
                </button>
              </div>
            </motion.div>
          )}

          {/* Welcome Message */}
          {!prediction && !loading && !error && (
            <motion.div 
              className="card welcome-card"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className="welcome-icon">🏁</div>
              <h3 className="welcome-title">Welcome to F1 Pulse</h3>
              <p className="welcome-description">
                Advanced AI-powered F1 position prediction system. 
                Follow the steps to get your race prediction!
              </p>
              
              <div className="feature-grid">
                <div className="feature-card">
                  <div className="feature-icon">🤖</div>
                  <div className="feature-title">AI Powered</div>
                  <p className="feature-description">Machine Learning predictions based on historical F1 data</p>
                </div>
                
                <div className="feature-card">
                  <div className="feature-icon">📊</div>
                  <div className="feature-title">Historical Data</div>
                  <p className="feature-description">Compare predictions with actual race results</p>
                </div>
                
                <div className="feature-card">
                  <div className="feature-icon">⚡</div>
                  <div className="feature-title">Real-time</div>
                  <p className="feature-description">Instant predictions with confidence metrics</p>
                </div>
              </div>
            </motion.div>
          )}
        </motion.div>
      </div>
    </div>
  );
}
