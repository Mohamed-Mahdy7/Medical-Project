import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getDoctor } from "../../services/doctorservice";  

export default function DoctorProfile() {
  
  const [doctor, setDoctor] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    
    const fetchDoctor = async () => {
      try {
        setLoading(true);
        const res = await getDoctor();
        setDoctor(res.data);
      } catch (err) {
        setError("Failed to load doctor profile");
      } finally {
        setLoading(false);
      }
    };

    fetchDoctor();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;
  if (!doctor) return <p>No doctor found</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h2>Doctor Profile</h2>

      <div style={{ marginTop: "20px" }}>
        <h3>Dr. {doctor.id}</h3>
        <p><b>Specialty:</b> {doctor.specialty}</p>
        <p><b>Email:</b> {doctor.profile_picture}</p>
        <p><b>Phone:</b> {doctor.phone}</p>
        <p><b>Bio:</b> {doctor.bio}</p>
        <p><b>Experience:</b> {doctor.years_of_experience} years</p>
      </div>
    </div>
  );
}
 