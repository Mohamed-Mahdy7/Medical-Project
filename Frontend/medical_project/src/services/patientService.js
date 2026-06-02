import api from "../api";

export const getPatientProfile = () =>
    api.get("/patients/me/");

export const updatePatientProfile = (data) =>
    api.put("/patients/me/", data);


export const getAppointments = (filters = {}) => {
    const params = new URLSearchParams();
    if (filters.status) params.append("status", filters.status);
    if (filters.type) params.append("type", filters.type);
    return api.get(`/appointments/?${params.toString()}`);
};

export const getAppointment = (id) =>
    api.get(`/appointments/${id}/`);

export const createAppointment = (data) =>
    api.post("/appointments/", data);

export const cancelAppointment = (id) =>
    api.post(`/appointments/${id}/`, { status: "CANCELLED" });

export const rescheduleAppointment = (id, start_time) =>
    api.post(`/appointments/${id}/reschedule/`, { start_time });


export const getDoctors = (filters = {}) => {
    const params = new URLSearchParams();
    if (filters.specialty) params.append("specialty", filters.specialty);
    if (filters.name) params.append("name", filters.name);
    return api.get(`/doctors/?${params.toString()}`);
};

export const getDoctor = (id) =>
    api.get(`/doctors/${id}/`);

export const getDoctorSlots = (id, date) =>
    api.get(`/doctors/${id}/slots/?date=${date}`);