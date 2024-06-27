// types.ts
import {ReactNode} from "react";

export interface User {
    first_name: string;
    last_name: string;
    email: string;
    linkedin: boolean;
    reddit: boolean;
}

export interface ContextProviderProps {
    children: ReactNode;
}


export interface StateContextProps {
    user: User | null;
    setUser: (user: User | null) => void;
    token: string | null;
    setToken: (token: string | null) => void;
}

export interface Tag {
    id: number;
    name: string;
}

export interface ListPost {
    id: number;
    title: string;
    content: string;
    description: string;
    link: string;
    tags: Tag[];
}
