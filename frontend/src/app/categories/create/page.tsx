"use client"
import { userState } from "@/app/userdata";
import { useAtom } from "jotai";
import { redirect } from "next/navigation";
import { useState } from "react";

const ADD_CATEGORY_ENDPOINT = "http://127.0.0.1:5000/create_category";

function CreateCategory() {
  const [categoryName, setCategoryName] = useState("");
  const [categoryType, setCategoryType] = useState("");
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
        category: categoryName,
        type: categoryType
    };
    const resp = await fetch(ADD_CATEGORY_ENDPOINT, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify(data)
    });
    const blob = await resp.blob();
    setStatus(resp.status === 200 ? "You have created a category" : await blob.text());
  };

  return (
    <div className="flex flex-row justify-center">
        <form onSubmit={handleSubmit} className="flex flex-col gap-2">
            <h1>Create a Category</h1>
            <label>Category Name
                <input type="text" onChange={(e) => setCategoryName(e.target.value)} value={categoryName} />
            </label>
            <label>Category Type
                <input type="text" onChange={(e) => setCategoryType(e.target.value)} value={categoryType} />
            </label>
            <button type="submit" disabled={!categoryName} className="btn btn-primary">
                Create
            </button>
            {status ? <h1>{status}</h1> : null}
        </form>
    </div>
  );
}

export default CreateCategory;