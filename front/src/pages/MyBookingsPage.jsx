
import { useState } from "react";
import { CalendarDays, Clock, Camera, User, XCircle } from "lucide-react";
import { Link } from "react-router-dom";

import "../styles/MyBookingsPage.css";

const initialBookings = [
  {
    id: 1,
    service: "Портретная фотосессия",
    photographer: "Александр Иванов",
    date: "2026-11-20",
    time: "12:00",
    duration: 60,
    price: 5000,
    status: "confirmed",
  },
  {
    id: 2,
    service: "Семейная фотосессия",
    photographer: "Мария Петрова",
    date: "2026-11-25",
    time: "15:00",
    duration: 90,
    price: 7500,
    status: "waiting",
  },
  {
    id: 3,
    service: "Love Story",
    photographer: "Дмитрий Смирнов",
    date: "2026-10-15",
    time: "14:00",
    duration: 90,
    price: 8000,
    status: "completed",
  },
];

const statusLabels = {
  waiting: "Ожидает подтверждения",
  confirmed: "Подтверждена",
  completed: "Завершена",
  canceled: "Отменена",
  no_show: "Неявка",
};

function formatDate(date) {
  return new Date(`${date}T00:00:00`).toLocaleDateString("ru-RU", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}

function MyBookingsPage() {
  const [bookings, setBookings] = useState(initialBookings);
  const [activeFilter, setActiveFilter] = useState("all");

  const filters = [
    { id: "all", label: "Все записи" },
    { id: "upcoming", label: "Предстоящие" },
    { id: "completed", label: "Завершённые" },
    { id: "canceled", label: "Отменённые" },
  ];

  const filteredBookings = bookings.filter((booking) => {
    if (activeFilter === "all") {
      return true;
    }

    if (activeFilter === "upcoming") {
      return ["waiting", "confirmed"].includes(booking.status);
    }

    if (activeFilter === "completed") {
      return booking.status === "completed";
    }

    return ["canceled", "no_show"].includes(booking.status);
  });

  function cancelBooking(id) {
    const confirmed = window.confirm(
      "Вы действительно хотите отменить эту запись?"
    );

    if (!confirmed) {
      return;
    }

    setBookings((previous) =>
      previous.map((booking) =>
        booking.id === id
          ? { ...booking, status: "canceled" }
          : booking
      )
    );
  }

  return (
    <section className="my-bookings-page">
      <div className="my-bookings-container">
        <div className="my-bookings-heading">
          <div>
            <span className="my-bookings-eyebrow">ЛИЧНЫЙ КАБИНЕТ</span>
            <h1>Мои записи</h1>
            <p>Управляйте своими фотосессиями и просматривайте историю.</p>
          </div>

          <Link to="/booking" className="my-bookings-create">
            <Camera size={18} />
            Записаться на фотосессию
          </Link>
        </div>

        <div className="my-bookings-filters">
          {filters.map((filter) => (
            <button
              key={filter.id}
              type="button"
              className={
                activeFilter === filter.id ? "active" : ""
              }
              onClick={() => setActiveFilter(filter.id)}
            >
              {filter.label}
            </button>
          ))}
        </div>

        <div className="my-bookings-list">
          {filteredBookings.length > 0 ? (
            filteredBookings.map((booking) => (
              <article className="my-booking-card" key={booking.id}>
                <div className="my-booking-main">
                  <div className="my-booking-icon">
                    <Camera size={23} />
                  </div>

                  <div className="my-booking-info">
                    <h2>{booking.service}</h2>

                    <span
                      className={`my-booking-status ${booking.status}`}
                    >
                      {statusLabels[booking.status]}
                    </span>
                  </div>
                </div>

                <div className="my-booking-details">
                  <div>
                    <CalendarDays size={17} />
                    <span>{formatDate(booking.date)}</span>
                  </div>

                  <div>
                    <Clock size={17} />
                    <span>
                      {booking.time} · {booking.duration} минут
                    </span>
                  </div>

                  <div>
                    <User size={17} />
                    <span>{booking.photographer}</span>
                  </div>
                </div>

                <div className="my-booking-footer">
                  <strong>
                    {booking.price.toLocaleString("ru-RU")} ₽
                  </strong>

                  {["waiting", "confirmed"].includes(booking.status) && (
                    <button
                      type="button"
                      className="my-booking-cancel"
                      onClick={() => cancelBooking(booking.id)}
                    >
                      <XCircle size={16} />
                      Отменить запись
                    </button>
                  )}
                </div>
              </article>
            ))
          ) : (
            <div className="my-bookings-empty">
              <CalendarDays size={36} />
              <h2>Записей пока нет</h2>
              <p>
                В этой категории пока нет фотосессий.
              </p>
              <Link to="/booking">
                Выбрать фотосессию
              </Link>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

export default MyBookingsPage;
