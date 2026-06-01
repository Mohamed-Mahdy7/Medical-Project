import { useEffect, useState } from "react";
import { getAppointments } from "../../services/appointmentService";

export default function DoctorAppointments() {
    const [appointments, setAppointments] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadAppointments();
    }, []);

    async function loadAppointments() {
        try {
            const response = await getAppointments();
            setAppointments(response.data.results);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    }

    if (loading) {
        return (
            <div className="page">
                <h2>Loading...</h2>
            </div>
        );
    }

    return (
        <div className="page">
            
            <div className="page-header">
                <h1>Doctor Appointments</h1>
                <p>View all your appointments</p>
            </div>

            <div className="card">

                <div className="table-wrap">
                    <table className="table">

                        <thead>
                            <tr>
                                <th>Patient</th>
                                <th>Status</th>
                                <th>Start Time</th>
                                <th>End Time</th>
                                <th>Notes</th>
                            </tr>
                        </thead>

                        <tbody>
                            {appointments.length === 0 ? (
                                <tr>
                                    <td colSpan="5">
                                        No appointments found
                                    </td>
                                </tr>
                            ) : (
                                appointments.map((a) => (
                                    <tr key={a.id}>
                                        <td>{a.patient_name}</td>

                                        <td>
                                            <span className={`badge-${a.status.toLowerCase()}`}>
                                                {a.status}
                                            </span>
                                        </td>

                                        <td>
                                            {new Date(a.start_time).toLocaleString()}
                                        </td>

                                        <td>
                                            {new Date(a.end_time).toLocaleString()}
                                        </td>

                                        <td>
                                            {a.notes || "-"}
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>

                    </table>
                </div>

            </div>
        </div>
    );
}