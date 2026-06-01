import { Link } from "react-router-dom";
import DoctorProfile from "./Doctorprofile";
import { DoctorContext } from "../../context/DoctorContext";
import { Routes, Route } from "react-router-dom";
import { DoctorProvider } from "../../context/DoctorContext";
import { useContext, useState } from "react";
import { getSpecialties, getSpecialty } from "../../services/doctorservice";

export default function DoctorDashboard() {
  // const { addspeciality } = useContext(DoctorContext);
  const [showSpecialtyForm, setShowSpecialtyForm] = useState("false");
  // const [speciality, setSpeciality] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();

    const success = await addspeciality(data);

    if (!success) {
      alert("Error creating a Speciality");
    }
    
    navigate("/doctor/list")
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

              <form className="card">
                <h2>Add Specialty</h2>
                <input
                  type="text"
                  name="specialty"
                  value={"speciality"}
                  placeholder="Enter specialty"
                  className="input"
                  onChange={(e) => setSpeciality(e.target.value)}
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
          <Link to="/doctor/profile/me">
            My Profile
          </Link>
        </div>

        <div>
          <Link to="/doctor/appointments">
            My Appointments
          </Link>
        </div>

        <div>
          <Link to="/doctor/availability">
            My Availability
          </Link>
        </div>
      </div>
    </div>
  );
}