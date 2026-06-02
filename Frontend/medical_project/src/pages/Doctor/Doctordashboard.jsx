import { Link } from "react-router-dom";
import DoctorProfile from "./Doctorprofile";
import { DoctorContext } from "../../context/doctorcontext";
import { Routes, Route } from "react-router-dom";
 import { useContext, useState } from "react";

<Routes>
  <Route path="profile/me" element={<DoctorProfile />} />
</Routes>
 
 

import { getSpecialties, getSpecialty } from "../../services/doctorservice";
export default function DoctorDashboard() {
    const [showSpecialtyForm, setShowSpecialtyForm] = useState(false);
      const { addspeciality } = useContext(DoctorContext);
      const [showModal, setShowModal] = useState(false);
      const [specialty, setSpecialty] = useState("");
      

      const handleSubmit = async (e) => {
        e.preventDefault();

  console.log("SPECIALTY VALUE =", specialty);
  const success = await addspeciality({
    name: specialty,  description: ""
    
  });

  if (success) {
    setSpecialty("");
    setShowSpecialtyForm(false);
  }

};
  return (
    <div>
     <h1 style={{ textAlign: "center" }}>Doctor Dashboard</h1> 
     <br />
      <div style={{ display: "flex", flexDirection: "row", gap: "10rem", justifyContent: "center" }}>
       <button
        onClick={() => setShowSpecialtyForm(true)}
      >
        + Add Specialty
      </button>

      {showSpecialtyForm && (
        <div className="overlay">
          <div className="modal"     style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0,0,0,0.4)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}>
            
        <form 
        onSubmit={handleSubmit}
        style={{
          border: "3px solid #0fa8df",
          background: "white",
          padding: "30px",
          borderRadius: "12px",
          minWidth: "350px",
          display: "flex",
          flexDirection: "column",
          gap: "15px",
        }}>
           <h2>Add Specialty</h2>
          <input
            type="text"
            name="specialty"

            placeholder="Enter specialty"
              value={specialty}
                onChange={(e) => setSpecialty(e.target.value)}
          />
          <button type="submit">
            Save
          </button>
          <button
            type="button"
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