import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import InputField from "../components/accounts/InputFields";
import AdminButton from "../components/admin";

function Login() {
    const { login, checkAuth } = useContext(AuthContext);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    async function handleSubmit(e) {
        e.preventDefault();

        const success = await login(
            username,
            password
        );

        if (!success) {
            alert("Invalid credentials");
        }
        navigate("/doctor/list")
    };
    
    return (
        <main className="card" style={{width: "60%", alignSelf: "center"}}>
            <form  onSubmit={handleSubmit}>
                <div style={{ maxWidth: 420, margin: '4rem auto'}}>
                    <InputField 
                        id="username"
                        label="Username"
                        type="text"
                        placeholder="Your Username"
                        value={username}
                        className="input"
                        setValue={setUsername}
                    />
                    <InputField 
                        id="password"
                        label="Password"
                        type="password"
                        placeholder="••••••••"
                        className="input"
                        value={password}
                        setValue={setPassword}
                    />
                    <button className="btn-primary" style={{ width: "100%"}}>
                        Login
                    </button>
                </div>
            <AdminButton />
            </form>
        </main>
    );
}

export default Login