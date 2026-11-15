
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Users,
  Camera,
  CalendarDays,
  ShoppingBag,
  CheckCircle2,
  Clock3,
  XCircle,
  TrendingUp,
  ChevronRight,
  UserPlus,
  Settings,
  Image,
  MessageCircle,
} from "lucide-react";

import "../styles/AdminDashboard.css";

const initialBookings = [
  {
    id: 1,
    client: "Анна Иванова",
    photographer: "Александр Петров",
    service: "Портретная фотосессия",
    date: "14 ноября 2026",
    time: "11:00",
    status: "waiting",
  },
  {
    id: 2,
    client: "Максим Смирнов",
    photographer: "Мария Волкова",
    service: "Свадебная фотосессия",
    date: "15 ноября 2026",
    time: "13:30",
    status: "confirmed",
  },
  {
    id: 3,
    client: "Екатерина Орлова",
    photographer: "Александр Петров",
    service: "Семейная фотосессия",
    date: "16 ноября 2026",
    time: "15:00",
    status: "waiting",
  },
  {
    id: 4,
    client: "Дмитрий Козлов",
    photographer: "Елена Соколова",
    service: "Предметная съёмка",
    date: "17 ноября 2026",
    time: "10:00",
    status: "canceled",
  },
];

const initialOrders = [
  {
    id: "PS-1042",
    client: "Анна Иванова",
    date: "13.11.2026",
    amount: "2 400 ₽",
    status: "В обработке",
  },
  {
    id: "PS-1041",
    client: "Максим Смирнов",
    date: "12.11.2026",
    amount: "1 800 ₽",
    status: "Новый",
  },
  {
    id: "PS-1040",
    client: "Екатерина Орлова",
    date: "11.11.2026",
    amount: "3 200 ₽",
    status: "Завершён",
  },
];

