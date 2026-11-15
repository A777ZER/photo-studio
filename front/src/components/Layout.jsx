
import { Link, NavLink, Outlet } from "react-router-dom";

import "../styles/Layout.css";

function Layout() {
  return (
    <div className="app-layout">
      <header className="header">
        <div className="header-container">
          <Link to="/" className="logo">
            Photo Studio
          </Link>

          <nav className="navigation">
            <NavLink to="/" end>
              Главная
            </NavLink>

            <NavLink to="/services">
              Услуги
            </NavLink>

            <NavLink to="/login">
              Войти
            </NavLink>

            <NavLink to="/register">
              Регистрация
            </NavLink>
          </nav>
        </div>
      </header>

      <main className="main-content">
        <Outlet />
      </main>

      <footer className="footer">
        <p>© {new Date().getFullYear()} Photo Studio</p>
        <p>Все права защищены.</p>
      </footer>
    </div>
  );
}

export default Layout;
