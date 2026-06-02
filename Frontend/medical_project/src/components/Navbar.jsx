import { Link, useNavigate } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import "../styles/Navbar.css"

const Navbar = () => {
    const {user, logout} = useContext(AuthContext);
    const navigate = useNavigate();

    async function handleLogout() {
        await logout();
        navigate("/login")
    }

    return(
        <>
            <nav className="navbar">
                <div className="auth">
                    {!user ? (
                        <span>
                            <Link to="/register">Register</Link>
                            <Link to="/login">Login</Link>
                        </span>
                    ) : (
                        <span>
                            {user.role === "D" && (
                                <Link to="/doctors/me">Profile</Link>
                            )}

                            {user.role === "P" && (
                                <Link to="/patient/profile">Profile</Link>
                            )}

                            <button onClick={handleLogout} className="btn-ghost">
                                Logout
                            </button>
                        </span>
                    )}
                </div>
                <div className="pages">
                    <Link to="/">Home</Link>
                    <Link to="about">About</Link>
                    {user && (
                        <>
                            {user.role === "D" && (
                                <Link to="/doctors/dashboard">Doctors</Link>
                            )}

                            {user.role === "P" && (
                                <Link to="/doctor/list">Doctors</Link>
                            )}
                        </>
                    )}
                </div>
            </nav>
        </>
    );
}

export default Navbar