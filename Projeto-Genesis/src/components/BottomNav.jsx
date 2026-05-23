import "../pages/ModoEstudo/ModoEstudo.css";
import HomeIconNav from '../assets/HomeIconNav.png'
import CalculadoraIconNav from '../assets/CalculadoraIconNav.png'
import EstudoIconNav from '../assets/EstudoIconNav.png'

export default function BottomNav({ navegar, active }) {
  return (
    <nav className="bottom-nav">
      <button
        className={`nav-btn ${active === 'home' ? 'active' : ''}`}
        onClick={() => navegar('home')}
        aria-label="Home"
      >
        <img src={HomeIconNav} alt='Icon Home' 
         style={{ width: '25px', height: '25px', objectFit: 'contain' }} />
      </button>

      <button
        className="nav-btn"
        aria-label="Calculadora"
        disabled
        style={{ opacity: 0.5, cursor: 'not-allowed' }}
      >
        <img src={CalculadoraIconNav} alt='Icon Calculador'
         style={{ width: '25px', height: '25px', objectFit: 'contain' }} />
      </button>

      <button
        className="nav-btn"
        aria-label="Modo Estudo"
        disabled
        style={{ opacity: 0.5, cursor: 'not-allowed' }}
      >
        <img src={EstudoIconNav} alt='Icon Estudo'
         style={{ width: '25px', height: '25px', objectFit: 'contain' }} />
      </button>
    </nav>
  )
}