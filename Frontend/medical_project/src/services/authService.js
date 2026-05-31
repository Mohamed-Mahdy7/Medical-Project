import api from "../api";

export const registerRequest = (data) =>
    api.post("/accounts/user/", data);

export const loginRequest = (data) =>
    api.post("/accounts/login/", data);

export const logoutRequest = () =>
    api.post("/accounts/logout/");

export const meRequest = () =>
    api.get("/accounts/user/me/");