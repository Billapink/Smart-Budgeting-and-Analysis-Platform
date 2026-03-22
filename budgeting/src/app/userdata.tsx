"use client";
import { atomWithStorage, createJSONStorage } from "jotai/utils";

const storage = createJSONStorage(() => localStorage);

export const userState = atomWithStorage("userData", {}, storage);