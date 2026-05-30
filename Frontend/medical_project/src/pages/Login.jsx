import { useContext, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import InputField from "../components/accounts/InputFields";

function Login() {
    const { login } = useContext(AuthContext);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    async function handleSubmit(e) {
        e.preventDefault();

        const success = await login(
            username,
            password
        );

        if (!success) {
            alert("Invalid credentials");
        }
    }

    return (
        <form onSubmit={handleSubmit}>
            <div className="card" style={{ maxWidth: 420, margin: '4rem auto'}}>
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
        </form>
    );
}

export default Login