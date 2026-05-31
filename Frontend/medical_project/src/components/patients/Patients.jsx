import { useState, useEffect } from "react";
import { getPatientProfile, updatePatientProfile } from "../../services/patientService";

function PatientProfile() {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [editing, setEditing] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);

    const [form, setForm] = useState({
        date_of_birth: "",
        gender: "",
        phone: "",
        address: "",
        medical_history_notes: "",
    });

    // With this:
    useEffect(() => {
        // TEMP: remove when auth is fixed
        setProfile({
            date_of_birth: "1999-05-15",
            gender: "M",
            phone: "01012345678",
            address: "Cairo, Egypt",
            medical_history_notes: "No known allergies.",
        });
        setForm({
            date_of_birth: "1999-05-15",
            gender: "M",
            phone: "01012345678",
            address: "Cairo, Egypt",
            medical_history_notes: "No known allergies.",
        });
        setLoading(false);
    }, []);

    // useEffect(() => {
    //     fetchProfile();
    // }, []);

    async function fetchProfile() {
        try {
            const response = await getPatientProfile();
            const data = response.data.data;
            setProfile(data);
            setForm({
                date_of_birth: data.date_of_birth || "",
                gender: data.gender || "",
                phone: data.phone || "",
                address: data.address || "",
                medical_history_notes: data.medical_history_notes || "",
            });
        } catch {
            setError("Failed to load profile.");
        } finally {
            setLoading(false);
        }
    }

    function handleChange(e) {
        setForm({ ...form, [e.target.name]: e.target.value });
    }

    async function handleSubmit(e) {
        e.preventDefault();
        setError(null);
        setSuccess(false);
        try {
            const response = await updatePatientProfile(form);
            setProfile(response.data.data);
            setEditing(false);
            setSuccess(true);
        } catch {
            setError("Failed to update profile.");
        }
    }

    if (loading) return <p className="text-center mt-4">Loading profile...</p>;

    return (
        <div className="card" style={{ maxWidth: 600, margin: "2rem auto" }}>
            <div className="page-header">
                <h2>My Profile</h2>
                <p>Manage your personal information</p>
            </div>

            {error && (
                <div className="alert alert-danger">{error}</div>
            )}
            {success && (
                <div className="alert alert-success">Profile updated successfully.</div>
            )}

            {!editing ? (
                // ── View mode ──
                <div>
                    <div className="my-2">
                        <label>Date of Birth</label>
                        <p>{profile.date_of_birth || "—"}</p>
                    </div>
                    <div className="my-2">
                        <label>Gender</label>
                        <p>
                            {profile.gender === "M"
                                ? "Male"
                                : profile.gender === "F"
                                ? "Female"
                                : profile.gender === "O"
                                ? "Other"
                                : "—"}
                        </p>
                    </div>
                    <div className="my-2">
                        <label>Phone</label>
                        <p>{profile.phone || "—"}</p>
                    </div>
                    <div className="my-2">
                        <label>Address</label>
                        <p>{profile.address || "—"}</p>
                    </div>
                    <div className="my-2">
                        <label>Medical History Notes</label>
                        <p>{profile.medical_history_notes || "—"}</p>
                    </div>
                    <button
                        className="btn-primary mt-3"
                        onClick={() => setEditing(true)}
                    >
                        Edit Profile
                    </button>
                </div>
            ) : (
                // ── Edit mode ──
                <form onSubmit={handleSubmit}>
                    <div className="my-2">
                        <label htmlFor="date_of_birth">Date of Birth</label>
                        <input
                            id="date_of_birth"
                            name="date_of_birth"
                            type="date"
                            className="input w-100"
                            value={form.date_of_birth}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="my-2">
                        <label htmlFor="gender">Gender</label>
                        <select
                            id="gender"
                            name="gender"
                            className="input w-100"
                            value={form.gender}
                            onChange={handleChange}
                        >
                            <option value="">Select gender</option>
                            <option value="M">Male</option>
                            <option value="F">Female</option>
                            <option value="O">Other</option>
                        </select>
                    </div>
                    <div className="my-2">
                        <label htmlFor="phone">Phone</label>
                        <input
                            id="phone"
                            name="phone"
                            type="text"
                            className="input w-100"
                            value={form.phone}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="my-2">
                        <label htmlFor="address">Address</label>
                        <input
                            id="address"
                            name="address"
                            type="text"
                            className="input w-100"
                            value={form.address}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="my-2 mb-4">
                        <label htmlFor="medical_history_notes">
                            Medical History Notes
                        </label>
                        <textarea
                            id="medical_history_notes"
                            name="medical_history_notes"
                            className="input w-100"
                            rows={4}
                            value={form.medical_history_notes}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="d-flex gap-2">
                        <button type="submit" className="btn-primary">
                            Save Changes
                        </button>
                        <button
                            type="button"
                            className="btn-secondary"
                            onClick={() => {
                                setEditing(false);
                                setError(null);
                            }}
                        >
                            Cancel
                        </button>
                    </div>
                </form>
            )}
        </div>
    );
}

export default PatientProfile;