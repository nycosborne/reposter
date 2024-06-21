import React, {createContext} from "react";


interface User {
    first_name: string;
    last_name: string;
    email: string;
    linkedin: boolean;
    reddit: boolean;
}

interface StateContextProps {
    user: User,
    setUser: (user: User | null) => void;
    token: string | null;
    setToken: (token: string | null) => void;
}

const defaultState: StateContextProps = {
    user: {
        first_name: 'Default',
        last_name: 'User',
        email: 'default@example.com',
        linkedin: false,
        reddit: false,
    },
    setUser: () => {
    },
    token: null,
    setToken: () => {
    },
};

const StateContext: React.Context<StateContextProps> = createContext<StateContextProps>(defaultState);

export default StateContext;