
import { useEffect, useRef, useState } from "react";
import {
  Send,
  Paperclip,
  MoreVertical,
  MessageCircle,
  CheckCheck,
} from "lucide-react";

import "../styles/ChatPage.css";

const initialMessages = [
  {
    id: 1,
    text: "Здравствуйте! Добро пожаловать в Photo Studio. Чем могу вам помочь?",
    sender: "admin",
    time: "10:15",
  },
  {
    id: 2,
    text: "Здравствуйте! Хотелось бы узнать подробнее о записи на фотосессию.",
    sender: "client",
    time: "10:18",
  },
  {
    id: 3,
    text: "Конечно! Вы можете выбрать услугу, фотографа и удобное время на странице записи. Если возникнут вопросы, я с удовольствием помогу.",
    sender: "admin",
    time: "10:20",
  },
  {
    id: 4,
    text: "Спасибо! А можно ли перенести запись, если планы изменятся?",
    sender: "client",
    time: "10:23",
  },
  {
    id: 5,
    text: "Да, конечно. Напишите нам заранее, и мы поможем подобрать другое время.",
    sender: "admin",
    time: "10:25",
  },
];

function ChatPage() {
  const [messages, setMessages] = useState(initialMessages);
  const [message, setMessage] = useState("");
  const [isSending, setIsSending] = useState(false);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  function handleSubmit(event) {
    event.preventDefault();

    const trimmedMessage = message.trim();

    if (!trimmedMessage || isSending) {
      return;
    }

    setIsSending(true);

    const now = new Date();

    const newMessage = {
      id: Date.now(),
      text: trimmedMessage,
      sender: "client",
      time: now.toLocaleTimeString("ru-RU", {
        hour: "2-digit",
        minute: "2-digit",
      }),
    };

    setMessages((previous) => [...previous, newMessage]);
    setMessage("");
    setIsSending(false);

    inputRef.current?.focus();
  }

  return (
    <section className="chat-page">
      <div className="chat-container">
        <div className="chat-heading">
          <div>
            <span className="chat-eyebrow">ПОДДЕРЖКА</span>
            <h1>Чат с администратором</h1>
            <p>
              Задайте вопрос — мы поможем разобраться с услугами,
              записью и заказами.
            </p>
          </div>
        </div>

        <div className="chat-window">
          <div className="chat-header">
            <div className="chat-admin-avatar">
              <MessageCircle size={22} />
            </div>

            <div className="chat-admin-info">
              <strong>Администратор Photo Studio</strong>
              <span>
                <span className="chat-online-dot"></span>
                Служба поддержки
              </span>
            </div>

            <button
              type="button"
              className="chat-more-button"
              aria-label="Дополнительные действия"
            >
              <MoreVertical size={20} />
            </button>
          </div>

          <div className="chat-messages">
            <div className="chat-date-divider">
              <span>История переписки</span>
            </div>

            {messages.map((item) => (
              <div
                className={`chat-message-row ${
                  item.sender === "client" ? "own" : "other"
                }`}
                key={item.id}
              >
                {item.sender === "admin" && (
                  <div className="chat-message-avatar">A</div>
                )}

                <div className="chat-message-content">
                  <div className="chat-message-bubble">
                    <p>{item.text}</p>
                  </div>

                  <div className="chat-message-meta">
                    <span>{item.time}</span>

                    {item.sender === "client" && (
                      <CheckCheck size={14} />
                    )}
                  </div>
                </div>
              </div>
            ))}

            <div ref={messagesEndRef} />
          </div>

          <form className="chat-input-area" onSubmit={handleSubmit}>
            <button
              type="button"
              className="chat-attachment-button"
              aria-label="Прикрепить файл"
              title="Прикрепление файлов пока недоступно"
              disabled
            >
              <Paperclip size={20} />
            </button>

            <input
              ref={inputRef}
              type="text"
              placeholder="Введите сообщение..."
              value={message}
              onChange={(event) => setMessage(event.target.value)}
              aria-label="Текст сообщения"
            />

            <button
              type="submit"
              className="chat-send-button"
              disabled={!message.trim() || isSending}
              aria-label="Отправить сообщение"
            >
              <Send size={19} />
            </button>
          </form>
        </div>

        <p className="chat-note">
          Ответы в демонстрационном чате не отправляются администратору.
        </p>
      </div>
    </section>
  );
}

export default ChatPage;
