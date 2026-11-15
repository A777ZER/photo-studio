
import { useState } from "react";
import { Link } from "react-router-dom";
import {
  Printer,
  Image,
  CalendarDays,
  ChevronDown,
  Package,
  Clock3,
  CheckCircle2,
  XCircle,
} from "lucide-react";

import "../styles/PrintOrdersPage.css";

const initialOrders = [
  {
    id: 1003,
    date: "12 ноября 2026",
    status: "processing",
    items: [
      { name: "Портретная фотография", size: "15 × 20 см", quantity: 3 },
      { name: "Семейная фотография", size: "20 × 30 см", quantity: 2 },
    ],
    total: 1450,
  },
  {
    id: 1002,
    date: "5 ноября 2026",
    status: "completed",
    items: [
      { name: "Пейзаж", size: "10 × 15 см", quantity: 10 },
    ],
    total: 1200,
  },
  {
    id: 1001,
    date: "28 октября 2026",
    status: "pending",
    items: [
      { name: "Портретная фотография", size: "15 × 20 см", quantity: 2 },
    ],
    total: 600,
  },
  {
    id: 1000,
    date: "20 октября 2026",
    status: "cancelled",
    items: [
      { name: "Семейная фотография", size: "20 × 30 см", quantity: 1 },
    ],
    total: 750,
  },
];

const statusLabels = {
  pending: "Ожидает обработки",
  processing: "В обработке",
  completed: "Выполнен",
  cancelled: "Отменён",
};

const statusIcons = {
  pending: Clock3,
  processing: Package,
  completed: CheckCircle2,
  cancelled: XCircle,
};

function PrintOrdersPage() {
  const [orders] = useState(initialOrders);
  const [filter, setFilter] = useState("all");
  const [expandedOrder, setExpandedOrder] = useState(null);

  const filteredOrders =
    filter === "all"
      ? orders
      : orders.filter((order) => order.status === filter);

  function toggleOrder(orderId) {
    setExpandedOrder((previous) =>
      previous === orderId ? null : orderId
    );
  }

  return (
    <section className="print-orders-page">
      <div className="print-orders-container">
        <div className="print-orders-header">
          <div>
            <span className="print-orders-eyebrow">
              ЛИЧНЫЙ КАБИНЕТ
            </span>
            <h1>Заказы на печать</h1>
            <p>
              Здесь вы можете просматривать свои заказы и следить за
              их статусом.
            </p>
          </div>

          <Link to="/photos" className="print-orders-create-button">
            <Printer size={18} />
            Заказать печать
          </Link>
        </div>

        <div className="print-orders-summary">
          <div className="print-summary-card">
            <div className="print-summary-icon">
              <Printer size={21} />
            </div>
            <div>
              <span>Всего заказов</span>
              <strong>{orders.length}</strong>
            </div>
          </div>

          <div className="print-summary-card">
            <div className="print-summary-icon processing">
              <Package size={21} />
            </div>
            <div>
              <span>В обработке</span>
              <strong>
                {orders.filter(
                  (order) => order.status === "processing"
                ).length}
              </strong>
            </div>
          </div>

          <div className="print-summary-card">
            <div className="print-summary-icon completed">
              <CheckCircle2 size={21} />
            </div>
            <div>
              <span>Выполнено</span>
              <strong>
                {orders.filter(
                  (order) => order.status === "completed"
                ).length}
              </strong>
            </div>
          </div>
        </div>

        <div className="print-orders-toolbar">
          <div>
            <h2>История заказов</h2>
            <p>Все ваши заказы на печать фотографий</p>
          </div>

          <div className="print-orders-filter">
            <label htmlFor="order-status-filter">Статус:</label>
            <div className="print-filter-select">
              <select
                id="order-status-filter"
                value={filter}
                onChange={(event) => setFilter(event.target.value)}
              >
                <option value="all">Все заказы</option>
                <option value="pending">Ожидают обработки</option>
                <option value="processing">В обработке</option>
                <option value="completed">Выполненные</option>
                <option value="cancelled">Отменённые</option>
              </select>
              <ChevronDown size={16} />
            </div>
          </div>
        </div>

        <div className="print-orders-list">
          {filteredOrders.length > 0 ? (
            filteredOrders.map((order) => {
              const StatusIcon = statusIcons[order.status];
              const isExpanded = expandedOrder === order.id;

              return (
                <article className="print-order-card" key={order.id}>
                  <div className="print-order-main">
                    <div className="print-order-info">
                      <div className="print-order-number">
                        <span>Заказ</span>
                        <strong>№ {order.id}</strong>
                      </div>

                      <div className="print-order-date">
                        <CalendarDays size={15} />
                        <span>{order.date}</span>
                      </div>

                      <div
                        className={`print-order-status ${order.status}`}
                      >
                        <StatusIcon size={15} />
                        <span>{statusLabels[order.status]}</span>
                      </div>
                    </div>

                    <div className="print-order-total">
                      <span>Стоимость</span>
                      <strong>
                        {order.total.toLocaleString("ru-RU")} ₽
                      </strong>
                    </div>

                    <button
                      type="button"
                      className="print-order-details-button"
                      onClick={() => toggleOrder(order.id)}
                      aria-expanded={isExpanded}
                    >
                      {isExpanded ? "Скрыть" : "Подробнее"}
                      <ChevronDown
                        size={17}
                        className={isExpanded ? "rotated" : ""}
                      />
                    </button>
                  </div>

                  {isExpanded && (
                    <div className="print-order-details">
                      <h3>Состав заказа</h3>

                      {order.items.map((item, index) => (
                        <div
                          className="print-order-item"
                          key={`${order.id}-${index}`}
                        >
                          <div className="print-order-item-icon">
                            <Image size={18} />
                          </div>

                          <div className="print-order-item-info">
                            <strong>{item.name}</strong>
                            <span>{item.size}</span>
                          </div>

                          <span className="print-order-item-quantity">
                            {item.quantity} шт.
                          </span>
                        </div>
                      ))}
                    </div>
                  )}
                </article>
              );
            })
          ) : (
            <div className="print-orders-empty">
              <div className="print-orders-empty-icon">
                <Printer size={30} />
              </div>
              <h3>Заказы не найдены</h3>
              <p>
                Заказов с выбранным статусом пока нет.
              </p>
              <Link to="/photos">Перейти к фотографиям</Link>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

export default PrintOrdersPage;
