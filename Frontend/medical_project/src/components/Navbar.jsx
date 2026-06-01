import { Link } from "react-router-dom";
import Home from "../pages/Home";
import About from "../pages/About";
import Login from "../pages/Login";
import Register from "../pages/Register";
import "../styles/Navbar.css"

const Navbar = () => {
    return(
        <>
            <nav className="navbar">
                <div className="auth">
                    <Link to="login">Login</Link>
                    <Link to="register">Register</Link>
                </div>
                <div className="pages">
                    <Link to="/">Home</Link>
                    <Link to="about">About</Link>
                </div>
            </nav>
        </>
    );
}

export default Navbar