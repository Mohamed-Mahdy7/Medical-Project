import { createContext, useEffect, useState} from "react";
import { loginRequest, logoutRequest, meRequest } from "../services/authService.js"

import api from "../api.js";

export const AuthContext = createContext();


export function AuthProvider({ children }) {

    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    async function checkAuth() {
        try {
            if (loading) {
                return <p>Loading...</p>;
            }
            const response = await meRequest();
            setUser(response.data);
        } catch {
            setUser(null);
        } finally {
            setLoading(false);
        }
    }

    async function login(username, password) {
        try{

            await loginRequest({
                    username,
                    password,
                });
            await checkAuth();
            return true;

        } catch (error) {
            return false;
        }
    }

    async function logout() {
        await logoutRequest();
    }

    useEffect(() => {
        checkAuth();
    }, []);

    return (
        <AuthContext.Provider
            value={{
                user,
                loading,
                login,
                logout,
                isAuthenticated: !!user,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}