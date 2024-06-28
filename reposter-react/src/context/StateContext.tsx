import React, {createContext} from "react";
import { StateContextProps } from "../components/types/types";


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