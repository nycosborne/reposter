import React from 'react';
import StateContext from "./StateContext";
import {User, ContextProviderProps } from "../components/types/types.tsx"

export const ContextProvider: React.FC<ContextProviderProps> = ({children}) => {
    const [user, _setUser] = React.useState<User | null>(null);
    // const [token, _setToken] = React.useState<string | null>('ACCESS_TOKEN');
    const [token, _setToken] = React.useState<string | null>(localStorage.getItem('ACCESS_TOKEN'));

    const setToken = (token: string | null) => {
        _setToken(token);
        if (token) {
            if (typeof token === "string") {
                localStorage.setItem('ACCESS_TOKEN', token);
            }
        } else {
            localStorage.removeItem('ACCESS_TOKEN');
        }
    };

    const setUser = (user: User | null) => {
        _setUser(user)
    }

    return (
        <StateContext.Provider value={{user: user, setUser, token, setToken}}>
            {children}
        </StateContext.Provider>
    );
};
