import AvailabilityForm from '../../components/availability/AvailabilityForm';
import AvailabilityList from '../../components/availability/AvailabilityList';
import { AvailabilityProvider } from '../../context/availabilityContext';

export default function AvailabilityPage() {
  return (
    <AvailabilityProvider>
      <div className="page" style={{ margin: '0 auto' }}>
        <div className="page-header">
          <h1>My Availability</h1>
          <p>Manage your weekly schedule .</p>
        </div>

        <AvailabilityForm />

        <hr className="divider" />

        <h2 style={{ marginBottom: '1rem' }}>Current availability</h2>
        <AvailabilityList />
      </div>
    </AvailabilityProvider>
  );
}