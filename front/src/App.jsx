
import { BrowserRouter, Route, Routes } from "react-router-dom";

import Layout from "./components/Layout.jsx";

import HomePage from "./pages/HomePage.jsx";
import ServicesPage from "./pages/ServicesPage.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import RegisterPage from "./pages/RegisterPage.jsx";
import ProfilePage from "./pages/ProfilePage.jsx";
import BookingPage from "./pages/BookingPage.jsx";
import MyBookingsPage from "./pages/MyBookingsPage.jsx";
import PhotosPage from "./pages/PhotosPage.jsx";
import PrintOrdersPage from "./pages/PrintOrdersPage.jsx";
import ChatPage from "./pages/ChatPage.jsx";
import PhotographerDashboard from "./pages/PhotographerDashboard.jsx";
import AdminDashboard from "./pages/AdminDashboard.jsx";

function NotFoundPage() {
  return (
    <section>
      <h1>404</h1>
      <p>Страница не найдена.</p>
    </section>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/services" element={<ServicesPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/booking" element={<BookingPage />} />
          <Route path="/my-bookings" element={<MyBookingsPage />} />
          <Route path="/photos" element={<PhotosPage />} />
          <Route path="/print-orders" element={<PrintOrdersPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route
            path="/photographer"
            element={<PhotographerDashboard />}
          />
          <Route path="/admin" element={<AdminDashboard />} />
        </Route>

        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
