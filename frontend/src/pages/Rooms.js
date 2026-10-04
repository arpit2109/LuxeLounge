import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

const Rooms = () => {
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [checkIn, setCheckIn] = useState(null);
  const [checkOut, setCheckOut] = useState(null);
  const [availability, setAvailability] = useState({});

  useEffect(() => {
    fetchRooms();
  }, []);

  const fetchRooms = async () => {
    try {
      const response = await axios.get('/api/rooms/');
      setRooms(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching rooms:', error);
      setLoading(false);
    }
  };

  const checkAvailability = async (roomId) => {
    if (!checkIn || !checkOut) {
      alert('Please select both check-in and check-out dates');
      return;
    }

    if (checkIn >= checkOut) {
      alert('Check-out date must be after check-in date');
      return;
    }

    try {
      const response = await axios.get(`/api/rooms/${roomId}/availability/`, {
        params: {
          check_in: checkIn.toISOString().split('T')[0],
          check_out: checkOut.toISOString().split('T')[0]
        }
      });
      
      setAvailability(prev => ({
        ...prev,
        [roomId]: response.data.is_available
      }));
    } catch (error) {
      console.error('Error checking availability:', error);
    }
  };

  if (loading) {
    return <div className="loading">Loading rooms...</div>;
  }

  return (
    <div className="rooms-page">
      <h2>Our Rooms</h2>
      
      <div className="date-selection">
        <h3>Select Dates to Check Availability</h3>
        <div className="date-pickers">
          <div>
            <label>Check-in:</label>
            <DatePicker
              selected={checkIn}
              onChange={date => setCheckIn(date)}
              minDate={new Date()}
              dateFormat="yyyy-MM-dd"
            />
          </div>
          <div>
            <label>Check-out:</label>
            <DatePicker
              selected={checkOut}
              onChange={date => setCheckOut(date)}
              minDate={checkIn || new Date()}
              dateFormat="yyyy-MM-dd"
            />
          </div>
        </div>
      </div>

      <div className="rooms-grid">
        {rooms.map(room => (
          <div key={room.id} className="room-card">
            <h3>{room.name}</h3>
            <p>{room.description}</p>
            <p>Price: ${room.price_per_night} per night</p>
            <p>Capacity: {room.capacity} guests</p>
            
            {checkIn && checkOut && (
              <div className="availability-section">
                <button 
                  onClick={() => checkAvailability(room.id)}
                  className="check-availability-btn"
                >
                  Check Availability
                </button>
                
                {availability[room.id] !== undefined && (
                  <p className={availability[room.id] ? 'available' : 'not-available'}>
                    {availability[room.id] 
                      ? 'Available for selected dates!' 
                      : 'Not available for selected dates'
                    }
                  </p>
                )}
                
                {availability[room.id] && (
                  <Link 
                    to={`/booking/${room.id}?check_in=${checkIn.toISOString().split('T')[0]}&check_out=${checkOut.toISOString().split('T')[0]}`}
                    className="book-now-btn"
                  >
                    Book Now
                  </Link>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Rooms;