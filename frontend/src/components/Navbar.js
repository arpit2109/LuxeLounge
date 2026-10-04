import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to="/">LuxeLounge</Link>
      </div>
      <div className="navbar-menu">
        <Link to="/" className="navbar-item">Home</Link>
        <Link to="/rooms" className="navbar-item">Rooms</Link>
        
        {user ? (
          <>
            <Link to="/profile" className="navbar-item">Profile</Link>
            {user.role === 'admin' && (
              <Link to="/admin" className="navbar-item">Admin</Link>
            )}
            <button onClick={logout} className="navbar-item">Logout</button>
          </>
        ) : (
          <Link to="/login" className="navbar-item">Login</Link>
        )}
      </div>
    </nav>
  );
};

export default Navbar;