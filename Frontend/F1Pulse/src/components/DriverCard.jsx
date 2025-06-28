// src/components/DriverCard.jsx
import React from 'react';
import { motion } from 'framer-motion';

const DriverCard = ({ driverName, info, index, isSelected, onSelect }) => {
  return (
    <motion.button
      type="button"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05 }}
      whileHover={{ 
        scale: 1.08, 
        y: -8,
        rotateY: 5,
        boxShadow: "0 20px 40px rgba(0,0,0,0.2)",
      }}
      whileTap={{ scale: 0.95 }}
      onClick={() => onSelect(driverName)}
      className="relative p-4 bg-white border-2 border-gray-200 rounded-xl shadow-sm hover:shadow-2xl transition-all duration-300 overflow-hidden group"
      style={{
        borderColor: 
          info.teamEncoded === 0 ? '#3B82F6' :
          info.teamEncoded === 1 ? '#6B7280' :
          info.teamEncoded === 2 ? '#DC2626' :
          info.teamEncoded === 3 ? '#F97316' :
          info.teamEncoded === 4 ? '#16A34A' :
          info.teamEncoded === 5 ? '#EC4899' :
          info.teamEncoded === 6 ? '#EF4444' :
          info.teamEncoded === 7 ? '#60A5FA' :
          info.teamEncoded === 8 ? '#1E40AF' :
          '#22C55E'
      }}
    >
      {/* Team color stripe */}
      <div 
        className="absolute top-0 left-0 w-full h-1"
        style={{
          backgroundColor: 
            info.teamEncoded === 0 ? '#3B82F6' :
            info.teamEncoded === 1 ? '#6B7280' :
            info.teamEncoded === 2 ? '#DC2626' :
            info.teamEncoded === 3 ? '#F97316' :
            info.teamEncoded === 4 ? '#16A34A' :
            info.teamEncoded === 5 ? '#EC4899' :
            info.teamEncoded === 6 ? '#EF4444' :
            info.teamEncoded === 7 ? '#60A5FA' :
            info.teamEncoded === 8 ? '#1E40AF' :
            '#22C55E'
        }}
      />
      
      {/* Hover glow effect */}
      <motion.div
        className="absolute inset-0 opacity-0 group-hover:opacity-20 transition-opacity duration-300"
        style={{
          background: `linear-gradient(45deg, transparent, ${
            info.teamEncoded === 0 ? '#3B82F6' :
            info.teamEncoded === 1 ? '#6B7280' :
            info.teamEncoded === 2 ? '#DC2626' :
            info.teamEncoded === 3 ? '#F97316' :
            info.teamEncoded === 4 ? '#16A34A' :
            info.teamEncoded === 5 ? '#EC4899' :
            info.teamEncoded === 6 ? '#EF4444' :
            info.teamEncoded === 7 ? '#60A5FA' :
            info.teamEncoded === 8 ? '#1E40AF' :
            '#22C55E'
          }, transparent)`,
        }}
      />
      
      {/* Driver number badge */}
      <div className="absolute top-2 right-2 bg-black text-white text-xs font-bold px-2 py-1 rounded-full">
        #{info.number}
      </div>
      
      {/* Selection indicator */}
      {isSelected && (
        <motion.div
          initial={{ scale: 0, rotate: 180 }}
          animate={{ scale: 1, rotate: 0 }}
          className="absolute -top-1 -left-1 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold z-10"
        >
          ✓
        </motion.div>
      )}
      
      <motion.img 
        src={info.image} 
        alt={driverName}
        className="w-full h-24 object-cover rounded-lg mb-3 group-hover:scale-110 transition-transform duration-300"
        whileHover={{ scale: 1.1 }}
        onError={(e) => {
          e.target.src = "https://via.placeholder.com/100x100/FF6B6B/FFFFFF?text=" + info.flag;
        }}
      />
      
      <motion.p 
        className="font-semibold text-sm text-center mb-1"
        animate={{
          color: isSelected ? '#DC2626' : '#374151',
        }}
      >
        {driverName.split(' ')[1]}
      </motion.p>
      
      <p className="text-xs text-gray-500 text-center mb-2">
        {info.flag} • {info.experience}y exp
      </p>
      
      <motion.div 
        className="text-xs text-center"
        whileHover={{ scale: 1.05 }}
      >
        <span 
          className={`px-2 py-1 rounded-full text-white font-semibold text-xs ${
            info.teamEncoded === 0 ? 'bg-blue-600' :
            info.teamEncoded === 1 ? 'bg-gray-600' :
            info.teamEncoded === 2 ? 'bg-red-600' :
            info.teamEncoded === 3 ? 'bg-orange-500' :
            info.teamEncoded === 4 ? 'bg-green-600' :
            info.teamEncoded === 5 ? 'bg-pink-500' :
            info.teamEncoded === 6 ? 'bg-red-400' :
            info.teamEncoded === 7 ? 'bg-blue-400' :
            info.teamEncoded === 8 ? 'bg-blue-800' :
            'bg-green-500'
          }`}
        >
          {info.team.split(' ')[0]}
        </span>
      </motion.div>
      
      {/* Performance indicator */}
      <motion.div 
        className="mt-2 flex justify-center space-x-1"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
      >
        {[...Array(Math.min(5, Math.max(1, Math.floor(info.experience / 4))))].map((_, i) => (
          <motion.div
            key={i}
            className="w-1 h-2 bg-yellow-400 rounded-full"
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
    </motion.button>
  );
};

export default DriverCard;
