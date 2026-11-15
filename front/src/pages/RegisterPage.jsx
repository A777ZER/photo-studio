
import { useState } from "react";
import { Link } from "react-router-dom";
import { Eye, EyeOff } from "lucide-react";

import { registerUser } from "../api/auth.js";
import "../styles/RegisterPage.css";

function RegisterPage() {
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    password: "",
    confirm_password: "",
  });

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setMessage("");
    setMessageType("");

    if (
      !formData.first_name.trim() ||
      !formData.last_name.trim() ||
      !formData.email.trim() ||
      !formData.phone.trim() ||
      !formData.password ||
      !formData.confirm_password
    ) {
      setMessage("Заполните все обязательные поля.");
      setMessageType("error");
      return;
    }

    if (formData.password.length < 8) {
      setMessage("Пароль должен содержать не менее 8 символов.");
      setMessageType("error");
      return;
    }

    if (formData.password !== formData.confirm_password) {
      setMessage("Пароли не совпадают.");
      setMessageType("error");
      return;
    }

    setIsLoading(true);

    try {
      const userData = {
        first_name: formData.first_name.trim(),
        last_name: formData.last_name.trim(),
        email: formData.email.trim(),
        phone: formData.phone.trim(),
        password: formData.password,
      };

      await registerUser(userData);

      setMessage(
        "Регистрация прошла успешно! Теперь вы можете войти в аккаунт."
      );
      setMessageType("success");

      setFormData({
        first_name: "",
        last_name: "",
        email: "",
        phone: "",
        password: "",
        confirm_password: "",
      });
    } catch (error) {
      const status = error.response?.status;

      if (status === 409) {
        setMessage("Пользователь с такой электронной почтой уже существует.");
      } else if (status === 422) {
        setMessage("Проверьте правильность введённых данных.");
      } else if (!error.response) {
        setMessage("Не удалось подключиться к серверу.");
      } else {
        setMessage("Не удалось выполнить регистрацию. Попробуйте ещё раз.");
      }

      setMessageType("error");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <section className="register-page">
      <div className="register-card">
        <div className="register-header">
          <h1>Создание аккаунта</h1>
          <p>Зарегистрируйтесь в Photo Studio.</p>
        </div>

        <form className="register-form" onSubmit={handleSubmit}>
          <div className="register-field">
            <label htmlFor="first_name">Имя</label>
            <input
              id="first_name"
              name="first_name"
              type="text"
              placeholder="Введите имя"
              value={formData.first_name}
              onChange={handleChange}
              autoComplete="given-name"
            />
          </div>

          <div className="register-field">
            <label htmlFor="last_name">Фамилия</label>
            <input
              id="last_name"
              name="last_name"
              type="text"
              placeholder="Введите фамилию"
              value={formData.last_name}
              onChange={handleChange}
              autoComplete="family-name"
            />
          </div>

          <div className="register-field">
            <label htmlFor="email">Электронная почта</label>
            <input
              id="email"
              name="email"
              type="email"
              placeholder="example@mail.com"
              value={formData.email}
              onChange={handleChange}
              autoComplete="email"
            />
          </div>

          <div className="register-field">
            <label htmlFor="phone">Телефон</label>
            <input
              id="phone"
              name="phone"
              type="tel"
              placeholder="+7 900 000-00-00"
              value={formData.phone}
              onChange={handleChange}
              autoComplete="tel"
            />
          </div>

          <div className="register-field">
            <label htmlFor="password">Пароль</label>

            <div className="register-password-wrapper">
              <input
                id="password"
                name="password"
                type={showPassword ? "text" : "password"}
                placeholder="Минимум 8 символов"
                value={formData.password}
                onChange={handleChange}
                autoComplete="new-password"
              />

              <button
                type="button"
                className="register-password-toggle"
                onClick={() => setShowPassword(!showPassword)}
                aria-label={showPassword ? "Скрыть пароль" : "Показать пароль"}
              >
                {showPassword ? <EyeOff size={19} /> : <Eye size={19} />}
              </button>
            </div>
          </div>

          <div className="register-field">
            <label htmlFor="confirm_password">Повторите пароль</label>

            <div className="register-password-wrapper">
              <input
                id="confirm_password"
                name="confirm_password"
                type={showConfirmPassword ? "text" : "password"}
                placeholder="Повторите пароль"
                value={formData.confirm_password}
                onChange={handleChange}
                autoComplete="new-password"
              />

              <button
                type="button"
                className="register-password-toggle"
                onClick={() =>
                  setShowConfirmPassword(!showConfirmPassword)
                }
                aria-label={
                  showConfirmPassword ? "Скрыть пароль" : "Показать пароль"
                }
              >
                {showConfirmPassword ? (
                  <EyeOff size={19} />
                ) : (
                  <Eye size={19} />
                )}
              </button>
            </div>
          </div>

          {message && (
            <div className={`register-message ${messageType}`} role="status">
              {message}
            </div>
          )}

          <button
            type="submit"
            className="register-submit"
            disabled={isLoading}
          >
            {isLoading ? "Регистрация..." : "Зарегистрироваться"}
          </button>
        </form>

        <div className="register-footer">
          <p>
            Уже есть аккаунт? <Link to="/login">Войти</Link>
          </p>
        </div>
      </div>
    </section>
  );
}

export default RegisterPage;
