import Link from "next/link";

export default function Home() {
  return (
    <div>
        <h2 className="text-lg my-2">User Routes</h2>
        <p>
            <Link href="user/register" className="font-medium text-zinc-950">
                Register
            </Link>
        </p>
        <p>
            <Link href="user/join-company" className="font-medium text-zinc-950">
                Join Company
            </Link>
        </p>
        <h2 className="text-lg my-2">Admin Routes</h2>
        <p>
            <Link href="admin/add_company" className="font-medium text-zinc-950">
                Add Company
            </Link>
        </p>
        <h2 className="text-lg my-2">Import Routes</h2>
        <p>
            <Link href="csvupload" className="font-medium text-zinc-950">
                Upload CSV File
            </Link>
        </p>
    </div>
  );
}
