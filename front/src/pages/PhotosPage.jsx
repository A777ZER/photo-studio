
import { useState } from "react";
import { Camera, X, Image as ImageIcon } from "lucide-react";

import "../styles/PhotosPage.css";

const initialPhotos = [
  {
    id: 1,
    title: "Портретная фотосессия",
    date: "15 октября 2026",
    image:
      "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=900",
  },
  {
    id: 2,
    title: "Портрет на природе",
    date: "18 октября 2026",
    image:
      "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?w=900",
  },
  {
    id: 3,
    title: "Студийная съёмка",
    date: "22 октября 2026",
    image:
      "https://images.unsplash.com/photo-1531123897727-8f129e1688ce?w=900",
  },
  {
    id: 4,
    title: "Семейная фотосессия",
    date: "25 октября 2026",
    image:
      "https://images.unsplash.com/photo-1511895426328-dc8714191300?w=900",
  },
  {
    id: 5,
    title: "Love Story",
    date: "28 октября 2026",
    image:
      "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?w=900",
  },
  {
    id: 6,
    title: "Прогулка в городе",
    date: "30 октября 2026",
    image:
      "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=900",
  },
];

function PhotosPage() {
  const [photos] = useState(initialPhotos);
  const [selectedPhoto, setSelectedPhoto] = useState(null);

  return (
    <section className="photos-page">
      <div className="photos-container">
        <div className="photos-heading">
          <div>
            <span className="photos-eyebrow">ЛИЧНЫЙ КАБИНЕТ</span>
            <h1>Мои фотографии</h1>
            <p>
              Все ваши фотографии собраны в одном месте.
            </p>
          </div>

          <div className="photos-count">
            <Camera size={20} />
            <span>{photos.length} фотографий</span>
          </div>
        </div>

        {photos.length > 0 ? (
          <div className="photos-grid">
            {photos.map((photo) => (
              <button
                type="button"
                className="photo-card"
                key={photo.id}
                onClick={() => setSelectedPhoto(photo)}
                aria-label={`Открыть фотографию: ${photo.title}`}
              >
                <div className="photo-card-image">
                  <img
                    src={photo.image}
                    alt={photo.title}
                    loading="lazy"
                  />

                  <div className="photo-card-overlay">
                    <ImageIcon size={26} />
                    <span>Посмотреть</span>
                  </div>
                </div>

                <div className="photo-card-info">
                  <h2>{photo.title}</h2>
                  <span>{photo.date}</span>
                </div>
              </button>
            ))}
          </div>
        ) : (
          <div className="photos-empty">
            <Camera size={42} />
            <h2>Фотографий пока нет</h2>
            <p>
              После фотосессий ваши фотографии появятся здесь.
            </p>
          </div>
        )}
      </div>

      {selectedPhoto && (
        <div
          className="photo-modal"
          onClick={() => setSelectedPhoto(null)}
        >
          <button
            type="button"
            className="photo-modal-close"
            onClick={() => setSelectedPhoto(null)}
            aria-label="Закрыть просмотр"
          >
            <X size={25} />
          </button>

          <div
            className="photo-modal-content"
            onClick={(event) => event.stopPropagation()}
          >
            <img
              src={selectedPhoto.image}
              alt={selectedPhoto.title}
            />

            <div className="photo-modal-info">
              <h2>{selectedPhoto.title}</h2>
              <span>{selectedPhoto.date}</span>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}

export default PhotosPage;
