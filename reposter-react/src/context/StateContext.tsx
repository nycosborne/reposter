import React, {createContext} from "react";


interface User {
    first_name: string;
    last_name: string;
    email: string;
    soc_accounts: string[];
}

interface StateContextProps {
    user: User | null,
    setUser: (user: User | null) => void;
    token: string | null;
    setToken: (token: string | null) => void;
}

const defaultState: StateContextProps = {
    user: null,
    setUser: () => {
    },
    token: null,
    setToken: () => {
    },
};

const StateContext: React.Context<StateContextProps> = createContext<StateContextProps>(defaultState);

export default StateContext;