"use client"
import { userState } from "@/app/userdata";
import { useAtom } from "jotai";
import { redirect } from "next/navigation";
import { useState } from "react";
import { formatDateForInput } from "../tools";

const GET_KPIS_ENDPOINT = "http://127.0.0.1:5000/get_kpis";

function ShowKPIs() {
  const [startDate, setStartDate] = useState(new Date());
  const [status, setStatus] = useState("");
  const [kpis, setKPIs] = useState();
  const [user] = useAtom(userState);

//   if (user && !(user.loggedIn && user.company)) {
//     redirect('/user/login');
//   }

  console.log('KPIs', kpis);
  
  const loadKPIs = async (event) => {
    event.preventDefault();
    if (!user) {
        return;
    }

    const params = new URLSearchParams();
    params.append("companyID", user.company);
    params.append("date", formatDateForInput(startDate));
    const resp = await fetch(`${GET_KPIS_ENDPOINT}?${params}`);
    const blob = await resp.blob();

    if (resp.status != 200) {
        setStatus(await blob.text());
        return;
    }

    const json = await blob.text();
    setKPIs(JSON.parse(json));
    setStatus("");
  };

  const handleDateChange = (event) => {
    console.log(event.target.value);
    setStartDate(new Date(event.target.value))
  }

  return (
    <div className="flex flex-row justify-center">
        <div className="flex flex-col gap-2">
            <form onSubmit={loadKPIs} className="flex flex-col gap-2">
                <h1>Show KPIs</h1>
                <label>Choose Date
                    <input type="date" onChange={handleDateChange} value={formatDateForInput(startDate)} />
                </label>
                <button type="submit" className="btn btn-primary">
                    Show
                </button>
            </form>
            {status ? <h1>{status}</h1> : null}
            {kpis && (<>
                <p><strong>Revenue:</strong> {kpis.Revenue}</p>
                <p><strong>GrossProfit:</strong> {kpis.GrossProfit}</p>
                <p><strong>GrossProfitMargin:</strong> {kpis.GrossProfitMargin}</p>
                <p><strong>NetProfit:</strong> {kpis.NetProfit}</p>
                <p><strong>NetProfitMargin:</strong> {kpis.NetProfitMargin}</p>
                <p><strong>COGS:</strong> {kpis.COGS}</p>
            </>)}
        </div>
    </div>
  );
}

export default ShowKPIs;