import './App.css';
import { Routes, Route, Navigate } from "react-router-dom";
import HomePage from "./page/home/HomePage";
import LoginPage from "./page/auth/login/LoginPage";
import SignUpPage from "./page/auth/signup/SignUpPage";
import Sidebar from './components/common/Sidebar'; // Fixed casing here
import RightPanel from './components/common/RightPanel';
import NotificationPage from './page/notification/NotificationPage';
import ProfilePage from './page/profile/ProfilePage';
import { Toaster } from 'react-hot-toast';
import { useQuery } from '@tanstack/react-query';
import { baseUrl } from './constant/url';
import LoadingSpinner from './components/common/LoadingSpinner';

function App() {
  const { data: authUser, isLoading } = useQuery({
    queryKey: ["authUser"],
    queryFn: async () => {
      try {
        const res = await fetch(`${baseUrl}/api/auth/me`, {
          method: "GET",
          credentials: "include",
          headers: {
            "Content-Type": "application/json"
          }
        });
        const data = await res.json();
        if (data.error) return null;
        if (!res.ok) {
          throw new Error(data.error || "Something went wrong");
        }
        console.log("authUser is here:", data);
        return data;
      } catch (error) {
        throw new Error(error);
      }
    },
    retry: false
  });

  if (isLoading) {
    return (
      <div className='flex justify-center items-center h-screen'>
        <LoadingSpinner size='lg' />
      </div>
    );
  }

  return (
    <div className='flex max-w-8xl mx-auto'>
      {authUser && <Sidebar />}
      <Routes>
        <Route path='/' element={authUser ? <HomePage /> : <Navigate to="/login" />} />
        <Route path='/login' element={!authUser ? <LoginPage /> : <Navigate to="/" />} />
        <Route path='/signup' element={!authUser ? <SignUpPage /> : <Navigate to="/" />} />
        <Route path='/notifications' element={authUser ? <NotificationPage /> : <Navigate to="/login" />} />
        <Route path='/profile/:userName' element={authUser ? <ProfilePage /> : <Navigate to="/login" />} />
      </Routes>
      {authUser && <RightPanel />}
      <Toaster />
    </div>
  );
}

export default App;
