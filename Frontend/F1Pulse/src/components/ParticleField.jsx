// src/components/ParticleField.jsx
import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

const ParticleField = () => {
  const [dimensions, setDimensions] = useState({
    width: typeof window !== 'undefined' ? window.innerWidth : 1200,
    height: typeof window !== 'undefined' ? window.innerHeight : 800,
  });

  useEffect(() => {
    const handleResize = () => {
      setDimensions({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const particles = Array.from({ length: 15 }, (_, i) => ({
    id: i,
    size: Math.random() * 4 + 2,
    delay: Math.random() * 10,
    duration: 15 + Math.random() * 10,
    color: Math.random() > 0.5 ? 'red' : 'blue',
  }));

  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
      {particles.map((particle) => (
        <motion.div
          key={particle.id}
          className={`absolute rounded-full opacity-20 ${
            particle.color === 'red' ? 'bg-red-400' : 'bg-blue-400'
          }`}
          style={{
            width: particle.size,
            height: particle.size,
          }}
          animate={{
            x: [
              Math.random() * dimensions.width,
              Math.random() * dimensions.width,
              Math.random() * dimensions.width,
              Math.random() * dimensions.width,
            ],
            y: [
              Math.random() * dimensions.height,
              Math.random() * dimensions.height,
              Math.random() * dimensions.height,
              Math.random() * dimensions.height,
            ],
            scale: [1, 1.5, 0.5, 1],
            opacity: [0.2, 0.6, 0.1, 0.3],
          }}
          transition={{
            duration: particle.duration,
            repeat: Infinity,
            ease: "linear",
            delay: particle.delay,
          }}
        />
      ))}
      
      {/* Racing stripe particles */}
      {Array.from({ length: 5 }, (_, i) => (
        <motion.div
          key={`stripe-${i}`}
          className="absolute h-1 bg-gradient-to-r from-transparent via-red-500/30 to-transparent"
          style={{
            width: 100 + Math.random() * 200,
            top: Math.random() * dimensions.height,
          }}
          animate={{
            x: [-300, dimensions.width + 300],
            opacity: [0, 1, 0],
          }}
          transition={{
            duration: 8 + Math.random() * 4,
            repeat: Infinity,
            ease: "linear",
            delay: i * 2,
          }}
        />
      ))}
    </div>
  );
};

export default ParticleField;
