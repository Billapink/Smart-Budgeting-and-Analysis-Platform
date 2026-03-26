"use client"
import { useState } from "react";

const REGISTER_ENDPOINT = "http://127.0.0.1:5000/register";

function UserRegistration() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [status, setStatus] = useState("");

  const handleSubmit = async (event: any) => {
    setStatus("");
    event.preventDefault();
    const data = {username, password};
    const resp = await fetch(REGISTER_ENDPOINT, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify(data)
    });
    const blob = await resp.blob();
    setStatus(resp.status === 200 ? "You have been registered" : await blob.text());
  };

  return (
    <div className="flex flex-row justify-center">
        <form onSubmit={handleSubmit} className="flex flex-col gap-2">
            <h1>Register</h1>
            <label>Username
                <input type="text" onChange={(e) => setUsername(e.target.value)} value={username} />
            </label>
            <label>Password
                <input type="password" onChange={(e) => setPassword(e.target.value)} value={password} />
            </label>
            <button type="submit" disabled={!(username && password)}>
                Register
            </button>
            {status ? <h1>{status}</h1> : null}
        </form>
    </div>
  );
}

export default UserRegistration;