"use client"
import { useState } from "react";
import { userState } from "../userdata";
import { useAtom } from "jotai";
import { redirect } from "next/navigation";

const UPLOAD_ENDPOINT = "http://127.0.0.1:5000/import_csv";

function VendorRegistration() {
  const [file, setFile] = useState<File>();
  const [name, setName] = useState("");
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
        csv: await file!.text(),
    };
    console.log('DATA', data)
    const resp = await fetch(UPLOAD_ENDPOINT, {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    const text = await resp.text()
    setStatus(resp.status === 200 ? "Thank you!" : `${text}`);
  };

  return (
    <div className="flex flex-row justify-center">
        <form onSubmit={handleSubmit} className="flex flex-col gap-2">
            <h1>React File Upload</h1>
            <input type="file" onChange={(e) => setFile(e.target.files![0])} 
                className="text-sm text-stone-500 file:mr-5 file:py-1 file:px-3 file:border-1
                    file:text-xs file:font-medium
                    file:bg-stone-50 file:text-stone-700
                    hover:file:cursor-pointer hover:file:bg-blue-50
                    hover:file:text-blue-700"
            />
            <input type="text" onChange={(e) => setName(e.target.value)} value={name} />
            <button type="submit" disabled={!(file && name)}>
                Upload File
            </button>
            {status ? <h1>{status}</h1> : null}
        </form>
    </div>
  );
}

export default VendorRegistration;