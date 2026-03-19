"use client";
import { useAtom } from "jotai";
import { userState } from "./userdata";
import Link from "next/link";

export default function Header() {
    const [user] = useAtom(userState);
    return (
        <div className="flex flex-row justify-between text-white bg-gray-900 p-4">
            <div><Link href="/" className="btn">Smart Budgeting and Analysis Platform</Link></div>
            <div>
                {user.loggedIn ? (<>
                    {user.username}
                    <Link href="/user/logout" className="btn pl-8">Logout</Link>
                </>) : (
                    <Link href="/user/login" className="btn">Login</Link>
                )}
            </div>
        </div>
    );
}