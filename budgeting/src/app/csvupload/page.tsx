"use client"
import { useState } from "react";

const UPLOAD_ENDPOINT = "http://127.0.0.1:8000/api/orders/vendor/register/";

function VendorRegistration() {
  const [file, setFile] = useState<File>();
  const [name, setName] = useState("");
  const [status, setStatus] = useState("");

  const handleSubmit = async (event: any) => {
    setStatus("");
    event.preventDefault();
    const data = {csv: await file!.text()};
    const resp = await fetch(UPLOAD_ENDPOINT, {
        method: "POST",
        body: JSON.stringify(data)
    });
    setStatus(resp.status === 200 ? "Thank you!" : "Error.");
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
        <main className="flex min-h-screen w-full max-w-3xl flex-col items-center justify-between py-32 px-16 bg-white dark:bg-black sm:items-start">
            <div className="flex flex-col items-center gap-6 text-center sm:items-start sm:text-left">
                <h1 className="max-w-xs text-3xl font-semibold leading-10 tracking-tight text-black dark:text-zinc-50">
                    Smart Budgeting and Analysis App
                </h1>

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
        </main>
    </div>
  );
}

export default VendorRegistration;