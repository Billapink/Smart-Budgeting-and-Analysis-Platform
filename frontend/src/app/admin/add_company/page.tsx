"use client"
import { userState } from "@/app/userdata";
import { useAtom } from "jotai";
import { redirect } from "next/navigation";
import { useState } from "react";

const ADD_COMPANY_ENDPOINT = "http://127.0.0.1:5000/create_company";

function AddCompany() {
  const [companyName, setCompanyName] = useState("");
  const [status, setStatus] = useState("");
  const [user] = useAtom(userState);

  if (user && !user.userID) {
    redirect('/user/login');
  }

  const handleSubmit = async (event: any) => {
    setStatus("");
    event.preventDefault();
    const data = {userID: user.userID, company: companyName};
    const resp = await fetch(ADD_COMPANY_ENDPOINT, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify(data)
    });
    const blob = await resp.blob();
    setStatus(resp.status === 200 ? "You have added a company" : await blob.text());
  };

  return (
    <div className="flex flex-row justify-center">
        <form onSubmit={handleSubmit} className="flex flex-col gap-2">
            <h1>Create a Company</h1>
            <label>Company Name
                <input type="text" onChange={(e) => setCompanyName(e.target.value)} value={companyName} />
            </label>
            <button type="submit" disabled={!companyName} className="btn btn-primary">
                Add
            </button>
            {status ? <h1>{status}</h1> : null}
        </form>
    </div>
  );
}

export default AddCompany;