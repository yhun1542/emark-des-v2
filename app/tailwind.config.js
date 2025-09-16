export default {
  content: ["./index.html","./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        surface: { low:"var(--surface-low)", mid:"var(--surface-mid)", high:"var(--surface-high)", border:"var(--surface-border)" },
        textc: { base:"var(--text-base)", muted:"var(--text-muted)", strong:"var(--text-strong)", inv:"var(--text-inv)" },
        brand: { 500:"#42a9ff", 600:"#148dff" }
      },
      boxShadow: { soft:"0 6px 20px rgba(0,0,0,.08)" }
    }
  },
  plugins: []
}
