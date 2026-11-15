
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Eye, EyeOff } from "lucide-react";

import { loginUser } from "../api/auth.js";
import "../styles/LoginPage.css";

function LoginPage() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();

    setMessage("");
    setMessageType("");

    if (!email.trim() || !password) {
      setMessage("Заполните все обязательные поля.");
      setMessageType("error");
      return;
    }

    setIsLoading(true);

    try {
      await loginUser({
        email: email.trim(),
        password,
      });

      navigate("/profile");
    } catch (error) {
      const status = error.response?.status;

      if (status === 401) {
        setMessage("Неверная электронная почта или пароль.");
      } else if (status === 422) {
        setMessage("Проверьте правильность введённых данных.");
      } else if (!error.response) {
        setMessage("Не удалось подключиться к серверу.");
      } else {
        setMessage("Не удалось выполнить вход. Попробуйте ещё раз.");
      }

      setMessageType("error");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <section className="login-page">
      <div className="login-card">
        <div className="login-header">
          <h1>С возвращением!</h1>
          <p>Войдите в свой аккаунт Photo Studio.</p>
        </div>

        <form className="login-form" onSubmit={handleSubmit}>
          <div className="login-field">
            <label htmlFor="login-email">
              Электронная почта
            </label>

            <input
              id="login-email"
              type="email"
              placeholder="example@mail.com"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              autoComplete="email"
            />
          </div>

          <div className="login-field">
            <label htmlFor="login-password">
              Пароль
            </label>

            <div className="register-password-wrapper">
              <input
                id="login-password"
                type={showPassword ? "text" : "password"}
                placeholder="Введите пароль"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                autoComplete="current-password"
              />

              <button
                type="button"
                className="register-password-toggle"
                onClick={() => setShowPassword(!showPassword)}
                aria-label={
                  showPassword ? "Скрыть пароль" : "Показать пароль"
                }
              >
                {showPassword ? (
                  <EyeOff size={19} />
                ) : (
                  <Eye size={19} />
                )}
              </button>
            </div>
          </div>

          {message && (
            <div className={`login-message ${messageType}`} role="alert">
              {message}
            </div>
          )}

          <button
            type="submit"
            className="login-submit"
            disabled={isLoading}
          >
            {isLoading ? "Выполняется вход..." : "Войти"}
          </button>
        </form>

        <div className="login-footer">
          <p>
            Ещё нет аккаунта?{" "}
            <Link to="/register">Зарегистрироваться</Link>
          </p>
        </div>
      </div>
    </section>
  );
}

export default LoginPage;
