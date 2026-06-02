import { createContext, useEffect, useState } from "react";
import { 
    getDoctors,
    getDoctorProfile,
    getDoctorSlots,
    createSpecialty,
    getSpecialties,
    getSpecialty
} from "../services/doctorservice.js";

export const DoctorContext = createContext();

export function DoctorProvider({ children }) {
    const [doctors, setDoctors] = useState([]);
    const [doctorProfile, setDoctorProfile] = useState(null);
    const [specialties, setSpecialties] = useState([]);
    const [loading, setLoading] = useState(true);

    async function fetchDoctors() {
        const result = await getDoctors();
        setDoctors(result.data);
    }

    async function fetchDoctorProfile() {
        const result = await getDoctorProfile();
        setDoctorProfile(result.data);
    }

    async function fetchDoctorSlots(id) {
        const result = await getDoctorSlots(id);
        return result.data;
    }

    async function fetchSpecialities() {
        const result = await getSpecialties();
        console.log(result.data);
        console.log(Array.isArray(result.data));
        setSpecialties(result.data.results);
    }

    async function fetchSpeciality(id) {
        const result = await getSpecialty(id);
        return result.data;
    }

    async function addSpeciality(name, description) {
        try{
            const result = await createSpecialty(name, description);
            await fetchSpecialities();
            return result.data;
        } catch(error) {
            console.log(error)
            return null;
        }
    }
    
    useEffect(() => {
        async function init() {
            try{
                await Promise.all([
                    fetchDoctors(),
                    fetchDoctorProfile(),
                    fetchSpecialities(),
                ]);
            } catch (error) {
                console.log(error)
            } finally {
                setLoading(false);
            }
        }
        init();
    }, []);
    

    return (
        <DoctorContext.Provider 
            value={{
                doctors,
                doctorProfile,
                specialties,
                loading,
                fetchDoctors,
                fetchDoctorProfile,
                fetchDoctorSlots,
                fetchSpecialities,
                fetchSpeciality,
                addSpeciality, 
            }}>
        {children}
        </DoctorContext.Provider>
    );
}