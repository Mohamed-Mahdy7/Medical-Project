import { useState, useEffect } from "react";
import { getPatientProfile, updatePatientProfile } from "../../services/patientService";
import InputField from "../accounts/InputFields";

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

    useEffect(() => {
        fetchProfile();
    }, []);

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
        } catch(error) {
            console.log(error)
            setError("Failed to update profile.");
        }
    }

    const genderLabel = { M: "Male", F: "Female" };

    if (loading) return <p>Loading profile...</p>;

    return (
        <div className="card" style={{ maxWidth: 600 }}>
            <div className="page-header">
                <h2>{profile.first_name} {profile.last_name}</h2>
                <p>{profile.email}</p>
            </div>

            {error && (
                <p style={{ color: "var(--color-cancelled-text)", marginBottom: "1rem" }}>
                    {error}
                </p>
            )}
            {success && (
                <p style={{ color: "var(--color-completed-text)", marginBottom: "1rem" }}>
                    Profile updated successfully.
                </p>
            )}

            {!editing ? (
                <div>
                    <div className="form-group">
                        <label>Date of Birth</label>
                        <p>{profile.date_of_birth || "—"}</p>
                    </div>
                    <div className="form-group">
                        <label>Gender</label>
                        <p>{genderLabel[profile.gender] || "—"}</p>
                    </div>
                    <div className="form-group">
                        <label>Phone</label>
                        <p>{profile.phone || "—"}</p>
                    </div>
                    <div className="form-group">
                        <label>Address</label>
                        <p>{profile.address || "—"}</p>
                    </div>
                    <div className="form-group">
                        <label>Medical History Notes</label>
                        <p>{profile.medical_history_notes || "—"}</p>
                    </div>
                    <button className="btn-primary" onClick={() => setEditing(true)}>
                        Edit Profile
                    </button>
                </div>
            ) : (
                <form onSubmit={handleSubmit}>
                    <InputField
                        id="date_of_birth"
                        label="Date of Birth"
                        type="date"
                        value={form.date_of_birth}
                        className="input"
                        setValue={(val) => setForm({ ...form, date_of_birth: val })}
                    />
                    <div className="form-group">
                        <label htmlFor="gender">Gender</label>
                        <select
                            id="gender"
                            name="gender"
                            className="select"
                            value={form.gender}
                            onChange={handleChange}
                        >
                            <option value="">Select gender</option>
                            <option value="M">Male</option>
                            <option value="F">Female</option>
                        </select>
                    </div>
                    <InputField
                        id="phone"
                        label="Phone"
                        type="text"
                        placeholder="Your phone number"
                        value={form.phone}
                        className="input"
                        setValue={(val) => setForm({ ...form, phone: val })}
                    />
                    <InputField
                        id="address"
                        label="Address"
                        type="text"
                        placeholder="Your address"
                        value={form.address}
                        className="input"
                        setValue={(val) => setForm({ ...form, address: val })}
                    />
                    <div className="form-group">
                        <label htmlFor="medical_history_notes">Medical History Notes</label>
                        <textarea
                            id="medical_history_notes"
                            name="medical_history_notes"
                            className="textarea"
                            value={form.medical_history_notes}
                            onChange={handleChange}
                        />
                    </div>
                    <div style={{ display: "flex", gap: "0.75rem" }}>
                        <button type="submit" className="btn-primary">
                            Save Changes
                        </button>
                        <button
                            type="button"
                            className="btn-ghost"
                            onClick={() => { setEditing(false); setError(null); }}
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