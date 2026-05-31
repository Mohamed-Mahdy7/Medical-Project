import { Link } from "react-router-dom";
import DoctorProfile from "./Doctorprofile";
import { Routes, Route } from "react-router-dom";

<Routes>
  <Route path="profile/:id" element={<DoctorProfile />} />
</Routes>
 
 
import { useState } from "react";
export default function DoctorDashboard() {
    const [showSpecialtyForm, setShowSpecialtyForm] = useState(false);
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
        <form>
          <input
            type="text"
            name="specialty"
            placeholder="Enter specialty"
          />
          <button type="submit">
            Save
          </button>
        </form>
      )}

      <div>
        <Link to="/doctor/profile/1">
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