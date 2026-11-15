
import { useState } from "react";
import { Link } from "react-router-dom";
import { Camera, CalendarDays, Clock, User, CheckCircle2 } from "lucide-react";

import "../styles/BookingPage.css";

const services = [
  {
    id: 1,
    name: "Портретная фотосессия",
    duration: 60,
    price: 5000,
  },
  {
    id: 2,
    name: "Семейная фотосессия",
    duration: 90,
    price: 7500,
  },
  {
    id: 3,
    name: "Свадебная фотосессия",
    duration: 120,
    price: 12000,
  },
  {
    id: 4,
    name: "Предметная съёмка",
    duration: 60,
    price: 6000,
  },
  {
    id: 5,
    name: "Love Story",
    duration: 90,
    price: 8000,
  },
];

const photographers = [
  {
    id: 1,
    name: "Александр Иванов",
    specialization: "Портретная фотография",
  },
  {
    id: 2,
    name: "Мария Петрова",
    specialization: "Семейная фотография",
  },
  {
    id: 3,
    name: "Дмитрий Смирнов",
    specialization: "Свадебная фотография",
  },
];

const timeSlots = [
  "09:00",
  "10:00",
  "11:00",
  "12:00",
  "13:00",
  "14:00",
  "15:00",
  "16:00",
  "17:00",
];

