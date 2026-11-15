
import {
  ArrowRight,
  Camera,
  CheckCircle2,
  Clock3,
  Image,
  Printer,
  Sparkles,
} from "lucide-react";

import "../styles/HomePage.css";

const services = [
  {
    icon: Camera,
    image: "/images/male-portrait.jpg",
    imageAlt: "Мужской портрет",
    title: "Портретная съёмка",
    description:
      "Индивидуальные фотосессии, раскрывающие вашу индивидуальность.",
    duration: "От 60 минут",
  },
  {
    icon: Sparkles,
    image: "/images/art-portrait.jpg",
    imageAlt: "Художественный студийный портрет",
    title: "Студийная съёмка",
    description:
      "Профессиональные фотографии в оборудованной фотостудии.",
    duration: "От 90 минут",
  },
  {
    icon: Image,
    image: "/images/horse.jpg",
    imageAlt: "Художественная фотография белой лошади",
    title: "Художественная съёмка",
    description:
      "Необычные кадры, выразительные образы и творческие идеи.",
    duration: "От 60 минут",
  },
  {
    icon: Printer,
    image: "/images/architecture.jpg",
    imageAlt: "Чёрно-белая фотография архитектуры",
    title: "Печать фотографий",
    description:
      "Печать ваших любимых кадров в различных форматах.",
    duration: "Несколько форматов",
  },
];

const advantages = [
  "Профессиональное оборудование",
  "Опытные фотографы",
  "Индивидуальный подход",
  "Высокое качество фотографий",
];

function HomePage() {
  return (
    <div className="home-page">
      <section className="hero">
        <div className="hero-container">
          <div className="hero-content">
            <span className="hero-label">
              <Sparkles size={16} />
              Пространство красивых историй
            </span>

            <h1>
              Сохраняем
              <br />
              <span>моменты жизни</span>
              <br />
              в фотографиях
            </h1>

            <p className="hero-description">
              Профессиональная фотостудия, где каждый кадр
              превращается в историю, которую хочется
              пересматривать снова и снова.
            </p>

            <div className="hero-actions">
              <a href="/register" className="button button-primary">
                Записаться на съёмку
                <ArrowRight size={18} />
              </a>

              <a href="/services" className="button button-secondary">
                Наши услуги
              </a>
            </div>

            <div className="hero-features">
              <div className="hero-feature">
                <Camera size={18} />
                <span>Профессиональная съёмка</span>
              </div>

              <div className="hero-feature">
                <Clock3 size={18} />
                <span>Удобная запись онлайн</span>
              </div>
            </div>
          </div>

          <div className="hero-visual">
            <img
              className="hero-image"
              src="/images/editorial-portrait.jpg"
              alt="Чёрно-белый художественный портрет"
            />

            <div className="hero-floating-card">
              <div className="floating-card-icon">
                <CheckCircle2 size={22} />
              </div>
              <div>
                <strong>Ваш момент — наша работа</strong>
                <span>Создаём фотографии с душой</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="services-section" id="services">
        <div className="section-container">
          <div className="section-heading">
            <div>
              <span className="section-label">ЧТО МЫ ПРЕДЛАГАЕМ</span>
              <h2>Наши услуги</h2>
            </div>

            <a href="/services" className="section-link">
              Все услуги
              <ArrowRight size={18} />
            </a>
          </div>

          <div className="services-grid">
            {services.map((service) => {
              const Icon = service.icon;

              return (
                <article className="service-card" key={service.title}>
                  <div className="service-image-wrapper">
                    <img
                      className="service-image"
                      src={service.image}
                      alt={service.imageAlt}
                      loading="lazy"
                    />
                  </div>

                  <div className="service-icon">
                    <Icon size={25} strokeWidth={1.7} />
                  </div>

                  <h3>{service.title}</h3>

                  <p>{service.description}</p>

                  <div className="service-duration">
                    <Clock3 size={15} />
                    {service.duration}
                  </div>

                  <a href="/register" className="service-link">
                    Подробнее
                    <ArrowRight size={16} />
                  </a>
                </article>
              );
            })}
          </div>
        </div>
      </section>

      <section className="about-section" id="about">
        <div className="about-container">
          <div className="about-content">
            <span className="section-label">О НАШЕЙ ФОТОСТУДИИ</span>

            <h2>
              Не просто фотографии.
              <br />
              <span>Воспоминания на всю жизнь.</span>
            </h2>

            <p>
              Photo Studio — пространство, в котором мы помогаем
              сохранить важные события, эмоции и людей.
              Наша цель — сделать процесс съёмки комфортным,
              а результат по-настоящему особенным.
            </p>

            <div className="advantages-list">
              {advantages.map((advantage) => (
                <div className="advantage-item" key={advantage}>
                  <CheckCircle2 size={19} />
                  <span>{advantage}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="about-visual">
            <img
              className="about-image"
              src="/images/saxophonist.jpg"
              alt="Чёрно-белая фотография музыканта с саксофоном"
              loading="lazy"
            />
          </div>
        </div>
      </section>

      <section className="booking-section">
        <div className="booking-container">
          <div>
            <span className="section-label">
              ВАША ИСТОРИЯ НАЧИНАЕТСЯ ЗДЕСЬ
            </span>
            <h2>Готовы к своей фотосессии?</h2>
            <p>
              Выберите услугу и запишитесь на удобное время.
            </p>
          </div>

          <a href="/register" className="button button-primary">
            Создать аккаунт
            <ArrowRight size={18} />
          </a>
        </div>
      </section>
    </div>
  );
}

export default HomePage;
