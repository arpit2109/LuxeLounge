import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';

const Profile = () => {
  const { user } = useAuth();
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchBookings = async () => {
      try {
        const response = await axios.get('/api/bookings/user/');
        setBookings(response.data);
      } catch (error) {
        setError('Failed to fetch bookings.');
        console.error('Error fetching bookings:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchBookings();
  }, []);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="profile-page">
      <h2>User Profile</h2>
      <div className="user-info">
        <p><strong>Username:</strong> {user.username}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Role:</strong> {user.role}</p>
        <p><strong>Phone:</strong> {user.phone_number || 'N/A'}</p>
      </div>

      <h3>Your Bookings</h3>
      {error && <div className="error-message">{error}</div>}
      <div className="bookings-list">
        {bookings.length === 0 ? (
          <p>No bookings found.</p>
        ) : (
          bookings.map(booking => (
            <div key={booking.id} className="booking-card">
              <h4>Booking #{booking.id}</h4>
              <p><strong>Room:</strong> {booking.room_details?.name || 'N/A'}</p>
              <p><strong>Check-in:</strong> {booking.check_in}</p>
              <p><strong>Check-out:</strong> {booking.check_out}</p>
              <p><strong>Guests:</strong> {booking.guests}</p>
              <p><strong>Total Price:</strong> ${booking.total_price}</p>
              <p><strong>Status:</strong> {booking.status}</p>
              {booking.special_requests && <p><strong>Special Requests:</strong> {booking.special_requests}</p>}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Profile;