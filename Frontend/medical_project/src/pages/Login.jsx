import { useContext, useState } from "react";
import { AuthContext } from "../context/AuthContext";

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
                <div className="page-header">
                    <h2>Log in</h2>
                    <p>Welcome back to the medical portal</p>
                </div>
                <div className="my-2">
                    <label htmlFor="username">Username</label>
                    <input
                        id="username"
                        type="text"
                        placeholder="Your Username"
                        value={username}
                        className="input w-100"
                        onChange={(e) =>
                            setUsername(e.target.value)
                        }
                    />
                </div>
                <div className="my-2 mb-4">
                    <label htmlFor="password">Password</label>
                    <input
                        id="password"
                        type="password"
                        placeholder="••••••••"
                        className="input w-100"
                        value={password}
                        onChange={(e) =>
                            setPassword(e.target.value)
                        }
                    />
                </div>
                <button className="btn-primary" style={{ width: "100%"}}>
                    Login
                </button>
            </div>
        </form>
    );
}

export default Login