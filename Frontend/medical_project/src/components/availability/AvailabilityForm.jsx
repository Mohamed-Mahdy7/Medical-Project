import { useState } from 'react';
import { useAvailability } from '../../context/availabilityContext';

const DAYS_OF_WEEK = [
  { value: 0, label: 'Monday' },
  { value: 1, label: 'Tuesday' },
  { value: 2, label: 'Wednesday' },
  { value: 3, label: 'Thursday' },
  { value: 4, label: 'Friday' },
  { value: 5, label: 'Saturday' },
  { value: 6, label: 'Sunday' },
];

const initialState = {
  day_of_week: '',
  start_time: '',
  end_time: '',
  slot_duration_minutes: '',
  price: '',
  is_active: true,
};

export default function AvailabilityForm() {
  const { addAvailability } = useAvailability();

  const [formData, setFormData] = useState(initialState);
  const [errors, setErrors]     = useState({});
  const [loading, setLoading]   = useState(false);
  const [successMsg, setSuccessMsg] = useState('');

  const validate = () => {
    const newErrors = {};

    if (formData.day_of_week === '')
      newErrors.day_of_week = 'Day of week is required.';

    if (!formData.start_time)
      newErrors.start_time = 'Start time is required.';

    if (!formData.end_time)
      newErrors.end_time = 'End time is required.';

    if (formData.start_time && formData.end_time) {
      if (formData.start_time >= formData.end_time)
        newErrors.end_time = 'End time must be after start time.';
    }

    if (!formData.slot_duration_minutes) {
      newErrors.slot_duration_minutes = 'Slot duration is required.';
    } else if (Number(formData.slot_duration_minutes) <= 0) {
      newErrors.slot_duration_minutes = 'Must be a positive number.';
    } else if (Number(formData.slot_duration_minutes) > 480) {
      newErrors.slot_duration_minutes = 'Cannot exceed 480 minutes.';
    } else if (formData.start_time && formData.end_time) {
      const [sh, sm] = formData.start_time.split(':').map(Number);
      const [eh, em] = formData.end_time.split(':').map(Number);
      const totalMinutes = (eh * 60 + em) - (sh * 60 + sm);
      if (Number(formData.slot_duration_minutes) > totalMinutes)
        newErrors.slot_duration_minutes = `Exceeds time window (${totalMinutes} min available).`;
    }

    if (!formData.price) {
      newErrors.price = 'Price is required.';
    } else if (Number(formData.price) < 0) {
      newErrors.price = 'Price cannot be negative.';
    }

    return newErrors;
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({ ...prev, [name]: type === 'checkbox' ? checked : value }));
    setErrors(prev => ({ ...prev, [name]: '' }));
    setSuccessMsg('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSuccessMsg('');

    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) { setErrors(validationErrors); return; }

    setLoading(true);
    const result = await addAvailability({
      ...formData,
      day_of_week: Number(formData.day_of_week),
      slot_duration_minutes: Number(formData.slot_duration_minutes),
      price: Number(formData.price),
    });
    setLoading(false);

    if (result.success) {
      setFormData(initialState);
      setErrors({});
      setSuccessMsg('Availability slot added successfully!');
    } else {
      const backendErrors = {};
      for (const [key, val] of Object.entries(result.errors))
        backendErrors[key] = Array.isArray(val) ? val[0] : val;
      setErrors(backendErrors);
    }
  };

  return (
    <div className="card" style={{ maxWidth: 560 , margin: '0 auto'}}>
      <div className="page-header" style={{ marginBottom: '1.25rem' }}>
        <h2>Add Availability Slot</h2>
        <p>Set a recurring weekly time block for patient bookings.</p>
      </div>

      {successMsg && (
        <div style={{
          background: 'var(--color-completed-bg)',
          color: 'var(--color-completed-text)',
          border: '0.5px solid var(--color-completed-border)',
          borderRadius: 'var(--radius-md)',
          padding: '10px 14px',
          fontSize: '0.875rem',
          marginBottom: '1rem',
        }}>
          {successMsg}
        </div>
      )}

      {errors.non_field_errors && (
        <div style={{
          background: 'var(--color-cancelled-bg)',
          color: 'var(--color-cancelled-text)',
          border: '0.5px solid var(--color-cancelled-border)',
          borderRadius: 'var(--radius-md)',
          padding: '10px 14px',
          fontSize: '0.875rem',
          marginBottom: '1rem',
        }}>
          {errors.non_field_errors}
        </div>
      )}

      <form onSubmit={handleSubmit} noValidate>

        {/* Day of week */}
        <div className="form-group">
          <label htmlFor="day_of_week">Day of Week</label>
          <select
            id="day_of_week"
            name="day_of_week"
            className="select"
            value={formData.day_of_week}
            onChange={handleChange}
          >
            <option value="">— Select a day —</option>
            {DAYS_OF_WEEK.map(d => (
              <option key={d.value} value={d.value}>{d.label}</option>
            ))}
          </select>
          {errors.day_of_week && <FieldError msg={errors.day_of_week} />}
        </div>

        {/* Start / End time */}
        <div className="grid-2">
          <div className="form-group">
            <label htmlFor="start_time">Start Time</label>
            <input
              type="time"
              id="start_time"
              name="start_time"
              className="input"
              value={formData.start_time}
              onChange={handleChange}
            />
            {errors.start_time && <FieldError msg={errors.start_time} />}
          </div>
          <div className="form-group">
            <label htmlFor="end_time">End Time</label>
            <input
              type="time"
              id="end_time"
              name="end_time"
              className="input"
              value={formData.end_time}
              onChange={handleChange}
            />
            {errors.end_time && <FieldError msg={errors.end_time} />}
          </div>
        </div>

        {/* Slot duration + Price side by side */}
        <div className="grid-2">
          <div className="form-group">
            <label htmlFor="slot_duration_minutes">Slot Duration (min)</label>
            <input
              type="number"
              id="slot_duration_minutes"
              name="slot_duration_minutes"
              className="input"
              min="1"
              max="480"
              placeholder="e.g. 30"
              value={formData.slot_duration_minutes}
              onChange={handleChange}
            />
            {errors.slot_duration_minutes && <FieldError msg={errors.slot_duration_minutes} />}
          </div>
          <div className="form-group">
            <label htmlFor="price">Price (EGP)</label>
            <input
              type="number"
              id="price"
              name="price"
              className="input"
              min="0"
              placeholder="e.g. 200"
              value={formData.price}
              onChange={handleChange}
            />
            {errors.price && <FieldError msg={errors.price} />}
          </div>
        </div>

        {/* Is active */}
        <div className="form-group" style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <input
            type="checkbox"
            id="is_active"
            name="is_active"
            checked={formData.is_active}
            onChange={handleChange}
            style={{ width: 16, height: 16, accentColor: 'var(--color-primary-600)', cursor: 'pointer' }}
          />
          <label htmlFor="is_active" style={{ marginBottom: 0, cursor: 'pointer' }}>
            Active — patients can book this slot
          </label>
        </div>

        <button
          type="submit"
          className="btn-primary"
          disabled={loading}
          style={{ width: '100%', marginTop: '0.5rem', opacity: loading ? 0.7 : 1 }}
        >
          {loading ? 'Saving…' : 'Save Availability'}
        </button>
      </form>
    </div>
  );
}

function FieldError({ msg }) {
  return (
    <span style={{
      display: 'block',
      marginTop: 4,
      fontSize: '0.8125rem',
      color: 'var(--color-cancelled-text)',
    }}>
      {msg}
    </span>
  );
}