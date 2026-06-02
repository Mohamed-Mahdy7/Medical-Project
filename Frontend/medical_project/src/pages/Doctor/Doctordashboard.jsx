import { Link, useNavigate } from "react-router-dom";
import { DoctorContext } from "../../context/DoctorContext";
import { Routes, Route } from "react-router-dom";
import { DoctorProvider } from "../../context/DoctorContext";
import { useContext, useState } from "react";
import { getSpecialties, getSpecialty } from "../../services/doctorservice";

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
    <div>
      <h1 style={{ textAlign: "center" }}>Doctor Dashboard</h1>
      <br />
      <div style={{ display: "flex", flexDirection: "row", gap: "10rem", justifyContent: "center" }}>
        <button
          className="btn-primary"
          onClick={() => setShowSpecialtyForm(true)}
        >
          + Add Specialty
        </button>

        {showSpecialtyForm && (
          <div className="overlay">
            <div className="modal"
              style={{
                position: "fixed",
                inset: 0,
                background: "rgba(0,0,0,0.4)",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
              }}
            >

              <form className="card" onSubmit={handleSubmit}>
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
                <button
                  type="submit"
                  className="btn-primary"
                  style={{ width: "45%", margin: "0px 5px" }}
                >
                  Save
                </button>
                <button
                  type="button"
                  className="btn-ghost"
                  style={{ width: "45%", margin: "0px 5px" }}
                  onClick={() => setShowSpecialtyForm(false)}
                >
                  Cancel
                </button>
              </form>
            </div>
          </div>
        )}

        <div>
          <Link to="/doctors/specialties/">
            <h3>Specialities</h3>
          </Link>
        </div>

        <div>
          <Link to="/doctors/me/">
            <h3>My Profile</h3>
          </Link>
        </div>

        <div>
          <Link to="/doctor/appointments">
            <h3>My Appointments</h3>
          </Link>
        </div>

        <div>
          <Link to="/availability">
          <h3>My Availability</h3>
          </Link>
        </div>
      </div>
    </div>
  );
}