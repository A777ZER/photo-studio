
import api from "./client.js";

// Регистрация нового пользователя
export async function registerUser(userData) {
  const response = await api.post("/auth/register", userData);

  return response.data;
}

// Авторизация пользователя
export async function loginUser(credentials) {
  const response = await api.post("/auth/login", credentials);

  return response.data;
}
