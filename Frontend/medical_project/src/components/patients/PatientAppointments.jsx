import { useState, useEffect } from "react";
import {
    getAppointments,
    cancelAppointment,
    rescheduleAppointment,
    getDoctorSlots,
} from "../../services/patientService";

function PatientAppointments() {
    const [appointments, setAppointments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [statusFilter, setStatusFilter] = useState("");
    const [typeFilter, setTypeFilter] = useState("");

    const [rescheduling, setRescheduling] = useState(null);
    const [rescheduleDate, setRescheduleDate] = useState("");
    const [rescheduleSlots, setRescheduleSlots] = useState([]);
    const [loadingSlots, setLoadingSlots] = useState(false);
    const [selectedSlot, setSelectedSlot] = useState(null);
    const [rescheduleError, setRescheduleError] = useState(null);

    useEffect(() => {
        fetchAppointments();
    }, [statusFilter, typeFilter]);

    async function fetchAppointments() {
        setLoading(true);
        setError(null);
        try {
            const response = await getAppointments({
                status: statusFilter,
                type: typeFilter,
            });
            setAppointments(response.data.results);
        } catch {
            setError("Failed to load appointments.");
        } finally {
            setLoading(false);
        }
    }

    async function handleCancel(id) {
        if (!confirm("Are you sure you want to cancel this appointment?")) return;
        try {
            await cancelAppointment(id);
            setAppointments(appointments.map(a =>
                a.id === id ? { ...a, status: "CANCELLED" } : a
            ));
        } catch {
            setError("Failed to cancel appointment.");
        }
    }

    function openReschedule(appointment) {
        setRescheduling(appointment.id);
        setRescheduleDate("");
        setRescheduleSlots([]);
        setSelectedSlot(null);
        setRescheduleError(null);
    }

    function closeReschedule() {
        setRescheduling(null);
        setRescheduleDate("");
        setRescheduleSlots([]);
        setSelectedSlot(null);
        setRescheduleError(null);
    }

    async function handleFetchRescheduleSlots(doctorId) {
        if (!rescheduleDate) return;
        setLoadingSlots(true);
        setRescheduleError(null);
        setSelectedSlot(null);
        try {
            const response = await getDoctorSlots(doctorId, rescheduleDate);
            setRescheduleSlots(response.data.data.available_slots);
        } catch {
            setRescheduleError("Failed to load slots.");
        } finally {
            setLoadingSlots(false);
        }
    }

    async function handleConfirmReschedule(appointment) {
        if (!selectedSlot) return;
        setRescheduleError(null);
        try {
            const [hours, minutes] = selectedSlot.split(":");
            const newStartTime = new Date(
                `${rescheduleDate}T${hours}:${minutes}:00`
            ).toISOString();
            await rescheduleAppointment(appointment.id, newStartTime);
            setAppointments(appointments.map(a =>
                a.id === appointment.id
                    ? { ...a, start_time: newStartTime }
                    : a
            ));
            closeReschedule();
        } catch {
            setRescheduleError("Failed to reschedule appointment.");
        }
    }

    function formatDateTime(dateStr) {
        return new Date(dateStr).toLocaleString("en-EG", {
            dateStyle: "medium",
            timeStyle: "short",
        });
    }

    const filtered = appointments.filter(a => {
        if (statusFilter && a.status !== statusFilter) return false;
        if (typeFilter === "upcoming" && new Date(a.start_time) < new Date()) return false;
        if (typeFilter === "past" && new Date(a.start_time) >= new Date()) return false;
        return true;
    });

    if (loading) return <p>Loading appointments...</p>;

    return (
        <div>
            {error && (
                <p style={{ color: "var(--color-cancelled-text)", marginBottom: "1rem" }}>
                    {error}
                </p>
            )}

            <div style={{ display: "flex", gap: "1rem", marginBottom: "1.5rem" }}>
                <div className="form-group" style={{ margin: 0 }}>
                    <label htmlFor="statusFilter">Status</label>
                    <select
                        id="statusFilter"
                        className="select"
                        value={statusFilter}
                        onChange={(e) => setStatusFilter(e.target.value)}
                    >
                        <option value="">All</option>
                        <option value="PENDING">Pending</option>
                        <option value="CONFIRMED">Confirmed</option>
                        <option value="CANCELLED">Cancelled</option>
                        <option value="COMPLETED">Completed</option>
                    </select>
                </div>
                <div className="form-group" style={{ margin: 0 }}>
                    <label htmlFor="typeFilter">Type</label>
                    <select
                        id="typeFilter"
                        className="select"
                        value={typeFilter}
                        onChange={(e) => setTypeFilter(e.target.value)}
                    >
                        <option value="">All</option>
                        <option value="upcoming">Upcoming</option>
                        <option value="past">Past</option>
                    </select>
                </div>
            </div>

            {filtered.length === 0 ? (
                <p>No appointments found.</p>
            ) : (
                filtered.map(appointment => (
                    <div key={appointment.id} style={{ marginBottom: "1rem" }}>
                        <div className={`card card-${appointment.status.toLowerCase()}`}>
                            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.75rem" }}>
                                <h4>{appointment.doctor}</h4>
                                <span className={`badge-${appointment.status.toLowerCase()}`}>
                                    {appointment.status}
                                </span>
                            </div>
                            <p><strong>From:</strong> {formatDateTime(appointment.start_time)}</p>
                            <p><strong>To:</strong> {formatDateTime(appointment.end_time)}</p>
                            {appointment.notes && (
                                <p style={{ marginTop: "0.5rem" }}>
                                    <strong>Notes:</strong> {appointment.notes}
                                </p>
                            )}
                            {(appointment.status === "PENDING" || appointment.status === "CONFIRMED") && (
                                <div style={{ display: "flex", gap: "0.75rem", marginTop: "1rem" }}>
                                    <button
                                        className="btn-primary"
                                        onClick={() =>
                                            rescheduling === appointment.id
                                                ? closeReschedule()
                                                : openReschedule(appointment)
                                        }
                                    >
                                        {rescheduling === appointment.id ? "Close" : "Reschedule"}
                                    </button>
                                    {appointment.status === "PENDING" && (
                                        <button
                                            className="btn-ghost"
                                            onClick={() => handleCancel(appointment.id)}
                                        >
                                            Cancel
                                        </button>
                                    )}
                                </div>
                            )}
                        </div>

                        {rescheduling === appointment.id && (
                            <div className="card" style={{ borderTop: "none", borderRadius: "0 0 var(--radius-lg) var(--radius-lg)" }}>
                                {rescheduleError && (
                                    <p style={{ color: "var(--color-cancelled-text)", marginBottom: "0.75rem" }}>
                                        {rescheduleError}
                                    </p>
                                )}
                                <div className="form-group">
                                    <label htmlFor="rescheduleDate">New Date</label>
                                    <div style={{ display: "flex", gap: "0.75rem" }}>
                                        <input
                                            id="rescheduleDate"
                                            type="date"
                                            className="input"
                                            value={rescheduleDate}
                                            min={new Date().toISOString().split("T")[0]}
                                            onChange={(e) => setRescheduleDate(e.target.value)}
                                            style={{ flex: 1 }}
                                        />
                                        <button
                                            className="btn-primary"
                                            onClick={() => handleFetchRescheduleSlots(appointment.doctor_id)}
                                            disabled={!rescheduleDate}
                                        >
                                            Check Slots
                                        </button>
                                    </div>
                                </div>

                                {loadingSlots && <p>Loading slots...</p>}

                                {rescheduleSlots.length > 0 && (
                                    <div className="form-group">
                                        <label>Available Slots</label>
                                        <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem", marginTop: "0.375rem" }}>
                                            {rescheduleSlots.map(slot => (
                                                <button
                                                    key={slot}
                                                    className={selectedSlot === slot ? "btn-primary" : "btn-ghost"}
                                                    onClick={() => setSelectedSlot(slot)}
                                                >
                                                    {slot}
                                                </button>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {rescheduleSlots.length === 0 && rescheduleDate && !loadingSlots && (
                                    <p style={{ marginBottom: "0.75rem" }}>No available slots for this date.</p>
                                )}

                                {selectedSlot && (
                                    <div style={{ display: "flex", gap: "0.75rem", marginTop: "0.5rem" }}>
                                        <button
                                            className="btn-primary"
                                            onClick={() => handleConfirmReschedule(appointment)}
                                        >
                                            Confirm — {selectedSlot}
                                        </button>
                                        <button
                                            className="btn-ghost"
                                            onClick={() => setSelectedSlot(null)}
                                        >
                                            Clear
                                        </button>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                ))
            )}
        </div>
    );
}

export default PatientAppointments;