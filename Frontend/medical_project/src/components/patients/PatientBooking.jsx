import { useState, useEffect } from "react";
import { getDoctors, getDoctorSlots, createAppointment } from "../../services/patientService";

const STEPS = { DOCTORS: 1, SLOTS: 2, CONFIRM: 3, SUCCESS: 4 };

function PatientBooking() {
    const [step, setStep] = useState(STEPS.DOCTORS);
    const [error, setError] = useState(null);

    const [nameFilter, setNameFilter] = useState("");
    const [doctors, setDoctors] = useState([]);
    const [selectedDoctor, setSelectedDoctor] = useState(null);

    const [date, setDate] = useState("");
    const [slots, setSlots] = useState([]);
    const [slotDuration, setSlotDuration] = useState(null);
    const [selectedSlot, setSelectedSlot] = useState(null);
    const [loadingSlots, setLoadingSlots] = useState(false);

    const [booking, setBooking] = useState(false);

    useEffect(() => {
        fetchDoctors();
    }, []);

    async function fetchDoctors() {
        setError(null);
        try {
            const response = await getDoctors({ name: nameFilter });
            setDoctors(response.data.results);
        } catch {
            setError("Failed to load doctors.");
        }
    }

    async function handleSearchDoctors() {
        await fetchDoctors();
    }

    function handleSelectDoctor(doctor) {
        setSelectedDoctor(doctor);
        setSlots([]);
        setSelectedSlot(null);
        setDate("");
        setStep(STEPS.SLOTS);
    }

    async function handleFetchSlots() {
        if (!date) return;
        setError(null);
        setLoadingSlots(true);
        setSelectedSlot(null);
        try {
            const response = await getDoctorSlots(selectedDoctor.id, date);
            setSlots(response.data.data.available_slots);
            setSlotDuration(response.data.data.slot_duration_minutes);
        } catch {
            setError("Failed to load available slots.");
        } finally {
            setLoadingSlots(false);
        }
    }

    function handleSelectSlot(slot) {
        setSelectedSlot(slot[1]);
        setStep(STEPS.CONFIRM);
    }

    async function handleConfirm() {
        setError(null);
        setBooking(true);
        try {
            const [hours, minutes] = selectedSlot.split(":");
            const startDateTime = new Date(`${date}T${hours}:${minutes}:00Z`);
            const endDateTime = new Date(startDateTime.getTime() + slotDuration * 60 * 1000);
            await createAppointment({
                doctor: selectedDoctor.id,
                start_time: startDateTime.toISOString(),
                end_time: endDateTime.toISOString(),
            });
            setStep(STEPS.SUCCESS);
        } catch (error){
            console.log(error)
            setError("Failed to book appointment.");
        } finally {
            setBooking(false);
        }
    }

    function handleReset() {
        setStep(STEPS.DOCTORS);
        setSelectedDoctor(null);
        setSelectedSlot(null);
        setDate("");
        setSlots([]);
        setSlotDuration(null);
        setError(null);
        setNameFilter("");
        fetchDoctors();
    }

    const filteredDoctors = doctors.filter(d =>
        `${d.user.first_name} ${d.user.last_name}`
            .toLowerCase()
            .includes(nameFilter.toLowerCase())
    );

    return (
        <div style={{ maxWidth: 640 }}>
            {error && (
                <p style={{ color: "var(--color-cancelled-text)", marginBottom: "1rem" }}>
                    {error}
                </p>
            )}

            {step !== STEPS.SUCCESS && (
                <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1.75rem" }}>
                    {["Find a Doctor", "Pick a Slot", "Confirm"].map((label, i) => {
                        const stepNum = i + 1;
                        const active = step === stepNum;
                        const done = step > stepNum;
                        return (
                            <div
                                key={label}
                                style={{
                                    display: "flex",
                                    alignItems: "center",
                                    gap: "0.4rem",
                                    fontSize: "0.875rem",
                                    fontWeight: active ? 600 : 400,
                                    color: active
                                        ? "var(--color-primary-600)"
                                        : done
                                            ? "var(--color-completed-text)"
                                            : "var(--color-ink-faint)",
                                }}
                            >
                                <span style={{
                                    width: 22,
                                    height: 22,
                                    borderRadius: "50%",
                                    display: "inline-flex",
                                    alignItems: "center",
                                    justifyContent: "center",
                                    fontSize: "0.75rem",
                                    fontWeight: 600,
                                    background: active
                                        ? "var(--color-primary-600)"
                                        : done
                                            ? "var(--color-completed-text)"
                                            : "var(--color-border)",
                                    color: active || done ? "#fff" : "var(--color-ink-muted)",
                                }}>
                                    {done ? "✓" : stepNum}
                                </span>
                                {label}
                                {i < 2 && (
                                    <span style={{ color: "var(--color-border-strong)", margin: "0 0.25rem" }}>
                                        /
                                    </span>
                                )}
                            </div>
                        );
                    })}
                </div>
            )}

            {step === STEPS.DOCTORS && (
                <div>
                    <div style={{ display: "flex", gap: "0.75rem", marginBottom: "1.25rem" }}>
                        <input
                            className="input"
                            placeholder="Search by doctor name..."
                            value={nameFilter}
                            onChange={(e) => setNameFilter(e.target.value)}
                            style={{ flex: 1 }}
                        />
                        <button className="btn-primary" onClick={handleSearchDoctors}>
                            Search
                        </button>
                    </div>

                    {filteredDoctors.length === 0 ? (
                        <p>No doctors found.</p>
                    ) : (
                        filteredDoctors.map(doctor => (
                            <div
                                key={doctor.id}
                                className="card"
                                style={{ marginBottom: "0.75rem" }}
                            >
                                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                                    <div>
                                        <h4>Dr. {doctor.user.first_name} {doctor.user.last_name}</h4>
                                        <small>{doctor.specialty.name} · {doctor.years_of_experience} yrs experience</small>
                                        {doctor.bio && (
                                            <p style={{ marginTop: "0.375rem", fontSize: "0.875rem" }}>
                                                {doctor.bio}
                                            </p>
                                        )}
                                        {doctor.available_days?.length > 0 && (
                                            <div style={{ marginTop: "0.5rem", display: "flex", flexWrap: "wrap", gap: "0.35rem" }}>
                                                {doctor.available_days.map(day => (
                                                    <span
                                                        key={day}
                                                        className="badge-confirmed"
                                                        style={{ fontSize: "0.75rem" }}
                                                    >
                                                        {day}
                                                    </span>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                    <button
                                        className="btn-primary"
                                        onClick={() => handleSelectDoctor(doctor)}
                                    >
                                        Book
                                    </button>
                                </div>
                            </div>
                        ))
                    )}
                </div>
            )}

            {step === STEPS.SLOTS && (
                <div>
                    <div className="card" style={{ marginBottom: "1.25rem" }}>
                        <h4>Dr. {selectedDoctor.user.first_name} {selectedDoctor.user.last_name}</h4>
                        <small>{selectedDoctor.specialty.name}</small>
                    </div>

                    <div className="form-group">
                        <label htmlFor="date">Select Date</label>
                        <div style={{ display: "flex", gap: "0.75rem" }}>
                            <input
                                id="date"
                                type="date"
                                className="input"
                                value={date}
                                min={new Date().toISOString().split("T")[0]}
                                onChange={(e) => setDate(e.target.value)}
                                style={{ flex: 1 }}
                            />
                            <button
                                className="btn-primary"
                                onClick={handleFetchSlots}
                                disabled={!date}
                            >
                                Check Slots
                            </button>
                        </div>
                    </div>

                    {loadingSlots && <p>Loading slots...</p>}

                    {slots.length > 0 && (
                        <div>
                            <label style={{ display: "block", marginBottom: "0.75rem" }}>
                                Available Slots
                            </label>
                            <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
                                {slots.map(slot => (
                                    <button
                                        key={slot}
                                        className={selectedSlot === slot ? "btn-primary" : "btn-ghost"}
                                        onClick={() => handleSelectSlot(slot)}
                                    >
                                        {slot[1]}
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}

                    {slots.length === 0 && date && !loadingSlots && (
                        <p>No available slots for this date.</p>
                    )}

                    <button
                        className="btn-ghost"
                        style={{ marginTop: "1.25rem" }}
                        onClick={() => setStep(STEPS.DOCTORS)}
                    >
                        ← Back
                    </button>
                </div>
            )}

            {step === STEPS.CONFIRM && (
                <div>
                    <div className="card card-confirmed" style={{ marginBottom: "1.25rem" }}>
                        <h4 style={{ marginBottom: "0.75rem" }}>Appointment Summary</h4>
                        <div className="form-group">
                            <label>Doctor</label>
                            <p>Dr. {selectedDoctor.user.first_name} {selectedDoctor.user.last_name}</p>
                        </div>
                        <div className="form-group">
                            <label>Specialty</label>
                            <p>{selectedDoctor.specialty.name}</p>
                        </div>
                        <div className="form-group">
                            <label>Date</label>
                            <p>{new Date(date).toLocaleDateString("en-EG", { dateStyle: "long" })}</p>
                        </div>
                        <div className="form-group" style={{ margin: 0 }}>
                            <label>Time</label>
                            <p>{selectedSlot}</p>
                        </div>
                    </div>

                    <div style={{ display: "flex", gap: "0.75rem" }}>
                        <button
                            className="btn-primary"
                            onClick={handleConfirm}
                            disabled={booking}
                        >
                            {booking ? "Booking..." : "Confirm Booking"}
                        </button>
                        <button
                            className="btn-ghost"
                            onClick={() => setStep(STEPS.SLOTS)}
                        >
                            ← Back
                        </button>
                    </div>
                </div>
            )}

            {step === STEPS.SUCCESS && (
                <div className="card card-completed" style={{ textAlign: "center", padding: "2rem" }}>
                    <h2 style={{ marginBottom: "0.5rem" }}>Booking Confirmed</h2>
                    <p style={{ marginBottom: "1.5rem" }}>
                        Your appointment with Dr. {selectedDoctor.user.first_name} {selectedDoctor.user.last_name} on {date} at {selectedSlot} has been booked.
                    </p>
                    <button className="btn-primary" onClick={handleReset}>
                        Book Another Appointment
                    </button>
                </div>
            )}
        </div>
    );
}

export default PatientBooking;