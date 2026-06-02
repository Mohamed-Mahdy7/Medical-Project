import { useState } from 'react';
import { useAvailability } from '../../context/availabilityContext';

const DAY_LABELS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];

const DAYS_OF_WEEK = [
  { value: 0, label: 'Monday' },
  { value: 1, label: 'Tuesday' },
  { value: 2, label: 'Wednesday' },
  { value: 3, label: 'Thursday' },
  { value: 4, label: 'Friday' },
  { value: 5, label: 'Saturday' },
  { value: 6, label: 'Sunday' },
];

function formatTime(timeStr) {
  if (!timeStr) return '—';
  const [h, m] = timeStr.split(':').map(Number);
  const ampm = h >= 12 ? 'PM' : 'AM';
  const hour = h % 12 || 12;
  return `${hour}:${String(m).padStart(2, '0')} ${ampm}`;
}

export default function AvailabilityList() {
  const { availabilities, loading, error, removeAvailability, editAvailability } = useAvailability();

  const [editingId, setEditingId]     = useState(null);
  const [editData, setEditData]       = useState({});
  const [editErrors, setEditErrors]   = useState({});
  const [editLoading, setEditLoading] = useState(false);

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this availability slot?')) return;
    const result = await removeAvailability(id);
    if (!result.success) alert('Cannot perform delete - Already booked');
  };

  const handleEditOpen = (a) => {
    setEditingId(a.id);
    setEditErrors({});
    setEditData({
      day_of_week:            a.day_of_week,
      start_time:             a.start_time.slice(0, 5),  
      end_time:               a.end_time.slice(0, 5),
      slot_duration_minutes:  a.slot_duration_minutes,
      price:                  a.price,
      is_active:              a.is_active,
    });
  };

  const handleEditCancel = () => {
    setEditingId(null);
    setEditData({});
    setEditErrors({});
  };

  const handleEditChange = (e) => {
    const { name, value, type, checked } = e.target;
    setEditData(prev => ({ ...prev, [name]: type === 'checkbox' ? checked : value }));
    setEditErrors(prev => ({ ...prev, [name]: '' }));
  };

  const validateEdit = () => {
    const e = {};
    if (!editData.start_time) e.start_time = 'Required.';
    if (!editData.end_time)   e.end_time   = 'Required.';
    if (editData.start_time && editData.end_time && editData.start_time >= editData.end_time)
      e.end_time = 'Must be after start time.';
    if (!editData.slot_duration_minutes || Number(editData.slot_duration_minutes) <= 0)
      e.slot_duration_minutes = 'Must be a positive number.';
    if (editData.price === '' || Number(editData.price) < 0)
      e.price = 'Must be 0 or more.';
    return e;
  };

  const handleEditSave = async (id) => {
    const validationErrors = validateEdit();
    if (Object.keys(validationErrors).length > 0) { setEditErrors(validationErrors); return; }

    setEditLoading(true);
    const result = await editAvailability(id, {
      day_of_week:           Number(editData.day_of_week),
      start_time:            editData.start_time,
      end_time:              editData.end_time,
      slot_duration_minutes: Number(editData.slot_duration_minutes),
      price:                 Number(editData.price),
      is_active:             editData.is_active,
    });
    setEditLoading(false);

    console.log(result);

    if (result.success) {
      handleEditCancel();
    } else {
      alert("Cannot perform update - Already booked");
    }
  };

  if (loading) return (
    <div style={{ padding: '2rem', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
      Loading slots…
    </div>
  );

  if (error) return (
    <div style={{
      background: 'var(--color-cancelled-bg)',
      color: 'var(--color-cancelled-text)',
      border: '0.5px solid var(--color-cancelled-border)',
      borderRadius: 'var(--radius-md)',
      padding: '10px 14px',
      fontSize: '0.875rem',
    }}>
      {error}
    </div>
  );

  if (availabilities.length === 0) return (
    <div style={{
      padding: '2rem',
      textAlign: 'center',
      color: 'var(--text-muted)',
      fontSize: '0.9rem',
      background: 'var(--bg-surface)',
      border: '0.5px solid var(--border-subtle)',
      borderRadius: 'var(--radius-lg)',
    }}>
      No availability slots yet. Add one above.
    </div>
  );

  return (
    <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
      <div className="table-wrap">
        <table className="table">
          <thead>
            <tr>
              <th>Day</th>
              <th>Start</th>
              <th>End</th>
              <th>Slot (min)</th>
              <th>Price</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {availabilities.map(a => (
              editingId === a.id
                ? (
                  /* ── Edit row ── */
                  <tr key={a.id} style={{ background: 'var(--bg-surface-2)' }}>
                    <td>
                      <select
                        name="day_of_week"
                        className="select"
                        value={editData.day_of_week}
                        onChange={handleEditChange}
                        style={{ minWidth: 110 }}
                      >
                        {DAYS_OF_WEEK.map(d => (
                          <option key={d.value} value={d.value}>{d.label}</option>
                        ))}
                      </select>
                    </td>
                    <td>
                      <input
                        type="time"
                        name="start_time"
                        className="input"
                        value={editData.start_time}
                        onChange={handleEditChange}
                        style={{ minWidth: 110 }}
                      />
                      {editErrors.start_time && <EditError msg={editErrors.start_time} />}
                    </td>
                    <td>
                      <input
                        type="time"
                        name="end_time"
                        className="input"
                        value={editData.end_time}
                        onChange={handleEditChange}
                        style={{ minWidth: 110 }}
                      />
                      {editErrors.end_time && <EditError msg={editErrors.end_time} />}
                    </td>
                    <td>
                      <input
                        type="number"
                        name="slot_duration_minutes"
                        className="input"
                        min="1"
                        max="480"
                        value={editData.slot_duration_minutes}
                        onChange={handleEditChange}
                        style={{ minWidth: 70 }}
                      />
                      {editErrors.slot_duration_minutes && <EditError msg={editErrors.slot_duration_minutes} />}
                    </td>
                    <td>
                      <input
                        type="number"
                        name="price"
                        className="input"
                        min="0"
                        value={editData.price}
                        onChange={handleEditChange}
                        style={{ minWidth: 80 }}
                      />
                      {editErrors.price && <EditError msg={editErrors.price} />}
                    </td>
                    <td>
                      <label style={{ display: 'flex', alignItems: 'center', gap: 6, cursor: 'pointer' }}>
                        <input
                          type="checkbox"
                          name="is_active"
                          checked={editData.is_active}
                          onChange={handleEditChange}
                          style={{ width: 15, height: 15, accentColor: 'var(--color-primary-600)' }}
                        />
                        <span style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>
                          Active
                        </span>
                      </label>
                    </td>
                    <td>
                      <div style={{ display: 'flex', gap: 6 }}>
                        <button
                          onClick={() => handleEditSave(a.id)}
                          disabled={editLoading}
                          className="btn-primary"
                          style={{ padding: '5px 12px', fontSize: '0.8125rem', opacity: editLoading ? 0.7 : 1 }}
                        >
                          {editLoading ? 'Saving…' : 'Save'}
                        </button>
                        <button
                          onClick={handleEditCancel}
                          className="btn-ghost"
                          style={{ padding: '5px 12px', fontSize: '0.8125rem' }}
                        >
                          Cancel
                        </button>
                      </div>
                    </td>
                  </tr>
                )
                : (
                  /* ── Normal row ── */
                  <tr key={a.id}>
                    <td style={{ fontWeight: 500, color: 'var(--text-primary)' }}>
                      {DAY_LABELS[a.day_of_week]}
                    </td>
                    <td>{formatTime(a.start_time)}</td>
                    <td>{formatTime(a.end_time)}</td>
                    <td>{a.slot_duration_minutes} min</td>
                    <td>EGP {a.price}</td>
                    <td>
                      <span className={a.is_active ? 'badge-confirmed' : 'badge-cancelled'}>
                        {a.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td>
                      <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
                        {/* Edit button */}
                        <button
                          onClick={() => !a.is_booked && handleEditOpen(a)}
                          className="btn-ghost"
                          disabled={a.is_booked}
                          title={a.is_booked ? 'Cannot edit — this slot has active bookings' : 'Edit'}
                          style={{
                            padding: '5px 12px',
                            fontSize: '0.8125rem',
                            opacity: a.is_booked ? 0.4 : 1,
                            cursor: a.is_booked ? 'not-allowed' : 'pointer',
                          }}
                        >
                          Edit
                        </button>

                        {/* Delete button */}
                        <button
                          onClick={() => !a.is_booked && handleDelete(a.id)}
                          disabled={a.is_booked}
                          title={a.is_booked ? 'Cannot delete — this slot has active bookings' : 'Delete'}
                          style={{
                            background: 'var(--color-cancelled-bg)',
                            color: 'var(--color-cancelled-text)',
                            border: '0.5px solid var(--color-cancelled-border)',
                            borderRadius: 'var(--radius-md)',
                            padding: '5px 12px',
                            fontSize: '0.8125rem',
                            fontWeight: 500,
                            cursor: a.is_booked ? 'not-allowed' : 'pointer',
                            opacity: a.is_booked ? 0.4 : 1,
                          }}
                        >
                          Delete
                        </button>

                        {/* Booked badge */}
                        {a.is_booked && (
                          <span className="badge-pending" title="This slot has active bookings">
                            Booked
                          </span>
                        )}
                      </div>
                    </td>
                  </tr>
                )
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function EditError({ msg }) {
  return (
    <span style={{
      display: 'block',
      marginTop: 3,
      fontSize: '0.75rem',
      color: 'var(--color-cancelled-text)',
    }}>
      {msg}
    </span>
  );
}