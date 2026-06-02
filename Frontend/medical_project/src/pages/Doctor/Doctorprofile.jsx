import { useEffect, useState, useContext } from "react";
import { getDoctors } from "../../services/doctorservice";
import { DoctorContext, DoctorProvider } from "../../context/DoctorContext";


export default function DoctorProfile() {
  const { doctorProfile, loading } = useContext(DoctorContext);

  if (loading) return <p>Loading...</p>;

  if (!doctorProfile) {
    return <p>Profile not created yet!</p>
  }

  console.log(doctorProfile)
  return (
    <div style={{ padding: "20px" }}>
      <h1>Doctor Profile</h1>

      <div style={{ marginTop: "20px" }}>
        <h2>
          Dr. {doctorProfile.user.first_name} {doctorProfile.user.last_name}
        </h2>
        <p>
          <b>Specialty:</b> 
          {doctorProfile.specialty?.name}
        </p>
        <p>
          <b>Profile Picture:</b> 
          {doctorProfile.profile_picture}
        </p>
        <p>
          <b>Phone:</b> 
          {doctorProfile.phone}
        </p>
        <p>
          <b>Bio:</b> 
          {doctorProfile.bio}
        </p>
        <p>
          <b>Experience:</b> 
          {doctorProfile.years_of_experience} years
        </p>
      </div>
    </div>
  );
}
