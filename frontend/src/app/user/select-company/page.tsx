"use client"
import { userState } from "@/app/userdata";
import { useAtom } from "jotai";
import { redirect, RedirectType } from "next/navigation";
import { useEffect, useState } from "react";

const GET_MEMBERSHIPS_ENDPOINT = "http://127.0.0.1:5000/get_memberships";

function SelectCompany() {
  const [companyID, setCompanyID] = useState();
  const [memberships, setMemberships] = useState([]);
  const [user, setUser] = useAtom(userState);

  if (user && !user.loggedIn) {
    redirect('/user/login', RedirectType.replace)
  }

  const loadMemberships = async () => {
    if (!user.loggedIn) {
        return;
    }

    const params = new URLSearchParams();
    params.append("user_id", user.userID);
    const resp = await fetch(`${GET_MEMBERSHIPS_ENDPOINT}?${params}`, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "GET",
    });
    const blob = await resp.blob();
    const json = await blob.text();
    setMemberships(JSON.parse(json));
  };

  useEffect(() => {
    loadMemberships();
  }, [user])

  const handleSubmit = async (event: any) => {
    event.preventDefault();
    setUser({
        ...user, 
        company: companyID,
        companyName: memberships.find((m) => m.company_id == companyID)?.company_name
    })
  };

  return (
    <div className="flex flex-row justify-center">
        <form onSubmit={handleSubmit} className="flex flex-col gap-2">
            <h1>Join Company</h1>
            <select className="pr-8" onChange={(e) => setCompanyID(e.target.value)}>
                <option defaultValue="">-- SELECT COMPANY --</option>
                {
                    memberships.map((m) => (<option value={m.company_id} key={m.company_id}>
                        {m.company_name} ({m.role})
                    </option>))
                }
            </select>
            <button type="submit" disabled={!(companyID)}>
                Choose
            </button>
        </form>
    </div>
  );
}

export default SelectCompany;