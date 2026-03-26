"use client"
import { userState } from "@/app/userdata";
import { useAtom } from "jotai";
import { redirect } from "next/navigation";
import { useEffect, useState } from "react";
import { formatDateForInput } from "../tools";

const GET_CATEGORIES_ENDPOINT = "http://127.0.0.1:5000/get_categories";
const GET_TRENDS_ENDPOINT = "http://127.0.0.1:5000/get_anomalies";

function ShowForecast() {
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState();
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const [status, setStatus] = useState("");
  const [anomalies, setAnomalies] = useState([]);
  const [user] = useAtom(userState);

//   if (user && !(user.loggedIn && user.company)) {
//     redirect('/user/login');
//   }

  console.log('KPIs', anomalies);
  
  const loadKPIs = async (event) => {
    event.preventDefault();
    if (!user) {
        return;
    }

    const params = new URLSearchParams();
    params.append("categoryID", selectedCategory.categoryID);
    params.append("start_date", formatDateForInput(startDate));
    params.append("end_date", formatDateForInput(endDate));
    const resp = await fetch(`${GET_TRENDS_ENDPOINT}?${params}`);
    const blob = await resp.blob();

    if (resp.status != 200) {
        setStatus(await blob.text());
        return;
    }
    
    const json = await blob.text()
    setAnomalies(JSON.parse(json));
    setStatus("");
  };

  const handleStartDateChange = (event) => {
    setStartDate(new Date(event.target.value))
  }

  const handleEndDateChange = (event) => {
    setEndDate(new Date(event.target.value))
  }


  const loadCategories = async () => {
    if (!user?.company ) {
        return;
    }

    const params = new URLSearchParams();
    params.append("companyID", user.company);
    const resp = await fetch(`${GET_CATEGORIES_ENDPOINT}?${params}`);
    const blob = await resp.blob();
    const json = await blob.text();
    setCategories(JSON.parse(json));
  };

  useEffect(() => {
    loadCategories();
  }, [user]);

  // if we haven't selected a category yet, we must do so first
  if (!selectedCategory) {
    console.log(categories)
    return (
        <div className="flex flex-row justify-center">
            <div className="flex flex-col gap-2">
            <h1>Select Category</h1>
                {categories.map((c) => (
                    <div className="flex flex-row justify-between" key={c.categoryID}>
                        <div>{c.category_name}</div>
                        <button className="btn" onClick={() => setSelectedCategory(c)}>Select</button>
                    </div>
                ))}
            </div>
        </div>
    );
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
                <button type="submit" className="btn btn-primary">
                    Show
                </button>
            </form>
            {status ? <h1>{status}</h1> : null}
            {anomalies.map((anom, i) => (<div key={i} className="border-b-1 border-b-gray-300 py-2">
                <p><strong>Date:</strong> {anom.month}</p>
                <p><strong>Total:</strong> {anom.total}</p>
                <p><strong>Deviation:</strong> {anom.deviation}</p>
                <p><strong>Score:</strong> {anom.score}</p>
            </div>))}
        </div>
    </div>
  );
}

export default ShowForecast;