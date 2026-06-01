import api from "../api";

export const getAppointments = () => {
    return api.get("/appointments/");
};

export const getUpcomingAppointments = () => {
    return api.get("/appointments/?type=upcoming");
};

export const getPastAppointments = () => {
    return api.get("/appointments/?type=past");
};

export const updateAppointment = (id, data) => {
    return api.patch(`/appointments/${id}/`, data);
};

export const rescheduleAppointment = (id, start_time) => {
    return api.patch(
        `/appointments/${id}/reschedule/`,
        { start_time }
    );
};