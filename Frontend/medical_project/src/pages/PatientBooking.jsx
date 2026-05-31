import PatientBooking from "../components/patients/PatientBooking";

function PatientBookingPage() {
    return (
        <main className="main-content">
            <div className="page">
                <div className="page-header">
                    <h1>Book an Appointment</h1>
                    <p>Find a doctor and schedule your visit</p>
                </div>
                <PatientBooking />
            </div>
        </main>
    );
}

export default PatientBookingPage;