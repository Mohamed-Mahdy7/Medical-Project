import { Link, useNavigate } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import "../styles/Navbar.css"

const Navbar = () => {
    const {logout} = useContext(AuthContext);
    const navigate = useNavigate();

    async function handleLogout() {
        await logout();
        navigate("/login")
    }

    return(
        <>
            <nav className="navbar">
                <div className="auth">
                    <Link to="register">Register</Link>
                    <Link to="login">Login</Link>
                    <button 
                        onClick={handleLogout}
                        className="btn-ghost"
                    >
                        Logout
                    </button>
                </div>
                <div className="pages">
                    <Link to="/">Home</Link>
                    <Link to="about">About</Link>
                    <Link to="doctors/dashboard">Doctors</Link>
                </div>
            </nav>
        </>
    );
}

export default Navbar