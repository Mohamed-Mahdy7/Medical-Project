import { Link, useNavigate } from "react-router-dom";
import { DoctorContext } from "../../context/DoctorContext";
import { Routes, Route } from "react-router-dom";
import { DoctorProvider } from "../../context/DoctorContext";
import { useContext, useState } from "react";
import { getSpecialties, getSpecialty } from "../../services/doctorservice";
import "../../styles/DoctorDashboard.css"

export default function DoctorDashboard() {
  const { addSpeciality, specialties } = useContext(DoctorContext);
  const [showSpecialtyForm, setShowSpecialtyForm] = useState(false);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();

    const success = await addSpeciality(name, description);

    if (!success) {
      alert("Error creating a Speciality");
      return;
    }
    
    navigate("/doctors/specialties/")
  };
  return (
    <div className="page">
      <div className="page-header">
          <h1>Doctor Dashboard</h1>
          <p>
              Manage your profile, appointments, availability and specialties.
          </p>
      </div>      
      <br className="divider"/>
      <div style={{ marginBottom: "1rem" }}>
        <button
          className="btn-primary"
          style={{width: "100%"}}
          onClick={() => setShowSpecialtyForm(true)}
        >
          + Add Specialty
        </button>
      </div>

      {showSpecialtyForm && (
        <div className="overlay">
          <div className="modal-backdrop">
            <form className="card  modal-card" onSubmit={handleSubmit}>
              <h2>Add Specialty</h2>
              <input
                type="text"
                name="specialty"
                value={name}
                placeholder="Enter specialty"
                className="input"
                onChange={(e) => setName(e.target.value)}
              />
              <textarea
                name="description"
                value={description}
                placeholder="Enter description"
                className="input"
                onChange={(e) => setDescription(e.target.value)}
              />
              <div className="modal-actions">
                <button type="submit" className="btn-primary">
                  Save
                </button>
                <button
                  type="button"
                  className="btn-ghost"
                  onClick={() => setShowSpecialtyForm(false)}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
      <div id="main">
        <section className="doctor-grid">
          <Link to="/doctors/specialties/">
            <div className="card doctor-card">
                <h3 className="titile">Specialities</h3>
            </div>
          </Link>

          <Link to="/doctors/me/">
            <div className="card doctor-card">
                <h3>My Profile</h3>
            </div>
          </Link>
        </section>
        <section>
          <Link to="/doctor/appointments">
            <div className="card doctor-card">
                <h3>My Appointments</h3>
            </div>
          </Link>

          <Link to="/availability">
            <div className="card doctor-card">
              <h3>My Availability</h3>
            </div>
          </Link>
        </section>
      </div>
    </div>
  );
}