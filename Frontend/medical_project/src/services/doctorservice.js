 import api from "../api.js";

export const getDoctors = (data) =>
    api.post("/doctors/", data);
    api.get("/doctors/");
     

export const getDoctor = (data) =>
    api.post("/doctors/me/", data);
    api.get("/doctors/me/");

      

      

export const getDoctorSlots = (id) =>
    api.get(`/doctors/${id}/slots/`);

export const getSpecialties = () =>
    api.get("/doctors/specialties/");

export const getSpecialty = (id) =>
    api.get(`/doctors/specialties/${id}/`);