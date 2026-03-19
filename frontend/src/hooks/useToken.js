// hooks/useToken.js
// Simple hook to get and manage token

export const useToken = () => {
  const token = localStorage.getItem('token');

  const getAuthHeader = () => {
    return {
      'Authorization': `Bearer ${token}`
    };
  };

  const logout = () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
  };

  const isAuthenticated = !!token;

  return { token, getAuthHeader, logout, isAuthenticated };
};