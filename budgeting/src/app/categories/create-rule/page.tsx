"use client"
import { userState } from "@/app/userdata";
import { useAtom } from "jotai";
import { redirect } from "next/navigation";
import { useEffect, useState } from "react";

const GET_CATEGORIES_ENDPOINT = "http://127.0.0.1:5000/get_categories";
const ADD_RULE_ENDPOINT = "http://127.0.0.1:5000/create_rule";

function CreateCategory() {
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState();
  const [matchType, setMatchType] = useState("exact");
  const [pattern, setPattern] = useState("");
  const [priority, setPriority] = useState("1");
  const [status, setStatus] = useState("");
  const [user] = useAtom(userState);

  if (user && !(user.loggedIn && user.company)) {
    redirect('/user/login');
  }

  const handleSubmit = async (event: any) => {
    setStatus("");
    event.preventDefault();

    const data = {
        companyID: user.company,
        categoryID: selectedCategory?.categoryID,
        matchType: matchType,
        pattern: pattern,
        priority: priority
    };
    const resp = await fetch(ADD_RULE_ENDPOINT, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify(data)
    });
    const blob = await resp.blob();
    setStatus(resp.status === 200 ? "You have created a rule" : await blob.text());
  };

  const loadCategories = async () => {
    if (!user) {
        return;
    }

    const params = new URLSearchParams();
    params.append("companyID", user.company);
    const resp = await fetch(`${GET_CATEGORIES_ENDPOINT}?${params}`, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "GET",
    });
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
            <h1>Create a Rule</h1>
            <h2>For category: {selectedCategory.category_name}</h2>
            <label>Match Type
                <select onChange={(e) => setMatchType(e.target.value)} value={matchType}>
                    <option value="exact">Exact</option>
                    <option value="regex">Regular Expression</option>
                </select>
            </label>
            <label>Pattern
                <input type="text" onChange={(e) => setPattern(e.target.value)} value={pattern} />
            </label>
            <label>Priority
                <input type="number" min="1" max="10" onChange={(e) => setPriority(e.target.value)} value={priority} />
            </label>
            <button type="submit" disabled={!(matchType && pattern && priority)} className="btn btn-primary">
                Create
            </button>
            {status ? <h1>{status}</h1> : null}

            <button className="mt-8 btn" onClick={() => setSelectedCategory(undefined)}>Change Category</button>
        </form>
    </div>
  );
}

export default CreateCategory;