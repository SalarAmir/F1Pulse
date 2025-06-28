// src/components/CircuitCard.jsx
import React from 'react';
import { motion } from 'framer-motion';

const CircuitRay = ({ race, isSelected = false, delay = 0 }) => (
  <div className="relative w-full h-32 overflow-hidden rounded-lg group">
    <motion.img 
      src={race.image} 
      alt={race.circuit}
      className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
      whileHover={{ scale: 1.05 }}
      onError={(e) => {
        e.target.src = "https://via.placeholder.com/400x200/FF6B6B/FFFFFF?text=Circuit+Map";
      }}
    />
    
    {/* Primary animated ray */}
    <motion.div
      className="absolute inset-0 bg-gradient-to-r from-transparent via-red-500/40 to-transparent"
      animate={{
        x: ["-150%", "150%"],
      }}
      transition={{
        duration: 2.5,
        repeat: Infinity,
        ease: "linear",
        delay: delay,
      }}
      style={{
        width: "120px",
        height: "100%",
      }}
    />
    
    {/* Secondary blue ray for enhanced effect */}
    <motion.div
      className="absolute inset-0 bg-gradient-to-r from-transparent via-blue-400/30 to-transparent"
      animate={{
        x: ["150%", "-150%"],
      }}
      transition={{
        duration: 3,
        repeat: Infinity,
        ease: "linear",
        delay: delay + 1,
      }}
      style={{
        width: "80px",
        height: "100%",
      }}
    />
    
    {/* Pulsing selection indicator */}
    {isSelected && (
      <motion.div
        className="absolute inset-0 bg-red-500/20 border-2 border-red-500 rounded-lg"
        animate={{
          opacity: [0.3, 0.7, 0.3],
        }}
        transition={{
          duration: 1.5,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />
    )}
    
    {/* Corner speed lines for F1 feel */}
    <div className="absolute top-2 left-2">
      <motion.div
        className="flex space-x-1"
        animate={{
          opacity: [0.4, 1, 0.4],
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: "easeInOut",
          delay: delay + 0.5,
        }}
      >
        {[1, 2, 3].map((i) => (
          <div
            key={i}
            className="w-1 bg-white"
            style={{
              height: `${4 + i * 2}px`,
            }}
          />
        ))}
      </motion.div>
    </div>
    
    <div className="absolute inset-0 bg-black/20 flex items-center justify-center">
      <motion.div 
        className="text-white text-center"
        whileHover={{ scale: 1.1 }}
        transition={{ type: "spring", stiffness: 300 }}
      >
        <motion.p 
          className="font-bold text-xl mb-1"
          animate={{
            textShadow: [
              "0 0 5px rgba(255,255,255,0.5)",
              "0 0 10px rgba(255,255,255,0.8)",
              "0 0 5px rgba(255,255,255,0.5)",
            ],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        >
          {race.flag}
        </motion.p>
        <p className="text-sm font-semibold bg-black/50 px-2 py-1 rounded">
          {race.laps} Laps
        </p>
      </motion.div>
    </div>
  </div>
);

const CircuitCard = ({ race, index, isSelected, onSelect }) => {
  return (
    <motion.button
      type="button"
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.03 }}
      whileHover={{ 
        scale: 1.03,
        rotateX: 2,
        boxShadow: "0 25px 50px rgba(0,0,0,0.15)",
      }}
      whileTap={{ scale: 0.98 }}
      onClick={() => onSelect(race.name)}
      className="relative p-4 bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-2xl transition-all duration-300 overflow-hidden group"
    >
      {/* Circuit with enhanced animations */}
      <CircuitRay 
        race={race} 
        isSelected={isSelected}
        delay={index * 0.1}
      />
      
      {/* Hover overlay */}
      <motion.div
        className="absolute inset-0 bg-gradient-to-t from-red-500/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"
        initial={{ opacity: 0 }}
        whileHover={{ opacity: 1 }}
      />
      
      <div className="mt-3 text-center relative z-10">
        <motion.p 
          className="font-semibold text-sm mb-1"
          animate={{
            color: isSelected ? '#DC2626' : '#374151',
          }}
        >
          {race.name}
        </motion.p>
        <p className="text-xs text-gray-500">{race.circuit}</p>
        
        {/* Race info badges */}
        <div className="flex justify-center space-x-2 mt-2">
          <motion.span 
            className="px-2 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-medium"
            whileHover={{ scale: 1.05, backgroundColor: "#F3F4F6" }}
          >
            {race.laps} Laps
          </motion.span>
          <motion.span 
            className="px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-medium"
            whileHover={{ scale: 1.05, backgroundColor: "#DBEAFE" }}
          >
            {race.flag}
          </motion.span>
        </div>
        
        {/* Selection indicator */}
        {isSelected && (
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold"
          >
            ✓
          </motion.div>
        )}
        
        {/* Circuit difficulty indicator */}
        <motion.div 
          className="mt-2 flex justify-center space-x-1"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          {/* Difficulty based on number of laps (more laps = more challenging) */}
          {[...Array(Math.min(5, Math.max(1, Math.ceil(race.laps / 15))))].map((_, i) => (
            <motion.div
              key={i}
              className="w-1 h-2 bg-orange-400 rounded-full"
              animate={{
                scaleY: [1, 1.5, 1],
              }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                delay: i * 0.1,
                ease: "easeInOut",
              }}
            />
          ))}
        </motion.div>
      </div>
    </motion.button>
  );
};

export default CircuitCard;
