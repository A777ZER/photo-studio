
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  CalendarDays,
  Camera,
  Clock3,
  CheckCircle2,
  Users,
  TrendingUp,
  ChevronRight,
  Image,
  MessageCircle,
} from "lucide-react";

import "../styles/PhotographerDashboard.css";

const initialBookings = [
  {
    id: 1,
    client: "Анна Смирнова",
    service: "Портретная фотосессия",
    time: "10:00",
    duration: "1 час",
    status: "confirmed",
  },
  {
    id: 2,
    client: "Максим Иванов",
    service: "Семейная фотосессия",
    time: "12:00",
    duration: "1,5 часа",
    status: "confirmed",
  },
  {
    id: 3,
    client: "Екатерина Волкова",
    service: "Индивидуальная фотосессия",
    time: "15:00",
    duration: "1 час",
    status: "waiting",
  },
  {
    id: 4,
    client: "Дмитрий Козлов",
    service: "Предметная фотосъёмка",
    time: "17:00",
    duration: "2 часа",
    status: "confirmed",
  },
];

const statusLabels = {
  confirmed: "Подтверждена",
  waiting: "Ожидает подтверждения",
};

function PhotographerDashboard() {
  const [bookings, setBookings] = useState(initialBookings);
  const navigate = useNavigate();

  function confirmBooking(id) {
    setBookings((previous) =>
      previous.map((booking) =>
        booking.id === id
          ? { ...booking, status: "confirmed" }
          : booking
      )
    );
  }

  const today = new Date().toLocaleDateString("ru-RU", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  const confirmedCount = bookings.filter(
    (booking) => booking.status === "confirmed"
  ).length;

  const waitingCount = bookings.filter(
    (booking) => booking.status === "waiting"
  ).length;

  const shortcuts = [
    {
      title: "Расписание",
      description: "Управление рабочим временем",
      icon: CalendarDays,
      route: "/my-bookings",
    },
    {
      title: "Клиенты",
      description: "Информация о записях",
      icon: Users,
      route: "/my-bookings",
    },
    {
      title: "Мои фотографии",
      description: "Работы и фотогалерея",
      icon: Image,
      route: "/photos",
    },
    {
      title: "Сообщения",
      description: "Общение с администратором",
      icon: MessageCircle,
      route: "/chat",
    },
  ];

  return (
    <section className="photographer-dashboard">
      <div className="photographer-container">
        <div className="photographer-heading">
          <div>
            <span className="photographer-eyebrow">
              РАБОЧЕЕ ПРОСТРАНСТВО
            </span>
            <h1>Кабинет фотографа</h1>
            <p>Здравствуйте! Вот что запланировано на сегодня.</p>
          </div>

          <div className="photographer-date">
            <CalendarDays size={18} />
            <span>{today}</span>
          </div>
        </div>

        <div className="photographer-welcome">
          <div className="photographer-welcome-icon">
            <Camera size={28} />
          </div>
          <div>
            <h2>Добро пожаловать, фотограф!</h2>
            <p>
              Управляйте записями, следите за расписанием и
              организуйте свои фотосессии.
            </p>
          </div>
        </div>

        <div className="photographer-stats">
          <article className="photographer-stat-card">
            <div className="photographer-stat-icon purple">
              <CalendarDays size={21} />
            </div>
            <div>
              <span>Записей сегодня</span>
              <strong>{bookings.length}</strong>
            </div>
          </article>

          <article className="photographer-stat-card">
            <div className="photographer-stat-icon green">
              <CheckCircle2 size={21} />
            </div>
            <div>
              <span>Подтверждено</span>
              <strong>{confirmedCount}</strong>
            </div>
          </article>

          <article className="photographer-stat-card">
            <div className="photographer-stat-icon yellow">
              <Clock3 size={21} />
            </div>
            <div>
              <span>Ожидают подтверждения</span>
              <strong>{waitingCount}</strong>
            </div>
          </article>

          <article className="photographer-stat-card">
            <div className="photographer-stat-icon blue">
              <Users size={21} />
            </div>
            <div>
              <span>Клиентов сегодня</span>
              <strong>{bookings.length}</strong>
            </div>
          </article>
        </div>

        <div className="photographer-content-grid">
          <section className="photographer-panel">
            <div className="photographer-panel-header">
              <div>
                <h2>Расписание на сегодня</h2>
                <p>Ваши предстоящие фотосессии</p>
              </div>
              <CalendarDays size={20} />
            </div>

            <div className="photographer-bookings">
              {bookings.map((booking) => (
                <article
                  className="photographer-booking"
                  key={booking.id}
                >
                  <div className="photographer-booking-time">
                    <strong>{booking.time}</strong>
                    <span>{booking.duration}</span>
                  </div>

                  <div className="photographer-booking-info">
                    <strong>{booking.client}</strong>
                    <span>{booking.service}</span>
                    <span
                      className={`photographer-booking-status ${booking.status}`}
                    >
                      {statusLabels[booking.status]}
                    </span>
                  </div>

                  {booking.status === "waiting" ? (
                    <button
                      type="button"
                      className="photographer-confirm-button"
                      onClick={() => confirmBooking(booking.id)}
                    >
                      Подтвердить
                    </button>
                  ) : (
                    <CheckCircle2
                      className="photographer-confirmed-icon"
                      size={20}
                    />
                  )}
                </article>
              ))}
            </div>
          </section>

          <aside className="photographer-side-panel">
            <div className="photographer-panel-header">
              <div>
                <h2>Быстрый доступ</h2>
                <p>Основные разделы кабинета</p>
              </div>
              <TrendingUp size={20} />
            </div>

            <div className="photographer-shortcuts">
              {shortcuts.map((shortcut) => {
                const Icon = shortcut.icon;

                return (
                  <button
                    type="button"
                    className="photographer-shortcut"
                    key={shortcut.title}
                    onClick={() => navigate(shortcut.route)}
                  >
                    <span className="photographer-shortcut-icon">
                      <Icon size={19} />
                    </span>
                    <span>
                      <strong>{shortcut.title}</strong>
                      <small>{shortcut.description}</small>
                    </span>
                    <ChevronRight size={18} />
                  </button>
                );
              })}
            </div>

            <div className="photographer-tip">
              <Camera size={21} />
              <div>
                <strong>Совет дня</strong>
                <p>
                  Проверяйте расписание заранее, чтобы подготовить
                  оборудование к каждой фотосессии.
                </p>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </section>
  );
}

export default PhotographerDashboard;
