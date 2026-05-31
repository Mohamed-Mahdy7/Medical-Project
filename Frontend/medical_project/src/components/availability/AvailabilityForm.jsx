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
  is_active: true,
};

export default function AvailabilityForm() {
  const { addAvailability } = useAvailability();

  const [formData, setFormData] = useState(initialState);
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
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
        newErrors.slot_duration_minutes = `Slot duration exceeds the time window (${totalMinutes} min).`;
    }

    return newErrors;
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
    setErrors((prev) => ({ ...prev, [name]: '' }));
    setSuccessMsg('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSuccessMsg('');

    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setLoading(true);
    const result = await addAvailability({
      ...formData,
      day_of_week: Number(formData.day_of_week),
      slot_duration_minutes: Number(formData.slot_duration_minutes),
    });
    setLoading(false);

    if (result.success) {
      setFormData(initialState);
      setErrors({});
      setSuccessMsg('Availability slot added successfully!');
    } else {
      const backendErrors = {};
      for (const [key, val] of Object.entries(result.errors)) {
        backendErrors[key] = Array.isArray(val) ? val[0] : val;
      }
      setErrors(backendErrors);
    }
  };

  return (
    <form onSubmit={handleSubmit} noValidate>
      <h2>Add Availability Slot</h2>

      {successMsg && <p style={{ color: 'green' }}>{successMsg}</p>}
      {errors.non_field_errors && <p style={{ color: 'red' }}>{errors.non_field_errors}</p>}

      <div>
        <label htmlFor="day_of_week">Day of Week *</label><br />
        <select
          id="day_of_week"
          name="day_of_week"
          value={formData.day_of_week}
          onChange={handleChange}
        >
          <option value="">-- Select a day --</option>
          {DAYS_OF_WEEK.map((d) => (
            <option key={d.value} value={d.value}>{d.label}</option>
          ))}
        </select>
        {errors.day_of_week && <span style={{ color: 'red' }}> {errors.day_of_week}</span>}
      </div>

      <div>
        <label htmlFor="start_time">Start Time *</label><br />
        <input
          type="time"
          id="start_time"
          name="start_time"
          value={formData.start_time}
          onChange={handleChange}
        />
        {errors.start_time && <span style={{ color: 'red' }}> {errors.start_time}</span>}
      </div>

      <div>
        <label htmlFor="end_time">End Time *</label><br />
        <input
          type="time"
          id="end_time"
          name="end_time"
          value={formData.end_time}
          onChange={handleChange}
        />
        {errors.end_time && <span style={{ color: 'red' }}> {errors.end_time}</span>}
      </div>

      <div>
        <label htmlFor="slot_duration_minutes">Slot Duration (minutes) *</label><br />
        <input
          type="number"
          id="slot_duration_minutes"
          name="slot_duration_minutes"
          min="1"
          max="480"
          value={formData.slot_duration_minutes}
          onChange={handleChange}
          placeholder="e.g. 30"
        />
        {errors.slot_duration_minutes && <span style={{ color: 'red' }}> {errors.slot_duration_minutes}</span>}
      </div>

      <div>
        <label>
          <input
            type="checkbox"
            name="is_active"
            checked={formData.is_active}
            onChange={handleChange}
          />
          {' '}Active
        </label>
      </div>

      <br />
      <button type="submit" disabled={loading}>
        {loading ? 'Saving...' : 'Save Availability'}
      </button>
    </form>
  );
}