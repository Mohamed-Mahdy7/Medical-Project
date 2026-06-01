import AvailabilityForm from '../../components/availability/AvailabilityForm';
import AvailabilityList from '../../components/availability/AvailabilityList';
import { AvailabilityProvider } from '../../context/availabilityContext';

export default function AvailabilityPage() {
  return (
    <AvailabilityProvider>
      <div>
        <AvailabilityForm />
        <hr />
        <h2>My Availability</h2>
        <AvailabilityList />
      </div>
    </AvailabilityProvider>
  );
}