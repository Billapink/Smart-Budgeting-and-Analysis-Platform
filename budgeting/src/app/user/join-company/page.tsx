"use client"
import { userState } from "@/app/userdata";
import { useAtom } from "jotai";
import { useState } from "react";

const REGISTER_ENDPOINT = "http://127.0.0.1:5000/join_company";

function JoinCompany() {
  const [companyID, setCompanyID] = useState("");
  const [role, setRole] = useState("");
  const [code, setCode] = useState("");
  const [status, setStatus] = useState("");
  const [user] = useAtom(userState);

  if (user && !user.userID) {
    redirect('/user/login');
  }

  const handleSubmit = async (event: any) => {
    setStatus("");
    event.preventDefault();
    const data = {
        user_id:  user.userID,
        company_id: companyID,
        role: role,
        code_input: code
    };
    const resp = await fetch(REGISTER_ENDPOINT, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify(data)
    });
    const blob = await resp.blob();
    setStatus(resp.status === 200 ? "You have joined the company" : await blob.text());
  };

  return (
    <div className="flex flex-row justify-center">
        <form onSubmit={handleSubmit} className="flex flex-col gap-2">
            <h1>Join Company</h1>
            <label>Company ID
                <input type="text" onChange={(e) => setCompanyID(e.target.value)} value={companyID} />
            </label>
            <label>Role
                <input type="text" onChange={(e) => setRole(e.target.value)} value={role} />
            </label>
            <label>Company Code (secret)
                <input type="password" onChange={(e) => setCode(e.target.value)} value={code} />
            </label>
            <button type="submit" disabled={!(companyID && role)}>
                Join
            </button>
            {status ? <h1>{status}</h1> : null}
        </form>
    </div>
  );
}

export default JoinCompany;