import { useEffect, useState } from "react";

import { getAppointments, updateAppointment } from "../../services/appointmentService";

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

    function renderActions(appointment) {
        const status = appointment.status;

        if (status === "PENDING") {
            return (
                <div style={{ display: "flex", gap: "8px" }}>
                    <button className="btn-primary" onClick={() => handleConfirm(appointment.id)}>Confirm</button>
                    <button className="btn-ghost" onClick={() => handleCancel(appointment.id)}>Cancel</button>
                </div>
            );
        }

        if (status === "CONFIRMED") {
            return (
                <div style={{ display: "flex", gap: "8px" }}>
                    <button className="btn-primary" onClick={() => handleComplete(appointment.id)}>Complete</button>
                    <button className="btn-ghost" onClick={() => handleCancel(appointment.id)}>Cancel</button>
                </div>
            );
        }

        return (
            <span style={{ color: "#8FA6B5", fontSize: "13px" }}>No actions</span>
        );
    }

    async function handleConfirm(id) {
        try {
            await updateAppointment(id, {
                status: "CONFIRMED"
            });

            loadAppointments()
        } catch (error) {
            console.error(error);
        }
    }

    async function handleCancel(id) {
        try {
            await updateAppointment(id, {
                status: "CANCELLED"
            });

            loadAppointments();
        } catch(error) {
            console.error(error);
        }
    }

    async function handleComplete(id) {
        try {
            await updateAppointment(id, {
                status: "COMPLETED"
            });

            loadAppointments();
        } catch(error) {
            console.error(error);
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
                                <th>Actions</th>
                            </tr>
                        </thead>

                        <tbody>
                            {appointments.length === 0 ? (
                                <tr>
                                    <td colSpan="6">
                                        No appointments found
                                    </td>
                                </tr>
                            ) : (
                                appointments.map((appointment) => (
                                    <tr key={appointment.id}>
                                        <td>{appointment.patient_name}</td>

                                        <td>
                                            <span className={`badge-${appointment.status.toLowerCase()}`}>
                                                {appointment.status}
                                            </span>
                                        </td>

                                        <td>
                                            {new Date(appointment.start_time).toLocaleString()}
                                        </td>

                                        <td>
                                            {new Date(appointment.end_time).toLocaleString()}
                                        </td>

                                        <td>
                                            {appointment.notes || "-"}
                                        </td>

                                        <td>
                                            { renderActions(appointment) }
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