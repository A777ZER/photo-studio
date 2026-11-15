
import { Link } from "react-router-dom";
import {
  ArrowRight,
  Camera,
  Clock3,
  Image,
  Printer,
  Sparkles,
  Users,
} from "lucide-react";

import "../styles/ServicesPage.css";

const services = [
  {
    icon: Camera,
    title: "Портретная съёмка",
    description:
      "Индивидуальная фотосессия для создания выразительных портретов. Подойдёт для личного архива, социальных сетей и профессионального портфолио.",
    duration: "60 минут",
    category: "Индивидуальная съёмка",
  },
  {
    icon: Sparkles,
    title: "Студийная съёмка",
    description:
      "Профессиональная съёмка в оборудованной студии с использованием света и различных фотозон.",
    duration: "90 минут",
    category: "Студийная съёмка",
  },
  {
    icon: Users,
    title: "Семейная съёмка",
    description:
      "Совместная фотосессия для семей, пар и близких людей. Сохраняем эмоции и важные моменты.",
    duration: "60 минут",
    category: "Семейная съёмка",
  },
  {
    icon: Image,
    title: "Творческая съёмка",
    description:
      "Необычные образы, творческие идеи и индивидуальная концепция фотосессии.",
    duration: "90 минут",
    category: "Авторская съёмка",
  },
  {
    icon: Printer,
    title: "Печать фотографий",
    description:
      "Заказ печати готовых фотографий. Можно выбрать формат, размер и количество экземпляров.",
    duration: "По заказу",
    category: "Печать",
  },
];

function ServicesPage() {
  return (
    <div className="services-page">
      <section className="services-hero">
        <div className="services-page-container">
          <span className="section-label">
            НАПРАВЛЕНИЯ РАБОТЫ
          </span>

          <h1>
            Наши <span>услуги</span>
          </h1>

          <p>
            Выберите подходящую услугу и доверьте нам
            сохранение своих лучших моментов.
          </p>
        </div>
      </section>

      <section className="services-catalog">
        <div className="services-page-container">
          <div className="services-page-heading">
            <div>
              <h2>Что мы предлагаем</h2>
              <p>
                Профессиональный подход к каждой фотографии.
              </p>
            </div>

            <span className="services-count">
              {services.length} услуг
            </span>
          </div>

          <div className="services-page-grid">
            {services.map((service) => {
              const Icon = service.icon;

              return (
                <article
                  className="services-page-card"
                  key={service.title}
                >
                  <div className="services-page-card-top">
                    <div className="services-page-icon">
                      <Icon size={27} strokeWidth={1.7} />
                    </div>

                    <span className="services-category">
                      {service.category}
                    </span>
                  </div>

                  <h3>{service.title}</h3>

                  <p className="services-card-description">
                    {service.description}
                  </p>

                  <div className="services-card-bottom">
                    <div className="services-card-duration">
                      <Clock3 size={17} />
                      <span>{service.duration}</span>
                    </div>

                    <Link
                      to="/register"
                      className="services-booking-link"
                    >
                      Записаться
                      <ArrowRight size={17} />
                    </Link>
                  </div>
                </article>
              );
            })}
          </div>
        </div>
      </section>

      <section className="services-page-cta">
        <div className="services-page-container services-cta-content">
          <div>
            <h2>Не знаете, что выбрать?</h2>
            <p>
              Зарегистрируйтесь и выберите подходящую услугу
              для своей фотосессии.
            </p>
          </div>

          <Link to="/register" className="button button-primary">
            Начать
            <ArrowRight size={18} />
          </Link>
        </div>
      </section>
    </div>
  );
}

export default ServicesPage;
