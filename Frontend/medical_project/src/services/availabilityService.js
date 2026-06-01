import api from '../api'; 

export const getAvailabilities = () => api.get('/availability/availability/');

export const createAvailability = (data) => api.post('/availability/availability/', data);

export const updateAvailability = (id, data) => api.put(`/availability/availability/${id}/`, data);

export const deleteAvailability = (id) => api.delete(`/availability/availability/${id}/`);