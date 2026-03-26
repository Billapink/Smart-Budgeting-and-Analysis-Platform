"use client"
import { useAtom } from "jotai";
import { userState } from "@/app/userdata";
import { redirect, RedirectType } from "next/navigation";
import { useState } from "react";

const LOGIN_ENDPOINT = "http://127.0.0.1:5000/login";

function UserLogin() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [status, setStatus] = useState("");
  const [user, setUser] = useAtom(userState);

  if (user?.loggedIn) {
    redirect(user.company ? '/' : '/user/select-company', RedirectType.replace)
  }

  const handleSubmit = async (event: any) => {
    setStatus("");
    event.preventDefault();
    const data = {username, password};
    const resp = await fetch(LOGIN_ENDPOINT, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify(data)
    });
    const blob = await resp.blob();
    console.log(await blob.text());
    if (resp.status !== 200) {
        setStatus(await blob.text());
    } else {
        setUser({
            loggedIn: true,
            username: username,
            userID: Number.parseInt(await blob.text())
        })
    }
  };

  return (
    <div className="flex flex-row justify-center">
        <form onSubmit={handleSubmit} className="flex flex-col gap-2">
            <h1>Login</h1>
            <label>Username
                <input type="text" onChange={(e) => setUsername(e.target.value)} value={username} />
            </label>
            <label>Password
                <input type="password" onChange={(e) => setPassword(e.target.value)} value={password} />
            </label>
            <button type="submit" disabled={!(username && password)}>
                Login
            </button>
            {status ? <h1>{status}</h1> : null}
        </form>
    </div>
  );
}

export default UserLogin;