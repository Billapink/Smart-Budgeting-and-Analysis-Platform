"use client"
import { userState } from "@/app/userdata";
import { useAtom } from "jotai";
import { redirect } from "next/navigation";
import { ChangeEvent, useEffect, useState } from "react";

const GET_RULES_ENDPOINT = "http://127.0.0.1:5000/get_rules";
const SET_RULE_ACTIVE_ENDPOINT = "http://127.0.0.1:5000/set_rule_active";
const UPDATE_RULE_PRIORITY_ENDPOINT = "http://127.0.0.1:5000/update_rule_priority";

function EditRules() {
  const [rules, setRules] = useState([]);
  const [status, setStatus] = useState("");
  const [user] = useAtom(userState);

  console.log('RULES', rules);
  if (user && !(user.loggedIn && user.company)) {
    redirect('/user/login');
  }

  const handleActiveChange = async (event: ChangeEvent<HTMLInputElement>, ruleID: number) => {
    const isActive = event.target.checked;
    setRules(oldRules => oldRules.map((rule) => (
        rule.ruleID === ruleID 
            ? {...rule, active: isActive}
            : rule 
    )));
    const data = {
        ruleID: ruleID,
        active: isActive
    };
    const resp = await fetch(SET_RULE_ACTIVE_ENDPOINT, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify(data)
    });
    const blob = await resp.blob();
    setStatus(resp.status === 200 ? "Rule active status has been updated" : await blob.text());

  };

  const handlePriorityChange = async (event: ChangeEvent<HTMLInputElement>, ruleID: number) => {
    const priority = event.target.value;
    setRules(oldRules => oldRules.map((rule) => (
        rule.ruleID === ruleID 
            ? {...rule, priority: priority}
            : rule 
    )));
    const data = {
        ruleID: ruleID,
        priority: priority
    };
    const resp = await fetch(UPDATE_RULE_PRIORITY_ENDPOINT, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify(data)
    });
    const blob = await resp.blob();
    setStatus(resp.status === 200 ? "Rule priority has been updated" : await blob.text());

  };
  const loadRules = async () => {
    if (!user) {
        return;
    }

    const params = new URLSearchParams();
    params.append("companyID", user.company);
    const resp = await fetch(`${GET_RULES_ENDPOINT}?${params}`);
    const blob = await resp.blob();
    const json = await blob.text();
    setRules(JSON.parse(json));
  };
  
  useEffect(() => {
    loadRules();
  }, []);


  return (
    <div className="flex flex-row justify-center">
        <form className="flex flex-col gap-2">
            <h1>Edit Rules</h1>
            {
                rules.map(rule => (
                    <div className="flex flex-row w-full" key={rule.ruleID}>
                        <div className="w-3/4">{rule.pattern}</div>
                        <div className="w-1/8"><input type="checkbox" checked={rule.active} onChange={(event) => handleActiveChange(event, rule.ruleID)}/></div>
                        <div className="w-1/8"><input type="number" value={rule.priority} className="w-[6em]" onChange={(event) => handlePriorityChange(event, rule.ruleID)}/></div>
                    </div>
                ))
            }
            {status ? <h1>{status}</h1> : null}
        </form>
    </div>
  );
}

export default EditRules;