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
        <p>
            <Link href="user/select-company" className="font-medium text-zinc-950">
                Select Company
            </Link>
        </p>
        <h2 className="text-lg my-2">Admin Routes</h2>
        <p>
            <Link href="admin/add_company" className="font-medium text-zinc-950">
                Add Company
            </Link>
        </p>
        <p>
            <Link href="categories/create" className="font-medium text-zinc-950">
                Add Category
            </Link>
        </p>
        <p>
            <Link href="categories/create-rule" className="font-medium text-zinc-950">
                Create Rule
            </Link>
        </p>
        <p>
            <Link href="categories/edit-rules" className="font-medium text-zinc-950">
                Edit Rules
            </Link>
        </p>
        <h2 className="text-lg my-2">Import Routes</h2>
        <p>
            <Link href="csvupload" className="font-medium text-zinc-950">
                Upload CSV File
            </Link>
        </p>
        <h2 className="text-lg my-2">Analytics Routes</h2>
        <p>
            <Link href="analytics/kpis" className="font-medium text-zinc-950">
                Show KPIs
            </Link>
        </p>
        <p>
            <Link href="analytics/trends" className="font-medium text-zinc-950">
                Show Trends
            </Link>
        </p>
        <p>
            <Link href="analytics/variance" className="font-medium text-zinc-950">
                Show Variances
            </Link>
        </p>
        <p>
            <Link href="analytics/forecast" className="font-medium text-zinc-950">
                Show Forecast
            </Link>
        </p>
        <p>
            <Link href="analytics/anomalies" className="font-medium text-zinc-950">
                Show Anomalies
            </Link>
        </p>
        <p>
            <Link href="analytics/set-budget" className="font-medium text-zinc-950">
                Set Budget
            </Link>
        </p>
    </div>
  );
}
