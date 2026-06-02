import { DoctorContext } from "../../context/DoctorContext";
import { useContext } from "react";

function DoctorsSpecialities() {
    const {specialties } = useContext(DoctorContext);
    console.log("specialties =", specialties);
    
    return(
        <div>
            {specialties.map((s) => (
                <div key={s.id} 
                style={{display: "flex", justifyContent: "space-between"}}>
                    <p>Name: {s.name}</p>
                    { s.description &&
                        <p>Description: {s.description}</p>
                    }
                </div>
            ))}
            
        </div>
    )
}

export default DoctorsSpecialities