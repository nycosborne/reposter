import React, {createContext} from "react";

interface StateContextProps {
    user: number | null
    setUser: (user: number | null) => void;
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