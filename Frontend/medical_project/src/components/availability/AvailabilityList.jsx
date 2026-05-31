import { useAvailability } from '../../context/availabilityContext';

export default function AvailabilityList() {
  const { availabilities, loading, error, removeAvailability } = useAvailability();

  const DAY_LABELS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this availability slot?')) return;
    const result = await removeAvailability(id);
    if (!result.success) alert('Failed to delete.');
  };

  if (loading) return <p>Loading...</p>;
  if (error)   return <p style={{ color: 'red' }}>{error}</p>;
  if (availabilities.length === 0) return <p>No availability slots yet.</p>;

  return (
    <table border="1" cellPadding="8">
      <thead>
        <tr>
          <th>Day</th>
          <th>Start</th>
          <th>End</th>
          <th>Slot (min)</th>
          <th>Active</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {availabilities.map((a) => (
          <tr key={a.id}>
            <td>{DAY_LABELS[a.day_of_week]}</td>
            <td>{a.start_time}</td>
            <td>{a.end_time}</td>
            <td>{a.slot_duration_minutes}</td>
            <td>{a.is_active ? 'Yes' : 'No'}</td>
            <td>
              <button onClick={() => handleDelete(a.id)}>Delete</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}