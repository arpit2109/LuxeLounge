import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import DatePicker from 'react-datepicker';

const Booking = () => {
  const { roomId } = useParams();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [room, setRoom] = useState(null);
  const [loading, setLoading] = useState(true);
  const [bookingData, setBookingData] = useState({
    check_in: searchParams.get('check_in') || '',
    check_out: searchParams.get('check_out') || '',
    guests: 1,
    special_requests: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const fetchRoom = useCallback(async () => {
    try {
      const response = await axios.get(`/api/rooms/${roomId}/`);
      setRoom(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching room:', error);
      setLoading(false);
    }
  }, [roomId]);

  useEffect(() => {
    fetchRoom();
  }, [fetchRoom]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setBookingData({
      ...bookingData,
      [name]: value
    });
  };

  const handleDateChange = (name, date) => {
    setBookingData({
      ...bookingData,
      [name]: date.toISOString().split('T')[0]
    });
  };

  // In the handleSubmit function, ensure proper data formatting
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!user) {
      setError('Please log in to make a booking');
      return;
    }

    try {
      // Ensure dates are in YYYY-MM-DD format and room ID is an integer
      const formattedData = {
        check_in: bookingData.check_in,
        check_out: bookingData.check_out,
        guests: parseInt(bookingData.guests),
        special_requests: bookingData.special_requests,
        room: parseInt(roomId), // Ensure room ID is an integer
      };

      const response = await axios.post('/api/bookings/', formattedData);
      setSuccess('Booking created successfully!');
      
      setTimeout(() => {
        navigate('/profile');
      }, 2000);
    } catch (error) {
      console.error('Booking error:', error.response);
      if (error.response?.data?.user) {
        setError('Authentication error. Please log in again.');
      } else {
        setError(error.response?.data?.error || error.response?.data?.message || 'Error creating booking');
      }
    }
  };

  if (loading) {
    return <div className="loading">Loading room details...</div>;
  }

  if (!room) {
    return <div className="error">Room not found</div>;
  }

  // Calculate total price
  const checkInDate = new Date(bookingData.check_in);
  const checkOutDate = new Date(bookingData.check_out);
  const nights = checkOutDate && checkInDate ? 
    Math.ceil((checkOutDate - checkInDate) / (1000 * 60 * 60 * 24)) : 0;
  const totalPrice = nights * room.price_per_night;

  return (
    <div className="booking-page">
      <h2>Book {room.name}</h2>
      
      <div className="booking-container">
        <div className="room-info">
          <h3>Room Details</h3>
          <p>{room.description}</p>
          <p><strong>Price per night:</strong> ${room.price_per_night}</p>
          <p><strong>Capacity:</strong> {room.capacity} guests</p>
          <p><strong>Amenities:</strong> {room.amenities.join(', ')}</p>
        </div>

        <form onSubmit={handleSubmit} className="booking-form">
          <h3>Booking Details</h3>
          
          {error && <div className="error-message">{error}</div>}
          {success && <div className="success-message">{success}</div>}

          <div className="form-group">
            <label>Check-in Date</label>
            <DatePicker
              selected={bookingData.check_in ? new Date(bookingData.check_in) : null}
              onChange={date => handleDateChange('check_in', date)}
              minDate={new Date()}
              dateFormat="yyyy-MM-dd"
            />
          </div>

          <div className="form-group">
            <label>Check-out Date</label>
            <DatePicker
              selected={bookingData.check_out ? new Date(bookingData.check_out) : null}
              onChange={date => handleDateChange('check_out', date)}
              minDate={bookingData.check_in ? new Date(bookingData.check_in) : new Date()}
              dateFormat="yyyy-MM-dd"
            />
          </div>

          <div className="form-group">
            <label>Number of Guests</label>
            <input
              type="number"
              name="guests"
              value={bookingData.guests}
              onChange={handleInputChange}
              min="1"
              max={room.capacity}
              required
            />
          </div>

          <div className="form-group">
            <label>Special Requests</label>
            <textarea
              name="special_requests"
              value={bookingData.special_requests}
              onChange={handleInputChange}
              rows="3"
            />
          </div>

          {nights > 0 && (
            <div className="price-summary">
              <h4>Price Summary</h4>
              <p>{nights} night(s) × ${room.price_per_night} = ${totalPrice}</p>
            </div>
          )}

          <button type="submit" className="submit-btn">
            Confirm Booking
          </button>
        </form>
      </div>
    </div>
  );
};

export default Booking;