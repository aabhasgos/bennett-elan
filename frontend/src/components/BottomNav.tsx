'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

export default function BottomNav() {
  const pathname = usePathname()

  const navItems = [
    { label: 'Discover', path: '/discover' },
    { label: 'Matches', path: '/matches' },
    { label: 'Event', path: '/event' },
    { label: 'Profile', path: '/profile' }
  ]

  return (
    <div className="fixed bottom-0 left-0 right-0 w-full max-w-md mx-auto bg-rose-dark/90 backdrop-blur-md border-t border-white/10 p-4 flex justify-around items-center z-50 rounded-t-3xl shadow-[0_-10px_30px_rgba(42,10,24,0.8)] pb-8">
      {navItems.map((item) => {
        const isActive = pathname.startsWith(item.path)
        return (
          <Link key={item.path} href={item.path} className="flex flex-col items-center gap-1 group">
            <span className={`text-xs font-bold tracking-widest uppercase transition-colors ${
              isActive 
                ? 'text-pink-primary' 
                : 'text-champagne/50 group-hover:text-champagne/80'
            }`}>
              {item.label}
            </span>
            {isActive && (
              <span className="w-1.5 h-1.5 rounded-full bg-pink-primary shadow-[0_0_8px_rgba(224,53,102,1)] absolute bottom-3"></span>
            )}
          </Link>
        )
      })}
    </div>
  )
}
