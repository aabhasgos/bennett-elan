import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-between p-4 bg-rose-dark relative overflow-hidden">
      
      {/* 3D Floating Elements */}
      <div className="absolute top-20 left-10 text-pink-primary opacity-20 text-6xl floating-heart">♥</div>
      <div className="absolute bottom-40 right-10 text-pink-soft opacity-30 text-8xl floating-heart" style={{ animationDelay: '2s' }}>♥</div>
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-pink-primary/10 rounded-full blur-[100px] pointer-events-none"></div>

      {/* Spacer */}
      <div className="flex-1"></div>

      {/* Main Content - Luxury Glass */}
      <div className="z-10 flex flex-col items-center text-center space-y-10 luxury-glass p-12 max-w-lg w-full">
        <div className="space-y-4 w-full">
          <h1 className="text-5xl md:text-6xl font-bold tracking-tight text-white font-serif drop-shadow-lg">
            Bennett Élan
          </h1>
          <p className="text-pink-soft tracking-[0.2em] text-sm uppercase font-medium">
            Ball Night 2026
          </p>
        </div>

        <div className="space-y-3 py-6 relative">
          <div className="absolute top-1/2 left-0 right-0 h-px bg-gradient-to-r from-transparent via-pink-primary/50 to-transparent"></div>
          <h2 className="text-3xl text-champagne italic font-serif relative inline-block bg-rose-dark px-4 z-10">Bridgerton</h2>
          <div className="space-y-1 text-white/80 pt-4">
            <p className="tracking-widest uppercase text-xs font-semibold">7 October</p>
            <p className="tracking-widest uppercase text-xs font-semibold">8 PM Onwards</p>
          </div>
        </div>

        <div className="pt-4 w-full">
          <Link href="/login" className="block w-full">
            <button className="w-full button-3d text-white font-bold py-5 px-8 text-lg tracking-wide">
              Enter with Google
            </button>
          </Link>
        </div>
      </div>

      {/* Spacer */}
      <div className="flex-1"></div>

      {/* Footer */}
      <footer className="w-full text-center py-6 text-xs text-pink-soft/60 space-x-6 border-t border-white/10 mt-8 z-10 font-medium">
        <Link href="/tos" className="hover:text-pink-soft transition-colors">Terms of Service</Link>
        <Link href="/privacy" className="hover:text-pink-soft transition-colors">Privacy Policy</Link>
        <span>© 2026 Bennett Élan</span>
      </footer>
    </div>
  )
}
