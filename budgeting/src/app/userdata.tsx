"use client";
import { atomWithStorage, createJSONStorage } from "jotai/utils";

export const defaultUserData = {
    loggedIn: false,
    username: "",
    userID: -1,
};

const storage = createJSONStorage(() => localStorage);

export const userState = atomWithStorage(
    "userData",
    defaultUserData,
    storage,
);