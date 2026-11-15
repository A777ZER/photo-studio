
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  User,
  CalendarDays,
  Images,
  ShoppingBag,
  MessageCircle,
  Camera,
  ArrowRight,
} from "lucide-react";

import "../styles/ProfilePage.css";

function ProfilePage() {
  const [activeSection, setActiveSection] = useState("profile");
  const navigate = useNavigate();

  const menuItems = [
    { id: "profile", label: "Мой профиль", icon: User },
    { id: "bookings", label: "Мои записи", icon: CalendarDays },
    { id: "photos", label: "Мои фотографии", icon: Images },
    { id: "orders", label: "Мои заказы", icon: ShoppingBag },
    { id: "chat", label: "Сообщения", icon: MessageCircle },
  ];

  const sectionRoutes = {
    bookings: "/my-bookings",
    photos: "/photos",
    orders: "/print-orders",
    chat: "/chat",
  };

  function renderContent() {
    switch (activeSection) {
      case "profile":
        return (
          <>
            <h2>Личная информация</h2>
            <p>Информация о вашем аккаунте.</p>

            <div className="profile-info-grid">
              <div className="profile-info-item">
                <span>Имя</span>
                <strong>Не указано</strong>
              </div>

              <div className="profile-info-item">
                <span>Фамилия</span>
                <strong>Не указана</strong>
              </div>

              <div className="profile-info-item">
                <span>Электронная почта</span>
                <strong>Не указана</strong>
              </div>

              <div className="profile-info-item">
                <span>Телефон</span>
                <strong>Не указан</strong>
              </div>
            </div>

            <div className="profile-action-card">
              <div className="profile-action-icon">
                <Camera size={22} />
              </div>

              <div className="profile-action-text">
                <h3>Готовы к новой фотосессии?</h3>
                <p>
                  Выберите услугу и удобное время для записи.
                </p>
              </div>

              <button
                type="button"
                onClick={() => navigate("/booking")}
              >
                Записаться
                <ArrowRight size={16} />
              </button>
            </div>
          </>
        );

      case "bookings":
        return (
          <>
            <h2>Мои записи</h2>
            <p>Управляйте своими записями на фотосессии.</p>

            <div className="profile-info-item">
              <strong>Перейдите к списку всех ваших записей.</strong>
              <button
                type="button"
                onClick={() => navigate("/my-bookings")}
              >
                Открыть мои записи
                <ArrowRight size={16} />
              </button>
            </div>
          </>
        );

      case "photos":
        return (
          <>
            <h2>Мои фотографии</h2>
            <p>Просматривайте загруженные фотографии.</p>

            <div className="profile-info-item">
              <strong>Ваша фотогалерея находится в отдельном разделе.</strong>
              <button
                type="button"
                onClick={() => navigate("/photos")}
              >
                Открыть фотографии
                <ArrowRight size={16} />
              </button>
            </div>
          </>
        );

      case "orders":
        return (
          <>
            <h2>Мои заказы</h2>
            <p>Следите за состоянием заказов на печать.</p>

            <div className="profile-info-item">
              <strong>Просмотрите историю заказов на печать.</strong>
              <button
                type="button"
                onClick={() => navigate("/print-orders")}
              >
                Открыть мои заказы
                <ArrowRight size={16} />
              </button>
            </div>
          </>
        );

      case "chat":
        return (
          <>
            <h2>Сообщения</h2>
            <p>Свяжитесь с администратором фотостудии.</p>

            <div className="profile-info-item">
              <strong>Откройте чат для общения с администратором.</strong>
              <button
                type="button"
                onClick={() => navigate("/chat")}
              >
                Перейти в чат
                <ArrowRight size={16} />
              </button>
            </div>
          </>
        );

      default:
        return null;
    }
  }

  function handleMenuClick(sectionId) {
    if (sectionRoutes[sectionId]) {
      navigate(sectionRoutes[sectionId]);
      return;
    }

    setActiveSection(sectionId);
  }

  return (
    <section className="profile-page">
      <div className="profile-header">
        <h1>Личный кабинет</h1>
        <p>Управляйте своим профилем и услугами Photo Studio.</p>
      </div>

      <div className="profile-layout">
        <aside className="profile-sidebar">
          <div className="profile-user">
            <div className="profile-avatar">U</div>
            <h2>Пользователь</h2>
            <p>Гость</p>
          </div>

          <nav
            className="profile-menu"
            aria-label="Меню личного кабинета"
          >
            {menuItems.map((item) => {
              const Icon = item.icon;

              return (
                <button
                  key={item.id}
                  type="button"
                  className={activeSection === item.id ? "active" : ""}
                  onClick={() => handleMenuClick(item.id)}
                >
                  <Icon size={17} />
                  {item.label}
                </button>
              );
            })}
          </nav>
        </aside>

        <div className="profile-content">
          {renderContent()}
        </div>
      </div>
    </section>
  );
}

export default ProfilePage;
