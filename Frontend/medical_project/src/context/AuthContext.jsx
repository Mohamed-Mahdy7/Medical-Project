import api from "../api.js";
import { createContext, useEffect, useState } from "react";
import {
    registerRequest,
    loginRequest,
    logoutRequest,
    meRequest
} from "../services/authService.js"


export const AuthContext = createContext();

export function AuthProvider({ children }) {

    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    async function checkAuth() {
        try {
            const response = await meRequest();
            setUser(response.data);
        } catch (error) {
            console.log(error);
            setUser(null);
        } finally {
            setLoading(false);
        }
    }


    async function register(
        username, email, first_name, last_name,
        password, confirm_password, role
    ) {
        console.log("role received:", role);
        console.log({
            username,
            email,
            first_name,
            last_name,
            password,
            role
        });
        try {
            await registerRequest({
                username, email, first_name, last_name,
                password, confirm_password, role
            });
            await login(username, password);
            return true;
        } catch (error) {
            console.error(error.response?.data);
            return false;
        }
    }

    async function login(username, password) {
        try {
            await loginRequest({
                username,
                password,
            });

            await checkAuth();
            return true;

        } catch (error) {
            console.error(error);
            return false;
        }
    }

    async function logout() {
        try{
            await logoutRequest();
        } finally {
            setUser(null);
        }
    }

    useEffect(() => {
        checkAuth();
    }, []);

    return (
        <AuthContext.Provider
            value={{
                user,
                loading,
                register,
                login,
                logout,
                isAuthenticated: !!user,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}