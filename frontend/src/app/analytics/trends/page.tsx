"use client"
import { userState } from "@/app/userdata";
import { useAtom } from "jotai";
import { redirect } from "next/navigation";
import { useState } from "react";
import { formatDateForInput } from "../tools";
import Plot from 'react-plotly.js'

const GET_TRENDS_ENDPOINT = "http://127.0.0.1:5000/get_trends";

function ShowTrends() {
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const [status, setStatus] = useState("");
  const [kpiChoice, setKPIChoice] = useState("GrossProfit");
  const [loadedKPI, setLoadedKPI] = useState("");
  const [kpis, setKPIs] = useState([]);
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
    params.append("start_date", formatDateForInput(startDate));
    params.append("end_date", formatDateForInput(endDate));
    params.append("kpi", kpiChoice);
    const resp = await fetch(`${GET_TRENDS_ENDPOINT}?${params}`);
    const blob = await resp.blob();

    if (resp.status != 200) {
        setStatus(await blob.text());
        return;
    }
    
    const json = await blob.text();
    setKPIs(JSON.parse(json));
    setLoadedKPI(kpiChoice);
    setStatus("");
  };

  const handleStartDateChange = (event) => {
    setStartDate(new Date(event.target.value))
  }

  const handleEndDateChange = (event) => {
    setEndDate(new Date(event.target.value))
  }

  return (
    <div className="flex flex-row justify-center">
        <div className="flex flex-col gap-2">
            <form onSubmit={loadKPIs} className="flex flex-col gap-2">
                <h1>Show Trends</h1>
                <label>Start Date
                    <input type="date" onChange={handleStartDateChange} value={formatDateForInput(startDate)} />
                </label>
                <label>End Date
                    <input type="date" onChange={handleEndDateChange} value={formatDateForInput(endDate)} />
                </label>
                <label>KPI
                    <select value={kpiChoice} onChange={(e) => setKPIChoice(e.target.value)}>
                        <option value="Revenue">Revenue</option>
                        <option value="GrossProfit">GrossProfit</option>
                        <option value="GrossProfitMargin">GrossProfitMargin</option>
                        <option value="NetProfit">NetProfit</option>
                        <option value="NetProfitMargin">NetProfitMargin</option>
                        <option value="COGS">COGS</option>
                    </select>
                </label>
                <button type="submit" className="btn btn-primary">
                    Show
                </button>
            </form>
            {status ? <h1>{status}</h1> : null}
            {kpis.length > 0 && (
                <Plot 
                    data={[
                        {
                            x: kpis.map((data) => data.month),
                            y: kpis.map((data) => data.kpi),
                            type: 'scatter',
                            mode: 'lines+markers',
                            marker: {color: 'red'},
                        },
                    ]}
                    layout={ {width: 800, height: 600, title: {text: loadedKPI}} }
                />
            )}
        </div>
    </div>
  );
}

export default ShowTrends;