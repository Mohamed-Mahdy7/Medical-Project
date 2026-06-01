 import { createContext, useEffect, useState } from "react";
import { getDoctor,createSpecialty } from "../services/doctorservice.js";

export const DoctorContext = createContext();

export function DoctorProvider({ children }) {
    const [doctor, setDoctor] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const token = localStorage.getItem("access");
 
        if (!token) {
            setLoading(false);
            return;
        }

        const fetchDoctor = async () => {
            try {
                const res = await getDoctor();
                setDoctor(res.data);
            } catch (err) {
                console.error("Failed to load doctor data", err);
                setDoctor(null);
            } finally {
                setLoading(false);
            }
        };

        fetchDoctor();
    }, []);
    async function addspeciality(data) { try {
        const res = await createSpecialty(data);
        console.log(res.data);
        return true;
    } catch (err) {
         console.log("Status:", err.response?.status);
        console.log("Data:", err.response?.data);
        console.error(err);
        return false;
        
        }
    }

    return (
        <DoctorContext.Provider value={{ doctor, loading, addspeciality }}>
            {children}
        </DoctorContext.Provider>
    );
}