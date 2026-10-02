'use client'

import { useState, useEffect } from 'react'
import BottomNav from '@/components/BottomNav'

export default function EventHubPage() {
  const [timeLeft, setTimeLeft] = useState({ days: 0, hours: 0, mins: 0, secs: 0 })

  useEffect(() => {
    const target = new Date("2026-10-07T20:00:00").getTime()
    
    const interval = setInterval(() => {
      const now = new Date().getTime()
      const distance = target - now
      
      if (distance < 0) {
        clearInterval(interval)
        return
      }
      
      setTimeLeft({
        days: Math.floor(distance / (1000 * 60 * 60 * 24)),
        hours: Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
        mins: Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)),
        secs: Math.floor((distance % (1000 * 60)) / 1000)
      })
    }, 1000)
    
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="min-h-screen bg-rose-dark flex flex-col p-4 relative overflow-x-hidden font-sans">
      
      <div className="absolute top-0 right-0 w-64 h-64 bg-pink-primary/10 rounded-full blur-[100px] pointer-events-none"></div>

      <div className="w-full max-w-md mx-auto flex-1 flex flex-col pt-4 pb-24 z-10 space-y-6">
        
        {/* Top Hero */}
        <div className="luxury-glass p-8 text-center relative overflow-hidden rounded-3xl border-t border-pink-soft/30 shadow-[0_15px_40px_rgba(42,10,24,0.6)]">
           <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(224,53,102,0.2),transparent_70%)] pointer-events-none"></div>
           
           <h1 className="text-4xl font-serif text-white font-bold drop-shadow-md mb-2">Bennett Élan</h1>
           <p className="text-pink-soft tracking-[0.2em] text-[10px] uppercase font-bold mb-8">Ball Night 2026</p>
           
           {/* Countdown */}
           <div className="flex justify-center gap-3">
             {Object.entries(timeLeft).map(([unit, value]) => (
               <div key={unit} className="flex flex-col items-center">
                 <div className="w-14 h-14 rounded-2xl bg-black/40 border border-white/10 flex items-center justify-center backdrop-blur-md shadow-inner">
                   <span className="text-2xl text-white font-serif font-bold">{value}</span>
                 </div>
                 <span className="text-[10px] text-pink-soft/70 uppercase tracking-widest mt-2">{unit}</span>
               </div>
             ))}
           </div>
        </div>

        {/* Info Grid */}
        <div className="grid grid-cols-2 gap-4">
           <div className="luxury-glass p-6 rounded-3xl flex flex-col items-center text-center justify-center border-t border-white/10 hover:border-pink-primary/30 transition-colors">
              <span className="text-3xl mb-3">🎩</span>
              <h3 className="text-white font-bold text-sm">Theme</h3>
              <p className="text-pink-soft/70 text-xs font-serif italic mt-1">Bridgerton</p>
           </div>
           <div className="luxury-glass p-6 rounded-3xl flex flex-col items-center text-center justify-center border-t border-white/10 hover:border-pink-primary/30 transition-colors">
              <span className="text-3xl mb-3">📍</span>
              <h3 className="text-white font-bold text-sm">Venue</h3>
              <p className="text-pink-soft/70 text-xs mt-1">Main Campus Lawn</p>
           </div>
        </div>

        {/* Map / Directions */}
        <div className="luxury-glass p-6 rounded-3xl">
           <h3 className="text-white font-bold text-lg mb-4 flex items-center gap-2">
             <span className="text-pink-primary">🗺️</span> Campus Map
           </h3>
           <div className="w-full aspect-video bg-black/40 rounded-2xl border border-white/10 flex items-center justify-center overflow-hidden relative group">
              <span className="text-white/30 text-sm font-medium z-10">Map Image Placeholder</span>
              <div className="absolute inset-0 bg-gradient-to-br from-pink-primary/5 to-burgundy/20 group-hover:opacity-50 transition-opacity"></div>
           </div>
           <p className="text-pink-soft/60 text-xs text-center mt-3 font-medium">Upload map image to view venue details</p>
        </div>

        {/* Itinerary */}
        <div className="luxury-glass p-6 rounded-3xl">
           <h3 className="text-white font-bold text-lg mb-6 flex items-center gap-2">
             <span className="text-pink-primary">✨</span> Itinerary
           </h3>
           
           <div className="space-y-6 relative before:absolute before:inset-0 before:ml-2.5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-white/10 before:to-transparent">
              
              <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                <div className="flex items-center justify-center w-5 h-5 rounded-full bg-pink-primary shadow-[0_0_10px_rgba(224,53,102,0.8)] border-2 border-rose-dark shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10"></div>
                <div className="w-[calc(100%-2.5rem)] md:w-[calc(50%-2.5rem)] bg-white/5 border border-white/10 p-4 rounded-2xl backdrop-blur-sm">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-bold text-white text-sm">Arrival & Mocktails</span>
                    <span className="text-xs text-pink-primary font-bold">8:00 PM</span>
                  </div>
                  <p className="text-xs text-pink-soft/70">Red carpet entrance and professional photography.</p>
                </div>
              </div>

              <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                <div className="flex items-center justify-center w-5 h-5 rounded-full bg-white/20 border-2 border-rose-dark shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10"></div>
                <div className="w-[calc(100%-2.5rem)] md:w-[calc(50%-2.5rem)] bg-white/5 border border-white/10 p-4 rounded-2xl backdrop-blur-sm">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-bold text-white text-sm">First Dance</span>
                    <span className="text-xs text-pink-primary font-bold">9:30 PM</span>
                  </div>
                  <p className="text-xs text-pink-soft/70">The floor opens with classical Bridgerton arrangements.</p>
                </div>
              </div>

           </div>
        </div>

      </div>
      <BottomNav />
    </div>
  )
}
