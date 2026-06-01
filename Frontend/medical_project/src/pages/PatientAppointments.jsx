import PatientAppointments from "../components/patients/PatientAppointments";

function PatientAppointmentsPage() {
    return (
        <main className="main-content">
            <div className="page">
                <div className="page-header">
                    <h1>My Appointments</h1>
                    <p>View and manage your appointments</p>
                </div>
                <PatientAppointments />
            </div>
        </main>
    );
}

export default PatientAppointmentsPage;