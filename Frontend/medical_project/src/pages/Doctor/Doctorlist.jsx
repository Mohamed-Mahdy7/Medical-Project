import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getDoctors } from  "../../services/doctorservice";

export default function DoctorsList() {
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDoctors();
  }, []);

  const fetchDoctors = async () => {
    try {
      const res = await getDoctors();

       
      setDoctors(res.data.data || res.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <h2>Loading Doctors...</h2>;
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>Doctors</h1>

      {doctors.length === 0 ? (
        <p>No Doctors Found</p>
      ) : (
        doctors.map((doctor) => (
          <div
            key={doctor.id}
            style={{
              border: "1px solid #ccc",
              padding: "15px",
              marginBottom: "10px",
              borderRadius: "8px",
            }}
          >
            <h3>
              {doctor.user_name || `Doctor #${doctor.id}`}
            </h3>

            <p>
              <strong>Specialty:</strong>{" "}
              {doctor.specialty_name || "Not Assigned"}
            </p>

            <p>
              <strong>Experience:</strong>{" "}
              {doctor.years_of_experience} years
            </p>

            <Link to={`/doctors/${doctor.id}`}>
              View Details
            </Link>
          </div>
        ))
      )}
    </div>
  );
}