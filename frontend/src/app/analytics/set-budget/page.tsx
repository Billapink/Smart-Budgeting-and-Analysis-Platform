"use client"
import { userState } from "@/app/userdata";
import { useAtom } from "jotai";
import { redirect } from "next/navigation";
import { useEffect, useState } from "react";
import { formatDateForInput } from "../tools";

const GET_CATEGORIES_ENDPOINT = "http://127.0.0.1:5000/get_categories";
const SET_BUDGET_ENDPOINT = "http://127.0.0.1:5000/set_budget";

function SetBudget() {
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState();
  const [date, setDate] = useState(new Date());
  const [budget, setBudget] = useState(0.0);
  const [status, setStatus] = useState("");
  const [user] = useAtom(userState);

  if (user && !(user.loggedIn && user.company)) {
    redirect('/user/login');
  }

  const handleSubmit = async (event: any) => {
    setStatus("");
    event.preventDefault();

    const data = {
        userID: user.userID,
        categoryID: selectedCategory?.categoryID,
        date: formatDateForInput(date),
        budget: budget
    };
    const resp = await fetch(SET_BUDGET_ENDPOINT, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify(data)
    });
    const blob = await resp.blob();
    setStatus(resp.status === 200 ? "You have set a budget" : await blob.text());
  };

  const handleDateChange = (event) => {
    setDate(new Date(event.target.value))
  }

  const loadCategories = async () => {
    if (!user) {
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
  }, []);

  // if we haven't selected a category yet, we must do so first
  if (!selectedCategory) {
    console.log(categories)
    return (
        <div className="flex flex-row justify-center">
            <div className="flex flex-col gap-2">
            <h1>Select Category</h1>
                {categories.map((c) => (
                    <div className="flex flex-row justify-between">
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
        <form onSubmit={handleSubmit} className="flex flex-col gap-2">
            <h1>Set a Budget</h1>
            <h2>For category: {selectedCategory.category_name}</h2>
            <label>Date
                <input type="date" onChange={handleDateChange} value={formatDateForInput(date)} />
            </label>
            <label>Budget
                <input type="number" onChange={(e) => setBudget(e.target.value)} value={budget} />
            </label>
            <button type="submit" disabled={!(matchType && pattern && priority)} className="btn btn-primary">
                Set Budget
            </button>
            {status ? <h1>{status}</h1> : null}

            <button className="mt-8 btn" onClick={() => setSelectedCategory(undefined)}>Change Category</button>
        </form>
    </div>
  );
}

export default SetBudget;