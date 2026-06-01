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
    async function addspeciality(data) {
        try { await createSpecialty(data); return true; } 
        
        catch (err) {
            console.error("Failed to create specialty", err);
            return false;
        }
    }

    return (
        <DoctorContext.Provider value={{ doctor, loading }}>
            {children}
        </DoctorContext.Provider>
    );
}