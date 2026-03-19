"use client"
import { userState } from "@/app/userdata";
import { useAtom } from "jotai";
import { redirect, RedirectType } from "next/navigation";

function UserLogin() {
  const [user, setUser] = useAtom(userState);

  if (!user.loggedIn) {
    redirect('/user/login', RedirectType.replace)
  }

  const handleSubmit = async (event: any) => {
    setUser({
        loggedIn: false,
        username: "",
        userID: -1
    });
  };

  return (
    <div className="flex flex-row justify-center">
        <form onSubmit={handleSubmit} className="flex flex-col gap-2">
            <h1>Logout</h1>
            <button type="submit" className="btn btn-primary">
                Log Out
            </button>
        </form>
    </div>
  );
}

export default UserLogin;