import { useContext, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import InputField from "../components/accounts/InputFields";

function Register() {
    const { register } = useContext(AuthContext)
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [first_name, setFirstName] = useState("");
    const [last_name, setLastName] = useState("");
    const [password, setPassword] = useState("");
    const [confirm_password, setConfirmPassword] = useState("");
    const [role, setRole] = useState("");

    async function handleSubmit(e) {
        e.preventDefault();

        console.log("role received:", role);
        const success = await register(
            username, email, first_name,  last_name, 
            password, confirm_password, role
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
                    id="email"
                    label="Email"
                    type="email"
                    placeholder="Your Email"
                    value={email}
                    className="input"
                    setValue={setEmail}
                />
                <InputField 
                    id="first_name"
                    label="First Name"
                    type="text"
                    placeholder="Your First Name"
                    value={first_name}
                    className="input"
                    setValue={setFirstName}
                />
                <InputField 
                    id="last_name"
                    label="Last name"
                    type="text"
                    placeholder="Your Last Name"
                    value={last_name}
                    className="input"
                    setValue={setLastName}
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
                <InputField 
                    id="confirm_password"
                    label="Confirm Password"
                    type="password"
                    placeholder="••••••••"
                    className="input"
                    value={confirm_password}
                    setValue={setConfirmPassword}
                />
                <select 
                    name="role" 
                    id="role" 
                    value={role} 
                    onChange={(e) => setRole(e.target.value)}
                >
                    <option value="">Select a role</option>
                    <option value="D">Doctor</option>
                    <option value="P">Patient</option>
                </select>
                <button className="btn-primary" style={{ width: "100%"}}>
                    Register
                </button>
            </div>
        </form>
    )

}

export default Register