function AdminDashboard() {
  const navigate = useNavigate();

  const [bookings, setBookings] = useState(initialBookings);

  const confirmBooking = (id) => {
    setBookings((current) =>
      current.map((booking) =>
        booking.id === id
          ? { ...booking, status: "confirmed" }
          : booking
      )
    );
  };

  const cancelBooking = (id) => {
    setBookings((current) =>
      current.map((booking) =>
        booking.id === id
          ? { ...booking, status: "canceled" }
          : booking
      )
    );
  };

  const waitingCount = bookings.filter(
    (booking) => booking.status === "waiting"
  ).length;

  const getStatusLabel = (status) => {
    const labels = {
      waiting: "Ожидает",
      confirmed: "Подтверждена",
      canceled: "Отменена",
    };

    return labels[status] || status;
  };

  const quickLinks = [
    {
      title: "Пользователи",
      icon: UserPlus,
      color: "purple",
      route: "/profile",
    },
    {
      title: "Фотографы",
      icon: Camera,
      color: "blue",
      route: "/photographer",
    },
    {
      title: "Услуги и галерея",
      icon: Image,
      color: "green",
      route: "/services",
    },
    {
      title: "Сообщения",
      icon: MessageCircle,
      color: "orange",
      route: "/chat",
    },
  ];

  return (
    <div className="admin-dashboard">
      <section className="admin-welcome">
        <div>
          <span className="admin-eyebrow">ПАНЕЛЬ УПРАВЛЕНИЯ</span>
          <h1>Добро пожаловать, администратор</h1>
          <p>
            Управляйте фотостудией, контролируйте записи и следите за
            заказами.
          </p>
        </div>

        <div className="admin-welcome-icon">
          <Settings size={30} />
        </div>
      </section>

      <section className="admin-stats">
        <article className="admin-stat-card">
          <div className="admin-stat-icon purple">
            <Users size={21} />
          </div>
          <span className="admin-stat-label">Пользователи</span>
          <strong>248</strong>
          <span className="admin-stat-note">
            <TrendingUp size={14} /> +12 за месяц
          </span>
        </article>

        <article className="admin-stat-card">
          <div className="admin-stat-icon blue">
            <Camera size={21} />
          </div>
          <span className="admin-stat-label">Фотографы</span>
          <strong>8</strong>
          <span className="admin-stat-note">Активные специалисты</span>
        </article>

        <article className="admin-stat-card">
          <div className="admin-stat-icon green">
            <CalendarDays size={21} />
          </div>
          <span className="admin-stat-label">Всего записей</span>
          <strong>126</strong>
          <span className="admin-stat-note">За всё время</span>
        </article>

        <article className="admin-stat-card">
          <div className="admin-stat-icon orange">
            <ShoppingBag size={21} />
          </div>
          <span className="admin-stat-label">Заказы печати</span>
          <strong>34</strong>
          <span className="admin-stat-note">За всё время</span>
        </article>
      </section>

      <section className="admin-main-grid">
        <div className="admin-panel admin-bookings-panel">
          <div className="admin-panel-header">
            <div>
              <h2>Последние записи</h2>
              <p>Управление заявками клиентов</p>
            </div>

            <span className="admin-pending-badge">
              <Clock3 size={14} />
              {waitingCount} ожидают
            </span>
          </div>

          <div className="admin-bookings-list">
            {bookings.map((booking) => (
              <article className="admin-booking-item" key={booking.id}>
                <div className="admin-booking-info">
                  <div className="admin-booking-avatar">
                    {booking.client.charAt(0)}
                  </div>

                  <div className="admin-booking-details">
                    <h3>{booking.client}</h3>
                    <p>{booking.service}</p>
                    <span>
                      {booking.photographer} · {booking.date} · {booking.time}
                    </span>
                  </div>
                </div>

                <div className="admin-booking-actions">
                  <span className={`admin-status ${booking.status}`}>
                    {getStatusLabel(booking.status)}
                  </span>

                  {booking.status === "waiting" && (
                    <div className="admin-action-buttons">
                      <button
                        type="button"
                        className="admin-confirm-button"
                        onClick={() => confirmBooking(booking.id)}
                        title="Подтвердить запись"
                      >
                        <CheckCircle2 size={16} />
                      </button>

                      <button
                        type="button"
                        className="admin-cancel-button"
                        onClick={() => cancelBooking(booking.id)}
                        title="Отменить запись"
                      >
                        <XCircle size={16} />
                      </button>
                    </div>
                  )}
                </div>
              </article>
            ))}
          </div>
        </div>

        <div className="admin-side-column">
          <div className="admin-panel admin-quick-panel">
            <div className="admin-panel-header">
              <div>
                <h2>Быстрый доступ</h2>
                <p>Основные разделы управления</p>
              </div>
            </div>

            <div className="admin-quick-links">
              {quickLinks.map((link) => {
                const Icon = link.icon;

                return (
                  <button
                    type="button"
                    className="admin-quick-link"
                    key={link.title}
                    onClick={() => navigate(link.route)}
                  >
                    <span className={`admin-quick-icon ${link.color}`}>
                      <Icon size={19} />
                    </span>

                    <span>{link.title}</span>

                    <ChevronRight size={17} />
                  </button>
                );
              })}
            </div>
          </div>

          <div className="admin-panel admin-orders-panel">
            <div className="admin-panel-header">
              <div>
                <h2>Последние заказы</h2>
                <p>Заказы на печать фотографий</p>
              </div>
            </div>

            <div className="admin-orders-list">
              {initialOrders.map((order) => (
                <div className="admin-order-item" key={order.id}>
                  <div>
                    <strong>{order.id}</strong>
                    <span>{order.client}</span>
                    <small>{order.date}</small>
                  </div>

                  <div className="admin-order-price">
                    <strong>{order.amount}</strong>
                    <span>{order.status}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="admin-tip">
        <div className="admin-tip-icon">
          <TrendingUp size={21} />
        </div>

        <div>
          <strong>Совет администратора</strong>
          <p>
            Проверяйте новые заявки и подтверждайте записи, чтобы
            клиенты своевременно получали информацию о своих фотосессиях.
          </p>
        </div>
      </section>
    </div>
  );
}

export default AdminDashboard;