function BookingPage() {
  const [serviceId, setServiceId] = useState("");
  const [photographerId, setPhotographerId] = useState("");
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");
  const [comment, setComment] = useState("");

  const [isSubmitted, setIsSubmitted] = useState(false);

  const selectedService = services.find(
    (service) => service.id === Number(serviceId)
  );

  const selectedPhotographer = photographers.find(
    (photographer) => photographer.id === Number(photographerId)
  );

  function getTodayDate() {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, "0");
    const day = String(today.getDate()).padStart(2, "0");

    return `${year}-${month}-${day}`;
  }

  function handleSubmit(event) {
    event.preventDefault();

    if (
      !serviceId ||
      !photographerId ||
      !date ||
      !time
    ) {
      return;
    }

    setIsSubmitted(true);
  }

  function handleReset() {
    setServiceId("");
    setPhotographerId("");
    setDate("");
    setTime("");
    setComment("");
    setIsSubmitted(false);
  }

  if (isSubmitted) {
    return (
      <section className="booking-page">
        <div className="booking-success">
          <div className="booking-success-icon">
            <CheckCircle2 size={42} />
          </div>

          <h1>Заявка заполнена!</h1>

          <p className="booking-success-description">
            Данные вашей записи подготовлены. После подключения
            сервера здесь будет происходить оформление бронирования.
          </p>

          <div className="booking-summary">
            <div>
              <span>Услуга</span>
              <strong>{selectedService?.name}</strong>
            </div>

            <div>
              <span>Фотограф</span>
              <strong>{selectedPhotographer?.name}</strong>
            </div>

            <div>
              <span>Дата</span>
              <strong>{date}</strong>
            </div>

            <div>
              <span>Время</span>
              <strong>{time}</strong>
            </div>

            <div>
              <span>Продолжительность</span>
              <strong>{selectedService?.duration} минут</strong>
            </div>

            <div>
              <span>Стоимость</span>
              <strong>{selectedService?.price.toLocaleString("ru-RU")} ₽</strong>
            </div>

            {comment && (
              <div className="booking-summary-comment">
                <span>Комментарий</span>
                <strong>{comment}</strong>
              </div>
            )}
          </div>

          <button
            type="button"
            className="booking-submit"
            onClick={handleReset}
          >
            Создать новую заявку
          </button>

          <Link to="/profile" className="booking-back-link">
            Вернуться в личный кабинет
          </Link>
        </div>
      </section>
    );
  }

  return (
    <section className="booking-page">
      <div className="booking-container">
        <div className="booking-heading">
          <span className="booking-eyebrow">БРОНИРОВАНИЕ</span>

          <h1>Запись на фотосессию</h1>

          <p>
            Выберите подходящую услугу, фотографа и удобное время.
          </p>
        </div>

        <div className="booking-content">
          <form className="booking-form" onSubmit={handleSubmit}>
            <div className="booking-section">
              <div className="booking-section-heading">
                <span className="booking-step">01</span>

                <div>
                  <h2>Выберите услугу</h2>
                  <p>Какую фотосессию вы хотите заказать?</p>
                </div>
              </div>

              <div className="booking-field">
                <label htmlFor="booking-service">
                  Услуга
                </label>

                <select
                  id="booking-service"
                  value={serviceId}
                  onChange={(event) => setServiceId(event.target.value)}
                  required
                >
                  <option value="">Выберите услугу</option>

                  {services.map((service) => (
                    <option key={service.id} value={service.id}>
                      {service.name} — {service.price.toLocaleString("ru-RU")} ₽
                    </option>
                  ))}
                </select>
              </div>

              {selectedService && (
                <div className="booking-service-info">
                  <div>
                    <span>Продолжительность</span>
                    <strong>{selectedService.duration} минут</strong>
                  </div>

                  <div>
                    <span>Стоимость</span>
                    <strong>
                      {selectedService.price.toLocaleString("ru-RU")} ₽
                    </strong>
                  </div>
                </div>
              )}
            </div>

            <div className="booking-section">
              <div className="booking-section-heading">
                <span className="booking-step">02</span>

                <div>
                  <h2>Выберите фотографа</h2>
                  <p>Кто будет проводить фотосессию?</p>
                </div>
              </div>

              <div className="booking-photographers">
                {photographers.map((photographer) => (
                  <label
                    key={photographer.id}
                    className={`booking-photographer ${
                      photographerId === String(photographer.id)
                        ? "selected"
                        : ""
                    }`}
                  >
                    <input
                      type="radio"
                      name="photographer"
                      value={photographer.id}
                      checked={photographerId === String(photographer.id)}
                      onChange={(event) =>
                        setPhotographerId(event.target.value)
                      }
                    />

                    <div className="booking-photographer-icon">
                      <User size={22} />
                    </div>

                    <div className="booking-photographer-info">
                      <strong>{photographer.name}</strong>
                      <span>{photographer.specialization}</span>
                    </div>
                  </label>
                ))}
              </div>
            </div>

            <div className="booking-section">
              <div className="booking-section-heading">
                <span className="booking-step">03</span>

                <div>
                  <h2>Дата и время</h2>
                  <p>Выберите удобный день и время съёмки.</p>
                </div>
              </div>

              <div className="booking-date-time">
                <div className="booking-field">
                  <label htmlFor="booking-date">
                    <CalendarDays size={17} />
                    Дата
                  </label>

                  <input
                    id="booking-date"
                    type="date"
                    min={getTodayDate()}
                    value={date}
                    onChange={(event) => setDate(event.target.value)}
                    required
                  />
                </div>

                <div className="booking-field">
                  <label htmlFor="booking-time">
                    <Clock size={17} />
                    Время
                  </label>

                  <select
                    id="booking-time"
                    value={time}
                    onChange={(event) => setTime(event.target.value)}
                    required
                  >
                    <option value="">Выберите время</option>

                    {timeSlots.map((slot) => (
                      <option key={slot} value={slot}>
                        {slot}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <p className="booking-time-note">
                Время пока демонстрационное. Реальная доступность
                будет определяться расписанием фотографа.
              </p>
            </div>

            <div className="booking-section">
              <div className="booking-section-heading">
                <span className="booking-step">04</span>

                <div>
                  <h2>Дополнительная информация</h2>
                  <p>Расскажите о ваших пожеланиях.</p>
                </div>
              </div>

              <div className="booking-field">
                <label htmlFor="booking-comment">
                  Комментарий
                </label>

                <textarea
                  id="booking-comment"
                  rows="4"
                  placeholder="Напишите ваши пожелания к фотосессии..."
                  value={comment}
                  onChange={(event) => setComment(event.target.value)}
                />
              </div>
            </div>

            <button type="submit" className="booking-submit">
              <Camera size={19} />
              Продолжить оформление
            </button>
          </form>

          <aside className="booking-sidebar">
            <div className="booking-sidebar-card">
              <span className="booking-sidebar-label">
                ВАША ЗАПИСЬ
              </span>

              <h3>План фотосессии</h3>

              <div className="booking-sidebar-item">
                <span>Услуга</span>
                <strong>
                  {selectedService?.name || "Не выбрана"}
                </strong>
              </div>

              <div className="booking-sidebar-item">
                <span>Фотограф</span>
                <strong>
                  {selectedPhotographer?.name || "Не выбран"}
                </strong>
              </div>

              <div className="booking-sidebar-item">
                <span>Дата</span>
                <strong>{date || "Не выбрана"}</strong>
              </div>

              <div className="booking-sidebar-item">
                <span>Время</span>
                <strong>{time || "Не выбрано"}</strong>
              </div>

              <div className="booking-sidebar-total">
                <span>Итого</span>
                <strong>
                  {selectedService
                    ? `${selectedService.price.toLocaleString("ru-RU")} ₽`
                    : "—"}
                </strong>
              </div>

              <p className="booking-sidebar-note">
                Оплата производится офлайн после согласования записи.
              </p>
            </div>

            <div className="booking-help">
              <h3>Нужна помощь?</h3>
              <p>
                Если у вас возникли вопросы, свяжитесь с администратором.
              </p>
              <Link to="/profile">Личный кабинет</Link>
            </div>
          </aside>
        </div>
      </div>
    </section>
  );
}

export default BookingPage;
